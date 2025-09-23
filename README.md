# Waskita - Aplikasi Klasifikasi Konten Media Sosial

Waskita adalah aplikasi web berbasis Flask untuk mengklasifikasikan konten media sosial sebagai radikal atau non-radikal menggunakan machine learning.

## Fitur Utama

### 🔐 Autentikasi & Otorisasi
- Sistem login/register dengan role-based access (Admin/User)
- Password hashing untuk keamanan
- Session management yang aman

### 📊 Manajemen Dataset
- Upload data dari file CSV/XLSX
- Scraping data dari media sosial (Twitter, TikTok, Facebook, Instagram)
- Pembersihan data otomatis (cleaning)
- Statistik dataset real-time

### 🤖 Klasifikasi Machine Learning
- Model Naive Bayes untuk klasifikasi konten
- Word2Vec untuk representasi teks
- Prediksi probabilitas radikal/non-radikal
- Batch processing untuk dataset besar

### 👨‍💼 Panel Admin
- Manajemen pengguna dan dataset
- Monitoring aktivitas sistem
- Statistik komprehensif
- Audit trail

## Teknologi yang Digunakan

- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Machine Learning**: scikit-learn, Gensim
- **Database**: PostgreSQL dengan trigger otomatis
- **Containerization**: Docker & Docker Compose

## Instalasi

### Menggunakan Docker (Recommended)

1. Clone repository:
```bash
git clone <repository-url>
cd waskita
```

2. Copy file environment:
```bash
cp .env.example .env
```

3. Jalankan dengan Docker Compose:
```bash
docker-compose up -d
```

4. Akses aplikasi di `http://localhost:5000`

### Manual Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Setup database PostgreSQL dan update `.env`

3. Jalankan migrasi database:
```bash
flask db upgrade
```

4. Jalankan aplikasi:
```bash
python app.py
```

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

## Kontribusi

1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## Lisensi

Project ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## Support

Untuk pertanyaan atau dukungan, silakan buat issue di repository ini.

---

**Catatan**: Aplikasi ini dikembangkan untuk tujuan penelitian dan edukasi dalam bidang klasifikasi teks dan analisis media sosial.