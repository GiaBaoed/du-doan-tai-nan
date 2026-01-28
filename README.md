# Dự Đoán Tai Nạn Giao Thông - Traffic Accident Prediction & Warning App

Ứng dụng di động cảnh báo tai nạn giao thông theo thời gian thực sử dụng Machine Learning và GPS.

## 📱 Tổng Quan

Ứng dụng phân tích dữ liệu tai nạn giao thông lịch sử để dự báo nguy cơ tai nạn trên các đoạn đường cụ thể. Khi người dùng di chuyển, ứng dụng sẽ:

- **Hiển thị màu sắc theo mức độ rủi ro** trên bản đồ:
  - 🟢 **Xanh (An toàn)**: Đoạn đường ít tai nạn
  - 🟡 **Vàng (Chú ý)**: Đoạn đường thường xuyên xảy ra tai nạn
  - 🔴 **Đỏ (Nguy hiểm)**: Đoạn đường có tần suất tai nạn cao

- **Cảnh báo tự động** bằng giọng nói và thông báo push
- **Theo dõi vị trí GPS** liên tục
- **Hiển thị tai nạn gần đó** trên bản đồ

## 🎯 Tính Năng Chính

### Ứng Dụng Mobile (Flutter)
- ✅ Bản đồ tương tác với Google Maps
- ✅ Theo dõi GPS thời gian thực
- ✅ Cảnh báo bằng giọng nói (Tiếng Việt)
- ✅ Thông báo push khi vào vùng nguy hiểm
- ✅ Hiển thị tai nạn lịch sử gần đó
- ✅ Phân tích độ an toàn của tuyến đường
- ✅ Giao diện thân thiện, dễ sử dụng

### Backend API (Python/FastAPI)
- ✅ API dự đoán rủi ro tai nạn
- ✅ Mô hình Machine Learning
- ✅ Quản lý dữ liệu tai nạn
- ✅ Phân tích tuyến đường
- ✅ Thống kê và báo cáo

## 🏗️ Kiến Trúc Hệ Thống

```
┌─────────────────────────────────────────────────────────┐
│                   Flutter Mobile App                     │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐   │
│  │   Map    │  │   GPS    │  │   Notifications    │   │
│  │ Display  │  │ Tracking │  │  (Voice + Push)    │   │
│  └──────────┘  └──────────┘  └────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                         │
                    HTTP/REST API
                         │
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend Server                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Prediction  │  │  ML Model    │  │   Database   │ │
│  │     API      │  │   Service    │  │  (SQLite/    │ │
│  │              │  │              │  │  PostgreSQL) │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Cài Đặt và Chạy

### Yêu Cầu Hệ Thống

- **Flutter**: SDK 3.10.7 trở lên
- **Python**: 3.8 trở lên
- **Node.js**: (tùy chọn, cho công cụ phát triển)
- **Android Studio** hoặc **Xcode** (để chạy trên thiết bị)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/du_doan_tai_nan.git
cd du_doan_tai_nan
```

### 2. Cài Đặt Backend

```bash
cd backend

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy server
python app/main.py
```

Backend sẽ chạy tại: `http://localhost:8000`

Xem API docs tại: `http://localhost:8000/docs`

### 3. Cài Đặt Flutter App

```bash
# Quay lại thư mục gốc
cd ..

# Cài đặt dependencies
flutter pub get

# Chạy app (Android)
flutter run

# Hoặc chạy trên iOS
flutter run -d ios
```

### 4. Cấu Hình

#### Google Maps API Key

