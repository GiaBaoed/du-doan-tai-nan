import 'package:flutter/material.dart';
import '../models/risk_prediction.dart';
import '../config/theme.dart';

/// Bottom sheet widget to display detailed risk information
class RiskInfoSheet extends StatelessWidget {
  final RiskPrediction? riskPrediction;
  final int nearbyAccidentsCount;

  const RiskInfoSheet({
    super.key,
    this.riskPrediction,
    required this.nearbyAccidentsCount,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(20),
          topRight: Radius.circular(20),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 10,
            offset: const Offset(0, -5),
          ),
        ],
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Handle bar
          Container(
            margin: const EdgeInsets.only(top: 12),
            width: 40,
            height: 4,
            decoration: BoxDecoration(
              color: Colors.grey[300],
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          
          if (riskPrediction != null) ...[
            Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Warning Message
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: AppTheme.getRiskColor(riskPrediction!.riskLevel)
                          .withOpacity(0.1),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(
                        color: AppTheme.getRiskColor(riskPrediction!.riskLevel),
                        width: 2,
                      ),
                    ),
                    child: Row(
                      children: [
                        Icon(
                          AppTheme.getRiskIcon(riskPrediction!.riskLevel),
                          color: AppTheme.getRiskColor(riskPrediction!.riskLevel),
                          size: 32,
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                riskPrediction!.message,
                                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                      fontWeight: FontWeight.bold,
                                    ),
                              ),
                              if (riskPrediction!.warningMessage != null) ...[
                                const SizedBox(height: 4),
                                Text(
                                  riskPrediction!.warningMessage!,
                                  style: Theme.of(context).textTheme.bodyMedium,
                                ),
                              ],
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                  
                  const SizedBox(height: 16),
                  
                  // Statistics
                  Row(
                    children: [
                      Expanded(
                        child: _buildStatCard(
                          context,
                          icon: Icons.warning_amber,
                          label: 'Tai nạn gần đây',
                          value: '$nearbyAccidentsCount',
                          color: Colors.orange,
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: _buildStatCard(
                          context,
                          icon: Icons.percent,
                          label: 'Xác suất',
                          value: '${(riskPrediction!.riskProbability * 100).toStringAsFixed(0)}%',
                          color: AppTheme.getRiskColor(riskPrediction!.riskLevel),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ] else ...[
            const Padding(
              padding: EdgeInsets.all(20.0),
              child: Center(
                child: Text('Đang tải thông tin...'),
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildStatCard(
    BuildContext context, {
    required IconData icon,
    required String label,
    required String value,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        children: [
          Icon(icon, color: color, size: 32),
          const SizedBox(height: 8),
          Text(
            value,
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  color: color,
                  fontWeight: FontWeight.bold,
                ),
          ),
          const SizedBox(height: 4),
          Text(
            label,
            style: Theme.of(context).textTheme.bodySmall,
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}
