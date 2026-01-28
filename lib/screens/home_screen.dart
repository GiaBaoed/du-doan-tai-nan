import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:provider/provider.dart';

import '../providers/app_state.dart';
import '../config/app_config.dart';
import '../config/theme.dart';
import '../widgets/risk_indicator.dart';
import '../widgets/risk_info_sheet.dart';

/// Main home screen with map and risk visualization
class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  GoogleMapController? _mapController;
  final Set<Marker> _markers = {};
  final Set<Circle> _circles = {};

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _initializeApp();
    });
  }

  Future<void> _initializeApp() async {
    final appState = Provider.of<AppState>(context, listen: false);
    await appState.initialize();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Cảnh Báo Tai Nạn Giao Thông'),
        actions: [
          IconButton(
            icon: const Icon(Icons.info_outline),
            onPressed: () {
              // Show info dialog
              _showInfoDialog();
            },
          ),
        ],
      ),
      body: Consumer<AppState>(
        builder: (context, appState, child) {
          if (appState.isLoading && !appState.hasLocation) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 16),
                  Text('Đang lấy vị trí...'),
                ],
              ),
            );
          }

          if (appState.errorMessage != null) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.error_outline, size: 64, color: Colors.red),
                  const SizedBox(height: 16),
                  Text(
                    appState.errorMessage!,
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 16),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () {
                      appState.clearError();
                      appState.getCurrentLocation();
                    },
                    child: const Text('Thử lại'),
                  ),
                ],
              ),
            );
          }

          return Stack(
            children: [
              // Google Map
              _buildMap(appState),
              
              // Risk Indicator (top)
              Positioned(
                top: 16,
                left: 16,
                right: 16,
                child: RiskIndicator(
                  riskPrediction: appState.currentRiskPrediction,
                ),
              ),
              
              // Risk Info Sheet (bottom)
              Positioned(
                bottom: 0,
                left: 0,
                right: 0,
                child: RiskInfoSheet(
                  riskPrediction: appState.currentRiskPrediction,
                  nearbyAccidentsCount: appState.nearbyAccidents.length,
                ),
              ),
            ],
          );
        },
      ),
      floatingActionButton: Consumer<AppState>(
        builder: (context, appState, child) {
          return Column(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              // Tracking toggle button
              FloatingActionButton(
                heroTag: 'tracking',
                onPressed: () {
                  if (appState.isTracking) {
                    appState.stopTracking();
                  } else {
                    appState.startTracking();
                  }
                },
                backgroundColor: appState.isTracking
                    ? AppTheme.highRiskColor
                    : AppTheme.primaryColor,
                child: Icon(
                  appState.isTracking ? Icons.stop : Icons.play_arrow,
                ),
              ),
              const SizedBox(height: 16),
              
              // Center on current location button
              FloatingActionButton(
                heroTag: 'center',
                onPressed: () {
                  _centerOnCurrentLocation(appState);
                },
                child: const Icon(Icons.my_location),
              ),
            ],
          );
        },
      ),
    );
  }

  Widget _buildMap(AppState appState) {
    final position = appState.currentPosition;
    
    if (position == null) {
      return const Center(child: Text('Không có vị trí'));
    }

    // Update markers
    _updateMarkers(appState);

    return GoogleMap(
      initialCameraPosition: CameraPosition(
        target: LatLng(position.latitude, position.longitude),
        zoom: AppConfig.defaultZoom,
      ),
      onMapCreated: (controller) {
        _mapController = controller;
      },
      markers: _markers,
      circles: _circles,
      myLocationEnabled: true,
      myLocationButtonEnabled: false,
      zoomControlsEnabled: false,
      mapToolbarEnabled: false,
      compassEnabled: true,
      trafficEnabled: true,
    );
  }

  void _updateMarkers(AppState appState) {
    _markers.clear();
    _circles.clear();

    final position = appState.currentPosition;
    final riskPrediction = appState.currentRiskPrediction;

    if (position == null) return;

    // Add risk circle around current location
    if (riskPrediction != null) {
      _circles.add(
        Circle(
          circleId: const CircleId('risk_area'),
          center: LatLng(position.latitude, position.longitude),
          radius: 500, // 500 meters
          fillColor: AppTheme.getRiskColor(riskPrediction.riskLevel)
              .withOpacity(0.2),
          strokeColor: AppTheme.getRiskColor(riskPrediction.riskLevel),
          strokeWidth: 2,
        ),
      );
    }

    // Add markers for nearby accidents
    for (var accident in appState.nearbyAccidents) {
      _markers.add(
        Marker(
          markerId: MarkerId('accident_${accident.id}'),
          position: LatLng(accident.latitude, accident.longitude),
          icon: BitmapDescriptor.defaultMarkerWithHue(
            _getAccidentMarkerHue(accident.severity),
          ),
          infoWindow: InfoWindow(
            title: 'Tai nạn ${accident.severity}',
            snippet: accident.roadName ?? 'Không rõ vị trí',
          ),
        ),
      );
    }
  }

  double _getAccidentMarkerHue(String severity) {
    switch (severity.toLowerCase()) {
      case 'fatal':
        return BitmapDescriptor.hueRed;
      case 'severe':
        return BitmapDescriptor.hueOrange;
      case 'moderate':
        return BitmapDescriptor.hueYellow;
      case 'minor':
        return BitmapDescriptor.hueGreen;
      default:
        return BitmapDescriptor.hueBlue;
    }
  }

  void _centerOnCurrentLocation(AppState appState) {
    final position = appState.currentPosition;
    if (position != null && _mapController != null) {
      _mapController!.animateCamera(
        CameraUpdate.newLatLngZoom(
          LatLng(position.latitude, position.longitude),
          AppConfig.defaultZoom,
        ),
      );
    }
  }

  void _showInfoDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Hướng dẫn sử dụng'),
        content: const SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                'Màu sắc cảnh báo:',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              SizedBox(height: 8),
              Row(
                children: [
                  Icon(Icons.circle, color: AppTheme.lowRiskColor, size: 16),
                  SizedBox(width: 8),
                  Text('Xanh: Đoạn đường an toàn'),
                ],
              ),
              SizedBox(height: 4),
              Row(
                children: [
                  Icon(Icons.circle, color: AppTheme.mediumRiskColor, size: 16),
                  SizedBox(width: 8),
                  Text('Vàng: Cần chú ý'),
                ],
              ),
              SizedBox(height: 4),
              Row(
                children: [
                  Icon(Icons.circle, color: AppTheme.highRiskColor, size: 16),
                  SizedBox(width: 8),
                  Text('Đỏ: Nguy hiểm cao'),
                ],
              ),
              SizedBox(height: 16),
              Text(
                'Chức năng:',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              SizedBox(height: 8),
              Text('• Nhấn nút Play để bắt đầu theo dõi'),
              Text('• Ứng dụng sẽ cảnh báo khi vào vùng nguy hiểm'),
              Text('• Xem thông tin tai nạn gần đó trên bản đồ'),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Đóng'),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _mapController?.dispose();
    super.dispose();
  }
}
