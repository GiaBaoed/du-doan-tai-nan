"""
Accident data API routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.models.database import Accident, RoadSegment
from app.models.schemas import (
    AccidentCreate, AccidentResponse,
    NearbyAccidentsRequest, RoadSegmentResponse,
    StatisticsResponse
)
from app.services.risk_calculator import RiskCalculator

router = APIRouter(prefix="/accidents", tags=["Accidents"])


@router.post("/", response_model=AccidentResponse)
async def create_accident(
    accident: AccidentCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new accident record
    
    This can be used for user-reported accidents or importing historical data
    """
    try:
        # Extract time features
        hour_of_day = accident.accident_date.hour
        day_of_week = accident.accident_date.weekday()
        
        # Create accident record
        db_accident = Accident(
            latitude=accident.latitude,
            longitude=accident.longitude,
            accident_date=accident.accident_date,
            hour_of_day=hour_of_day,
            day_of_week=day_of_week,
            severity=accident.severity,
            road_name=accident.road_name,
            road_type=accident.road_type.value if accident.road_type else None,
            weather_condition=accident.weather_condition.value if accident.weather_condition else None,
            description=accident.description,
            num_casualties=accident.num_casualties,
            num_vehicles=accident.num_vehicles,
            reported_by="user"
        )
        
        db.add(db_accident)
        db.commit()
        db.refresh(db_accident)
        
        # Update road segment statistics
        segment_id = RiskCalculator.generate_segment_id(
            accident.latitude,
            accident.longitude
        )
        
        # Check if segment exists, create if not
        segment = db.query(RoadSegment).filter(
            RoadSegment.segment_id == segment_id
        ).first()
        
        if segment:
            RiskCalculator.update_segment_statistics(db, segment_id)
        
        return AccidentResponse(
            id=db_accident.id,
            latitude=db_accident.latitude,
            longitude=db_accident.longitude,
            accident_date=db_accident.accident_date,
            severity=db_accident.severity,
            road_name=db_accident.road_name,
            road_type=db_accident.road_type,
            weather_condition=db_accident.weather_condition
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating accident: {str(e)}")


@router.post("/nearby", response_model=List[AccidentResponse])
async def get_nearby_accidents(
    request: NearbyAccidentsRequest,
    db: Session = Depends(get_db)
):
    """
    Get accidents near a specific location
    
    Returns list of accidents within specified radius
    """
    try:
        accidents = RiskCalculator.get_nearby_accidents(
            db,
            request.latitude,
            request.longitude,
            radius_km=request.radius_km,
            limit=request.limit
        )
        
        return [
            AccidentResponse(
                id=accident.id,
                latitude=accident.latitude,
                longitude=accident.longitude,
                accident_date=accident.accident_date,
                severity=accident.severity,
                road_name=accident.road_name,
                road_type=accident.road_type,
                weather_condition=accident.weather_condition,
                distance_km=round(accident.distance_km, 2)
            )
            for accident in accidents
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching accidents: {str(e)}")


@router.get("/", response_model=List[AccidentResponse])
async def list_accidents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    severity: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    List accidents with optional filters
    """
    try:
        query = db.query(Accident)
        
        # Apply filters
        if severity:
            query = query.filter(Accident.severity == severity)
        
        if start_date:
            query = query.filter(Accident.accident_date >= start_date)
        
        if end_date:
            query = query.filter(Accident.accident_date <= end_date)
        
        # Order by date descending
        query = query.order_by(desc(Accident.accident_date))
        
        # Pagination
        accidents = query.offset(skip).limit(limit).all()
        
        return [
            AccidentResponse(
                id=accident.id,
                latitude=accident.latitude,
                longitude=accident.longitude,
                accident_date=accident.accident_date,
                severity=accident.severity,
                road_name=accident.road_name,
                road_type=accident.road_type,
                weather_condition=accident.weather_condition
            )
            for accident in accidents
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing accidents: {str(e)}")


@router.get("/statistics", response_model=StatisticsResponse)
async def get_statistics(
    days: int = Query(365, ge=1, le=3650),
    db: Session = Depends(get_db)
):
    """
    Get accident statistics for specified time period
    """
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get accidents in date range
        accidents = db.query(Accident).filter(
            Accident.accident_date >= start_date
        ).all()
        
        total_accidents = len(accidents)
        
        # Accidents by severity
        accidents_by_severity = {}
        for accident in accidents:
            severity = accident.severity or "unknown"
            accidents_by_severity[severity] = accidents_by_severity.get(severity, 0) + 1
        
        # Accidents by road type
        accidents_by_road_type = {}
        for accident in accidents:
            road_type = accident.road_type or "unknown"
            accidents_by_road_type[road_type] = accidents_by_road_type.get(road_type, 0) + 1
        
        # Accidents by hour
        accidents_by_hour = {}
        for accident in accidents:
            hour = accident.hour_of_day
            if hour is not None:
                accidents_by_hour[str(hour)] = accidents_by_hour.get(str(hour), 0) + 1
        
        # Accidents by day of week
        accidents_by_day = {}
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for accident in accidents:
            day = accident.day_of_week
            if day is not None:
                day_name = day_names[day]
                accidents_by_day[day_name] = accidents_by_day.get(day_name, 0) + 1
        
        # Count high risk segments
        high_risk_segments = db.query(RoadSegment).filter(
            RoadSegment.risk_level == "high"
        ).count()
        
        return StatisticsResponse(
            total_accidents=total_accidents,
            accidents_by_severity=accidents_by_severity,
            accidents_by_road_type=accidents_by_road_type,
            accidents_by_hour=accidents_by_hour,
            accidents_by_day=accidents_by_day,
            high_risk_segments_count=high_risk_segments,
            last_updated=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")


@router.get("/segments", response_model=List[RoadSegmentResponse])
async def list_road_segments(
    risk_level: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    List road segments with optional risk level filter
    """
    try:
        query = db.query(RoadSegment)
        
        if risk_level:
            query = query.filter(RoadSegment.risk_level == risk_level)
        
        # Order by risk score descending
        query = query.order_by(desc(RoadSegment.risk_score))
        
        segments = query.offset(skip).limit(limit).all()
        
        return [
            RoadSegmentResponse(
                segment_id=segment.segment_id,
                start_lat=segment.start_lat,
                start_lon=segment.start_lon,
                end_lat=segment.end_lat,
                end_lon=segment.end_lon,
                road_name=segment.road_name,
                road_type=segment.road_type,
                total_accidents=segment.total_accidents,
                accidents_last_year=segment.accidents_last_year,
                risk_score=segment.risk_score,
                risk_level=segment.risk_level,
                last_updated=segment.last_updated
            )
            for segment in segments
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing segments: {str(e)}")


@router.delete("/{accident_id}")
async def delete_accident(
    accident_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an accident record (admin only in production)
    """
    try:
        accident = db.query(Accident).filter(Accident.id == accident_id).first()
        
        if not accident:
            raise HTTPException(status_code=404, detail="Accident not found")
        
        db.delete(accident)
        db.commit()
        
        return {"message": "Accident deleted successfully", "id": accident_id}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting accident: {str(e)}")
