# 🚀 Hướng Dẫn Upload Dự Án Lên GitHub

## ✅ Trạng Thái Hiện Tại

- ✅ Git repository đã được khởi tạo
- ✅ Đã commit 92 files dự án
- ✅ Đã loại bỏ các files không cần thiết (windows, linux, macos, web, test)
- ✅ File .gitignore đã được cấu hình đúng

## 📊 Thống Kê Dự Án

**Tổng số files đã commit:** 92 files  
**Tổng số dòng code:** 6,724 dòng

### Cấu Trúc Files:
- **Documentation:** 4 files (README.md, SETUP_GUIDE.md, TODO.md, CLEANUP_SUMMARY.md)
- **Flutter App:** 13 files (lib/)
- **Android Platform:** 22 files
- **iOS Platform:** 39 files  
- **Backend API:** 11 files (Python/FastAPI)
- **Configuration:** 3 files

---

## 🌐 Cách 1: Tạo Repository Trên GitHub (Khuyến Nghị)

### Bước 1: Tạo Repository Mới Trên GitHub

1. Truy cập: https://github.com/new
2. Điền thông tin:
   - **Repository name:** `du-doan-tai-nan` hoặc `traffic-accident-prediction`
   - **Description:** `🚗 Ứng dụng dự đoán và cảnh báo tai nạn giao thông sử dụng Flutter + FastAPI + Machine Learning`
   - **Visibility:** Chọn Public hoặc Private
   - ⚠️ **KHÔNG** chọn "Initialize this repository with a README"
   - ⚠️ **KHÔNG** thêm .gitignore hoặc license (đã có sẵn)

3. Click **"Create repository"**

### Bước 2: Push Code Lên GitHub

Sau khi tạo repository, GitHub sẽ hiển thị hướng dẫn. Chạy các lệnh sau trong terminal:

```bash
# Thêm remote repository (thay YOUR_USERNAME bằng username GitHub của bạn)
git remote add origin https://github.com/YOUR_USERNAME/du-doan-tai-nan.git

# Đổi tên branch thành main (nếu cần)
git branch -M main

# Push code lên GitHub
git push -u origin main
```

**Ví dụ cụ thể:**
```bash
git remote add origin https://github.com/nguyenvana/du-doan-tai-nan.git
git branch -M main
git push -u origin main
```

### Bước 3: Xác Nhận

Sau khi push thành công, truy cập:
```
https://github.com/YOUR_USERNAME/du-doan-tai-nan
```

Bạn sẽ thấy tất cả 92 files đã được upload!

---

## 🔧 Cách 2: Sử Dụng GitHub CLI (Tự Động)

### Cài Đặt GitHub CLI

**Windows (Winget):**
```bash
winget install --id GitHub.cli
```

**Windows (Chocolatey):**
```bash
choco install gh
```

**Hoặc tải từ:** https://cli.github.com/

### Sau Khi Cài Đặt

```bash
# Đăng nhập GitHub
gh auth login

# Tạo repository và push (tự động)
gh repo create du-doan-tai-nan --public --source=. --remote=origin --push

# Hoặc tạo private repository
gh repo create du-doan-tai-nan --private --source=. --remote=origin --push
```

---

## 📝 Các Lệnh Git Hữu Ích

### Kiểm Tra Trạng Thái
```bash
# Xem trạng thái hiện tại
git status

# Xem lịch sử commit
git log --oneline

# Xem remote repository
git remote -v

# Đếm số files đã commit
git ls-files | wc -l
```

### Cập Nhật Code Sau Này
```bash
# Thêm files mới/thay đổi
git add .

# Tạo commit
git commit -m "Mô tả thay đổi"

# Push lên GitHub
git push origin main
```

### Tạo Branch Mới
```bash
# Tạo và chuyển sang branch mới
git checkout -b feature/ten-tinh-nang

# Push branch mới lên GitHub
git push -u origin feature/ten-tinh-nang
```

---

## 🎯 Sau Khi Upload Thành Công

### 1. Cập Nhật README.md

Thay đổi dòng này trong README.md:
```markdown
git clone https://github.com/yourusername/du_doan_tai_nan.git
```

Thành:
```markdown
git clone https://github.com/YOUR_ACTUAL_USERNAME/du-doan-tai-nan.git
```

### 2. Thêm Topics/Tags

Trên GitHub repository, click **"Add topics"** và thêm:
- `flutter`
- `fastapi`
- `machine-learning`
- `traffic-safety`
- `accident-prediction`
- `mobile-app`
- `vietnam`

### 3. Tạo GitHub Pages (Tùy Chọn)

Nếu muốn tạo trang web giới thiệu dự án:
1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: main → /docs (hoặc tạo branch gh-pages)

### 4. Bật GitHub Actions (Tùy Chọn)

Tạo file `.github/workflows/flutter.yml` để tự động build và test:

```yaml
name: Flutter CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.10.7'
    - run: flutter pub get
    - run: flutter analyze
    - run: flutter build apk
```

---

## 🔒 Bảo Mật

### Files Không Nên Commit (Đã Được .gitignore Bảo Vệ)

- ✅ `backend/venv/` - Virtual environment
- ✅ `backend/__pycache__/` - Python cache
- ✅ `build/` - Build artifacts
- ✅ `.env` - Environment variables (chứa API keys)
- ✅ `*.db`, `*.sqlite` - Database files

### Nếu Đã Commit Nhầm File Nhạy Cảm

```bash
# Xóa file khỏi Git nhưng giữ lại local
git rm --cached path/to/sensitive/file

# Thêm vào .gitignore
echo "path/to/sensitive/file" >> .gitignore

# Commit thay đổi
git add .gitignore
git commit -m "Remove sensitive file from Git"
git push origin main
```

---

## 📞 Link Repository Sau Khi Tạo

Sau khi hoàn thành, link repository của bạn sẽ là:

```
https://github.com/YOUR_USERNAME/du-doan-tai-nan
```

**Clone URL:**
```bash
# HTTPS
https://github.com/YOUR_USERNAME/du-doan-tai-nan.git

# SSH (nếu đã setup SSH key)
git@github.com:YOUR_USERNAME/du-doan-tai-nan.git
```

---

## ✅ Checklist Hoàn Thành

- [ ] Tạo repository trên GitHub
- [ ] Push code lên GitHub
- [ ] Cập nhật README.md với link đúng
- [ ] Thêm description và topics
- [ ] Kiểm tra tất cả 92 files đã được upload
- [ ] Test clone repository về máy khác
- [ ] Chia sẻ link với team/cộng đồng

---

## 🎉 Hoàn Thành!

Dự án của bạn đã sẵn sàng trên GitHub với:
- ✅ 92 files source code
- ✅ Documentation đầy đủ
- ✅ .gitignore được cấu hình đúng
- ✅ Cấu trúc dự án chuyên nghiệp

**Chúc mừng! 🎊**
