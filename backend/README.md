# Traffic Accident Prediction API - Backend

FastAPI-based backend for predicting traffic accident risks and serving ML models.

## Features

- **Risk Prediction API**: Predict accident risk for specific GPS coordinates
- **Route Analysis**: Analyze safety of entire routes
- **Accident Data Management**: Store and query historical accident data
- **ML Model Integration**: Serve trained machine learning models
- **Real-time Updates**: Support for real-time risk assessment

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (development) / PostgreSQL (production)
- **ML Libraries**: scikit-learn, XGBoost, pandas, numpy
- **ORM**: SQLAlchemy
- **Validation**: Pydantic

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
# Update DATABASE_URL, API keys, etc.
```

### 4. Initialize Database

```bash
# The database will be automatically created on first run
# Or you can initialize it manually:
python -c "from app.database import init_db; init_db()"
```

### 5. Run the Server

```bash
# Development mode (with auto-reload)
python app/main.py

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## API Endpoints

### Prediction

- `POST /api/v1/prediction/risk` - Predict risk for a location
- `POST /api/v1/prediction/route-analysis` - Analyze route safety
- `GET /api/v1/prediction/health` - Health check

### Accidents

- `POST /api/v1/accidents/` - Create accident record
- `POST /api/v1/accidents/nearby` - Get nearby accidents
- `GET /api/v1/accidents/` - List accidents
- `GET /api/v1/accidents/statistics` - Get statistics
- `GET /api/v1/accidents/segments` - List road segments

## Example API Calls

### Predict Risk

```bash
curl -X POST "http://localhost:8000/api/v1/prediction/risk" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 21.0285,
    "longitude": 105.8542,
    "weather_condition": "clear",
    "road_type": "urban"
  }'
```

### Get Nearby Accidents

```bash
curl -X POST "http://localhost:8000/api/v1/accidents/nearby" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 21.0285,
    "longitude": 105.8542,
    "radius_km": 5.0,
    "limit": 50
  }'
```

## Machine Learning Model

### Training the Model

1. Prepare your accident data in the `data/raw/` directory
2. Run the data exploration notebook:
   ```bash
   jupyter notebook notebooks/data_exploration.ipynb
   ```
3. Train the model:
   ```bash
   jupyter notebook notebooks/model_training.ipynb
   ```
4. The trained model will be saved to `data/models/`

### Model Features

The model uses the following features:
- GPS coordinates (latitude, longitude)
- Time features (hour, day of week, weekend, rush hour)
- Weather conditions
- Road type
- Historical accident count

### Fallback Prediction

If no trained model is available, the system uses a heuristic-based fallback prediction that considers:
- Historical accidents in the area
- Weather conditions
- Road type
- Time of day

## Database Schema

### Accidents Table
- Location (latitude, longitude)
- Time information
- Severity
- Road details
- Weather conditions

### Road Segments Table
- Segment boundaries
- Risk metrics
- Accident statistics

### Predictions Table
- Prediction history
- Model version tracking

## Deployment

### Using Docker

```bash
# Build image
docker build -t traffic-accident-api .

# Run container
docker run -p 8000:8000 traffic-accident-api
```

### Deploy to Cloud

#### Heroku
```bash
heroku create your-app-name
git push heroku main
```

#### AWS/GCP
- Use the provided Dockerfile
- Configure environment variables
- Set up PostgreSQL database
- Deploy using your preferred method

## Configuration

Edit `config.py` or set environment variables:

- `DATABASE_URL`: Database connection string
- `MODEL_PATH`: Path to trained ML model
- `LOW_RISK_THRESHOLD`: Threshold for low risk (default: 0.2)
- `HIGH_RISK_THRESHOLD`: Threshold for high risk (default: 0.5)
- `ROAD_SEGMENT_LENGTH_KM`: Road segment size (default: 1.0 km)

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
