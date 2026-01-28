import 'package:flutter/material.dart';
import '../models/risk_prediction.dart';
import '../config/theme.dart';

/// Widget to display current risk level indicator
class RiskIndicator extends StatelessWidget {
  final RiskPrediction? riskPrediction;

  const RiskIndicator({
    super.key,
    this.riskPrediction,
  });

  @override
  Widget build(BuildContext context) {
    if (riskPrediction == null) {
      return Card(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Row(
            children: [
              const CircularProgressIndicator(),
              const SizedBox(width: 16),
              Text(
                'Đang phân tích...',
                style: Theme.of(context).textTheme.titleMedium,
              ),
            ],
          ),
        ),
      );
    }

    final riskColor = AppTheme.getRiskColor(riskPrediction!.riskLevel);
    final riskIcon = AppTheme.getRiskIcon(riskPrediction!.riskLevel);

    return Card(
      elevation: 4,
      child: Container(
        padding: const EdgeInsets.all(16.0),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          gradient: LinearGradient(
            colors: [
              riskColor.withOpacity(0.1),
              Colors.white,
            ],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Row(
          children: [
            // Risk Icon
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: riskColor.withOpacity(0.2),
                shape: BoxShape.circle,
              ),
              child: Icon(
                riskIcon,
                color: riskColor,
                size: 32,
              ),
            ),
            const SizedBox(width: 16),
            
            // Risk Information
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    _getRiskLevelText(riskPrediction!.riskLevel),
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          color: riskColor,
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Mức độ rủi ro: ${riskPrediction!.riskScore.toStringAsFixed(0)}%',
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ],
              ),
            ),
            
            // Risk Score Badge
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: riskColor,
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(
                '${riskPrediction!.riskScore.toStringAsFixed(0)}',
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  fontSize: 18,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  String _getRiskLevelText(String riskLevel) {
    switch (riskLevel.toLowerCase()) {
      case 'low':
        return 'AN TOÀN';
      case 'medium':
        return 'CHÚ Ý';
      case 'high':
        return 'NGUY HIỂM';
      default:
        return 'KHÔNG RÕ';
    }
  }
}
