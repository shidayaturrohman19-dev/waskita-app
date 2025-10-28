# 🔄 Workflow: Local Development ke Docker Deployment

Panduan lengkap untuk mengembangkan aplikasi Waskita secara lokal dan kemudian deploy ke Docker.

## 📋 Overview Workflow

```
1. Clone Repository → 2. Local Development → 3. Testing → 4. Docker Deployment
```

---

## 🚀 Phase 1: Setup Awal (Clone Repository)

### 1.1 Clone dan Setup Environment
```bash
# Clone repository
git clone https://github.com/kaptenusop/waskita.git
cd waskita

# Setup Python virtual environment
python -m venv venv

# Aktivasi virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 1.2 Verifikasi Prasyarat
- ✅ Python 3.11.x (WAJIB untuk kompatibilitas optimal)
- ✅ PostgreSQL 15+ terinstall dan berjalan
- ✅ Git untuk version control
- ✅ Docker Desktop (untuk phase deployment)

---

## 🛠️ Phase 2: Local Development

### 2.1 Setup Database PostgreSQL Lokal
```bash
# Opsi A: Setup Otomatis (Recommended)
python setup_postgresql.py
```

Script ini akan:
- ✅ Membuat database `waskita_dev` dan `waskita_test`
- ✅ Membuat user `waskita_user` dengan password
- ✅ Import schema dari `database_schema.sql`
- ✅ Membuat admin user default
- ✅ Update file `.env.local` dengan konfigurasi database

### 2.2 Konfigurasi Environment Lokal
File `.env.local` akan otomatis dikonfigurasi oleh setup script dengan:

```bash
# Database Configuration
DATABASE_URL=postgresql://waskita_user:waskita_password@localhost:5432/waskita_dev
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Flask Configuration
SECRET_KEY=waskita_secret_key
FLASK_ENV=production
FLASK_DEBUG=True

# Admin Configuration
ADMIN_EMAIL=admin@waskita.com

# Model Paths (lokal)
WORD2VEC_MODEL_PATH=models/embeddings/wiki_word2vec_csv_updated.model
NAIVE_BAYES_MODEL1_PATH=models/navesbayes/naive_bayes_model1.pkl
# ... dst
```

### 2.3 Jalankan Aplikasi Lokal
```bash
python app.py
```

Aplikasi akan berjalan di: `http://localhost:5000`

**Kredensial Default:**
- Admin: `admin` / `admin123`
- User: `testuser` / `testuser123`

### 2.4 Development Workflow
```bash
# 1. Buat branch untuk fitur baru
git checkout -b feature/nama-fitur

# 2. Develop dan test secara lokal
python app.py

# 3. Test perubahan
# - Manual testing di browser
# - Unit testing jika ada

# 4. Commit perubahan
git add .
git commit -m "feat: deskripsi fitur"

# 5. Push ke repository
git push origin feature/nama-fitur
```

---

## 🧪 Phase 3: Testing & Validation

### 3.1 Testing Lokal
```bash
# Test aplikasi berjalan normal
curl http://localhost:5000

# Test database connection
python -c "from models import db; print('Database OK' if db.engine.execute('SELECT 1').scalar() == 1 else 'Database Error')"

# Test model loading (jika ada models)
python -c "from utils import load_models; load_models(); print('Models loaded successfully')"
```

### 3.2 Validasi Konfigurasi
- ✅ Database connection berfungsi
- ✅ File upload berfungsi
- ✅ Authentication system berfungsi
- ✅ Model ML dapat dimuat (jika ada)
- ✅ Email service berfungsi (jika dikonfigurasi)

---

## 🐳 Phase 4: Docker Deployment

### 4.1 Persiapan Docker Environment

**Pastikan Docker Desktop berjalan:**
```bash
docker --version
docker-compose --version
```

### 4.2 Konfigurasi Docker Environment
File `.env.docker` sudah dikonfigurasi untuk Docker deployment:

```bash
# Database Configuration (Docker)
DATABASE_URL=postgresql://waskita_user:waskita_password@db:5432/waskita_dev
DATABASE_HOST=db
DATABASE_PORT=5432

# Model Paths (Docker - absolute paths)
WORD2VEC_MODEL_PATH=/app/models/embeddings/wiki_word2vec_csv_updated.model
NAIVE_BAYES_MODEL1_PATH=/app/models/navesbayes/naive_bayes_model1.pkl
# ... dst
```

### 4.3 Docker Deployment Options

