"""
Risk calculation and analysis service
"""

from typing import List, Tuple, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
import math

from app.models.database import Accident, RoadSegment
from app.models.schemas import RiskLevel
from config import settings


class RiskCalculator:
    """Service for calculating accident risk"""
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula
        Returns distance in kilometers
        """
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return distance
    
    @staticmethod
    def get_nearby_accidents(
        db: Session,
        latitude: float,
        longitude: float,
        radius_km: float = None,
        limit: int = 100
    ) -> List[Accident]:
        """
        Get accidents within radius of given location
        """
        radius_km = radius_km or settings.NEARBY_RADIUS_KM
        
        # Approximate degree offset for the radius
        # 1 degree latitude ≈ 111 km
        lat_offset = radius_km / 111.0
        lon_offset = radius_km / (111.0 * math.cos(math.radians(latitude)))
        
        # Query accidents within bounding box
        accidents = db.query(Accident).filter(
            and_(
                Accident.latitude.between(latitude - lat_offset, latitude + lat_offset),
                Accident.longitude.between(longitude - lon_offset, longitude + lon_offset)
            )
        ).limit(limit).all()
        
        # Filter by exact distance
        nearby_accidents = []
        for accident in accidents:
            distance = RiskCalculator.calculate_distance(
                latitude, longitude,
                accident.latitude, accident.longitude
            )
            if distance <= radius_km:
                # Add distance attribute for sorting/display
                accident.distance_km = distance
                nearby_accidents.append(accident)
        
        # Sort by distance
        nearby_accidents.sort(key=lambda x: x.distance_km)
        
        return nearby_accidents
    
    @staticmethod
    def calculate_segment_risk(
        db: Session,
        segment_id: str
    ) -> Tuple[float, RiskLevel]:
        """
        Calculate risk score and level for a road segment
        Returns (risk_score, risk_level)
        """
        segment = db.query(RoadSegment).filter(
            RoadSegment.segment_id == segment_id
        ).first()
        
        if not segment:
            return 0.0, RiskLevel.LOW
        
        # Calculate risk based on accident frequency
        accidents_per_year = segment.accidents_last_year
        
        # Base risk score (0-100)
        if accidents_per_year == 0:
            risk_score = 0.0
        elif accidents_per_year <= 2:
            risk_score = 15.0
        elif accidents_per_year <= 5:
            risk_score = 35.0
        elif accidents_per_year <= 10:
            risk_score = 60.0
        else:
            risk_score = min(85.0 + (accidents_per_year - 10) * 2, 100.0)
        
        # Adjust for recent accidents (last month)
        if segment.accidents_last_month > 0:
            risk_score += min(segment.accidents_last_month * 5, 15)
        
        # Adjust for average severity
        if segment.avg_severity:
            risk_score *= (1 + segment.avg_severity * 0.2)
        
        # Cap at 100
        risk_score = min(risk_score, 100.0)
        
        # Determine risk level
        risk_probability = risk_score / 100.0
        if risk_probability < settings.LOW_RISK_THRESHOLD:
            risk_level = RiskLevel.LOW
        elif risk_probability < settings.HIGH_RISK_THRESHOLD:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.HIGH
        
        return risk_score, risk_level
    
    @staticmethod
    def generate_segment_id(
        latitude: float,
        longitude: float,
        precision: int = 3
    ) -> str:
        """
        Generate a unique segment ID based on coordinates
        Rounds coordinates to create segments
        """
        lat_rounded = round(latitude, precision)
        lon_rounded = round(longitude, precision)
        return f"SEG_{lat_rounded}_{lon_rounded}"
    
    @staticmethod
    def update_segment_statistics(db: Session, segment_id: str):
        """
        Update statistics for a road segment based on accidents
        """
        segment = db.query(RoadSegment).filter(
            RoadSegment.segment_id == segment_id
        ).first()
        
        if not segment:
            return
        
        # Get all accidents in this segment
        accidents = db.query(Accident).filter(
            and_(
                Accident.latitude.between(segment.start_lat - 0.01, segment.end_lat + 0.01),
                Accident.longitude.between(segment.start_lon - 0.01, segment.end_lon + 0.01)
            )
        ).all()
        
        # Update total accidents
        segment.total_accidents = len(accidents)
        
        # Count accidents in last year
        one_year_ago = datetime.now() - timedelta(days=365)
        segment.accidents_last_year = sum(
            1 for a in accidents if a.accident_date >= one_year_ago
        )
        
        # Count accidents in last month
        one_month_ago = datetime.now() - timedelta(days=30)
        segment.accidents_last_month = sum(
            1 for a in accidents if a.accident_date >= one_month_ago
        )
        
        # Calculate average severity (0-1 scale)
        severity_scores = {'minor': 0.25, 'moderate': 0.5, 'severe': 0.75, 'fatal': 1.0}
        if accidents:
            avg_severity = sum(
                severity_scores.get(a.severity, 0.5) for a in accidents
            ) / len(accidents)
            segment.avg_severity = avg_severity
        
        # Find peak accident hour
        if accidents:
            hour_counts = {}
            for accident in accidents:
                hour = accident.hour_of_day
                hour_counts[hour] = hour_counts.get(hour, 0) + 1
            segment.peak_accident_hour = max(hour_counts, key=hour_counts.get)
        
        # Calculate risk score and level
        risk_score, risk_level = RiskCalculator.calculate_segment_risk(db, segment_id)
        segment.risk_score = risk_score / 100.0  # Store as 0-1
        segment.risk_level = risk_level.value
        
        segment.last_updated = datetime.now()
        db.commit()
    
    @staticmethod
    def analyze_route(
        db: Session,
        route_points: List[Tuple[float, float]]
    ) -> dict:
        """
        Analyze safety of entire route
        Returns statistics and risk assessment
        """
        if len(route_points) < 2:
            return {
                'total_distance_km': 0,
                'overall_risk_score': 0,
                'overall_risk_level': RiskLevel.LOW,
                'high_risk_segments': []
            }
        
        total_distance = 0
        total_risk_score = 0
        high_risk_segments = []
        
        # Analyze each segment of the route
        for i in range(len(route_points) - 1):
            lat1, lon1 = route_points[i]
            lat2, lon2 = route_points[i + 1]
            
            # Calculate segment distance
            distance = RiskCalculator.calculate_distance(lat1, lon1, lat2, lon2)
            total_distance += distance
            
            # Get midpoint for risk assessment
            mid_lat = (lat1 + lat2) / 2
            mid_lon = (lon1 + lon2) / 2
            
            # Get nearby accidents
            accidents = RiskCalculator.get_nearby_accidents(
                db, mid_lat, mid_lon, radius_km=1.0
            )
            
            # Calculate segment risk
            segment_risk = len(accidents) * 10  # Simple risk score
            total_risk_score += segment_risk
            
            if segment_risk > 50:
                high_risk_segments.append({
                    'start': (lat1, lon1),
                    'end': (lat2, lon2),
                    'risk_score': segment_risk,
                    'accidents_count': len(accidents)
                })
        
        # Calculate overall risk
        avg_risk_score = total_risk_score / len(route_points) if route_points else 0
        
        if avg_risk_score < 20:
            overall_risk_level = RiskLevel.LOW
        elif avg_risk_score < 50:
            overall_risk_level = RiskLevel.MEDIUM
        else:
            overall_risk_level = RiskLevel.HIGH
        
        return {
            'total_distance_km': round(total_distance, 2),
            'overall_risk_score': round(avg_risk_score, 2),
            'overall_risk_level': overall_risk_level,
            'high_risk_segments': high_risk_segments,
            'segment_count': len(route_points) - 1
        }
