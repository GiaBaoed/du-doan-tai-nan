# Quick Setup Guide - Traffic Accident Prediction App

## Prerequisites

- **Python 3.8+** (Python 3.11.4 confirmed working)
- **Flutter SDK 3.10.7+**
- **Android Studio** or **Xcode** (for mobile development)
- **Git**

## Backend Setup (5 minutes)

### 1. Navigate to backend directory
```bash
cd backend
```

### 2. Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
*Note: This may take 3-5 minutes due to large ML libraries*

### 4. Create environment file
```bash
# Copy example file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

### 5. Run the server
```bash
python app/main.py
```

Server will start at: **http://localhost:8000**

API Docs: **http://localhost:8000/docs**

---

## Flutter App Setup (5 minutes)

### 1. Install Flutter dependencies
```bash
# From project root
flutter pub get
```

### 2. Configure Google Maps API Key

**Get API Key:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project
3. Enable "Maps SDK for Android" and "Maps SDK for iOS"
4. Create credentials (API Key)

**Add to Android:**
Edit `android/app/src/main/AndroidManifest.xml`:
```xml
<meta-data
    android:name="com.google.android.geo.API_KEY"
    android:value="YOUR_API_KEY_HERE"/>
```

**Add to iOS:**
Edit `ios/Runner/AppDelegate.swift` (add import and provide key):
```swift
import GoogleMaps

GMSServices.provideAPIKey("YOUR_API_KEY_HERE")
```

**Add to Flutter:**
Edit `lib/config/app_config.dart`:
```dart
static const String googleMapsApiKey = 'YOUR_API_KEY_HERE';
```

### 3. Configure Backend URL

Edit `lib/config/app_config.dart`:

```dart
// For Android Emulator
static const String apiBaseUrl = 'http://10.0.2.2:8000/api/v1';

// For iOS Simulator
static const String apiBaseUrl = 'http://localhost:8000/api/v1';

// For Physical Device (replace with your computer's IP)
static const String apiBaseUrl = 'http://192.168.1.XXX:8000/api/v1';
```

To find your IP:
- **Windows**: `ipconfig` (look for IPv4 Address)
- **Mac/Linux**: `ifconfig` or `ip addr`

### 4. Run the app

```bash
# Check connected devices
flutter devices

# Run on Android
flutter run

# Run on iOS
flutter run -d ios

# Run on specific device
flutter run -d <device-id>
```

---

## Quick Test

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Predict risk
curl -X POST "http://localhost:8000/api/v1/prediction/risk" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 21.0285,
    "longitude": 105.8542
  }'
```

### Test Flutter App

1. Launch app
2. Grant location permission
3. Tap Play button to start tracking
4. Map should show your location
5. Risk indicator should appear at top

---

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in config.py
PORT: int = 8001  # Use different port
```

**Module not found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Flutter Issues

**Pub get fails:**
```bash
flutter clean
flutter pub get
```

**Build fails:**
```bash
flutter clean
flutter pub get
flutter run
```

**Location permission denied:**
- Android: Settings > Apps > du_doan_tai_nan > Permissions > Location
- iOS: Settings > Privacy > Location Services > du_doan_tai_nan

**Map not showing:**
- Verify Google Maps API key is correct
- Check API key has Maps SDK enabled
- Check billing is enabled on Google Cloud

---

## Development Tips

### Backend Development

```bash
# Run with auto-reload
uvicorn app.main:app --reload

# View logs
# Logs appear in terminal

# Access interactive API docs
# Open http://localhost:8000/docs
```

### Flutter Development

```bash
# Hot reload: Press 'r' in terminal or Save file
# Hot restart: Press 'R' in terminal

# View logs
flutter logs

# Build release APK
flutter build apk --release
```

---

## Next Steps

1. ✅ Backend running at http://localhost:8000
2. ✅ Flutter app running on device/emulator
3. 📊 Add sample accident data (see backend/README.md)
4. 🤖 Train ML model (see backend/notebooks/)
5. 🚀 Deploy to production

---

## Support

- **Backend Issues**: See `backend/README.md`
- **Flutter Issues**: See main `README.md`
- **API Documentation**: http://localhost:8000/docs

---

**Estimated Total Setup Time: 10-15 minutes**

Good luck! 🚀