1. Lấy API key từ [Google Cloud Console](https://console.cloud.google.com/)
2. Bật Google Maps SDK for Android/iOS
3. Cập nhật API key:

**Android**: `android/app/src/main/AndroidManifest.xml`
```xml
<meta-data
    android:name="com.google.android.geo.API_KEY"
    android:value="YOUR_API_KEY_HERE"/>
```

**iOS**: `ios/Runner/AppDelegate.swift`
```swift
GMSServices.provideAPIKey("YOUR_API_KEY_HERE")
```

**Flutter**: `lib/config/app_config.dart`
```dart
static const String googleMapsApiKey = 'YOUR_API_KEY_HERE';
```

#### Backend URL

Cập nhật URL backend trong `lib/config/app_config.dart`:

```dart
// Cho Android emulator
static const String apiBaseUrl = 'http://10.0.2.2:8000/api/v1';

// Cho iOS simulator
static const String apiBaseUrl = 'http://localhost:8000/api/v1';

// Cho thiết bị thật (thay YOUR_IP bằng IP máy tính)
static const String apiBaseUrl = 'http://YOUR_IP:8000/api/v1';
```

## 📖 Hướng Dẫn Sử Dụng

### Khởi Động Ứng Dụng

1. **Mở ứng dụng** - Cho phép quyền truy cập vị trí
2. **Nhấn nút Play** ▶️ - Bắt đầu theo dõi
3. **Di chuyển** - Ứng dụng sẽ tự động cảnh báo

### Màu Sắc Cảnh Báo

- 🟢 **Xanh**: Đoạn đường an toàn, ít tai nạn
- 🟡 **Vàng**: Cần chú ý, đoạn đường có tai nạn trung bình
- 🔴 **Đỏ**: Nguy hiểm cao, giảm tốc độ và cẩn thận

### Cảnh Báo

- **Giọng nói**: "Đoạn đường có mức độ tai nạn cao, xin lái xe cẩn thận"
- **Thông báo**: Popup trên màn hình
- **Bản đồ**: Vùng màu đỏ xung quanh vị trí nguy hiểm

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov=app tests/
```

### Flutter Tests

```bash
flutter test
flutter test --coverage
```

## 📊 Dữ Liệu và Machine Learning

### Thu Thập Dữ Liệu

Dữ liệu tai nạn có thể thu thập từ:
- Cục CSGT Việt Nam
- Bộ GTVT
- Dữ liệu mở (Kaggle, Open Data Portal)
- Báo cáo người dùng

### Huấn Luyện Mô Hình

```bash
cd backend
jupyter notebook notebooks/model_training.ipynb
```

Mô hình sử dụng:
- **Random Forest** / **XGBoost** cho phân loại
- Features: GPS, thời gian, thời tiết, loại đường, lịch sử tai nạn
- Output: Mức độ rủi ro (Low/Medium/High)

## 🚢 Deployment

### Backend (Heroku)

```bash
cd backend
heroku create your-app-name
git push heroku main
```

### Mobile App

#### Android
```bash
flutter build apk --release
# APK tại: build/app/outputs/flutter-apk/app-release.apk
```

#### iOS
```bash
flutter build ios --release
# Mở Xcode để archive và upload
```

## 📁 Cấu Trúc Thư Mục

```
du_doan_tai_nan/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── models/         # Database & ML models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── main.py         # App entry point
│   ├── data/               # Data & trained models
│   ├── notebooks/          # Jupyter notebooks
│   └── requirements.txt
│
├── lib/                    # Flutter app source
│   ├── config/            # Configuration
│   ├── models/            # Data models
│   ├── providers/         # State management
│   ├── screens/           # UI screens
│   ├── services/          # API, GPS, notifications
│   ├── widgets/           # Reusable widgets
│   └── main.dart          # App entry point
│
├── android/               # Android specific
├── ios/                   # iOS specific
└── README.md
```

## 🤝 Đóng Góp

Chúng tôi hoan nghênh mọi đóng góp! Vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📝 License

MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết

## 👥 Tác Giả

- **Your Name** - *Initial work*

## 🙏 Cảm Ơn

- Flutter team
- FastAPI team
- Google Maps Platform
- Cộng đồng open source

## 📞 Liên Hệ

- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

## 🔮 Tính Năng Tương Lai

- [ ] Tích hợp dữ liệu thời tiết thời gian thực
- [ ] Gợi ý tuyến đường an toàn hơn
- [ ] Báo cáo tai nạn từ người dùng
- [ ] Thống kê chi tiết theo khu vực
- [ ] Hỗ trợ nhiều ngôn ngữ
- [ ] Chế độ offline
- [ ] Tích hợp với camera giao thông

---

**⚠️ Lưu Ý**: Đây là ứng dụng hỗ trợ, không thay thế cho việc tuân thủ luật giao thông và lái xe cẩn thận. Luôn chú ý quan sát và tuân thủ biển báo giao thông.
