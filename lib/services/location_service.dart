import 'package:geolocator/geolocator.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:logger/logger.dart';

/// Location service for GPS tracking
class LocationService {
  final Logger _logger = Logger();
  Position? _lastPosition;

  /// Check if location services are enabled
  Future<bool> isLocationServiceEnabled() async {
    return await Geolocator.isLocationServiceEnabled();
  }

  /// Check location permission status
  Future<LocationPermission> checkPermission() async {
    return await Geolocator.checkPermission();
  }

  /// Request location permission
  Future<bool> requestPermission() async {
    try {
      // Check if location service is enabled
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        _logger.w('Location services are disabled');
        return false;
      }

      // Check permission
      LocationPermission permission = await Geolocator.checkPermission();
      
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          _logger.w('Location permission denied');
          return false;
        }
      }

      if (permission == LocationPermission.deniedForever) {
        _logger.e('Location permission denied forever');
        // Open app settings
        await openAppSettings();
        return false;
      }

      _logger.i('Location permission granted');
      return true;
    } catch (e) {
      _logger.e('Error requesting location permission: $e');
      return false;
    }
  }

  /// Get current location
  Future<Position?> getCurrentLocation() async {
    try {
      // Check permission first
      bool hasPermission = await requestPermission();
      if (!hasPermission) {
        return null;
      }

      // Get current position
      Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
        timeLimit: const Duration(seconds: 10),
      );

      _lastPosition = position;
      _logger.d('Current location: ${position.latitude}, ${position.longitude}');
      return position;
    } catch (e) {
      _logger.e('Error getting current location: $e');
      return null;
    }
  }

  /// Get last known location
  Future<Position?> getLastKnownLocation() async {
    try {
      Position? position = await Geolocator.getLastKnownPosition();
      if (position != null) {
        _lastPosition = position;
        _logger.d('Last known location: ${position.latitude}, ${position.longitude}');
      }
      return position;
    } catch (e) {
      _logger.e('Error getting last known location: $e');
      return null;
    }
  }

  /// Stream location updates
  Stream<Position> getLocationStream({
    LocationAccuracy accuracy = LocationAccuracy.high,
    int distanceFilter = 10, // meters
    int intervalDuration = 5000, // milliseconds
  }) {
    final locationSettings = LocationSettings(
      accuracy: accuracy,
      distanceFilter: distanceFilter,
      timeLimit: Duration(milliseconds: intervalDuration),
    );

    return Geolocator.getPositionStream(locationSettings: locationSettings);
  }

  /// Calculate distance between two points in meters
  double calculateDistance(
    double startLatitude,
    double startLongitude,
    double endLatitude,
    double endLongitude,
  ) {
    return Geolocator.distanceBetween(
      startLatitude,
      startLongitude,
      endLatitude,
      endLongitude,
    );
  }

  /// Calculate bearing between two points
  double calculateBearing(
    double startLatitude,
    double startLongitude,
    double endLatitude,
    double endLongitude,
  ) {
    return Geolocator.bearingBetween(
      startLatitude,
      startLongitude,
      endLatitude,
      endLongitude,
    );
  }

  /// Get last cached position
  Position? get lastPosition => _lastPosition;

  /// Check if location has changed significantly
  bool hasLocationChangedSignificantly(Position newPosition, {double thresholdMeters = 50}) {
    if (_lastPosition == null) return true;

    double distance = calculateDistance(
      _lastPosition!.latitude,
      _lastPosition!.longitude,
      newPosition.latitude,
      newPosition.longitude,
    );

    return distance >= thresholdMeters;
  }
}
