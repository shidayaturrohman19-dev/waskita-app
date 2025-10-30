# Waskita - Sistem Klasifikasi Konten Media Sosial Berbasis Machine Learning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)

**Waskita** merupakan sistem penelitian berbasis web yang mengimplementasikan pendekatan *Machine Learning* untuk klasifikasi otomatis konten media sosial. Sistem ini menggunakan algoritma *Naive Bayes* dengan *Word2Vec embedding* untuk mengidentifikasi dan mengkategorikan konten sebagai **Radikal** atau **Non-Radikal**. 

Penelitian ini dikembangkan sebagai kontribusi akademik dalam bidang *Natural Language Processing* (NLP) dan analisis sentimen untuk deteksi konten ekstremis di platform media sosial Indonesia.

---

## 🚀 Quick Start

### 🐳 Docker (Rekomendasi - Setup 1 Langkah)
```bash
# 1. Clone repository
git clone https://github.com/shidayaturrohman19-dev/waskita-app.git
cd waskita-app

# 2. Setup environment
cp .env.example .env

# 3. Jalankan semua services (database, app, nginx)
docker-compose up -d

# ✅ SELESAI! Aplikasi siap digunakan
# http://localhost:5000 (aplikasi)
# http://localhost:80 (nginx proxy)
```

**🎯 Keunggulan Docker Setup:**
- ✅ Database PostgreSQL otomatis terkonfigurasi
- ✅ Admin user otomatis dibuat
- ✅ Sample data otomatis dimuat
- ✅ Semua dependencies terinstall
- ✅ Nginx reverse proxy aktif
- ✅ Setup selesai dalam 5 menit

### Development Lokal (Manual Setup)
```bash
# 1. Clone repository
git clone https://github.com/shidayaturrohman19-dev/waskita-app.git
cd waskita-app

# 2. Copy dan setup environment
cp .env.example .env
# Edit .env sesuai kebutuhan (database, email, dll)

# 3. Setup virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 4. Install dependencies
pip install -r requirements.txt

# 5. Setup database
python setup_postgresql.py

# 6. Jalankan aplikasi
python app.py
```

**🎯 Setelah setup, login dengan:**
- **Admin**: admin@waskita.com / admin123
- **User**: user@test.com / user123

---

## 📚 Dokumentasi Lengkap

### 📖 Panduan Utama
- **[🚀 Setup Apps Guide](docs/SETUP_APPS.md)** - Panduan setup lokal dan Docker, user guide, dan deployment terpusat
- **[🔒 Security Guide](docs/SECURITY_GUIDE.md)** - Panduan keamanan, audit report, dan API documentation

---

## Daftar Isi

