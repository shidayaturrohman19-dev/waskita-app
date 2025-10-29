# 📚 PANDUAN PENGGUNA LENGKAP WASKITA

**Waskita** adalah sistem berbasis web yang menggunakan Machine Learning untuk mengklasifikasikan konten media sosial sebagai **Radikal** atau **Non-Radikal** dengan akurasi hingga 92% menggunakan 3 model Naive Bayes dan Word2Vec embedding.

---

## 🚀 Memulai

### Persyaratan Sistem
- **Python**: 3.11.x (TIDAK mendukung 3.12/3.13)
- **RAM**: Minimal 4GB (Direkomendasikan: 8GB untuk model ML)
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Koneksi Internet**: Diperlukan untuk web scraping dan email OTP

### Akses Aplikasi
1. **Buka browser** dan akses `http://localhost:5000`
2. **Login** dengan kredensial:
   - **Admin**: `admin` / `admin123` (ubah setelah login pertama)
   - **User Baru**: Daftar melalui sistem OTP email

---

## 🎯 DASHBOARD UTAMA

### Statistik Real-time
Dashboard menampilkan 4 metrik utama:
- **📤 Data Upload**: Total data yang diupload manual
- **🕷️ Data Scraping**: Total data dari web scraping
- **🧹 Data Cleaned**: Total data yang sudah dibersihkan
- **🧠 Terklasifikasi**: Total data yang sudah diklasifikasi

### Quick Actions
- **Upload Data**: Upload file CSV/XLSX
- **Scraping Data**: Scraping dari media sosial
- **Kelola Dataset**: Manajemen dataset
- **Klasifikasi**: Klasifikasi konten AI

### Status Sistem
- **Word2Vec Model**: Status model embedding
- **Naive Bayes Models**: Status 3 model klasifikasi (x/3)
- **Database Connection**: Status koneksi database

---

## 📊 FITUR UTAMA

### 1. 📤 UPLOAD DATASET

#### Format File yang Didukung
- **CSV**: Dengan encoding UTF-8, UTF-8-BOM, Latin1
- **Excel**: Format .xlsx dan .xls
- **Kolom Wajib**: `content` (berisi teks yang akan diklasifikasi)
- **Kolom Opsional**: `username`, `url`, `platform`

#### Langkah Upload
1. **Navigasi**: Dashboard → Upload Data
2. **Pilih File**: Klik "Choose File" dan pilih dataset
3. **Validasi**: Sistem otomatis validasi format dan duplikasi
4. **Konfirmasi**: Review data preview sebelum upload
5. **Proses**: Data disimpan ke database dengan timestamp

#### Validasi Keamanan
- **File Size**: Maksimal 50MB per file
- **MIME Type**: Validasi tipe file yang aman
- **Content Scan**: Deteksi malware dan virus
- **Duplicate Check**: Otomatis deteksi konten duplikat

### 2. 🕷️ WEB SCRAPING

#### Platform yang Didukung
- **Twitter/X**: Scraping tweets berdasarkan keyword
- **Facebook**: Posts publik dan komentar
- **Instagram**: Posts dan caption
- **TikTok**: Video descriptions dan komentar

#### Setup Scraping
1. **Konfigurasi API**: Dapatkan Apify API token
2. **Set Environment**: Tambahkan `APIFY_API_TOKEN` ke `.env`
3. **Pilih Platform**: Pilih platform target scraping
4. **Input Keyword**: Masukkan kata kunci pencarian
5. **Set Parameters**: Tentukan jumlah data dan rentang tanggal

#### Fitur Advanced
- **Date Range**: Scraping berdasarkan rentang tanggal
- **Max Results**: Batasi jumlah hasil (default: 25)
- **Real-time Progress**: Monitor progress scraping
- **Error Handling**: Otomatis retry jika gagal

### 3. 🧹 DATA CLEANING

#### Proses Otomatis
- **Remove Emoji**: Hapus semua emoji dan emoticon
- **Clean URLs**: Hapus link dan URL
- **Remove Mentions**: Hapus @username dan #hashtag
- **Special Characters**: Hapus karakter khusus dan angka
- **Normalize Text**: Konversi ke lowercase dan trim whitespace

#### Preprocessing Indonesia
- **Stopwords**: Hapus kata-kata umum bahasa Indonesia
- **Stemming**: Konversi ke kata dasar (opsional)
- **Tokenization**: Pisahkan kata untuk Word2Vec

#### Batch Processing
- **Bulk Clean**: Proses ribuan data sekaligus
- **Progress Tracking**: Monitor progress real-time
- **Error Recovery**: Lanjutkan jika ada data error

### 4. 🧠 KLASIFIKASI AI

#### Model Machine Learning
- **Word2Vec**: Model embedding 300 dimensi
- **Naive Bayes 1**: Model klasifikasi utama
- **Naive Bayes 2**: Model validasi silang
- **Naive Bayes 3**: Model ensemble

