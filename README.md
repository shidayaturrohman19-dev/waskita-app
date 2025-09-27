# 🛡️ Waskita - Sistem Klasifikasi Konten Radikal Media Sosial

Waskita adalah aplikasi web berbasis Flask yang menggunakan teknologi Machine Learning untuk mengklasifikasikan konten media sosial sebagai **Radikal** atau **Non-Radikal** dengan akurasi tinggi menggunakan algoritma Naive Bayes.

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

## 🚀 Quick Start dengan Docker

### Prasyarat
- Docker Desktop 4.0+
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space

### Instalasi

1. **Clone Repository**
```bash
git clone <repository-url>
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
POSTGRES_PASSWORD=your-secure-password

# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=production

# Model Paths (sudah dikonfigurasi)
WORD2VEC_MODEL_PATH=/app/models/embeddings/wiki_word2vec_csv_updated.model
NAIVE_BAYES_MODEL1_PATH=/app/models/navesbayes/naive_bayes_model1.pkl
NAIVE_BAYES_MODEL2_PATH=/app/models/navesbayes/naive_bayes_model2.pkl
NAIVE_BAYES_MODEL3_PATH=/app/models/navesbayes/naive_bayes_model3.pkl
```

## 📖 Dokumentasi Lengkap

- **[User Guide Lengkap](USER_GUIDE_LENGKAP.md)** - Panduan penggunaan komprehensif
- **[Security Guide](SECURITY_GUIDE.md)** - Panduan keamanan dan best practices
- **[Database Schema](database_schema.sql)** - Struktur database dan relasi

## 🔒 Keamanan

- Password hashing dengan Bcrypt
- Session management yang aman
- CSRF protection
- SQL injection prevention
- XSS protection
- Rate limiting untuk API

## 📊 Performa

- **Akurasi Model**: 85-92% (tergantung jenis konten)
- **Processing Speed**: ~1000 data/menit
- **Memory Usage**: 2-4GB (tergantung dataset)
- **Response Time**: <200ms untuk klasifikasi tunggal

## Konfigurasi

Sesuaikan file `.env` dengan konfigurasi Anda:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/waskita_db

# Flask
FLASK_SECRET_KEY=your-secret-key
FLASK_DEBUG=False

# File Upload
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# Model Paths
WORD2VEC_MODEL_PATH=../embeddings/wiki_word2vec_csv_updated.model
NAIVE_BAYES_MODEL_PATH=../navesbayes/

# API Keys (untuk scraping)
APIFY_API_TOKEN=your-apify-token
```

## Struktur Database

Aplikasi menggunakan PostgreSQL dengan tabel utama:
- `users` - Data pengguna dan role
- `datasets` - Metadata dataset
- `raw_data` - Data mentah dari upload
- `raw_data_scraper` - Data mentah dari scraping
- `clean_data_upload` - Data bersih dari upload
- `clean_data_scraper` - Data bersih dari scraping
- `classification_results` - Hasil klasifikasi
- `dataset_statistics` - Statistik real-time

## API Endpoints

### Autentikasi
- `POST /login` - Login pengguna
- `POST /register` - Registrasi pengguna
- `GET /logout` - Logout pengguna

### Dataset Management
- `GET /dataset_management` - Halaman manajemen dataset
- `POST /upload_data` - Upload file dataset
- `POST /process_column_mapping` - Proses mapping kolom
- `GET /dataset/<id>/details` - Detail dataset
- `POST /api/dataset/<id>/clean` - Bersihkan dataset

### Scraping
- `GET /scraping` - Halaman scraping
- `POST /start_scraping` - Mulai scraping data
- `POST /process_scraping_column_mapping` - Proses data scraping

### Klasifikasi
- `POST /classify_data` - Klasifikasi data
- `GET /classification/results` - Hasil klasifikasi

### Admin
- `GET /admin` - Panel admin
- `GET /admin/users` - Manajemen pengguna

## Fitur Keamanan

- Password hashing dengan Werkzeug
- Session-based authentication
- Role-based access control
- CSRF protection
- Input validation dan sanitization
- SQL injection prevention dengan ORM

## Monitoring & Logging

- Real-time statistics dengan database triggers
- User activity logging
- Error tracking dan debugging
- Performance monitoring

## 🤝 Kontribusi

1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📄 Lisensi

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Support

- **Documentation**: Baca [User Guide Lengkap](USER_GUIDE_LENGKAP.md)
- **Issues**: Laporkan bug di GitHub Issues
- **Email**: support@waskita.app

---

**© 2024 Waskita - Sistem Klasifikasi Konten Radikal Media Sosial**