# Waskita - Sistem Klasifikasi Konten Media Sosial

*Dikembangkan sebagai kontribusi penelitian akademik dalam bidang Natural Language Processing dan Machine Learning untuk analisis konten media sosial Indonesia*

## 📋 Deskripsi

Waskita adalah sistem berbasis web untuk mengklasifikasikan konten media sosial menggunakan Machine Learning (Naive Bayes dengan Word2Vec embedding) untuk mengidentifikasi konten radikal atau non-radikal. Sistem ini dikembangkan sebagai kontribusi akademik dalam bidang NLP dan analisis sentimen untuk deteksi konten ekstremis dalam media sosial Indonesia.

## 🚀 Instalasi

### Prasyarat
- Python 3.8+
- PostgreSQL 12+
- Git

### 1. Instalasi dengan Docker (Direkomendasikan)

```bash
# Clone repository
git clone https://github.com/kaptenusop/waskita.git
cd waskita

# Jalankan dengan Docker Compose
docker-compose up -d

# Akses aplikasi di http://localhost:5000
```

### 2. Instalasi Manual Lokal

```bash
# Clone repository
git clone https://github.com/kaptenusop/waskita.git
cd waskita

# Buat virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup database PostgreSQL
python setup_postgresql.py

# Setup environment variables
copy .env.example .env
# Edit .env sesuai konfigurasi Anda

# Setup model ML (diperlukan)
mkdir -p models/embeddings
mkdir -p models/navesbayes
# Letakkan file model:
# - models/embeddings/wiki_word2vec_csv_updated.model
# - models/navesbayes/naive_bayes_model1.pkl
# - models/navesbayes/naive_bayes_model2.pkl
# - models/navesbayes/naive_bayes_model3.pkl

# Jalankan aplikasi
python app.py
```

### 3. Konfigurasi Environment

Edit file `.env` dengan konfigurasi berikut:

```bash
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/waskita_db

# Flask
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Email (untuk OTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Model Paths
WORD2VEC_MODEL_PATH=models/embeddings/wiki_word2vec_csv_updated.model
NAIVE_BAYES_MODEL1_PATH=models/navesbayes/naive_bayes_model1.pkl
NAIVE_BAYES_MODEL2_PATH=models/navesbayes/naive_bayes_model2.pkl
NAIVE_BAYES_MODEL3_PATH=models/navesbayes/naive_bayes_model3.pkl
```

## 🔬 Fitur Penelitian

### **Machine Learning Methodology**
- **Algoritma**: Naive Bayes dengan Word2Vec embedding
- **Akurasi**: 85-92% pada dataset uji
- **Preprocessing**: Tokenisasi, normalisasi teks bahasa Indonesia
- **Feature Extraction**: Word2Vec untuk representasi semantik

### **Security & Authentication**
- **Multi-layer Authentication**: Password hashing, OTP verification
- **Web Protection**: CSRF, rate limiting, input validation
- **Database Security**: SQLAlchemy ORM, parameterized queries

### **Research Data Management**
- **Multi-format Input**: CSV, XLSX, JSON untuk dataset
- **Data Validation**: Otomatis cleaning dan preprocessing
- **Export Capabilities**: Hasil klasifikasi dalam berbagai format

### **Analytics Dashboard**
- **Real-time Statistics**: Monitoring performa model
- **Visualization**: Chart dan grafik untuk analisis data
- **Audit Trail**: Logging aktivitas untuk penelitian

## 🛠️ Teknologi

- **Python** - Bahasa pemrograman utama
- **Flask** - Web framework
- **PostgreSQL** - Database
- **Scikit-learn** - Machine learning library
- **Word2Vec** - Text embedding
- **Bootstrap** - Frontend framework
- **Docker** - Containerization

## 📚 Dokumentasi Lengkap

- **[Setup Guide](docs/SETUP_APPS.md)** - Panduan instalasi detail
- **[Security Guide](docs/SECURITY_GUIDE.md)** - Konfigurasi keamanan

## 🤝 Kontribusi Penelitian

Kontribusi untuk pengembangan penelitian ini sangat diterima dari komunitas akademik. Silakan:

1. Fork repository ini
2. Buat branch untuk fitur baru (`git checkout -b feature/fitur-baru`)
3. Commit perubahan (`git commit -m 'Tambah fitur baru'`)
4. Push ke branch (`git push origin feature/fitur-baru`)
5. Buat Pull Request

## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

## ⚠️ Disclaimer Penelitian

Sistem **Waskita** dikembangkan sebagai instrumen penelitian akademik dalam bidang *Natural Language Processing* dan analisis konten media sosial.

**Ketentuan Penggunaan:**
- Dirancang khusus untuk keperluan penelitian dan pengembangan akademik
- Implementasi produksi memerlukan evaluasi dan validasi tambahan
- Hasil klasifikasi harus diinterpretasikan dalam konteks penelitian
- Pengguna bertanggung jawab memastikan kepatuhan regulasi dan etika penelitian

**Rekomendasi Penelitian:**
- Lakukan validasi silang dengan dataset independen
- Pertimbangkan bias dan limitasi model dalam interpretasi hasil
- Dokumentasikan metodologi untuk reproduktibilitas
- Patuhi prinsip etika penelitian dalam penggunaan data

---

*Dikembangkan sebagai kontribusi penelitian akademik dalam bidang Natural Language Processing dan Machine Learning untuk analisis konten media sosial Indonesia*