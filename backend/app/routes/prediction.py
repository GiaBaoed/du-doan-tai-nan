"""
Prediction API routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.schemas import (
    PredictionRequest, PredictionResponse,
    RouteAnalysisRequest, RouteAnalysisResponse,
    RouteSegmentRisk, RoutePoint, RiskLevel
)
from app.models.ml_model import accident_model
from app.services.risk_calculator import RiskCalculator
from config import settings

router = APIRouter(prefix="/prediction", tags=["Prediction"])


@router.post("/risk", response_model=PredictionResponse)
async def predict_risk(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Predict accident risk for a specific location
    
    Returns risk level (low/medium/high), probability, and warning message
    """
    try:
        # Get nearby accidents for context
        nearby_accidents = RiskCalculator.get_nearby_accidents(
            db,
            request.latitude,
            request.longitude,
            radius_km=settings.NEARBY_RADIUS_KM
        )
        
        # Generate segment ID
        segment_id = RiskCalculator.generate_segment_id(
            request.latitude,
            request.longitude
        )
        
        # Prepare timestamp
        timestamp = request.timestamp or datetime.now()
        
        # Get prediction from ML model
        risk_level, risk_probability = accident_model.predict_risk(
            latitude=request.latitude,
            longitude=request.longitude,
            timestamp=timestamp,
            weather_condition=request.weather_condition.value if request.weather_condition else "clear",
            road_type=request.road_type.value if request.road_type else "urban",
            historical_accidents=len(nearby_accidents)
        )
        
        # Get appropriate message
        messages = accident_model.get_risk_message(risk_level, language="vi")
        
        # Calculate risk score (0-100)
        risk_score = risk_probability * 100
        
        return PredictionResponse(
            latitude=request.latitude,
            longitude=request.longitude,
            risk_level=RiskLevel(risk_level),
            risk_probability=risk_probability,
            risk_score=risk_score,
            message=messages["message"],
            warning_message=messages["warning"],
            nearby_accidents_count=len(nearby_accidents),
            road_segment_id=segment_id,
            timestamp=timestamp
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.post("/route-analysis", response_model=RouteAnalysisResponse)
async def analyze_route(
    request: RouteAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze safety of an entire route
    
    Provides risk assessment for each segment and overall route safety
    """
    try:
        if len(request.route_points) < 2:
            raise HTTPException(
                status_code=400,
                detail="Route must have at least 2 points"
            )
        
        # Sort route points by order
        sorted_points = sorted(request.route_points, key=lambda p: p.order)
        
        # Convert to coordinate tuples
        route_coords = [(p.latitude, p.longitude) for p in sorted_points]
        
        # Analyze route
        analysis = RiskCalculator.analyze_route(db, route_coords)
        
        # Build segment risks
        segment_risks = []
        total_distance = 0
        high_risk_count = 0
        
        for i in range(len(sorted_points) - 1):
            start_point = sorted_points[i]
            end_point = sorted_points[i + 1]
            
            # Calculate segment distance
            distance = RiskCalculator.calculate_distance(
                start_point.latitude, start_point.longitude,
                end_point.latitude, end_point.longitude
            )
            total_distance += distance
            
            # Get midpoint for risk assessment
            mid_lat = (start_point.latitude + end_point.latitude) / 2
            mid_lon = (start_point.longitude + end_point.longitude) / 2
            
            # Get prediction for segment
            risk_level, risk_probability = accident_model.predict_risk(
                latitude=mid_lat,
                longitude=mid_lon,
                historical_accidents=len(RiskCalculator.get_nearby_accidents(
                    db, mid_lat, mid_lon, radius_km=1.0
                ))
            )
            
            if risk_level == "high":
                high_risk_count += 1
            
            # Estimate time (assuming 50 km/h average speed)
            estimated_time = (distance / 50) * 60  # minutes
            
            segment_risks.append(RouteSegmentRisk(
                start_point=start_point,
                end_point=end_point,
                risk_level=RiskLevel(risk_level),
                risk_score=risk_probability * 100,
                distance_km=round(distance, 2),
                estimated_time_minutes=round(estimated_time, 1),
                accidents_count=len(RiskCalculator.get_nearby_accidents(
                    db, mid_lat, mid_lon, radius_km=1.0
                ))
            ))
        
        # Calculate overall metrics
        avg_risk_score = sum(s.risk_score for s in segment_risks) / len(segment_risks)
        estimated_total_time = sum(s.estimated_time_minutes for s in segment_risks)
        
        # Determine overall risk level
        if avg_risk_score < 20:
            overall_risk_level = RiskLevel.LOW
        elif avg_risk_score < 50:
            overall_risk_level = RiskLevel.MEDIUM
        else:
            overall_risk_level = RiskLevel.HIGH
        
        # Generate recommendations
        recommendations = []
        if high_risk_count > 0:
            recommendations.append(
                f"Tuyến đường có {high_risk_count} đoạn nguy hiểm. Cân nhắc chọn tuyến đường khác."
            )
        if overall_risk_level == RiskLevel.HIGH:
            recommendations.append(
                "Mức độ rủi ro tổng thể cao. Giảm tốc độ và tăng cường cảnh giác."
            )
        if avg_risk_score > 30:
            recommendations.append(
                "Tránh di chuyển vào giờ cao điểm hoặc thời tiết xấu nếu có thể."
            )
        if not recommendations:
            recommendations.append(
                "Tuyến đường tương đối an toàn. Vẫn cần chú ý quan sát."
            )
        
        return RouteAnalysisResponse(
            total_distance_km=round(total_distance, 2),
            estimated_time_minutes=round(estimated_total_time, 1),
            overall_risk_level=overall_risk_level,
            overall_risk_score=round(avg_risk_score, 2),
            segment_risks=segment_risks,
            high_risk_segments_count=high_risk_count,
            recommendations=recommendations
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Route analysis error: {str(e)}")


@router.get("/health")
async def health_check():
    """Check if prediction service is healthy"""
    return {
        "status": "healthy",
        "model_loaded": accident_model.is_trained,
        "timestamp": datetime.now().isoformat()
    }
