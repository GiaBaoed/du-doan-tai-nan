"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class RiskLevel(str, Enum):
    """Risk level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RoadType(str, Enum):
    """Road type enumeration"""
    HIGHWAY = "highway"
    NATIONAL_ROAD = "national_road"
    URBAN = "urban"
    RURAL = "rural"


class WeatherCondition(str, Enum):
    """Weather condition enumeration"""
    CLEAR = "clear"
    RAIN = "rain"
    FOG = "fog"
    SNOW = "snow"
    STORM = "storm"


class LocationRequest(BaseModel):
    """Request schema for location-based queries"""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    
    @validator('latitude')
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError('Latitude must be between -90 and 90')
        return v
    
    @validator('longitude')
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError('Longitude must be between -180 and 180')
        return v


class PredictionRequest(BaseModel):
    """Request schema for risk prediction"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timestamp: Optional[datetime] = None
    weather_condition: Optional[WeatherCondition] = WeatherCondition.CLEAR
    road_type: Optional[RoadType] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "latitude": 21.0285,
                "longitude": 105.8542,
                "timestamp": "2024-01-15T14:30:00",
                "weather_condition": "clear",
                "road_type": "urban"
            }
        }


class PredictionResponse(BaseModel):
    """Response schema for risk prediction"""
    latitude: float
    longitude: float
    risk_level: RiskLevel
    risk_probability: float = Field(..., ge=0, le=1)
    risk_score: float = Field(..., ge=0, le=100)
    message: str
    warning_message: Optional[str] = None
    nearby_accidents_count: int = 0
    road_segment_id: Optional[str] = None
    timestamp: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "latitude": 21.0285,
                "longitude": 105.8542,
                "risk_level": "medium",
                "risk_probability": 0.35,
                "risk_score": 35.0,
                "message": "Đoạn đường hay xảy ra tai nạn, xin chú ý",
                "warning_message": "Cẩn thận khi lái xe trong khu vực này",
                "nearby_accidents_count": 5,
                "road_segment_id": "SEG_21.028_105.854",
                "timestamp": "2024-01-15T14:30:00"
            }
        }


class AccidentCreate(BaseModel):
    """Schema for creating accident record"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    accident_date: datetime
    severity: str
    road_name: Optional[str] = None
    road_type: Optional[RoadType] = None
    weather_condition: Optional[WeatherCondition] = WeatherCondition.CLEAR
    description: Optional[str] = None
    num_casualties: int = 0
    num_vehicles: int = 1


class AccidentResponse(BaseModel):
    """Response schema for accident data"""
    id: int
    latitude: float
    longitude: float
    accident_date: datetime
    severity: str
    road_name: Optional[str]
    road_type: Optional[str]
    weather_condition: Optional[str]
    distance_km: Optional[float] = None
    
    class Config:
        from_attributes = True


class RoadSegmentResponse(BaseModel):
    """Response schema for road segment data"""
    segment_id: str
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float
    road_name: Optional[str]
    road_type: Optional[str]
    total_accidents: int
    accidents_last_year: int
    risk_score: float
    risk_level: RiskLevel
    last_updated: datetime
    
    class Config:
        from_attributes = True


class RoutePoint(BaseModel):
    """Single point in a route"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    order: int = Field(..., ge=0)


class RouteAnalysisRequest(BaseModel):
    """Request schema for route safety analysis"""
    route_points: List[RoutePoint] = Field(..., min_length=2)
    
    class Config:
        json_schema_extra = {
            "example": {
                "route_points": [
                    {"latitude": 21.0285, "longitude": 105.8542, "order": 0},
                    {"latitude": 21.0385, "longitude": 105.8642, "order": 1},
                    {"latitude": 21.0485, "longitude": 105.8742, "order": 2}
                ]
            }
        }


class RouteSegmentRisk(BaseModel):
    """Risk information for a route segment"""
    start_point: RoutePoint
    end_point: RoutePoint
    risk_level: RiskLevel
    risk_score: float
    distance_km: float
    estimated_time_minutes: float
    accidents_count: int


class RouteAnalysisResponse(BaseModel):
    """Response schema for route analysis"""
    total_distance_km: float
    estimated_time_minutes: float
    overall_risk_level: RiskLevel
    overall_risk_score: float
    segment_risks: List[RouteSegmentRisk]
    high_risk_segments_count: int
    recommendations: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_distance_km": 15.5,
                "estimated_time_minutes": 25,
                "overall_risk_level": "medium",
                "overall_risk_score": 42.5,
                "segment_risks": [],
                "high_risk_segments_count": 2,
                "recommendations": [
                    "Cẩn thận tại km 5-7, đoạn đường có mức độ tai nạn cao",
                    "Giảm tốc độ khi đi qua khu vực đông dân cư"
                ]
            }
        }


class NearbyAccidentsRequest(BaseModel):
    """Request schema for nearby accidents query"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_km: float = Field(default=5.0, ge=0.1, le=50)
    limit: int = Field(default=50, ge=1, le=500)


class StatisticsResponse(BaseModel):
    """Response schema for statistics"""
    total_accidents: int
    accidents_by_severity: dict
    accidents_by_road_type: dict
    accidents_by_hour: dict
    accidents_by_day: dict
    high_risk_segments_count: int
    last_updated: datetime