#### Proses Klasifikasi
1. **Pilih Dataset**: Pilih data yang sudah dibersihkan
2. **Model Selection**: Pilih model yang akan digunakan
3. **Batch Process**: Klasifikasi otomatis semua data
4. **Real-time Progress**: Monitor progress per model
5. **Results**: Lihat hasil dengan probabilitas

#### Output Klasifikasi
- **Prediksi**: Radikal / Non-Radikal
- **Probabilitas Radikal**: Persentase kemungkinan radikal
- **Probabilitas Non-Radikal**: Persentase kemungkinan non-radikal
- **Confidence Score**: Tingkat kepercayaan model

### 5. 📁 EXPORT HASIL

#### Format Export
- **CSV**: Format comma-separated values
- **Excel**: Format .xlsx dengan formatting
- **Include Data**: Teks asli, hasil klasifikasi, probabilitas semua model

#### Struktur Export
```
ID | Username | Konten | URL | Tipe Data | Tanggal |
Model 1 - Prediksi | Model 1 - Prob Radikal | Model 1 - Prob Non-Radikal |
Model 2 - Prediksi | Model 2 - Prob Radikal | Model 2 - Prob Non-Radikal |
Model 3 - Prediksi | Model 3 - Prob Radikal | Model 3 - Prob Non-Radikal
```

### 6. 📈 DATASET MANAGEMENT

#### Fitur Management
- **Create Dataset**: Buat dataset baru dengan nama dan deskripsi
- **View Details**: Lihat detail data raw, cleaned, dan classified
- **Statistics**: Statistik lengkap per dataset
- **Delete Dataset**: Hapus dataset beserta semua data terkait

#### Tabs Dataset Detail
- **Raw Data**: Data mentah dari upload/scraping
- **Cleaned Data**: Data yang sudah dibersihkan
- **Classification Results**: Hasil klasifikasi semua model

---

## 🔐 KEAMANAN & AUTENTIKASI

### Sistem OTP Email
- **Registrasi**: Verifikasi email dengan OTP 6 digit
- **Keamanan**: OTP berlaku 10 menit
- **Resend**: Bisa kirim ulang OTP setelah 1 menit
- **Admin Approval**: Admin harus approve registrasi baru

### Role-Based Access
- **Admin**: Akses penuh + approve user baru
- **User**: Akses fitur klasifikasi dan data management
- **Security**: Rate limiting 500 request/hari, 200/jam

### Fitur Keamanan
- **CSRF Protection**: Perlindungan dari serangan CSRF
- **Input Validation**: Sanitasi semua input pengguna
- **File Upload Security**: Validasi MIME type dan virus scan
- **Security Headers**: HTTP security headers otomatis
- **Activity Logging**: Log semua aktivitas pengguna

---

## 📱 ANTARMUKA PENGGUNA

### Responsive Design
- **Desktop**: Layout penuh dengan sidebar
- **Tablet**: Layout adaptif dengan collapsible menu
- **Mobile**: Layout mobile-first dengan bottom navigation

### Accessibility
- **Screen Reader**: Support ARIA labels dan descriptions
- **Keyboard Navigation**: Navigasi penuh dengan keyboard
- **High Contrast**: Mode kontras tinggi
- **Font Scaling**: Support zoom browser hingga 200%

### Modern UI Features
- **Real-time Updates**: Progress bars dan notifications
- **Interactive Charts**: Chart.js untuk visualisasi data
- **Modal Dialogs**: Detail data dalam modal popup
- **Toast Notifications**: Notifikasi sukses/error yang elegant

---

## 🔧 TROUBLESHOOTING

### Masalah Upload
**Q: File tidak bisa diupload?**
- ✅ Pastikan format CSV/XLSX
- ✅ Ukuran file < 50MB
- ✅ File memiliki kolom 'content'
- ✅ Encoding UTF-8

**Q: Data duplikat terdeteksi?**
- ✅ Sistem otomatis skip data duplikat
- ✅ Check kolom content yang sama
- ✅ Lihat log untuk detail duplikasi

### Masalah Scraping
**Q: Scraping gagal?**
- ✅ Pastikan APIFY_API_TOKEN valid
- ✅ Check koneksi internet
- ✅ Pastikan kredit Apify mencukupi
- ✅ Coba keyword yang berbeda

**Q: Hasil scraping kosong?**
- ✅ Keyword terlalu spesifik
- ✅ Platform tidak memiliki data publik
- ✅ Batasan API platform

### Masalah Klasifikasi
**Q: Model tidak load?**
- ✅ Pastikan file model ada di folder `models/`
- ✅ Check RAM minimal 4GB
- ✅ Restart aplikasi
- ✅ Contact admin untuk file model

**Q: Klasifikasi lambat?**
- ✅ Proses batch memerlukan waktu
- ✅ RAM tidak mencukupi
- ✅ Tutup aplikasi lain
- ✅ Kurangi jumlah data per batch

### Masalah Login
**Q: OTP tidak diterima?**
- ✅ Check folder spam email
- ✅ Pastikan email valid
- ✅ Tunggu hingga 5 menit
- ✅ Coba resend OTP