#### Option A: Fresh Build (Menghapus Semua Data)
```bash
# Windows PowerShell
.\fresh-build.ps1

# Linux/Mac/WSL
make fresh-build

# Manual
docker-compose down --volumes --remove-orphans
docker volume rm waskita_postgres_data -f
CREATE_SAMPLE_DATA=true docker-compose up --build -d
```

#### Option B: Normal Build (Data Persistent)
```bash
# Menggunakan Makefile
make build

# Manual
docker-compose up --build -d
```

### 4.4 Verifikasi Docker Deployment
```bash
# Check container status
docker-compose ps

# Check logs
docker-compose logs -f web

# Test aplikasi
curl http://localhost:5000

# Check database
docker-compose exec db psql -U waskita_user -d waskita_dev -c "SELECT COUNT(*) FROM users;"
```

### 4.5 Docker Management Commands
```bash
make help          # Tampilkan bantuan
make status        # Status container
make logs          # Lihat logs aplikasi
make restart       # Restart services
make stop          # Stop semua services
make clean         # Hapus container dan volume
```

---

## 🔄 Workflow Lengkap: Local → Docker

### Skenario 1: Development Baru
```bash
# 1. Setup lokal
git clone https://github.com/kaptenusop/waskita.git
cd waskita
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
python setup_postgresql.py

# 2. Develop
python app.py
# ... develop fitur ...

# 3. Test lokal
# ... testing ...

# 4. Deploy ke Docker
make fresh-build
```

### Skenario 2: Update Existing
```bash
# 1. Pull latest changes
git pull origin main

# 2. Update dependencies (jika ada)
pip install -r requirements.txt

# 3. Test lokal
python app.py

# 4. Deploy ke Docker (dengan data persistent)
make build
```

### Skenario 3: Production Deployment
```bash
# 1. Pastikan semua test passed
python app.py  # Test lokal

# 2. Update production environment variables
# Edit .env.docker untuk production settings

# 3. Deploy dengan data persistent
make build

# 4. Monitor deployment
make logs
make status
```

---

## ⚠️ Penting: Perbedaan Environment

### Local Development (.env.local)
- Database: `localhost:5432`
- Model paths: Relative paths
- Debug: `FLASK_DEBUG=True`
- Development-friendly settings

### Docker Deployment (.env.docker)
- Database: `db:5432` (Docker service name)
- Model paths: Absolute paths dalam container
- Production-ready settings
- Container networking

### File Environment yang Digunakan
- **Local**: `.env.local` (otomatis dibuat oleh `setup_postgresql.py`)
- **Docker**: `.env.docker` (sudah dikonfigurasi)
- **Example**: `.env.example` (template)

---

## 🎯 Best Practices

### Development
1. **Selalu gunakan virtual environment** untuk isolasi dependencies
2. **Test lokal dulu** sebelum deploy ke Docker
3. **Commit frequently** dengan pesan yang jelas
4. **Backup database** sebelum perubahan besar

### Docker Deployment
1. **Gunakan `make build`** untuk deployment normal (data persistent)
2. **Gunakan `make fresh-build`** hanya untuk reset complete
3. **Monitor logs** setelah deployment: `make logs`
4. **Backup volume** sebelum `fresh-build`

### Security
1. **Ganti semua password default** sebelum production
2. **Gunakan environment variables** untuk kredensial
3. **Jangan commit file .env** ke repository
4. **Enable HTTPS** untuk production

---

## 🆘 Troubleshooting

### Local Development Issues
```bash
# Database connection error
python setup_postgresql.py  # Re-run setup

# Model loading error
# Pastikan file model ada di folder models/

# Port already in use
# Ganti port di app.py atau kill process yang menggunakan port 5000
```

### Docker Issues
```bash
# Container tidak start
docker-compose logs web

# Database connection error
docker-compose exec db psql -U waskita_user -d waskita_dev

# Port conflict
# Edit docker-compose.yml untuk ganti port mapping

# Volume permission error (Linux)
sudo chown -R $USER:$USER uploads/ logs/
```

### Performance Issues
```bash
# Check resource usage
docker stats

# Check database performance
docker-compose exec db psql -U waskita_user -d waskita_dev -c "SELECT * FROM pg_stat_activity;"

# Clear cache
make clean && make build
```

---

## 📚 Resources

- **[README.md](README.md)** - Dokumentasi utama
- **[README_DOCKER.md](README_DOCKER.md)** - Panduan Docker lengkap
- **[docs/](docs/)** - Dokumentasi detail
- **[SECURITY.md](SECURITY.md)** - Panduan keamanan

---

**🎉 Selamat! Anda sekarang memiliki workflow lengkap dari local development hingga Docker deployment.**