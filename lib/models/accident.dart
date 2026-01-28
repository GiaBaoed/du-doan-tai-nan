/// Accident model
class Accident {
  final int id;
  final double latitude;
  final double longitude;
  final DateTime accidentDate;
  final String severity;
  final String? roadName;
  final String? roadType;
  final String? weatherCondition;
  final double? distanceKm;

  Accident({
    required this.id,
    required this.latitude,
    required this.longitude,
    required this.accidentDate,
    required this.severity,
    this.roadName,
    this.roadType,
    this.weatherCondition,
    this.distanceKm,
  });

  factory Accident.fromJson(Map<String, dynamic> json) {
    return Accident(
      id: json['id'] ?? 0,
      latitude: json['latitude']?.toDouble() ?? 0.0,
      longitude: json['longitude']?.toDouble() ?? 0.0,
      accidentDate: json['accident_date'] != null
          ? DateTime.parse(json['accident_date'])
          : DateTime.now(),
      severity: json['severity'] ?? 'unknown',
      roadName: json['road_name'],
      roadType: json['road_type'],
      weatherCondition: json['weather_condition'],
      distanceKm: json['distance_km']?.toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'latitude': latitude,
      'longitude': longitude,
      'accident_date': accidentDate.toIso8601String(),
      'severity': severity,
      'road_name': roadName,
      'road_type': roadType,
      'weather_condition': weatherCondition,
      'distance_km': distanceKm,
    };
  }

  bool get isFatal => severity.toLowerCase() == 'fatal';
  bool get isSevere => severity.toLowerCase() == 'severe';
  bool get isModerate => severity.toLowerCase() == 'moderate';
  bool get isMinor => severity.toLowerCase() == 'minor';
}
