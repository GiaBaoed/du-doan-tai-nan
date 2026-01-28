import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Application
    APP_NAME: str = "Traffic Accident Prediction API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite:///./traffic_accidents.db"
    # For PostgreSQL: postgresql://user:password@localhost/dbname
    
    # ML Model
    MODEL_PATH: str = "./data/models/accident_risk_model.joblib"
    SCALER_PATH: str = "./data/models/scaler.joblib"
    
    # Risk Thresholds
    LOW_RISK_THRESHOLD: float = 0.2  # < 20% probability
    HIGH_RISK_THRESHOLD: float = 0.5  # > 50% probability
    
    # Geospatial
    ROAD_SEGMENT_LENGTH_KM: float = 1.0  # Segment roads into 1km chunks
    NEARBY_RADIUS_KM: float = 5.0  # Search radius for nearby accidents
    
    # Cache
    CACHE_EXPIRY_SECONDS: int = 300  # 5 minutes
    
    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "*"  # Allow all for development
    ]
    
    # API Keys (set via environment variables)
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    WEATHER_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