- [🚀 Quick Start](#-quick-start)
- [📚 Dokumentasi Lengkap](#-dokumentasi-lengkap)
- [Fitur](#fitur)
- [🎬 Demo & Screenshots](#-demo--screenshots)
- [⚙️ Konfigurasi](#️-konfigurasi)
- [📖 Penggunaan](#-penggunaan)
- [🏗️ Arsitektur Sistem](#️-arsitektur-sistem)
- [🔒 Keamanan](#-keamanan)
- [🤝 Kontribusi](#-kontribusi)
- [📄 Lisensi](#-lisensi)
- [🆘 Dukungan & Kontak](#-dukungan--kontak)
- [🏆 Acknowledgments](#-acknowledgments)
- [Disclaimer](#disclaimer)

---

## Fitur Penelitian

### Metodologi Machine Learning
- Implementasi 3 model *Naive Bayes* dengan *Word2Vec embedding* untuk representasi semantik
- Tingkat akurasi klasifikasi mencapai 85-92% berdasarkan evaluasi dataset uji
- Sistem *preprocessing* otomatis dengan teknik pembersihan teks bahasa Indonesia
- Kemampuan *batch processing* untuk analisis dataset skala besar

### Sistem Keamanan & Autentikasi
- Implementasi sistem *One-Time Password* (OTP) melalui email untuk verifikasi registrasi
- Arsitektur *role-based access control* (Admin/User) dengan *middleware* keamanan berlapis
- Mekanisme *rate limiting* (500 request/hari, 200 request/jam) untuk mencegah penyalahgunaan
- Perlindungan *Cross-Site Request Forgery* (CSRF) dan keamanan sesi
- Sistem *audit logging* komprehensif untuk pelacakan aktivitas penelitian

### Manajemen Data Penelitian
- Dukungan multi-format input: CSV, XLSX, TXT untuk fleksibilitas dataset
- Sistem manajemen dataset dengan *soft delete* untuk integritas data
- Validasi data otomatis dan *preprocessing* pipeline terintegrasi
- Ekspor hasil analisis dalam format CSV/Excel untuk analisis lanjutan

### Dashboard Analitik & Visualisasi
- Statistik *real-time* dan visualisasi hasil klasifikasi
- Riwayat klasifikasi dengan sistem *filtering* dan pencarian
- Panel manajemen pengguna untuk administrator penelitian
- *System monitoring* dan *health checks* untuk stabilitas sistem

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
.\install-build.ps1

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

## 🏗️ Arsitektur Sistem Penelitian

### Stack Teknologi Penelitian

```
Frontend:  Bootstrap 5 + jQuery + Chart.js (Antarmuka Penelitian)
Backend:   Flask + SQLAlchemy + PostgreSQL (Infrastruktur Data)
ML:        Scikit-learn + Pandas + NumPy + NLTK (Pipeline Analisis)
Security:  Flask-Login + OTP + CSRF Protection (Keamanan Penelitian)
Deploy:    Docker + Nginx + Gunicorn (Deployment Terdistribusi)
```

### Skema Database Penelitian

```sql
-- Manajemen Pengguna & Autentikasi
users (id, username, email, password_hash, role, is_verified)
otp_codes (id, email, code, expires_at, is_used)

-- Data Penelitian & Klasifikasi
raw_data (id, text, label, user_id, created_at)
classification_results (id, text, prediction, confidence, user_id)

-- Audit Trail Penelitian
audit_logs (id, user_id, action, details, timestamp)
```

### Arsitektur Model Machine Learning

```
Input Text → Preprocessing → Word2Vec Embedding → Naive Bayes Classifier → Output
     ↓             ↓              ↓                    ↓                ↓
"Teks Input" → Normalisasi → Vektor Semantik → Probabilitas Kelas → Label Prediksi
```

**Metodologi Klasifikasi:**
1. **Tahap Preprocessing**: Tokenisasi, normalisasi, dan pembersihan teks bahasa Indonesia
2. **Feature Extraction**: Transformasi teks ke representasi vektor menggunakan Word2Vec
3. **Classification**: Implementasi algoritma Naive Bayes untuk prediksi kategori
4. **Evaluation**: Validasi model menggunakan metrik akurasi, precision, dan recall

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

## Disclaimer Penelitian

Sistem **Waskita** dikembangkan sebagai instrumen penelitian akademik dalam bidang *Natural Language Processing* dan analisis konten media sosial.

**Ketentuan Penggunaan Penelitian:**
- Sistem ini dirancang khusus untuk keperluan penelitian dan pengembangan akademik
- Implementasi dalam lingkungan produksi memerlukan evaluasi dan validasi tambahan
- Pengguna bertanggung jawab untuk memastikan kepatuhan terhadap regulasi dan etika penelitian yang berlaku
- Hasil klasifikasi harus diinterpretasikan dalam konteks penelitian dan bukan sebagai keputusan final
- Tim peneliti tidak bertanggung jawab atas implementasi atau interpretasi hasil di luar konteks akademik

**Rekomendasi Penelitian:**
- Lakukan validasi silang (*cross-validation*) dengan dataset independen
- Pertimbangkan bias dan limitasi model dalam interpretasi hasil
- Dokumentasikan metodologi dan parameter yang digunakan untuk reproduktibilitas
- Patuhi prinsip etika penelitian dalam penggunaan data dan publikasi hasil

---

## Kontribusi Penelitian

Kontribusi untuk pengembangan penelitian ini sangat diterima dari komunitas akademik. Silakan:

1. Fork repository penelitian ini
2. Buat branch untuk pengembangan fitur (`git checkout -b research/nama-fitur`)
3. Commit perubahan dengan dokumentasi yang jelas (`git commit -m 'Menambahkan metodologi baru'`)
4. Push ke branch (`git push origin research/nama-fitur`)
5. Buat Pull Request dengan penjelasan kontribusi penelitian

**Panduan Kontribusi Akademik:**
- Sertakan dokumentasi metodologi yang digunakan
- Tambahkan referensi literatur yang relevan
- Lakukan pengujian statistik untuk validasi hasil
- Patuhi standar penulisan kode dan dokumentasi penelitian

---

## Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail lengkap.

---

*Dikembangkan sebagai kontribusi penelitian akademik dalam bidang Natural Language Processing dan Machine Learning untuk analisis konten media sosial Indonesia*