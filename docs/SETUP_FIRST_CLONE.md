# 🚀 Setup Guide - First Clone dari GitHub

Panduan lengkap untuk setup pertama kali setelah clone repository Waskita dari GitHub.

## 📋 Prerequisites

- Python 3.8+ 
- PostgreSQL 12+
- Git
- Docker & Docker Compose (untuk deployment)

## 🔧 Setup Local Development

### 1. Clone Repository
```bash
git clone https://github.com/your-username/waskita.git
cd waskita
```

### 2. Setup Environment Variables
```bash
# Copy template environment file
cp .env.example .env

# Edit file .env dengan konfigurasi Anda
# PENTING: Ganti nilai berikut:
# - SECRET_KEY (generate random string)
# - DATABASE_URL (sesuai PostgreSQL lokal Anda)
# - MAIL_USERNAME & MAIL_PASSWORD (untuk OTP email)
# - ADMIN_EMAIL (email admin pertama)
```

### 3. Setup Database PostgreSQL

#### Opsi A: Manual Setup
```bash
# Buat database
createdb waskita_db

# Import schema
psql -d waskita_db -f database_schema.sql
```

#### Opsi B: Menggunakan Script
```bash
python setup_postgresql.py
```

### 4. Setup Python Environment
```bash
# Buat virtual environment
python -m venv venv

# Aktivasi virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Setup Model Files
```bash
# Buat direktori models (sudah dibuat otomatis)
# Letakkan file model ML di:
# - models/embeddings/wiki_word2vec_csv_updated.model
# - models/navesbayes/naive_bayes_model1.pkl
# - models/navesbayes/naive_bayes_model2.pkl  
# - models/navesbayes/naive_bayes_model3.pkl

# CATATAN: File model tidak ada di repository
# Anda perlu melatih model atau mendapatkan dari tim
```

### 6. Database Migration
```bash
# Inisialisasi migrasi (jika belum ada)
flask db init

# Buat migrasi
flask db migrate -m "Initial migration"

# Apply migrasi
flask db upgrade
```

### 7. Buat Admin User
```bash
python create_admin.py
```

### 8. Jalankan Aplikasi
```bash
python app.py
```

Aplikasi akan berjalan di: http://localhost:5000

## 🐳 Setup Docker Development

### 1. Setup Environment Docker
```bash
# File .env.docker sudah dikonfigurasi
# Edit jika perlu sesuai kebutuhan Anda
```

### 2. Build dan Jalankan
```bash
# Build dan jalankan semua services
docker-compose up --build

# Atau jalankan di background
docker-compose up -d --build
```

### 3. Akses Aplikasi
- **Web App**: http://localhost:5000
- **Database**: localhost:5432
- **Redis**: localhost:6379
- **Nginx**: http://localhost:80

## ⚠️ Troubleshooting

### Database Connection Error
```bash
# Periksa PostgreSQL berjalan
sudo systemctl status postgresql  # Linux
# atau
brew services list | grep postgresql  # Mac

# Periksa konfigurasi DATABASE_URL di .env
```

### Model File Not Found
```bash
# Periksa file model ada di direktori yang benar
ls -la models/embeddings/
ls -la models/navesbayes/

# Periksa path di config.py atau .env
```

### Docker Build Error
```bash
# Clean build
docker-compose down
docker system prune -f
docker-compose up --build --force-recreate
```

### Permission Error (Linux/Mac)
```bash
# Fix permission untuk direktori uploads
chmod -R 755 uploads/
chmod -R 755 static/uploads/
```

## 🔐 Konfigurasi Keamanan

### 1. Generate SECRET_KEY Baru
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 2. Setup Email untuk OTP
- Gunakan Gmail App Password
- Aktifkan 2FA di Gmail
- Generate App Password khusus untuk aplikasi

### 3. Database Security
- Ganti default password PostgreSQL
- Gunakan user khusus untuk aplikasi
- Batasi akses network jika perlu

## 📚 Next Steps

1. **Baca Dokumentasi**: Lihat folder `docs/` untuk panduan lengkap
2. **Setup Model**: Latih atau dapatkan file model ML
3. **Konfigurasi Email**: Setup SMTP untuk fitur OTP
4. **Testing**: Jalankan `python run_security_tests.py`
5. **Production**: Lihat `docs/DEPLOYMENT_GUIDE.md`

## 🆘 Bantuan

Jika mengalami masalah:
1. Periksa log error di terminal
2. Baca file dokumentasi di folder `docs/`
3. Periksa issue di GitHub repository
4. Hubungi tim pengembang

---

**Selamat coding! 🎉**