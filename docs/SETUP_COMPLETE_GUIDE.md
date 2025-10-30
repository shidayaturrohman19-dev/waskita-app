# 📋 PANDUAN SETUP LENGKAP WASKITA

Panduan lengkap untuk setup aplikasi Waskita dari awal hingga siap digunakan.

## 🚀 Quick Start

### Metode 1: Development Lokal
```bash
# 1. Clone repository
git clone <repository-url>
cd waskita

# 2. Setup environment
cp .env.example .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database
python setup_postgresql.py

# 5. Create admin user
python create_admin.py

# 6. Run application
python app.py
```

### Metode 2: Docker
```bash
# 1. Clone repository
git clone <repository-url>
cd waskita

# 2. Setup environment
cp .env.example .env

# 3. Run with Docker
docker-compose up --build
```

### 🔑 Kredensial Login Default (Development)
- **Email**: admin@waskita.com
- **Password**: admin123

⚠️ **PENTING**: Ganti kredensial ini di production!

## 📋 Prasyarat

### Untuk Development Lokal:
- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### Untuk Docker:
- Docker
- Docker Compose

## 🔧 Panduan Development Lengkap

### 1. Clone Repository
```bash
git clone <repository-url>
cd waskita
```

### 2. Setup Virtual Environment (Opsional tapi Direkomendasikan)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Setup Environment Variables
```bash
# Copy template environment
cp .env.example .env

# Edit .env sesuai kebutuhan (opsional untuk development)
# File .env.example sudah berisi nilai siap pakai untuk development
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup Database
```bash
# Jalankan script setup database
python setup_postgresql.py

# Script ini akan:
# - Membuat database PostgreSQL
# - Menjalankan migrasi
# - Setup tabel yang diperlukan
```

### 6. Create Admin User
```bash
# Buat user admin
python create_admin.py

# Atau gunakan kredensial default:
# Email: admin@waskita.com
# Password: admin123
```

### 7. Download Model Files (Jika Diperlukan)
```bash
# Buat folder models jika belum ada
mkdir models

# Download model files ke folder models/
# - word2vec_model.bin
# - naive_bayes_model1.pkl
# - naive_bayes_model2.pkl  
# - naive_bayes_model3.pkl
```

### 8. Run Application
```bash
# Development mode
python app.py

# Atau dengan Flask CLI
flask run

# Aplikasi akan berjalan di http://localhost:5000
```

## 🐳 Docker Deployment

### 1. Setup Environment
```bash
cp .env.example .env
```

### 2. Build dan Run
```bash
# Build dan jalankan semua services
docker-compose up --build

# Atau run di background
docker-compose up -d --build
```

### 3. Akses Aplikasi
- **Web App**: http://localhost:5000
- **Database**: localhost:5432
- **Redis**: localhost:6379

## 🔧 Perintah Docker Berguna

```bash
# Stop semua services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f

# Rebuild specific service
docker-compose up --build web

# Access container shell
docker-compose exec web bash
docker-compose exec db psql -U waskita_user -d waskita_db
```

## ⚙️ Konfigurasi Lanjutan

### Environment Variables Penting

#### Database Configuration
```env
DATABASE_URL=postgresql://waskita_user:waskita_password123@localhost:5432/waskita_db
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=waskita_db
DATABASE_USER=waskita_user
DATABASE_PASSWORD=waskita_password123
```

#### Flask Configuration
```env
SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True
```

#### Email Configuration (Untuk OTP)
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Model Paths
```env
WORD2VEC_MODEL_PATH=models/word2vec_model.bin
NAIVE_BAYES_MODEL1_PATH=models/naive_bayes_model1.pkl
NAIVE_BAYES_MODEL2_PATH=models/naive_bayes_model2.pkl
NAIVE_BAYES_MODEL3_PATH=models/naive_bayes_model3.pkl
```

## 🔍 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Restart PostgreSQL
sudo systemctl restart postgresql

# Check database exists
psql -U waskita_user -d waskita_db -c "\l"
```

### Port Already in Use
```bash
# Find process using port 5000
netstat -tulpn | grep :5000

# Kill process
kill -9 <PID>
```

### Docker Issues
```bash
# Clean up Docker
docker-compose down -v
docker system prune -a

# Rebuild from scratch
docker-compose up --build --force-recreate
```

### Model Files Missing
1. Pastikan folder `models/` ada
2. Download model files yang diperlukan
3. Periksa path di `.env` file
4. Restart aplikasi

## 📝 Langkah Selanjutnya

Setelah setup berhasil:

1. **Login ke aplikasi** dengan kredensial admin
2. **Konfigurasi email** untuk sistem OTP
3. **Upload model files** jika diperlukan
4. **Test fitur klasifikasi** dengan data sample
5. **Baca dokumentasi API** untuk integrasi
6. **Setup monitoring** untuk production

## 📚 Dokumentasi Terkait

- [Panduan Keamanan](SECURITY_GUIDE.md) - Keamanan dan OTP
- [Panduan Pengguna](USER_GUIDE_LENGKAP.md) - Cara menggunakan aplikasi
- [Dokumentasi API](API_DOCUMENTATION.md) - API endpoints
- [Panduan Deployment](DEPLOYMENT_GUIDE.md) - Production deployment

## 🆘 Bantuan

Jika mengalami masalah:

1. Periksa log aplikasi: `tail -f logs/app.log`
2. Periksa log Docker: `docker-compose logs -f`
3. Periksa konfigurasi `.env`
4. Restart aplikasi/services
5. Buka issue di repository GitHub

---

**Catatan**: Panduan ini untuk development environment. Untuk production, pastikan mengganti semua kredensial default dan mengikuti panduan keamanan.