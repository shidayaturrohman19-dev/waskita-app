# Waskita - Sistem Klasifikasi Konten Media Sosial

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)

Aplikasi web berbasis Flask yang menggunakan Machine Learning untuk mengklasifikasikan konten media sosial sebagai **Radikal** atau **Non-Radikal** menggunakan algoritma Naive Bayes. Proyek ini dikembangkan untuk tujuan penelitian dan pengembangan akademik.

---

## Daftar Isi

- [Fitur](#fitur)
- [Arsitektur Teknis](#arsitektur-teknis)
- [Instalasi](#instalasi)
- [Konfigurasi](#konfigurasi)
- [Setup Development](#setup-development)
- [Dokumentasi API](#dokumentasi-api)
- [Keamanan](#keamanan)
- [Testing](#testing)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)

---

## Fitur

### Machine Learning
- 3 Model Naive Bayes dengan Word2Vec embedding
- Akurasi 85-92% dalam klasifikasi konten
- Preprocessing otomatis dengan pembersihan teks Indonesia
- Batch processing untuk dataset besar

### Keamanan & Autentikasi
- Sistem OTP via email untuk registrasi
- Role-based access (Admin/User) dengan middleware keamanan
- Rate limiting (500/hari, 200/jam)
- CSRF protection dan session security
- Audit logging untuk semua aktivitas

### Manajemen Data
- Upload multi-format: CSV, XLSX, TXT
- Dataset management dengan soft delete
- Data validation dan preprocessing otomatis
- Export results dalam format CSV/Excel

### Dashboard & Analytics
- Real-time statistics dan visualisasi
- Classification history dengan filtering
- User management untuk admin
- System monitoring dan health checks

---

## 🎬 Demo & Screenshots

### Dashboard Utama
```
┌─────────────────────────────────────────────┐
│  📊 Dashboard Analytics (Contoh)            │
│  ├── Total Klasifikasi: [Dinamis]          │
│  ├── Akurasi Model: ~85-92%                │
│  ├── Pengguna Aktif: [Real-time]           │
│  └── Dataset Tersedia: [Berdasarkan Upload]│
└─────────────────────────────────────────────┘
```

> **📝 Catatan:** Data di atas adalah contoh tampilan dashboard. Nilai aktual akan berubah secara dinamis berdasarkan:
> - **Total Klasifikasi**: Jumlah teks yang telah diklasifikasi oleh sistem
> - **Akurasi Model**: Performa model berdasarkan testing dataset (rentang 85-92%)
> - **Pengguna Aktif**: Jumlah pengguna yang sedang online atau aktif dalam periode tertentu
> - **Dataset Tersedia**: Jumlah dataset yang telah diupload dan tersedia untuk klasifikasi

### Proses Klasifikasi
```
Input Text → Preprocessing → Model Prediction → Results
     ↓              ↓              ↓            ↓
"Teks media"  → Clean Text  → [0.85, 0.15] → "Non-Radikal"
```

---

## 🚀 Instalasi Cepat

### Metode 1: Pengembangan Lokal

```bash
# Clone repository
git clone https://github.com/kaptenusop/waskita.git
cd waskita

# Setup virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup database
python setup_postgresql.py

# Jalankan aplikasi
python app.py
```

### Metode 2: Docker Deployment

```bash
# Clone dan jalankan dengan Docker
git clone https://github.com/kaptenusop/waskita.git
cd waskita
docker-compose up -d --build
```

### Metode 3: Quick Setup Script

```bash
# Windows PowerShell
.\fresh-build.ps1

# Linux/Mac
chmod +x init_admin.sh && ./init_admin.sh
```

**Akses Aplikasi:**
- **Lokal**: http://localhost:5000
- **Docker**: http://localhost
- **Admin Panel**: /admin (admin/admin123)

---

## ⚙️ Konfigurasi

### Environment Variables

Buat file `.env` dengan konfigurasi berikut:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/waskita_db

# Security Keys
SECRET_KEY=your-super-secret-key-here
SECURITY_PASSWORD_SALT=your-unique-salt-here

# Email Configuration (Gmail SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Application Settings
FLASK_ENV=development
FLASK_DEBUG=True
```

### Database Setup

```bash
# PostgreSQL (Recommended)
createdb waskita_db
python setup_postgresql.py

# Atau gunakan SQLite untuk development
# DATABASE_URL=sqlite:///waskita.db
```

### Model Configuration

```bash
# Download required models
mkdir -p models
# Place your trained models:
# - word2vec_model.bin
# - naive_bayes_model.pkl
# - vectorizer.pkl
```

---

## 📖 Penggunaan

### 1. **Registrasi & Login**

```python
# Registrasi pengguna baru
POST /register
{
    "username": "user123",
    "email": "user@example.com",
    "password": "SecurePass123"
}

# Verifikasi OTP
POST /verify-otp
{
    "email": "user@example.com",
    "otp": "[6-digit-code]"
}
```

### 2. **Klasifikasi Teks**

#### Single Text Classification
```python
# Via Web Interface
1. Login ke aplikasi
2. Pilih "Klasifikasi" → "Single Text"
3. Input teks yang ingin diklasifikasi
4. Klik "Klasifikasi"
5. Lihat hasil dan confidence score
```

#### Batch Classification
```python
# Upload CSV/XLSX
1. Siapkan file dengan kolom "text"
2. Upload via "Klasifikasi" → "Batch Upload"
3. Tunggu proses selesai
4. Download hasil dalam format CSV/Excel
```

### 3. **Manajemen Dataset**

```python
# Upload dataset training
POST /dataset/upload
Content-Type: multipart/form-data
File: dataset.csv (columns: text, label)

# Preprocessing otomatis:
# - Pembersihan teks
# - Tokenisasi
# - Stopword removal
# - Normalisasi
```

### 4. **Admin Functions**

```python
# Approve registrasi pengguna
GET /admin/pending-registrations
POST /admin/approve-user/{user_id}

# Monitor sistem
GET /admin/system-stats
GET /admin/audit-logs
```

---

## 🏗️ Arsitektur Sistem

### Stack Teknologi

```
Frontend:  Bootstrap 5 + jQuery + Chart.js
Backend:   Flask + SQLAlchemy + PostgreSQL
ML:        Scikit-learn + Pandas + NumPy + NLTK
Security:  Flask-Login + OTP + CSRF Protection
Deploy:    Docker + Nginx + Gunicorn
```

### Struktur Database

```sql
-- Users & Authentication
users (id, username, email, password_hash, role, is_verified)
otp_codes (id, email, code, expires_at, is_used)

-- Classification Data
raw_data (id, text, label, user_id, created_at)
classification_results (id, text, prediction, confidence, user_id)

-- System Logs
audit_logs (id, user_id, action, details, timestamp)
```

### Model Architecture

```
Input Text → Preprocessing → Word2Vec → Naive Bayes → Output
     ↓             ↓            ↓           ↓         ↓
"Text input" → Clean Text → Vectors → Probability → Label
```

---

## 🔒 Keamanan

### Fitur Keamanan Terintegrasi

✅ **Autentikasi Multi-layer**
- Password hashing dengan bcrypt
- OTP verification via email
- Session management dengan Flask-Login
- Role-based access control

✅ **Proteksi Web**
- CSRF protection dengan Flask-WTF
- Rate limiting ([Konfigurasi]/hari, [Konfigurasi]/jam)
- Input validation dan sanitization
- XSS protection

✅ **Database Security**
- SQLAlchemy ORM (SQL injection protection)
- Parameterized queries
- Soft delete untuk data penting

✅ **File Upload Security**
- File type validation
- Size limitations
- Virus scanning (optional)
- Secure file storage

### Konfigurasi Keamanan Produksi

```bash
# Generate secure keys
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Environment variables
export FLASK_ENV=production
export FLASK_DEBUG=False
export SECRET_KEY="your-production-secret-key"

# HTTPS Configuration (Nginx)
ssl_certificate /path/to/cert.pem;
ssl_certificate_key /path/to/key.pem;
```

### Audit & Monitoring

```python
# Security audit report tersedia di:
docs/LAPORAN_AUDIT_KEAMANAN.md

# Monitoring endpoints:
GET /health          # System health check
GET /admin/logs      # Audit logs
GET /admin/stats     # Security statistics
```

---

## 📚 Dokumentasi Lengkap

### Panduan Spesifik

| Dokumen | Deskripsi | Target Audience |
|---------|-----------|-----------------|
| **[SETUP_GUIDE.md](docs/SETUP_GUIDE.md)** | Instalasi dan deployment lengkap | DevOps, Developer |
| **[USER_GUIDE_LENGKAP.md](docs/USER_GUIDE_LENGKAP.md)** | Panduan penggunaan semua fitur | End User, Admin |
| **[SECURITY_OTP_GUIDE.md](docs/SECURITY_OTP_GUIDE.md)** | Konfigurasi keamanan dan OTP | Admin, Developer |
| **[LAPORAN_AUDIT_KEAMANAN.md](docs/LAPORAN_AUDIT_KEAMANAN.md)** | Audit keamanan dan testing | Security Team |
| **[models/README.md](models/README.md)** | Konfigurasi model ML | Data Scientist |

### API Documentation

```python
# Classification API
POST /api/classify
{
    "text": "Teks yang ingin diklasifikasi",
    "return_confidence": true
}

Response:
{
    "prediction": "Non-Radikal",
    "confidence": "[0.0-1.0]",
    "processing_time": "[seconds]"
}
```

### Troubleshooting Umum

**Q: Model tidak ditemukan?**
```bash
# Download dan letakkan model di folder models/
# Pastikan file: word2vec_model.bin, naive_bayes_model.pkl
```

**Q: Database connection error?**
```bash
# Periksa DATABASE_URL di .env
# Pastikan PostgreSQL berjalan
python setup_postgresql.py
```

**Q: Email OTP tidak terkirim?**
```bash
# Periksa konfigurasi SMTP di .env
# Gunakan App Password untuk Gmail
# Pastikan "Less secure app access" diaktifkan
```

---

## 🤝 Kontribusi

Kami menyambut kontribusi dari komunitas! Berikut cara berkontribusi:

### Quick Start Contributing

```bash
# 1. Fork repository
git clone https://github.com/yourusername/waskita.git

# 2. Buat branch fitur
git checkout -b feature/fitur-baru

# 3. Commit perubahan
git commit -m "feat: tambah fitur baru"

# 4. Push dan buat PR
git push origin feature/fitur-baru
```

### Contribution Guidelines

- **Code Style**: Ikuti PEP 8 untuk Python
- **Testing**: Tambahkan unit tests untuk fitur baru
- **Documentation**: Update dokumentasi jika diperlukan
- **Security**: Laporkan vulnerability via email pribadi

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run security tests
python run_security_tests.py

# Code formatting
black . && flake8 .
```

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah **MIT License** - lihat file [LICENSE](LICENSE) untuk detail lengkap.

```
MIT License - Copyright (c) 2024 Waskita Team
Permission is hereby granted, free of charge, to any person obtaining a copy...
```

---

## 🆘 Dukungan & Kontak

### Tim Support

- **📧 Email**: support@waskita.com
- **🐛 Bug Reports**: [GitHub Issues](https://github.com/kaptenusop/waskita/issues)
- **💬 Diskusi**: [GitHub Discussions](https://github.com/kaptenusop/waskita/discussions)
- **📖 Wiki**: [Project Wiki](https://github.com/kaptenusop/waskita/wiki)

### Response Time

- **Critical Issues**: < [X] jam
- **Bug Reports**: [X] hari kerja
- **Feature Requests**: [X] minggu
- **General Questions**: [X] hari kerja

---

## 🏆 Acknowledgments

- **Scikit-learn** untuk framework machine learning
- **Flask** untuk web framework yang powerful
- **Bootstrap** untuk UI components yang responsive
- **PostgreSQL** untuk database yang reliable
- **Docker** untuk containerization yang mudah

---

## Disclaimer

Aplikasi ini dikembangkan untuk tujuan penelitian dan edukasi.

- Pastikan kepatuhan terhadap regulasi yang berlaku
- Lakukan testing menyeluruh sebelum deployment produksi
- Gunakan dengan bijak dan bertanggung jawab
- Tim pengembang tidak bertanggung jawab atas penyalahgunaan

---

## Kontribusi

Kontribusi untuk pengembangan proyek ini sangat diterima. Silakan:

1. Fork repository ini
2. Buat branch untuk fitur baru (`git checkout -b feature/nama-fitur`)
3. Commit perubahan (`git commit -m 'Menambahkan fitur baru'`)
4. Push ke branch (`git push origin feature/nama-fitur`)
5. Buat Pull Request

---

## Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail lengkap.

---

*Dikembangkan untuk keperluan penelitian dan pengembangan akademik*