**Q: Login gagal terus?**
- ✅ Pastikan username/password benar
- ✅ Account sudah diapprove admin
- ✅ Clear browser cache
- ✅ Coba browser berbeda

---

## 💡 TIPS PENGGUNAAN

### Workflow Optimal
1. **Setup**: Login → Check model status di dashboard
2. **Data Input**: Upload dataset ATAU scraping dari media sosial
3. **Preprocessing**: Otomatis cleaning saat upload/scraping
4. **Classification**: Pilih dataset → Run klasifikasi
5. **Analysis**: Review hasil di dashboard dan dataset details
6. **Export**: Download hasil untuk analisis lanjutan

### Best Practices
- **Dataset Size**: Optimal 100-10,000 data per batch
- **Keyword Scraping**: Gunakan keyword spesifik untuk hasil relevan
- **Model Validation**: Gunakan 3 model untuk validasi silang
- **Regular Backup**: Export hasil secara berkala
- **Monitor Resources**: Check RAM usage saat proses besar

### Interpretasi Hasil
- **Probabilitas > 70%**: Prediksi sangat yakin
- **Probabilitas 50-70%**: Prediksi cukup yakin
- **Probabilitas < 50%**: Prediksi kurang yakin, perlu review manual
- **Konsensus Model**: Jika 2-3 model setuju, hasil lebih akurat

---

## 📞 DUKUNGAN

### Bantuan Teknis
- **Email**: [admin@waskita.com](mailto:admin@waskita.com)
- **Documentation**: Lihat folder `docs/` untuk panduan lengkap
- **GitHub Issues**: Report bug di repository GitHub

### Pelatihan
- **User Training**: Tersedia pelatihan penggunaan sistem
- **Admin Training**: Pelatihan khusus administrator
- **Custom Training**: Pelatihan sesuai kebutuhan organisasi

---

## 📋 CHECKLIST PENGGUNAAN

### Setup Awal
- [ ] ✅ Login berhasil dengan kredensial
- [ ] ✅ Dashboard menampilkan statistik
- [ ] ✅ Model status "Loaded" (Word2Vec + 3 Naive Bayes)
- [ ] ✅ Test upload file sample
- [ ] ✅ Test klasifikasi manual

### Penggunaan Harian
- [ ] ✅ Monitor statistik dashboard
- [ ] ✅ Check aktivitas terbaru
- [ ] ✅ Backup hasil klasifikasi
- [ ] ✅ Review data yang diragukan
- [ ] ✅ Update dataset secara berkala

### Maintenance
- [ ] ✅ Check disk space untuk upload
- [ ] ✅ Monitor RAM usage
- [ ] ✅ Update password secara berkala
- [ ] ✅ Review security logs
- [ ] ✅ Backup database

---

**🎉 Selamat menggunakan Waskita! Sistem klasifikasi konten media sosial yang aman, akurat, dan mudah digunakan.**
- **Statistik**: Total data, akurasi, distribusi klasifikasi
- **Grafik**: Visualisasi hasil real-time
- **Model Status**: Monitor status loading model ML

## 🔧 Troubleshooting

| Masalah | Solusi |
|---------|--------|
| **Login gagal** | Gunakan admin/admin123 atau reset password |
| **Upload gagal** | Pastikan format CSV/XLSX dengan kolom 'content' |
| **Model tidak load** | Pastikan file model ada di folder models/ |
| **Scraping error** | Check Apify API token dan koneksi internet |
| **Klasifikasi lambat** | Gunakan dataset lebih kecil (<1000 baris) |
| **Memory error** | Restart aplikasi, close aplikasi lain |

## 🎯 Tips Penggunaan

### Untuk Hasil Optimal:
1. **Data Quality**: Gunakan teks bahasa Indonesia yang jelas
2. **Dataset Size**: Mulai dengan <500 baris untuk testing
3. **Cleaning**: Selalu lakukan data cleaning sebelum klasifikasi
4. **Model Status**: Pastikan semua model "Loaded" di dashboard

### Workflow Recommended:
1. Upload dataset → 2. Clean data → 3. Classify → 4. Export hasil

## 📊 Interpretasi Hasil

### Klasifikasi Output:
- **Radikal**: Konten berpotensi mengandung unsur radikalisme
- **Non-Radikal**: Konten normal/aman
- **Probabilitas**: 0-100% (semakin tinggi = semakin yakin)

### Threshold Rekomendasi:
- **>80%**: Hasil sangat yakin
- **60-80%**: Hasil cukup yakin  
- **<60%**: Perlu review manual

## 🆘 Dukungan

### Jika Mengalami Masalah:
1. Check troubleshooting di atas
2. Restart aplikasi
3. Check log error di terminal
4. Hubungi pengembang dengan detail error

### Informasi Sistem:
- **Open Source**: Gratis digunakan
- **Data Privacy**: Semua data disimpan lokal
- **Security**: Tidak ada data dikirim ke server eksternal

---

**Catatan**: Panduan ini untuk versi terbaru Waskita. Pastikan menggunakan versi yang sesuai.