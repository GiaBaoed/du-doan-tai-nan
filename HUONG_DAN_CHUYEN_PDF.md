# 📄 HƯỚNG DẪN CHUYỂN BÁO CÁO SANG PDF

## 🎯 File Báo Cáo

**File Markdown:** `BAO_CAO_TIEU_LUAN.md`  
**Kích thước:** ~50 trang  
**Nội dung:** Báo cáo tiểu luận đầy đủ về dự án

---

## 🚀 CÁCH 1: Sử Dụng VSCode (Khuyến Nghị)

### Bước 1: Cài Extension

1. Mở VSCode
2. Vào Extensions (Ctrl + Shift + X)
3. Tìm và cài đặt: **"Markdown PDF"** by yzane

### Bước 2: Chuyển Đổi

1. Mở file `BAO_CAO_TIEU_LUAN.md` trong VSCode
2. Nhấn `Ctrl + Shift + P` (hoặc `Cmd + Shift + P` trên Mac)
3. Gõ: `Markdown PDF: Export (pdf)`
4. Chọn và nhấn Enter

### Kết Quả

File PDF sẽ được tạo tại: `BAO_CAO_TIEU_LUAN.pdf`

---

## 🌐 CÁCH 2: Sử Dụng Online Tools

### Option A: Dillinger.io

1. Truy cập: https://dillinger.io/
2. Copy toàn bộ nội dung file `BAO_CAO_TIEU_LUAN.md`
3. Paste vào Dillinger
4. Click **Export as** → **PDF**

### Option B: Markdown to PDF

1. Truy cập: https://www.markdowntopdf.com/
2. Upload file `BAO_CAO_TIEU_LUAN.md`
3. Click **Convert**
4. Download file PDF

### Option C: CloudConvert

1. Truy cập: https://cloudconvert.com/md-to-pdf
2. Upload file `BAO_CAO_TIEU_LUAN.md`
3. Click **Convert**
4. Download file PDF

---

## 💻 CÁCH 3: Sử Dụng Pandoc (Chuyên Nghiệp)

### Cài Đặt Pandoc

**Windows:**
```bash
# Sử dụng Chocolatey
choco install pandoc

# Hoặc tải từ: https://pandoc.org/installing.html
```

**Mac:**
```bash
brew install pandoc
```

**Linux:**
```bash
sudo apt-get install pandoc
```

### Cài Thêm LaTeX (Cho PDF đẹp hơn)

**Windows:**
```bash
choco install miktex
```

**Mac:**
```bash
brew install --cask mactex
```

**Linux:**
```bash
sudo apt-get install texlive-full
```

### Chuyển Đổi

**Cơ bản:**
```bash
pandoc BAO_CAO_TIEU_LUAN.md -o BAO_CAO_TIEU_LUAN.pdf
```

**Nâng cao (với styling):**
```bash
pandoc BAO_CAO_TIEU_LUAN.md -o BAO_CAO_TIEU_LUAN.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=2.5cm \
  -V fontsize=12pt \
  -V documentclass=report \
  -V lang=vi \
  --toc \
  --toc-depth=3 \
  --number-sections
```

**Giải thích options:**
- `--pdf-engine=xelatex`: Engine hỗ trợ tiếng Việt tốt
- `-V geometry:margin=2.5cm`: Lề 2.5cm
- `-V fontsize=12pt`: Font size 12pt
- `-V documentclass=report`: Kiểu document báo cáo
- `-V lang=vi`: Ngôn ngữ tiếng Việt
- `--toc`: Tạo mục lục tự động
- `--toc-depth=3`: Độ sâu mục lục 3 cấp
- `--number-sections`: Đánh số các section

---

## 📝 CÁCH 4: Sử Dụng Microsoft Word

### Bước 1: Chuyển MD sang DOCX

**Sử dụng Pandoc:**
```bash
pandoc BAO_CAO_TIEU_LUAN.md -o BAO_CAO_TIEU_LUAN.docx
```

**Hoặc online:** https://cloudconvert.com/md-to-docx

### Bước 2: Chỉnh Sửa trong Word

1. Mở file DOCX trong Microsoft Word
2. Chỉnh sửa format, font, spacing
3. Thêm header/footer, số trang
4. Thêm logo trường, khoa (nếu cần)

