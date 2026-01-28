"""
Machine Learning model wrapper for accident risk prediction
"""

import joblib
import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional
from datetime import datetime
import os
from pathlib import Path

from config import settings


class AccidentRiskModel:
    """Wrapper class for the ML model"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = [
            'latitude', 'longitude', 'hour', 'day_of_week', 
            'is_weekend', 'is_rush_hour', 'weather_score',
            'road_type_score', 'historical_accidents_nearby'
        ]
        self.is_trained = False
        
    def load_model(self, model_path: str = None, scaler_path: str = None):
        """Load trained model and scaler from disk"""
        try:
            model_path = model_path or settings.MODEL_PATH
            scaler_path = scaler_path or settings.SCALER_PATH
            
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                print(f"Model loaded from {model_path}")
                self.is_trained = True
            else:
                print(f"Model file not found at {model_path}. Using fallback prediction.")
                self.is_trained = False
                
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                print(f"Scaler loaded from {scaler_path}")
            else:
                print(f"Scaler file not found at {scaler_path}")
                
        except Exception as e:
            print(f"Error loading model: {e}")
            self.is_trained = False
    
    def save_model(self, model_path: str = None, scaler_path: str = None):
        """Save trained model and scaler to disk"""
        try:
            model_path = model_path or settings.MODEL_PATH
            scaler_path = scaler_path or settings.SCALER_PATH
            
            # Create directories if they don't exist
            Path(model_path).parent.mkdir(parents=True, exist_ok=True)
            Path(scaler_path).parent.mkdir(parents=True, exist_ok=True)
            
            if self.model:
                joblib.dump(self.model, model_path)
                print(f"Model saved to {model_path}")
                
            if self.scaler:
                joblib.dump(self.scaler, scaler_path)
                print(f"Scaler saved to {scaler_path}")
                
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def prepare_features(
        self, 
        latitude: float, 
        longitude: float,
        timestamp: Optional[datetime] = None,
        weather_condition: str = "clear",
        road_type: str = "urban",
        historical_accidents: int = 0
    ) -> np.ndarray:
        """Prepare features for prediction"""
        
        if timestamp is None:
            timestamp = datetime.now()
        
        # Extract time features
        hour = timestamp.hour
        day_of_week = timestamp.weekday()
        is_weekend = 1 if day_of_week >= 5 else 0
        is_rush_hour = 1 if hour in [7, 8, 9, 17, 18, 19] else 0
        
        # Weather score (0-1, higher = worse conditions)
        weather_scores = {
            'clear': 0.0,
            'rain': 0.5,
            'fog': 0.7,
            'snow': 0.8,
            'storm': 1.0
        }
        weather_score = weather_scores.get(weather_condition.lower(), 0.0)
        
        # Road type score (0-1, higher = more dangerous)
        road_type_scores = {
            'highway': 0.3,
            'national_road': 0.5,
            'urban': 0.4,
            'rural': 0.6
        }
        road_type_score = road_type_scores.get(road_type.lower(), 0.4)
        
        # Create feature array
        features = np.array([[
            latitude,
            longitude,
            hour,
            day_of_week,
            is_weekend,
            is_rush_hour,
            weather_score,
            road_type_score,
            historical_accidents
        ]])
        
        # Scale features if scaler is available
        if self.scaler:
            features = self.scaler.transform(features)
        
        return features
    
    def predict_risk(
        self,
        latitude: float,
        longitude: float,
        timestamp: Optional[datetime] = None,
        weather_condition: str = "clear",
        road_type: str = "urban",
        historical_accidents: int = 0
    ) -> Tuple[str, float]:
        """
        Predict accident risk for given location and conditions
        
        Returns:
            Tuple of (risk_level, risk_probability)
            risk_level: 'low', 'medium', or 'high'
            risk_probability: float between 0 and 1
        """
        
        # Prepare features
        features = self.prepare_features(
            latitude, longitude, timestamp, 
            weather_condition, road_type, historical_accidents
        )
        
        # Make prediction
        if self.is_trained and self.model:
            try:
                # Get probability prediction
                risk_probability = self.model.predict_proba(features)[0][1]
            except:
                # Fallback if predict_proba not available
                risk_probability = self.model.predict(features)[0]
        else:
            # Fallback prediction based on heuristics
            risk_probability = self._fallback_prediction(
                latitude, longitude, timestamp,
                weather_condition, road_type, historical_accidents
            )
        
        # Determine risk level based on thresholds
        if risk_probability < settings.LOW_RISK_THRESHOLD:
            risk_level = "low"
        elif risk_probability < settings.HIGH_RISK_THRESHOLD:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        return risk_level, float(risk_probability)
    
    def _fallback_prediction(
        self,
        latitude: float,
        longitude: float,
        timestamp: Optional[datetime],
        weather_condition: str,
        road_type: str,
        historical_accidents: int
    ) -> float:
        """
        Fallback prediction method when model is not trained
        Uses simple heuristics based on features
        """
        
        base_risk = 0.2  # Base risk level
        
        # Adjust for historical accidents (most important factor)
        if historical_accidents > 10:
            base_risk += 0.4
        elif historical_accidents > 5:
            base_risk += 0.25
        elif historical_accidents > 2:
            base_risk += 0.15
        
        # Adjust for weather
        weather_adjustments = {
            'clear': 0.0,
            'rain': 0.15,
            'fog': 0.2,
            'snow': 0.25,
            'storm': 0.3
        }
        base_risk += weather_adjustments.get(weather_condition.lower(), 0.0)
        
        # Adjust for road type
        road_adjustments = {
            'highway': 0.05,
            'national_road': 0.1,
            'urban': 0.05,
            'rural': 0.15
        }
        base_risk += road_adjustments.get(road_type.lower(), 0.0)
        
        # Adjust for time of day
        if timestamp:
            hour = timestamp.hour
            # Higher risk during rush hours and late night
            if hour in [7, 8, 9, 17, 18, 19]:
                base_risk += 0.1
            elif hour >= 22 or hour <= 5:
                base_risk += 0.15
        
        # Cap at 1.0
        return min(base_risk, 1.0)
    
    def get_risk_message(self, risk_level: str, language: str = "vi") -> Dict[str, str]:
        """
        Get appropriate warning message based on risk level
        
        Args:
            risk_level: 'low', 'medium', or 'high'
            language: 'vi' for Vietnamese, 'en' for English
        
        Returns:
            Dictionary with 'message' and 'warning' keys
        """
        
        messages = {
            "vi": {
                "low": {
                    "message": "Đoạn đường an toàn",
                    "warning": "Vẫn cần chú ý quan sát khi lái xe"
                },
                "medium": {
                    "message": "Đoạn đường hay xảy ra tai nạn, xin chú ý",
                    "warning": "Giảm tốc độ và tăng cường quan sát"
                },
                "high": {
                    "message": "Đoạn đường có mức độ tai nạn cao, xin lái xe cẩn thận",
                    "warning": "Cực kỳ nguy hiểm! Giảm tốc độ và cẩn thận tối đa"
                }
            },
            "en": {
                "low": {
                    "message": "Safe road segment",
                    "warning": "Stay alert while driving"
                },
                "medium": {
                    "message": "Moderate accident risk area, please be careful",
                    "warning": "Reduce speed and increase awareness"
                },
                "high": {
                    "message": "High accident risk area, drive with extreme caution",
                    "warning": "Very dangerous! Reduce speed and be extremely careful"
                }
            }
        }
        
        return messages.get(language, messages["vi"]).get(risk_level, messages["vi"]["low"])


# Global model instance
accident_model = AccidentRiskModel()
