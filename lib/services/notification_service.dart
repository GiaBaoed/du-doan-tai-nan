import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:logger/logger.dart';
import '../config/app_config.dart';
import '../models/risk_prediction.dart';

/// Notification service for alerts and voice warnings
class NotificationService {
  final FlutterLocalNotificationsPlugin _notificationsPlugin =
      FlutterLocalNotificationsPlugin();
  final FlutterTts _flutterTts = FlutterTts();
  final Logger _logger = Logger();
  
  bool _isInitialized = false;
  String? _lastSpokenMessage;
  DateTime? _lastNotificationTime;

  /// Initialize notification service
  Future<void> initialize() async {
    if (_isInitialized) return;

    try {
      // Initialize local notifications
      const androidSettings = AndroidInitializationSettings('@mipmap/ic_launcher');
      const iosSettings = DarwinInitializationSettings(
        requestAlertPermission: true,
        requestBadgePermission: true,
        requestSoundPermission: true,
      );

      const initSettings = InitializationSettings(
        android: androidSettings,
        iOS: iosSettings,
      );

      await _notificationsPlugin.initialize(
        initSettings,
        onDidReceiveNotificationResponse: _onNotificationTapped,
      );

      // Initialize TTS
      await _initializeTts();

      _isInitialized = true;
      _logger.i('Notification service initialized');
    } catch (e) {
      _logger.e('Error initializing notification service: $e');
    }
  }

  /// Initialize Text-to-Speech
  Future<void> _initializeTts() async {
    try {
      await _flutterTts.setLanguage(AppConfig.voiceLanguage);
      await _flutterTts.setSpeechRate(0.5); // Slower for clarity
      await _flutterTts.setVolume(1.0);
      await _flutterTts.setPitch(1.0);

      // Set voice for Vietnamese if available
      if (AppConfig.voiceLanguage == 'vi-VN') {
        var voices = await _flutterTts.getVoices;
        if (voices != null) {
          for (var voice in voices) {
            if (voice['locale'] == 'vi-VN') {
              await _flutterTts.setVoice({'name': voice['name'], 'locale': voice['locale']});
              break;
            }
          }
        }
      }

      _logger.i('TTS initialized with language: ${AppConfig.voiceLanguage}');
    } catch (e) {
      _logger.e('Error initializing TTS: $e');
    }
  }

  /// Handle notification tap
  void _onNotificationTapped(NotificationResponse response) {
    _logger.d('Notification tapped: ${response.payload}');
    // Handle navigation or actions based on payload
  }

  /// Show risk warning notification
  Future<void> showRiskWarning(RiskPrediction prediction) async {
    if (!_isInitialized) await initialize();

    // Prevent spam notifications (minimum 30 seconds between notifications)
    if (_lastNotificationTime != null) {
      final difference = DateTime.now().difference(_lastNotificationTime!);
      if (difference.inSeconds < 30) {
        _logger.d('Skipping notification - too soon since last one');
        return;
      }
    }

    try {
      if (AppConfig.enablePushNotifications) {
        await _showPushNotification(prediction);
      }

      if (AppConfig.enableVoiceAlerts) {
        await _speakWarning(prediction);
      }

      _lastNotificationTime = DateTime.now();
    } catch (e) {
      _logger.e('Error showing risk warning: $e');
    }
  }

  /// Show push notification
  Future<void> _showPushNotification(RiskPrediction prediction) async {
    try {
      const androidDetails = AndroidNotificationDetails(
        'risk_warnings',
        'Risk Warnings',
        channelDescription: 'Notifications for traffic accident risk warnings',
        importance: Importance.high,
        priority: Priority.high,
        enableVibration: true,
        playSound: true,
      );

      const iosDetails = DarwinNotificationDetails(
        presentAlert: true,
        presentBadge: true,
        presentSound: true,
      );

      const notificationDetails = NotificationDetails(
        android: androidDetails,
        iOS: iosDetails,
      );

      await _notificationsPlugin.show(
        prediction.hashCode,
        _getNotificationTitle(prediction.riskLevel),
        prediction.message,
        notificationDetails,
        payload: prediction.riskLevel,
      );

      _logger.i('Push notification shown: ${prediction.riskLevel}');
    } catch (e) {
      _logger.e('Error showing push notification: $e');
    }
  }

  /// Speak warning message
  Future<void> _speakWarning(RiskPrediction prediction) async {
    try {
      // Don't repeat the same message too quickly
      if (_lastSpokenMessage == prediction.message) {
        _logger.d('Skipping voice alert - same message');
        return;
      }

      // Only speak for medium and high risk
      if (prediction.isMediumRisk || prediction.isHighRisk) {
        await _flutterTts.speak(prediction.message);
        _lastSpokenMessage = prediction.message;
        _logger.i('Voice alert spoken: ${prediction.message}');
      }
    } catch (e) {
      _logger.e('Error speaking warning: $e');
    }
  }

  /// Get notification title based on risk level
  String _getNotificationTitle(String riskLevel) {
    switch (riskLevel.toLowerCase()) {
      case 'high':
        return '⚠️ CẢNH BÁO NGUY HIỂM';
      case 'medium':
        return '⚡ CHÚ Ý';
      case 'low':
        return '✅ An Toàn';
      default:
        return 'Thông Báo';
    }
  }

  /// Show custom notification
  Future<void> showNotification({
    required String title,
    required String body,
    String? payload,
  }) async {
    if (!_isInitialized) await initialize();

    try {
      const androidDetails = AndroidNotificationDetails(
        'general',
        'General Notifications',
        channelDescription: 'General app notifications',
        importance: Importance.defaultImportance,
        priority: Priority.defaultPriority,
      );

      const iosDetails = DarwinNotificationDetails();

      const notificationDetails = NotificationDetails(
        android: androidDetails,
        iOS: iosDetails,
      );

      await _notificationsPlugin.show(
        DateTime.now().millisecondsSinceEpoch ~/ 1000,
        title,
        body,
        notificationDetails,
        payload: payload,
      );
    } catch (e) {
      _logger.e('Error showing notification: $e');
    }
  }

  /// Speak custom message
  Future<void> speak(String message) async {
    try {
      await _flutterTts.speak(message);
    } catch (e) {
      _logger.e('Error speaking message: $e');
    }
  }

  /// Stop speaking
  Future<void> stopSpeaking() async {
    try {
      await _flutterTts.stop();
    } catch (e) {
      _logger.e('Error stopping speech: $e');
    }
  }

  /// Cancel all notifications
  Future<void> cancelAll() async {
    try {
      await _notificationsPlugin.cancelAll();
    } catch (e) {
      _logger.e('Error canceling notifications: $e');
    }
  }

  /// Dispose resources
  void dispose() {
    _flutterTts.stop();
  }
}
