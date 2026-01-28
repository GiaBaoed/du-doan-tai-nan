"""
Database models for traffic accident data
"""

from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class Accident(Base):
    """Model for storing accident records"""
    __tablename__ = "accidents"
    
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    
    # Time information
    accident_date = Column(DateTime, nullable=False, index=True)
    hour_of_day = Column(Integer)  # 0-23
    day_of_week = Column(Integer)  # 0-6 (Monday-Sunday)
    
    # Location details
    road_name = Column(String(255))
    road_type = Column(String(50))  # highway, national_road, urban, rural
    district = Column(String(100))
    city = Column(String(100))
    
    # Accident details
    severity = Column(String(20))  # minor, moderate, severe, fatal
    num_casualties = Column(Integer, default=0)
    num_vehicles = Column(Integer, default=1)
    accident_type = Column(String(100))  # collision, pedestrian, single_vehicle, etc.
    
    # Environmental conditions
    weather_condition = Column(String(50))  # clear, rain, fog, etc.
    road_condition = Column(String(50))  # dry, wet, icy
    light_condition = Column(String(50))  # daylight, dark, dawn/dusk
    
    # Additional info
    description = Column(Text)
    reported_by = Column(String(100))  # user, official, system
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Accident(id={self.id}, date={self.accident_date}, severity={self.severity})>"


class RoadSegment(Base):
    """Model for storing road segment risk data"""
    __tablename__ = "road_segments"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Segment boundaries
    start_lat = Column(Float, nullable=False)
    start_lon = Column(Float, nullable=False)
    end_lat = Column(Float, nullable=False)
    end_lon = Column(Float, nullable=False)
    
    # Segment info
    segment_id = Column(String(100), unique=True, index=True)
    road_name = Column(String(255))
    road_type = Column(String(50))
    length_km = Column(Float)
    
    # Risk metrics
    total_accidents = Column(Integer, default=0)
    accidents_last_year = Column(Integer, default=0)
    accidents_last_month = Column(Integer, default=0)
    risk_score = Column(Float, default=0.0)  # 0.0 - 1.0
    risk_level = Column(String(20))  # low, medium, high
    
    # Statistics
    avg_severity = Column(Float)
    peak_accident_hour = Column(Integer)  # Hour with most accidents
    
    # Metadata
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<RoadSegment(id={self.segment_id}, risk={self.risk_level})>"


class Prediction(Base):
    """Model for storing prediction history"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Prediction
    risk_probability = Column(Float)  # 0.0 - 1.0
    risk_level = Column(String(20))  # low, medium, high
    
    # Context
    timestamp = Column(DateTime, default=func.now())
    weather_condition = Column(String(50))
    time_of_day = Column(Integer)
    
    # Model info
    model_version = Column(String(50))
    
    def __repr__(self):
        return f"<Prediction(risk={self.risk_level}, prob={self.risk_probability})>"
