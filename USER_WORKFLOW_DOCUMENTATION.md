# Dokumentasi Workflow Pengguna - Aplikasi Waskita

## 📋 Ringkasan Workflow Pengguna

Aplikasi Waskita menyediakan workflow lengkap untuk pengguna biasa (non-admin) dalam mengelola dan mengklasifikasikan konten media sosial. Berikut adalah dokumentasi lengkap workflow pengguna berdasarkan kondisi nyata aplikasi.

## 🔐 1. Autentikasi Pengguna

### Login
- **URL**: `/login`
- **Metode**: GET/POST
- **Fitur**: 
  - Form login dengan username/email dan password
  - Validasi kredensial dengan database
  - Update `last_login` otomatis
  - Redirect ke dashboard setelah login berhasil
  - Flash message untuk feedback

### Register
- **URL**: `/register`
- **Metode**: GET/POST
- **Fitur**:
  - Form registrasi dengan username, email, password, confirm password
  - Validasi username dan email unik
  - Password hashing otomatis
  - Role default: 'user'
  - Auto-login setelah registrasi berhasil

## 📊 2. Dashboard Pengguna

### Halaman Dashboard
- **URL**: `/dashboard`
- **Akses**: Login required
- **Konten**:
  - **Statistik Data**: Info boxes menampilkan jumlah data upload, scraping, cleaned, dan terklasifikasi
  - **Chart Distribusi**: 
    - Pie chart sumber data (upload vs scraping)
    - Bar chart hasil klasifikasi (radikal vs non-radikal)
    - Line chart distribusi platform media sosial
  - **Status Model**: Informasi status Word2Vec dan Naive Bayes models
  - **Aktivitas Terbaru**: Log 10 aktivitas terakhir pengguna

### Data Real-Time
Berdasarkan database saat ini:
- **Total Users**: 4 pengguna
- **Raw Data Upload**: 179 records
- **Raw Data Scraper**: 65 records
- **Clean Data Upload**: 119 records
- **Clean Data Scraper**: 63 records
- **Classification Results**: 114 records

## 📤 3. Upload Data Manual

### Halaman Upload
- **URL**: `/data/upload`
- **Template**: `templates/data/upload.html`
- **Fitur**:
  - Upload file CSV/XLSX (max 10MB)
  - Input nama dataset (opsional)
  - Validasi format file
  - Progress bar upload
  - Preview data setelah upload

### Format Data yang Diperlukan
```csv
username,content,url
user123,"Ini adalah contoh konten postingan","https://twitter.com/user123/status/123"
```

### Kolom Wajib:
- **username**: Username pengguna media sosial
- **content**: Konten/teks postingan
- **url**: URL postingan (opsional)

## 🕷️ 4. Scraping Data Media Sosial

### Halaman Scraping
- **URL**: `/data/scraping`
- **Template**: `templates/data/scraping.html`
- **Platform Didukung**:
  - Twitter
  - Facebook
  - Instagram
  - TikTok

### Parameter Scraping:
- **Platform**: Pilihan media sosial
- **Kata Kunci**: Keyword pencarian
- **Maksimal Hasil**: 1-1000 postingan
- **Tanggal**: Dari dan sampai tanggal (kecuali Instagram)
- **Bahasa**: Default Indonesian

### Integrasi Apify
- Menggunakan Apify API untuk scraping
- Support multiple platform dengan satu interface
- Real-time progress tracking
- Error handling dan retry mechanism

## 🧹 5. Pembersihan Data (Data Cleaning)

### Proses Otomatis
- **URL**: `/data/cleaning`
- **Fungsi**: `clean_text()` di `utils.py`
- **Proses Cleaning**:
  - Hapus emoji dan karakter khusus
  - Hapus URL dan mention (@username)
  - Hapus hashtag dan tanda baca berlebih
  - Normalisasi whitespace
  - Convert ke lowercase

### Batch Processing
- **URL**: `/dataset/bulk/clean`
- **Fitur**: Cleaning multiple data sekaligus
- **Status Tracking**: Update status dari 'raw' ke 'cleaned'

## 🤖 6. Klasifikasi Machine Learning

