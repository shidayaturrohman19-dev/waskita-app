# 🛡️ Waskita - Sistem Klasifikasi Konten Radikal Media Sosial

Waskita adalah aplikasi web berbasis Flask yang menggunakan teknologi Machine Learning untuk mengklasifikasikan konten media sosial sebagai **Radikal** atau **Non-Radikal** dengan akurasi tinggi menggunakan algoritma Naive Bayes.

## ⚠️ PERINGATAN KEAMANAN

**JANGAN PERNAH** menggunakan kredensial default di production:
- Ganti semua password default sebelum deployment
- Generate SECRET_KEY yang unik untuk setiap environment  
- Gunakan environment variables untuk kredensial sensitif
- Jangan commit file .env ke repository

---

## 📋 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Teknologi yang Digunakan](#️-teknologi-yang-digunakan)
- [Quick Start](#-quick-start)
- [Dokumentasi Lengkap](#-dokumentasi-lengkap)
- [Deployment](#-deployment)
- [Kontribusi](#-kontribusi)
- [Lisensi](#-lisensi)

## 📚 Dokumentasi Lengkap

Untuk dokumentasi yang lebih detail, silakan kunjungi folder **[docs/](docs/)**:

### 📖 **Panduan Utama**
- **[docs/USER_GUIDE_LENGKAP.md](docs/USER_GUIDE_LENGKAP.md)** - Panduan lengkap penggunaan aplikasi
- **[docs/README.md](docs/README.md)** - Index navigasi semua dokumentasi

### 🔧 **Setup & Konfigurasi**
- **[docs/MODEL_SETUP_GUIDE.md](docs/MODEL_SETUP_GUIDE.md)** - Setup model Machine Learning
- **[SECURITY.md](SECURITY.md)** - Panduan keamanan production

### 🐳 **Docker & API**
- **[README_DOCKER.md](README_DOCKER.md)** - Panduan Docker lengkap
- **[docs/DOCKER_EXPORT_GUIDE.md](docs/DOCKER_EXPORT_GUIDE.md)** - Export dan transfer Docker
- **[docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)** - Dokumentasi API endpoints

### 🕷️ **Web Scraping**
- **[docs/APIFY_SETUP_GUIDE.md](docs/APIFY_SETUP_GUIDE.md)** - Setup Apify untuk scraping
- **[docs/APIFY_ACTOR_LIMITS.md](docs/APIFY_ACTOR_LIMITS.md)** - Limitasi dan quota

---

## ✨ Fitur Utama

### 🔐 Autentikasi & Manajemen Pengguna
- Sistem login/register dengan role-based access (Admin/User)
- Password hashing dengan Bcrypt untuk keamanan maksimal
- Session management yang aman dengan Flask-Login
- Dark/Light mode interface dengan Soft UI Dashboard

### 📊 Manajemen Data Komprehensif
- **Upload Dataset**: Import data dari file CSV/XLSX dengan validasi otomatis
- **Web Scraping**: Otomatis mengambil data dari 4 platform (Twitter, Facebook, Instagram, TikTok)
- **Data Cleaning**: Pembersihan otomatis emoji, link, karakter khusus
- **Real-time Statistics**: Dashboard dengan visualisasi data interaktif

### 🤖 Klasifikasi AI Canggih
- **3 Model Naive Bayes** independen untuk akurasi maksimal
- **Word2Vec Embedding** untuk representasi teks yang optimal
- **Majority Voting** untuk prediksi final yang akurat
- **Confidence Score** 0-100% untuk setiap prediksi
- **Batch Processing** untuk dataset besar dengan progress monitoring

### 👨‍💼 Panel Administrator
- Manajemen pengguna dan role assignment
- Monitoring aktivitas sistem real-time
- Audit trail lengkap semua aktivitas
- System health monitoring dan performance metrics

## 🛠️ Teknologi yang Digunakan

- **Backend**: Python Flask, SQLAlchemy, PostgreSQL
- **Frontend**: Soft UI Dashboard, Bootstrap 5, JavaScript ES6
- **Machine Learning**: Scikit-learn, Gensim Word2Vec, NumPy
- **Database**: PostgreSQL 15 dengan trigger otomatis
- **Caching**: Redis untuk performa optimal
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx sebagai reverse proxy

## 🚀 Quick Start

### Prasyarat
- **Python 3.11.x ONLY** (Wajib untuk kompatibilitas optimal dengan Gensim dan semua dependencies)
- **PostgreSQL 15+** 
- **Git** (untuk clone repository)

### 🔧 Setup Cepat

#### 1. Clone Repository
```bash
git clone https://github.com/kaptenusop/waskita.git
cd waskita
```

#### 2. Setup Python Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Setup Database PostgreSQL

**Opsi A: Setup Otomatis (Recommended)**
```bash
python setup_postgresql.py
```

**Opsi B: Setup Manual**
```sql
-- Buat database dan user
CREATE DATABASE waskita_dev;
CREATE DATABASE waskita_test;
CREATE USER waskita_user WITH PASSWORD 'waskita_password';
GRANT ALL PRIVILEGES ON DATABASE waskita_dev TO waskita_user;
GRANT ALL PRIVILEGES ON DATABASE waskita_test TO waskita_user;

-- Import schema
psql -U waskita_user -d waskita_dev -f database_schema.sql
```

#### 4. Konfigurasi Environment
```bash
# Copy dan edit file environment
cp .env.example .env.local
# Edit .env.local sesuai konfigurasi database Anda
```

#### 5. Jalankan Aplikasi
```bash
python app.py
```

Aplikasi akan berjalan di `http://localhost:5000`

### 🐳 Quick Start dengan Docker

#### Prerequisites
- Docker Desktop terinstall dan berjalan
- Git untuk clone repository
- PowerShell (Windows) atau Terminal (Linux/Mac)

#### 🔥 Fresh Build (Menghapus Semua Data)
**⚠️ PERINGATAN: Fresh build akan menghapus SEMUA data yang ada!**

Fresh build akan menghapus semua data dan membuat database baru dengan sample data.

```bash
# Menggunakan PowerShell script (Windows)
.\fresh-build.ps1

# Atau menggunakan Makefile (Linux/Mac/Windows dengan WSL)
make fresh-build

# Atau manual dengan Docker Compose
docker-compose down --volumes --remove-orphans
docker volume rm waskita_postgres_data -f
CREATE_SAMPLE_DATA=true docker-compose up --build -d
```

#### 🛠️ Normal Build (Data Persistent)
Normal build menggunakan database persistent tanpa menghapus data yang ada.

```bash
# Menggunakan Makefile
make build

# Atau manual dengan Docker Compose
docker-compose up --build -d
```

#### 📋 Makefile Commands
```bash
make help          # Tampilkan bantuan
make fresh-build   # Fresh build dengan menghapus semua data
make build         # Normal build dengan data persistent
make clean         # Hapus semua container dan volume
make status        # Tampilkan status container
make logs          # Tampilkan logs aplikasi
make restart       # Restart services
make stop          # Stop semua services
```

#### 🔐 Login Default
Setelah build berhasil, gunakan kredensial berikut:

**Admin User:**
- Username: `admin`
- Password: `admin123`
- Role: Administrator (akses penuh)

**Test User:**
- Username: `testuser`
- Password: `testuser123`
- Role: User biasa (akses terbatas)

#### 🌐 Akses Aplikasi
- **Web App**: http://localhost:5000
- **Nginx**: http://localhost:80

### Quick Start dengan Docker

#### Prasyarat
- Docker Desktop 4.0+
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space

### 🐍 Development dengan Virtual Environment

#### Prasyarat
- **Python 3.11.x ONLY** (Wajib untuk kompatibilitas optimal dengan Gensim dan semua dependencies)
- **PostgreSQL 15+** (Database utama)
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space

#### Setup Development Environment
```bash
# Clone repository
git clone https://github.com/kaptenusop/waskita.git
cd waskita

# Buat virtual environment dengan Python 3.11 ONLY
python3.11 -m venv venv_dev

# PASTIKAN menggunakan Python 3.11, bukan versi lain
python --version  # Harus menampilkan Python 3.11.x

# Aktivasi virtual environment
# Windows PowerShell:
.\venv_dev\Scripts\Activate.ps1
# Windows Command Prompt:
venv_dev\Scripts\activate.bat
# Linux/Mac:
source venv_dev/bin/activate

# Upgrade tools
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt

# 🗄️ SETUP DATABASE POSTGRESQL (WAJIB)
# Jalankan script setup otomatis untuk membuat database dan user admin
python setup_database.py

# ATAU setup manual PostgreSQL:
# 1. Install PostgreSQL 15+
# 2. Buat database: waskita_dev dan waskita_test
# 3. Buat user: waskita_user dengan password
# 4. Import schema: psql -U waskita_user -d waskita_dev -f database_schema.sql

# Setup environment variables (sudah otomatis jika pakai setup_database.py)
cp .env.example .env.local
# Edit .env.local sesuai kebutuhan development

# Jalankan aplikasi
python app.py
```

## 🗄️ Database Setup

### Setup PostgreSQL (Otomatis)

**Untuk instalasi baru**, gunakan script setup otomatis:

```bash
python setup_postgresql.py
```

Script ini akan:
- ✅ Membuat database PostgreSQL (`waskita_dev` dan `waskita_test`)
- ✅ Membuat user database (`waskita_user`)
- ✅ Menjalankan schema database
- ✅ Membuat user admin default
- ✅ Mengupdate file `.env.local`

**Login Admin Default:**
- **Username**: `admin`
- **Email**: `admin@waskita.com`
- **Password**: Lihat dokumentasi setup atau hubungi administrator

### Setup PostgreSQL (Manual)

Jika ingin setup manual:

1. **Install PostgreSQL**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib

   # Windows: Download dari https://www.postgresql.org/download/windows/
   # macOS: brew install postgresql
   ```

2. **Buat Database dan User**
   ```sql
   sudo -u postgres psql
   CREATE DATABASE waskita_dev;
   CREATE DATABASE waskita_test;
   CREATE USER waskita_user WITH PASSWORD 'your_secure_password_here';
   GRANT ALL PRIVILEGES ON DATABASE waskita_dev TO waskita_user;
   GRANT ALL PRIVILEGES ON DATABASE waskita_test TO waskita_user;
   \q
   ```

3. **Copy dan Edit .env.local**
   ```bash
   cp .env.example .env.local
   ```
   
   Edit `.env.local`:
   ```
   DATABASE_URL=postgresql://waskita_user:your_secure_password_here@localhost:5432/waskita_dev
   TEST_DATABASE_URL=postgresql://waskita_user:your_secure_password_here@localhost:5432/waskita_test
   SECRET_KEY=generate_your_own_secret_key_here
   ```

4. **Jalankan Schema Database**
   ```bash
   psql -h localhost -U waskita_user -d waskita_dev -f database_schema.sql
   ```

### 🐳 Production dengan Docker

### Instalasi

1. **Clone Repository**
```bash
git clone https://github.com/kaptenusop/waskita.git
cd waskita
```

2. **Setup Environment**
```bash
cp .env.example .env.docker
# Edit .env.docker sesuai kebutuhan
```

3. **Build dan Run Aplikasi**
```bash
docker-compose up -d --build
```

4. **Akses Aplikasi**
- Web App: `http://localhost:5000`
- Database: `localhost:5432`
- Redis: `localhost:6379`

### 🔧 Konfigurasi Environment

Edit file `.env.docker` untuk konfigurasi production:
```env
# Database Configuration
POSTGRES_DB=waskita_prod
POSTGRES_USER=waskita_user
POSTGRES_PASSWORD=your_secure_password_here

# Flask Configuration
SECRET_KEY=generate_your_own_secret_key_here
FLASK_ENV=production

# Model Paths (sudah dikonfigurasi)
WORD2VEC_MODEL_PATH=/app/models/embeddings/wiki_word2vec_csv_updated.model
NAIVE_BAYES_MODEL1_PATH=/app/models/navesbayes/naive_bayes_model1.pkl
NAIVE_BAYES_MODEL2_PATH=/app/models/navesbayes/naive_bayes_model2.pkl
NAIVE_BAYES_MODEL3_PATH=/app/models/navesbayes/naive_bayes_model3.pkl
```

## 📚 Dokumentasi

### 📖 Panduan Lengkap
- **[User Guide Lengkap](docs/USER_GUIDE_LENGKAP.md)** - Panduan komprehensif untuk pengguna
- **[API Documentation](docs/API_DOCUMENTATION.md)** - Dokumentasi API lengkap
- **[Security Guide](docs/SECURITY_GUIDE.md)** - Panduan keamanan aplikasi

### 🔧 Setup & Konfigurasi
- **[Apify Setup Guide](docs/APIFY_SETUP_GUIDE.md)** - Konfigurasi API Apify untuk scraping
- **[Docker Export Guide](docs/DOCKER_EXPORT_GUIDE.md)** - Panduan deployment Docker
- **[Apify Actor Limits](docs/APIFY_ACTOR_LIMITS.md)** - Batasan dan limitasi Apify
## 🛠️ Development

### Setup Development Environment
```bash
# Clone repository
git clone https://github.com/kaptenusop/waskita.git
cd waskita

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# atau
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup database
python setup_postgresql.py

# Copy environment file
cp .env.example .env.local

# Run application
python app.py
```

### Testing
```bash
# Run unit tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=app tests/
```

### Code Quality
```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## 🔒 Keamanan

- Password hashing dengan Bcrypt
- Session management yang aman
- CSRF protection
- SQL injection prevention
- XSS protection
- Rate limiting untuk API

## 📊 Performa & Spesifikasi

- **Akurasi Model**: 85-92% (tergantung jenis konten)
- **Processing Speed**: ~1000 data/menit
- **Memory Usage**: 2-4GB (tergantung dataset)
- **Response Time**: <200ms untuk klasifikasi tunggal
- **Database**: PostgreSQL 15+ dengan optimasi query
- **Concurrent Users**: Mendukung hingga 100 pengguna bersamaan

## 🤝 Contributing

1. Fork repository ini
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👥 Developer

- **Developer**: samshidayaturrohman@student.telkomuniversity.ac.id
- **Institution**: Telkom University

## 📞 Support

Jika Anda mengalami masalah atau memiliki pertanyaan:

1. Cek [dokumentasi lengkap](docs/)
2. Buka [GitHub Issues](https://github.com/your-username/waskita/issues)
3. Hubungi tim development

---

**Waskita** - Sistem Klasifikasi Konten Media Sosial dengan AI  
Made by Telkom University Students