### Bước 3: Export PDF

1. File → Save As
2. Chọn định dạng: **PDF**
3. Click **Save**

---

## 🎨 CÁCH 5: Sử Dụng LaTeX (Chuyên Nghiệp Nhất)

### Bước 1: Chuyển MD sang LaTeX

```bash
pandoc BAO_CAO_TIEU_LUAN.md -o BAO_CAO_TIEU_LUAN.tex
```

### Bước 2: Chỉnh Sửa LaTeX

Mở file `.tex` và thêm preamble:

```latex
\documentclass[12pt,a4paper]{report}
\usepackage[utf8]{vietnam}
\usepackage[margin=2.5cm]{geometry}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{listings}
\usepackage{xcolor}

\title{ỨNG DỤNG DỰ ĐOÁN VÀ CẢNH BÁO TAI NẠN GIAO THÔNG}
\author{[Họ và tên]}
\date{\today}

\begin{document}
\maketitle
\tableofcontents
\newpage

% Nội dung ở đây

\end{document}
```

### Bước 3: Compile

```bash
pdflatex BAO_CAO_TIEU_LUAN.tex
pdflatex BAO_CAO_TIEU_LUAN.tex  # Chạy 2 lần để tạo mục lục
```

---

## ✨ CÁCH 6: Sử Dụng Typora (Đơn Giản Nhất)

### Cài Đặt Typora

Tải từ: https://typora.io/

### Chuyển Đổi

1. Mở file `BAO_CAO_TIEU_LUAN.md` trong Typora
2. File → Export → PDF
3. Chọn vị trí lưu
4. Click **Save**

---

## 🎯 KHUYẾN NGHỊ

### Cho Sinh Viên

**Cách đơn giản nhất:**
1. **VSCode + Markdown PDF Extension** (Nhanh, dễ)
2. **Typora** (Đẹp, trực quan)
3. **Online tools** (Không cần cài đặt)

**Cách chuyên nghiệp:**
1. **Pandoc + LaTeX** (Đẹp nhất, chuẩn nhất)
2. **Word → PDF** (Dễ chỉnh sửa)

### Cho Báo Cáo Chính Thức

Nên sử dụng:
- **Pandoc với LaTeX engine**
- **Microsoft Word** (để thêm logo, chỉnh format)

---

## 📋 CHECKLIST SAU KHI CHUYỂN PDF

- [ ] Kiểm tra mục lục
- [ ] Kiểm tra số trang
- [ ] Kiểm tra font tiếng Việt
- [ ] Kiểm tra code blocks
- [ ] Kiểm tra tables
- [ ] Kiểm tra links
- [ ] Kiểm tra hình ảnh (nếu có)
- [ ] Kiểm tra header/footer
- [ ] Thêm thông tin sinh viên
- [ ] Thêm logo trường (nếu cần)

---

## 🔧 XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi: Font tiếng Việt bị lỗi

**Giải pháp:**
```bash
# Sử dụng XeLaTeX thay vì PDFLaTeX
pandoc BAO_CAO_TIEU_LUAN.md -o BAO_CAO_TIEU_LUAN.pdf --pdf-engine=xelatex
```

### Lỗi: Code blocks không đẹp

**Giải pháp:**
```bash
pandoc BAO_CAO_TIEU_LUAN.md -o BAO_CAO_TIEU_LUAN.pdf \
  --highlight-style=tango \
  --listings
```

### Lỗi: Tables bị vỡ

**Giải pháp:**
- Chuyển sang DOCX trước
- Chỉnh sửa tables trong Word
- Export PDF từ Word

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề, có thể:
1. Xem documentation của tool đang dùng
2. Tìm kiếm trên Stack Overflow
3. Hỏi trên các forum công nghệ

---

## 🎉 KẾT QUẢ

Sau khi hoàn thành, bạn sẽ có:
- ✅ File PDF chuyên nghiệp
- ✅ Mục lục tự động
- ✅ Đánh số trang
- ✅ Format đẹp, dễ đọc
- ✅ Sẵn sàng nộp báo cáo

**Chúc bạn thành công! 🚀**