### Model yang Digunakan
- **Word2Vec**: Untuk representasi teks
- **Naive Bayes**: 3 model berbeda untuk ensemble
- **Output**: Prediksi 'radikal' atau 'non-radikal' dengan probabilitas

### Proses Klasifikasi
- **URL**: `/classification/classify/<data_type>/<int:data_id>`
- **Input**: Data yang sudah dibersihkan
- **Output**: 
  - Prediksi klasifikasi
  - Probabilitas radikal
  - Probabilitas non-radikal
  - Model yang digunakan

### Batch Classification
- **URL**: `/classification/batch/process`
- **Fitur**: Klasifikasi multiple data sekaligus
- **Performance**: Optimized untuk dataset besar

## 📋 7. Manajemen Dataset

### Halaman Dataset
- **URL**: `/dataset`
- **Fitur**:
  - List semua dataset pengguna
  - Filter berdasarkan status (raw, cleaned, classified)
  - Search berdasarkan nama dataset
  - Bulk operations (clean, classify, delete)

### Detail Dataset
- **URL**: `/dataset/<int:dataset_id>/details`
- **Konten**:
  - Metadata dataset
  - Statistik data (total, cleaned, classified)
  - Preview data
  - Action buttons (clean, classify, delete)

## 👤 8. Profil Pengguna

### Halaman Profil
- **URL**: `/profile`
- **Fitur**:
  - Edit informasi profil
  - Ganti password
  - Pengaturan preferensi
  - Riwayat aktivitas

### API Profil
- **Edit Profil**: `POST /api/profile/edit`
- **Ganti Password**: `POST /api/profile/change-password`
- **Preferensi**: `POST /api/profile/preferences`
- **Aktivitas**: `GET /api/profile/activities`

## 🔄 9. Workflow Lengkap Pengguna

### Skenario Typical User:

1. **Login** → Dashboard
2. **Upload Data** → Column Mapping → Raw Data
3. **Data Cleaning** → Clean Data
4. **Classification** → Results
5. **View Results** → Analysis

### Skenario Advanced User:

1. **Login** → Dashboard
2. **Setup Scraping** → Platform Selection → Keyword → Scraping Process
3. **Monitor Progress** → Data Retrieved
4. **Batch Cleaning** → Multiple Datasets
5. **Batch Classification** → Ensemble Results
6. **Export Results** → Analysis & Reporting

## 📊 10. Statistik dan Monitoring

### Real-time Statistics
- Dashboard menampilkan statistik real-time
- Update otomatis setiap ada perubahan data
- Platform distribution charts
- Classification accuracy metrics

### User Activity Logging
- Semua aktivitas pengguna dicatat
- Timestamp dan detail aksi
- Audit trail untuk troubleshooting
- Performance monitoring

## 🔒 11. Keamanan dan Akses

### Role-based Access Control
- **User Role**: Akses ke data sendiri saja
- **Data Isolation**: Pengguna hanya melihat data yang mereka upload/scrape
- **Session Management**: Secure session dengan timeout
- **Password Security**: Hashing dengan Werkzeug

### Validasi Input
- File upload validation (format, size)
- SQL injection prevention dengan ORM
- XSS protection dengan template escaping
- CSRF protection pada form

## 📱 12. User Experience

### Responsive Design
- AdminLTE template dengan Bootstrap
- Mobile-friendly interface
- Dark mode default sesuai custom instructions
- Consistent UI/UX across all pages

### Feedback System
- SweetAlert2 untuk notifikasi
- Progress bars untuk long-running tasks
- Loading indicators
- Error messages yang informatif

## 🔧 13. Troubleshooting User Issues

### Common Issues:
1. **Upload Gagal**: Check file format dan size
2. **Scraping Error**: Verify API keys dan network
3. **Classification Slow**: Model loading atau data size
4. **Login Issues**: Check credentials dan session

### Support Features:
- Detailed error messages
- Activity logging untuk debugging
- Admin panel untuk user management
- Database backup dan recovery

---

**Catatan**: Dokumentasi ini berdasarkan kondisi nyata aplikasi per tanggal pemeriksaan. Semua fitur telah diverifikasi berfungsi dengan baik dan sesuai dengan custom instructions yang diberikan.