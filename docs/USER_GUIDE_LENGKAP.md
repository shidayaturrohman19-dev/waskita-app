# 📖 PANDUAN PENGGUNA LENGKAP APLIKASI WASKITA
## Sistem Klasifikasi Konten Radikal Media Sosial

---

## 📋 DAFTAR ISI

1. [Pengenalan Aplikasi](#1-pengenalan-aplikasi)
2. [Persyaratan Sistem](#2-persyaratan-sistem)
3. [Instalasi dan Setup](#3-instalasi-dan-setup)
4. [Autentikasi dan Manajemen Akun](#4-autentikasi-dan-manajemen-akun)
5. [Dashboard Utama](#5-dashboard-utama)
6. [Pengelolaan Data](#6-pengelolaan-data)
7. [Proses Klasifikasi](#7-proses-klasifikasi)
8. [Interpretasi Hasil](#8-interpretasi-hasil)
9. [Panduan Administrator](#9-panduan-administrator)
10. [Troubleshooting](#10-troubleshooting)
11. [FAQ](#11-faq)

---

## 1. PENGENALAN APLIKASI

### 🎯 Tujuan Aplikasi
**Waskita** adalah sistem berbasis web yang dirancang untuk mengklasifikasikan konten media sosial sebagai **Radikal** atau **Non-Radikal** menggunakan teknologi Machine Learning dengan algoritma Naive Bayes.

### ✨ Fitur Utama
- **Upload Dataset**: Import data dari file CSV/XLSX
- **Web Scraping**: Otomatis mengambil data dari platform media sosial
- **Data Cleaning**: Pembersihan otomatis konten (emoji, link, karakter khusus)
- **Klasifikasi AI**: 3 model Naive Bayes untuk akurasi tinggi
- **Analisis Probabilitas**: Tingkat kepercayaan klasifikasi (0-100%)
- **Export Hasil**: Download hasil dalam format CSV/Excel
- **Multi-User**: Sistem role-based (Admin & User)
- **Dark/Light Mode**: Antarmuka yang dapat disesuaikan

### 🔧 Teknologi yang Digunakan
- **Backend**: Python 3.11.x Flask (WAJIB Python 3.11 untuk kompatibilitas optimal)
- **Database**: PostgreSQL
- **Machine Learning**: Scikit-learn, Gensim Word2Vec
- **Frontend**: Soft UI Dashboard (Bootstrap)
- **Containerization**: Docker & Docker Compose

---

## 2. PERSYARATAN SISTEM

### 💻 Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.11.x ONLY (TIDAK mendukung 3.12/3.13 karena masalah kompatibilitas Gensim)
- **RAM**: 4GB (Recommended: 8GB+)
- **Storage**: 2GB free space
- **Docker**: Docker Desktop 4.0+
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+

### 🌐 Network Requirements
- **Internet**: Diperlukan untuk web scraping
- **Ports**: 5000 (Web App), 5432 (Database), 6379 (Redis)

---

## 3. INSTALASI DAN SETUP

### 🚀 Quick Start dengan Docker

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

3. **Build dan Run**
   ```bash
   docker-compose up -d --build
   ```

4. **Akses Aplikasi**
   - Buka browser: `http://localhost:5000`
   - Login dengan akun default atau register

### ⚙️ Konfigurasi Environment

Edit file `.env.docker`:
```env
# Database Configuration
POSTGRES_DB=waskita_prod
POSTGRES_USER=waskita_user
POSTGRES_PASSWORD=waskita_password

# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=production

# Model Paths (sudah dikonfigurasi)
WORD2VEC_MODEL_PATH=/app/models/embeddings/wiki_word2vec_csv_updated.model
NAIVE_BAYES_MODEL1_PATH=/app/models/navesbayes/naive_bayes_model1.pkl
NAIVE_BAYES_MODEL2_PATH=/app/models/navesbayes/naive_bayes_model2.pkl
NAIVE_BAYES_MODEL3_PATH=/app/models/navesbayes/naive_bayes_model3.pkl
```

---

## 4. AUTENTIKASI DAN MANAJEMEN AKUN

### 🔐 Registrasi Pengguna Baru

1. **Akses Halaman Register**
   - Klik "Register" di halaman login
   - URL: `http://localhost:5000/register`

2. **Isi Form Registrasi**
   ```
   Username: [3-20 karakter, unik]
   Email: [format email valid]
   Password: [minimal 6 karakter]
   Confirm Password: [harus sama dengan password]
   ```

3. **Verifikasi dan Aktivasi**
   - Akun otomatis aktif setelah registrasi
   - Role default: **User** (bukan Admin)

### 🔑 Login ke Sistem

1. **Halaman Login**
   - URL: `http://localhost:5000/login`
   - Masukkan username/email dan password

2. **Jenis Akun**
   - **User**: Akses data pribadi, upload, scraping, klasifikasi
   - **Admin**: Akses penuh ke semua data dan pengguna

### 👤 Manajemen Profil

1. **Edit Profil**
   - Klik nama pengguna di navbar
   - Pilih "Profile"
   - Update informasi personal

2. **Ganti Password**
   - Masuk ke halaman Profile
   - Klik "Change Password"
   - Masukkan password lama dan baru

3. **Pengaturan Tema**
   - Toggle Dark/Light mode di navbar
   - Preferensi tersimpan otomatis

---

## 5. DASHBOARD UTAMA

### 📊 Overview Dashboard

Dashboard menampilkan ringkasan aktivitas:

1. **Statistik Utama**
   - Total Dataset yang diupload
   - Total Data yang di-scrape
   - Total Klasifikasi yang dilakukan
   - Akurasi rata-rata model

2. **Grafik dan Visualisasi**
   - Distribusi klasifikasi (Radikal vs Non-Radikal)
   - Trend aktivitas harian/mingguan
   - Performa model per platform

3. **Aktivitas Terbaru**
   - Log aktivitas pengguna
   - Status proses scraping
   - Notifikasi sistem

### 🎨 Kustomisasi Interface

1. **Dark/Light Mode**
   - Toggle di pojok kanan atas
   - Otomatis tersimpan per user

2. **Bahasa Interface**
   - Default: Bahasa Indonesia
   - Dapat diubah di pengaturan profil

---

## 6. PENGELOLAAN DATA

### 📁 Upload Dataset

#### Langkah-langkah Upload:

1. **Persiapan File**
   - Format: CSV atau XLSX
   - Kolom wajib: `content` (konten teks)
   - Kolom opsional: `username`, `platform`, `date`, `url`

2. **Proses Upload**
   ```
   Menu: Data Management → Upload Dataset
   1. Klik "Choose File"
   2. Pilih file CSV/XLSX
   3. Isi nama dataset
   4. Klik "Upload"
   ```

3. **Validasi Data**
   - Sistem otomatis validasi format
   - Deteksi duplikasi konten
   - Preview data sebelum import

#### Format File yang Didukung:

**CSV Example:**
```csv
content,username,platform,date,url
"Ini adalah contoh konten",user123,twitter,2024-01-15,https://twitter.com/...
"Konten kedua untuk testing",user456,facebook,2024-01-16,https://facebook.com/...
```

**XLSX Example:**
| content | username | platform | date | url |
|---------|----------|----------|------|-----|
| Ini adalah contoh konten | user123 | twitter | 2024-01-15 | https://twitter.com/... |

### 🕷️ Web Scraping

#### Platform yang Didukung:
- **Twitter/X**: Tweet, reply, mention
- **Facebook**: Post, comment
- **Instagram**: Post, caption, comment
- **TikTok**: Video description, comment

#### Langkah-langkah Scraping:

1. **Setup Scraping**
   ```
   Menu: Data Management → Web Scraping
   1. Pilih platform (Twitter/Facebook/Instagram/TikTok)
   2. Masukkan keyword pencarian
   3. Set tanggal mulai dan akhir
   4. Tentukan jumlah maksimal data
   5. Klik "Start Scraping"
   ```

2. **Parameter Scraping**
   - **Keyword**: Kata kunci pencarian (wajib)
   - **Date Range**: Rentang tanggal data (opsional)
   - **Max Results**: Maksimal 1000 data per scraping
   - **Language**: Filter bahasa (default: Indonesia)

3. **Monitoring Progress**
   - Real-time progress bar
   - Estimasi waktu selesai
   - Jumlah data berhasil diambil
   - Log error jika ada

#### Tips Scraping Efektif:
- Gunakan keyword spesifik untuk hasil relevan
- Batasi rentang tanggal untuk performa optimal
- Scraping bertahap untuk dataset besar
- Monitor rate limit platform

### 🧹 Data Cleaning

#### Proses Otomatis:
Sistem otomatis membersihkan:
- **Emoji dan emoticon** (😀 → [dihapus])
- **URL dan link** (https://... → [dihapus])
- **Mention dan hashtag** (@user #tag → [dihapus])
- **Karakter khusus** (!@#$%^&* → [dihapus])
- **Extra whitespace** (spasi berlebih → 1 spasi)
- **Case normalization** (HURUF BESAR → huruf kecil)

#### Manual Cleaning:
1. **Akses Data Cleaning**
   ```
   Menu: Data Management → Clean Data
   1. Pilih dataset yang akan dibersihkan
   2. Preview hasil cleaning
   3. Klik "Apply Cleaning"
   ```

2. **Custom Rules**
   - Tambah kata yang akan dihapus
   - Atur replacement rules
   - Simpan template cleaning

#### Before/After Example:
```
Before: "Halo @user123! 😀 Cek link ini: https://example.com #trending"
After:  "halo cek link ini"
```

---

## 7. PROSES KLASIFIKASI

### 🤖 Sistem Klasifikasi

#### Arsitektur Model:
- **3 Model Naive Bayes** independen
- **Word2Vec Embedding** untuk representasi teks
- **Majority Voting** untuk prediksi final
- **Confidence Score** 0-100%

#### Langkah-langkah Klasifikasi:

1. **Pilih Data untuk Klasifikasi**
   ```
   Menu: Classification → Classify Data
   1. Pilih dataset atau data scraping
   2. Pilih data yang sudah di-cleaning
   3. Klik "Start Classification"
   ```

2. **Proses Klasifikasi**
   - Vectorization dengan Word2Vec
   - Prediksi dengan 3 model Naive Bayes
   - Perhitungan probabilitas
   - Majority voting untuk hasil final

3. **Real-time Monitoring**
   - Progress bar klasifikasi
   - Jumlah data berhasil diproses
   - Estimasi waktu selesai
   - Error handling otomatis

### 📊 Batch Classification

Untuk dataset besar:
1. **Automatic Batching**
   - Sistem otomatis membagi data dalam batch
   - Maksimal 1000 data per batch
   - Parallel processing untuk efisiensi

2. **Resume Capability**
   - Dapat melanjutkan jika terputus
   - Auto-save progress setiap batch
   - Skip data yang sudah diproses

---

## 8. INTERPRETASI HASIL

### 📈 Memahami Output Klasifikasi

#### Format Hasil:
```json
{
  "prediction": "radikal" | "non-radikal",
  "model1": {
    "prediction": "radikal",
    "probability_radikal": 0.85,
    "probability_non_radikal": 0.15
  },
  "model2": { ... },
  "model3": { ... },
  "final_prediction": "radikal",
  "confidence": "high" | "medium" | "low"
}
```

#### Interpretasi Probabilitas:

1. **Probabilitas Radikal**
   - **90-100%**: Sangat yakin konten radikal
   - **70-89%**: Cenderung radikal
   - **51-69%**: Sedikit cenderung radikal
   - **0-50%**: Non-radikal

2. **Contoh Interpretasi**
   ```
   Hasil: "Non-Radikal 39.7%"
   Artinya: 
   - 39.7% kemungkinan non-radikal
   - 60.3% kemungkinan radikal
   - Prediksi final: RADIKAL (karena >50%)
   ```

3. **Tingkat Kepercayaan**
   - **High**: Ketiga model setuju (3/3)
   - **Medium**: Dua model setuju (2/3)
   - **Low**: Hasil split atau probabilitas mendekati 50%

### 📋 Analisis Hasil

#### Dashboard Hasil:
1. **Summary Statistics**
   - Total data diklasifikasi
   - Persentase radikal vs non-radikal
   - Distribusi confidence level
   - Akurasi per model

2. **Detailed View**
   - Tabel hasil per data
   - Filter berdasarkan prediksi
   - Sort berdasarkan confidence
   - Search konten spesifik

3. **Export Options**
   - CSV dengan semua detail
   - Excel dengan formatting
   - JSON untuk integrasi API
   - PDF report summary

#### Visualisasi:
- **Pie Chart**: Distribusi klasifikasi
- **Bar Chart**: Performa per model
- **Timeline**: Trend klasifikasi
- **Heatmap**: Confidence distribution

---

## 9. PANDUAN ADMINISTRATOR

### 👑 Akses Administrator

#### Fitur Khusus Admin:
- Kelola semua pengguna
- Akses semua dataset
- Monitor sistem secara keseluruhan
- Konfigurasi model dan parameter
- Audit log aktivitas

### 👥 Manajemen Pengguna

1. **User Management**
   ```
   Menu: Admin Panel → User Management
   - Lihat semua pengguna
   - Edit role pengguna
   - Reset password pengguna
   - Deaktivasi/aktivasi akun
   ```

2. **Role Assignment**
   - **Admin**: Full access
   - **User**: Limited access
   - **Viewer**: Read-only access

### 📊 System Monitoring

1. **Performance Metrics**
   - CPU dan memory usage
   - Database performance
   - Model response time
   - Error rate monitoring

2. **Activity Logs**
   - User login/logout
   - Data upload/scraping
   - Classification activities
   - System errors

### ⚙️ System Configuration

1. **Model Management**
   - Update model files
   - Adjust model parameters
   - Performance tuning
   - A/B testing setup

2. **System Settings**
   - Rate limiting
   - File size limits
   - Scraping quotas
   - Backup schedules

---

## 10. TROUBLESHOOTING

### ❗ Masalah Umum dan Solusi

#### 1. Login Issues
**Problem**: Tidak bisa login
**Solutions**:
- Periksa username/email dan password
- Clear browser cache dan cookies
- Pastikan akun sudah aktif
- Reset password jika perlu

#### 2. Upload Gagal
**Problem**: File tidak bisa diupload
**Solutions**:
- Periksa format file (CSV/XLSX only)
- Pastikan ukuran file < 50MB
- Validasi struktur kolom
- Periksa encoding file (UTF-8)

#### 3. Scraping Error
**Problem**: Web scraping gagal
**Solutions**:
- Periksa koneksi internet
- Validasi keyword pencarian
- Kurangi jumlah data yang diminta
- Coba platform lain

#### 4. Klasifikasi Lambat
**Problem**: Proses klasifikasi lama
**Solutions**:
- Bagi dataset menjadi batch kecil
- Pastikan data sudah di-cleaning
- Restart container jika perlu
- Monitor resource usage

#### 5. Model Error
**Problem**: Error saat klasifikasi
**Solutions**:
- Periksa model files tersedia
- Restart aplikasi
- Validasi format input data
- Hubungi administrator

### 🔧 Diagnostic Tools

1. **Health Check**
   ```bash
   # Cek status container
   docker ps
   
   # Cek logs aplikasi
   docker logs waskita_app
   
   # Cek resource usage
   docker stats
   ```

2. **Database Check**
   ```bash
   # Connect ke database
   docker exec -it waskita_db psql -U waskita_user -d waskita_prod
   
   # Check tables
   \dt
   
   # Check data count
   SELECT COUNT(*) FROM users;
   ```

---

## 11. FAQ

### ❓ Pertanyaan yang Sering Diajukan

#### Q1: Apakah aplikasi ini gratis?
**A**: Ya, Waskita adalah aplikasi open-source yang dapat digunakan secara gratis.

#### Q2: Berapa akurasi model klasifikasi?
**A**: Akurasi model berkisar 85-92% tergantung jenis konten dan kualitas data training.

#### Q3: Bisakah menambah platform scraping lain?
**A**: Ya, sistem dirancang modular untuk menambah platform baru dengan mudah.

#### Q4: Apakah data aman dan privat?
**A**: Ya, semua data disimpan lokal di server Anda dan tidak dikirim ke pihak ketiga.

#### Q5: Bagaimana cara backup data?
**A**: Gunakan `docker exec` untuk backup database PostgreSQL secara berkala.

#### Q6: Bisakah mengubah bahasa interface?
**A**: Saat ini hanya mendukung Bahasa Indonesia, tapi dapat dikustomisasi.

#### Q7: Apakah bisa dijalankan tanpa Docker?
**A**: Ya, tapi Docker sangat direkomendasikan untuk kemudahan deployment.

#### Q8: Bagaimana cara update aplikasi?
**A**: Pull update terbaru dari repository dan rebuild container.

#### Q9: Bisakah mengintegrasikan dengan sistem lain?
**A**: Ya, tersedia REST API untuk integrasi dengan sistem eksternal.

#### Q10: Apa yang harus dilakukan jika model tidak akurat?
**A**: Lakukan retraining model dengan data yang lebih banyak dan berkualitas.

---

## 📞 DUKUNGAN DAN KONTAK

### 🆘 Mendapatkan Bantuan

1. **Documentation**: Baca panduan ini secara lengkap
2. **GitHub Issues**: Laporkan bug atau request fitur
3. **Community Forum**: Diskusi dengan pengguna lain
4. **Email Support**: Untuk bantuan teknis khusus

### 🔄 Update dan Maintenance

- **Regular Updates**: Cek update mingguan
- **Security Patches**: Install patch keamanan segera
- **Backup Schedule**: Backup data setiap hari
- **Performance Monitoring**: Monitor resource usage

---

## 📝 CHANGELOG

### Version 1.0.0 (Current)
- ✅ Initial release
- ✅ Basic classification functionality
- ✅ Web scraping for 4 platforms
- ✅ Multi-user support
- ✅ Docker containerization

### Planned Features
- 🔄 Real-time classification API
- 🔄 Advanced analytics dashboard
- 🔄 Mobile responsive design
- 🔄 Multi-language support
- 🔄 Advanced model tuning

---

**© 2024 Waskita - Sistem Klasifikasi Konten Radikal**

*Panduan ini akan terus diperbarui seiring dengan perkembangan aplikasi.*