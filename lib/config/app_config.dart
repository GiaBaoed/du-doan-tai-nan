/// Application configuration
class AppConfig {
  // API Configuration
  static const String apiBaseUrl = 'http://localhost:8000/api/v1';
  
  // For Android emulator use: http://10.0.2.2:8000/api/v1
  // For iOS simulator use: http://localhost:8000/api/v1
  // For physical device use your computer's IP: http://192.168.x.x:8000/api/v1
  
  static const String predictionEndpoint = '/prediction/risk';
  static const String routeAnalysisEndpoint = '/prediction/route-analysis';
  static const String nearbyAccidentsEndpoint = '/accidents/nearby';
  static const String statisticsEndpoint = '/accidents/statistics';
  
  // Map Configuration
  static const String googleMapsApiKey = 'YOUR_GOOGLE_MAPS_API_KEY_HERE';
  
  // Default map location (Hanoi, Vietnam)
  static const double defaultLatitude = 21.0285;
  static const double defaultLongitude = 105.8542;
  static const double defaultZoom = 14.0;
  
  // Risk Configuration
  static const double nearbyRadius = 5.0; // km
  static const int locationUpdateInterval = 5; // seconds
  
  // Notification Configuration
  static const bool enableVoiceAlerts = true;
  static const bool enablePushNotifications = true;
  static const String voiceLanguage = 'vi-VN'; // Vietnamese
  
  // Cache Configuration
  static const int cacheExpiryMinutes = 5;
  
  // UI Configuration
  static const double mapPadding = 50.0;
  static const double bottomSheetHeight = 200.0;
}
