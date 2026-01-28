import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:logger/logger.dart';

import '../config/app_config.dart';
import '../models/risk_prediction.dart';
import '../models/accident.dart';
import '../services/api_service.dart';
import '../services/location_service.dart';
import '../services/notification_service.dart';
import '../services/mock_data.dart';

/// Update risk prediction for current location
  Future<void> updateRiskPrediction() async {
