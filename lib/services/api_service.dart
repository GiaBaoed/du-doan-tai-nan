import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:logger/logger.dart';
import '../config/app_config.dart';
import '../models/risk_prediction.dart';
import '../models/accident.dart';

/// API service for communicating with backend
class ApiService {
  final String baseUrl;
  final Logger _logger = Logger();

  ApiService({String? baseUrl}) : baseUrl = baseUrl ?? AppConfig.apiBaseUrl;

  /// Predict risk for a specific location
  Future<RiskPrediction?> predictRisk({
    required double latitude,
    required double longitude,
    String? weatherCondition,
    String? roadType,
  }) async {
    try {
      final url = Uri.parse('$baseUrl${AppConfig.predictionEndpoint}');
      
      final body = {
        'latitude': latitude,
        'longitude': longitude,
        'timestamp': DateTime.now().toIso8601String(),
      };

      if (weatherCondition != null) {
        body['weather_condition'] = weatherCondition;
      }
      if (roadType != null) {
        body['road_type'] = roadType;
      }

      _logger.d('Predicting risk for: $latitude, $longitude');

      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _logger.i('Risk prediction successful: ${data['risk_level']}');
        return RiskPrediction.fromJson(data);
      } else {
        _logger.e('Risk prediction failed: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      _logger.e('Error predicting risk: $e');
      return null;
    }
  }

  /// Get nearby accidents
  Future<List<Accident>> getNearbyAccidents({
    required double latitude,
    required double longitude,
    double radiusKm = 5.0,
    int limit = 50,
  }) async {
    try {
      final url = Uri.parse('$baseUrl${AppConfig.nearbyAccidentsEndpoint}');

      final body = {
        'latitude': latitude,
        'longitude': longitude,
        'radius_km': radiusKm,
        'limit': limit,
      };

      _logger.d('Fetching nearby accidents for: $latitude, $longitude');

      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        _logger.i('Found ${data.length} nearby accidents');
        return data.map((json) => Accident.fromJson(json)).toList();
      } else {
        _logger.e('Failed to fetch nearby accidents: ${response.statusCode}');
        return [];
      }
    } catch (e) {
      _logger.e('Error fetching nearby accidents: $e');
      return [];
    }
  }

  /// Report a new accident
  Future<bool> reportAccident({
    required double latitude,
    required double longitude,
    required DateTime accidentDate,
    required String severity,
    String? roadName,
    String? roadType,
    String? weatherCondition,
    String? description,
    int numCasualties = 0,
    int numVehicles = 1,
  }) async {
    try {
      final url = Uri.parse('$baseUrl/accidents/');

      final body = {
        'latitude': latitude,
        'longitude': longitude,
        'accident_date': accidentDate.toIso8601String(),
        'severity': severity,
        'num_casualties': numCasualties,
        'num_vehicles': numVehicles,
      };

      if (roadName != null) body['road_name'] = roadName;
      if (roadType != null) body['road_type'] = roadType;
      if (weatherCondition != null) body['weather_condition'] = weatherCondition;
      if (description != null) body['description'] = description;

      _logger.d('Reporting accident at: $latitude, $longitude');

      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        _logger.i('Accident reported successfully');
        return true;
      } else {
        _logger.e('Failed to report accident: ${response.statusCode}');
        return false;
      }
    } catch (e) {
      _logger.e('Error reporting accident: $e');
      return false;
    }
  }

  /// Get statistics
  Future<Map<String, dynamic>?> getStatistics({int days = 365}) async {
    try {
      final url = Uri.parse('$baseUrl${AppConfig.statisticsEndpoint}?days=$days');

      _logger.d('Fetching statistics for last $days days');

      final response = await http.get(url).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _logger.i('Statistics fetched successfully');
        return data;
      } else {
        _logger.e('Failed to fetch statistics: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      _logger.e('Error fetching statistics: $e');
      return null;
    }
  }

  /// Check API health
  Future<bool> checkHealth() async {
    try {
      final url = Uri.parse('$baseUrl/prediction/health');
      final response = await http.get(url).timeout(const Duration(seconds: 5));
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _logger.i('API health check: ${data['status']}');
        return data['status'] == 'healthy';
      }
      return false;
    } catch (e) {
      _logger.e('API health check failed: $e');
      return false;
    }
  }
}
