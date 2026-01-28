/// Risk prediction model
class RiskPrediction {
  final double latitude;
  final double longitude;
  final String riskLevel;
  final double riskProbability;
  final double riskScore;
  final String message;
  final String? warningMessage;
  final int nearbyAccidentsCount;
  final String? roadSegmentId;
  final DateTime timestamp;

  RiskPrediction({
    required this.latitude,
    required this.longitude,
    required this.riskLevel,
    required this.riskProbability,
    required this.riskScore,
    required this.message,
    this.warningMessage,
    required this.nearbyAccidentsCount,
    this.roadSegmentId,
    required this.timestamp,
  });

  factory RiskPrediction.fromJson(Map<String, dynamic> json) {
    return RiskPrediction(
      latitude: json['latitude']?.toDouble() ?? 0.0,
      longitude: json['longitude']?.toDouble() ?? 0.0,
      riskLevel: json['risk_level'] ?? 'low',
      riskProbability: json['risk_probability']?.toDouble() ?? 0.0,
      riskScore: json['risk_score']?.toDouble() ?? 0.0,
      message: json['message'] ?? '',
      warningMessage: json['warning_message'],
      nearbyAccidentsCount: json['nearby_accidents_count'] ?? 0,
      roadSegmentId: json['road_segment_id'],
      timestamp: json['timestamp'] != null
          ? DateTime.parse(json['timestamp'])
          : DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'latitude': latitude,
      'longitude': longitude,
      'risk_level': riskLevel,
      'risk_probability': riskProbability,
      'risk_score': riskScore,
      'message': message,
      'warning_message': warningMessage,
      'nearby_accidents_count': nearbyAccidentsCount,
      'road_segment_id': roadSegmentId,
      'timestamp': timestamp.toIso8601String(),
    };
  }

  bool get isHighRisk => riskLevel.toLowerCase() == 'high';
  bool get isMediumRisk => riskLevel.toLowerCase() == 'medium';
  bool get isLowRisk => riskLevel.toLowerCase() == 'low';
}
