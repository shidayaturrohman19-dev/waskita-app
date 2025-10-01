# 📖 MANUAL PENGGUNA APLIKASI WASKITA
## Sistem Klasifikasi Konten Radikal Media Sosial

---

**Tujuan:** Dokumen ini menyediakan panduan komprehensif untuk membantu pengguna akhir memahami dan menggunakan **Aplikasi Waskita** secara efisien. Manual ini mencakup deskripsi fitur utama, prosedur setup, panduan penggunaan, tips troubleshooting, dan informasi dukungan.

---

## 1. PENGENALAN

**Aplikasi Waskita** dirancang untuk **mengklasifikasikan konten media sosial sebagai Radikal atau Non-Radikal menggunakan teknologi Machine Learning dengan algoritma Naive Bayes**. Manual ini bertujuan untuk memandu pengguna melalui instalasi, penggunaan, dan pemeliharaan sistem.

### 🎯 Keunggulan Waskita
- Akurasi klasifikasi tinggi (85-92%)
- Mendukung 4 platform media sosial (Twitter, Facebook, Instagram, TikTok)
- Interface modern dengan Dark/Light mode
- Sistem multi-user dengan role-based access
- Real-time processing dengan progress monitoring

---

## 2. PERSYARATAN SISTEM

### 💻 **Perangkat Keras Minimum:**
- **Processor:** Intel Core i3 atau AMD Ryzen 3 (2.0 GHz+)
- **RAM:** 4GB minimum (Direkomendasikan: 8GB+)
- **Storage:** 2GB ruang kosong untuk aplikasi dan data
- **Network:** Koneksi internet stabil untuk web scraping

### 🖥️ **Sistem Operasi:**
- **Windows:** Windows 10/11 (64-bit)
- **macOS:** macOS 10.15 Catalina atau lebih baru
- **Linux:** Ubuntu 18.04+, CentOS 7+, atau distribusi kompatibel

### 🌐 **Browser yang Didukung:**
- **Google Chrome:** Versi 90 atau lebih baru
- **Mozilla Firefox:** Versi 88 atau lebih baru
- **Safari:** Versi 14 atau lebih baru
- **Microsoft Edge:** Versi 90 atau lebih baru

### 🐳 **Software Dependencies:**
- **Docker Desktop:** Versi 4.0 atau lebih baru
- **Docker Compose:** Versi 2.0 atau lebih baru

---

## 3. PETUNJUK INSTALASI

### 📥 **Unduh Paket Instalasi**
Unduh paket instalasi dari **https://github.com/Sansidam16/myapp/releases**

### 🚀 **Instalasi dengan Docker (Direkomendasikan)**

1. **Unduh dan ekstrak file** `waskita-docker.zip` ke direktori pilihan Anda
2. **Klik dua kali** file `install-waskita.bat` (Windows) atau `install-waskita.sh` (Linux/macOS) untuk menjalankan installer
3. **Ikuti instruksi di layar** untuk menyelesaikan instalasi

### ⚙️ **Catatan Instalasi:**
- Pastikan Docker Desktop sudah berjalan sebelum instalasi
- Proses instalasi membutuhkan koneksi internet untuk mengunduh dependencies
- Instalasi pertama dapat memakan waktu 10-15 menit tergantung kecepatan internet
- Port 5000, 5432, dan 6379 harus tersedia (tidak digunakan aplikasi lain)

---

## 4. MEMULAI PENGGUNAAN

Bagian ini menjelaskan cara mulai menggunakan **Aplikasi Waskita** setelah instalasi.

### 🚀 **Menjalankan Aplikasi**
1. **Klik ikon** `Waskita App` di desktop atau menu Start
2. **Login dengan kredensial** Anda (username dan password)
3. **Ikuti setup terpandu** untuk mengkonfigurasi preferensi awal

### 👤 **Akun Default:**
- **Username:** admin
- **Password:** admin123
- **Role:** Administrator

### 🔧 **Konfigurasi Awal:**
1. Ubah password default untuk keamanan
2. Pilih tema interface (Dark/Light mode)
3. Konfigurasi API keys untuk web scraping (opsional)
4. Set preferensi bahasa dan timezone

---

## 5. IKHTISAR FITUR

### 🔑 **Fitur Utama:**

#### **🔐 Autentikasi & Manajemen Pengguna:**
Sistem login/register dengan role-based access (Admin/User), password hashing untuk keamanan, dan session management yang aman

#### **📊 Manajemen Dataset:**
Upload data dari file CSV/XLSX dengan validasi otomatis, web scraping dari 4 platform media sosial, dan pembersihan data otomatis

#### **🤖 Klasifikasi Machine Learning:**
3 model Naive Bayes independen untuk akurasi maksimal, Word2Vec embedding untuk representasi teks optimal, dan confidence score 0-100%

#### **👨‍💼 Panel Administrator:**
Manajemen pengguna dan dataset, monitoring aktivitas sistem real-time, dan audit trail lengkap semua aktivitas

#### **📈 Dashboard & Visualisasi:**
Statistik real-time dengan grafik interaktif, monitoring performa sistem, dan export hasil dalam berbagai format

#### **🌐 Web Scraping Otomatis:**
Scraping data dari Twitter, Facebook, Instagram, dan TikTok dengan parameter yang dapat dikustomisasi

---

## 6. PETUNJUK PENGGUNAAN

Langkah-langkah detail untuk melakukan tugas-tugas umum:

### 📤 **Upload dan Klasifikasi Dataset**

#### **Langkah 1: Persiapan Data**
- Siapkan file CSV/XLSX dengan kolom teks yang akan diklasifikasi
- Pastikan data tidak mengandung karakter khusus yang dapat mengganggu proses
- Maksimal ukuran file: 16MB

#### **Langkah 2: Upload Dataset**
- Klik menu "Dataset Management" di sidebar
- Pilih "Upload Dataset" dan browse file Anda
- Lakukan mapping kolom sesuai dengan format yang diminta
- Klik "Upload" dan tunggu proses validasi selesai

#### **Langkah 3: Pembersihan Data**
- Setelah upload berhasil, klik "Clean Data" pada dataset
- Sistem akan otomatis menghapus emoji, link, dan karakter khusus
- Monitor progress pembersihan di dashboard

#### **Langkah 4: Klasifikasi**
- Klik "Classify Data" pada dataset yang sudah dibersihkan
- Pilih model klasifikasi (atau gunakan semua model untuk akurasi maksimal)
- Tunggu proses klasifikasi selesai
- Lihat hasil di halaman "Classification Results"

### 🕷️ **Web Scraping Media Sosial**

#### **Langkah 1: Konfigurasi Scraping**
- Buka menu "Web Scraping" di sidebar
- Pilih platform media sosial (Twitter/Facebook/Instagram/TikTok)
- Masukkan kata kunci pencarian dan parameter lainnya

#### **Langkah 2: Mulai Scraping**
- Klik "Start Scraping" untuk memulai proses
- Monitor progress di dashboard real-time
- Scraping akan berjalan di background

#### **Langkah 3: Proses Data Hasil Scraping**
- Setelah scraping selesai, data akan muncul di "Scraped Data"
- Lakukan pembersihan data seperti pada dataset upload
- Lanjutkan dengan proses klasifikasi

### 📊 **Analisis Hasil Klasifikasi**

#### **Langkah 1: Akses Hasil**
- Buka menu "Classification Results"
- Pilih dataset yang ingin dianalisis
- Lihat statistik keseluruhan dan detail per item

#### **Langkah 2: Interpretasi Skor**
- **Confidence Score 80-100%:** Klasifikasi sangat yakin
- **Confidence Score 60-79%:** Klasifikasi cukup yakin
- **Confidence Score <60%:** Perlu review manual

#### **Langkah 3: Export Hasil**
- Klik "Export Results" untuk download dalam format CSV/Excel
- Pilih kolom yang ingin disertakan dalam export
- File akan diunduh otomatis ke folder Downloads

---

## 7. PANDUAN TROUBLESHOOTING

Jika Anda mengalami masalah, rujuk tabel di bawah ini untuk kemungkinan penyebab dan solusi:

| **Masalah** | **Penyebab** | **Solusi** |
|-------------|--------------|------------|
| **Aplikasi tidak dapat diakses** | Docker tidak berjalan atau port 5000 digunakan aplikasi lain | Pastikan Docker Desktop berjalan, restart aplikasi, atau ubah port di konfigurasi |
| **Login gagal** | Username/password salah atau session expired | Periksa kredensial, reset password jika perlu, atau clear browser cache |
| **Upload file gagal** | Format file tidak didukung atau ukuran terlalu besar | Gunakan format CSV/XLSX, maksimal 16MB, periksa struktur kolom |
| **Scraping tidak berjalan** | API key tidak valid atau platform membatasi akses | Periksa API key di konfigurasi, coba lagi nanti, atau gunakan parameter berbeda |
| **Klasifikasi error** | Model tidak ditemukan atau data tidak valid | Restart aplikasi, periksa log error, atau hubungi support |
| **Hasil tidak akurat** | Data training kurang atau preprocessing tidak optimal | Gunakan dataset yang lebih besar, lakukan cleaning data yang lebih baik |
| **Performance lambat** | RAM tidak cukup atau dataset terlalu besar | Tutup aplikasi lain, upgrade RAM, atau bagi dataset menjadi batch kecil |
| **Database connection error** | PostgreSQL tidak berjalan atau konfigurasi salah | Restart Docker containers, periksa konfigurasi database di .env |

---

## 8. PERTANYAAN YANG SERING DIAJUKAN (FAQ)

### **❓ Apakah Waskita dapat mengklasifikasi bahasa selain Indonesia?**
**Jawab:** Saat ini Waskita dioptimalkan untuk bahasa Indonesia. Untuk bahasa lain, akurasi mungkin menurun dan memerlukan model yang disesuaikan.

### **❓ Berapa lama waktu yang dibutuhkan untuk mengklasifikasi 1000 data?**
**Jawab:** Rata-rata 1-2 menit untuk 1000 data, tergantung spesifikasi hardware dan kompleksitas teks.

### **❓ Apakah data yang diupload aman dan privat?**
**Jawab:** Ya, semua data disimpan secara lokal di server Anda dan tidak dikirim ke pihak ketiga. Pastikan untuk menggunakan password yang kuat.

### **❓ Bagaimana cara meningkatkan akurasi klasifikasi?**
**Jawab:** Gunakan data training yang berkualitas, lakukan preprocessing yang baik, dan gunakan semua 3 model untuk majority voting.

### **❓ Apakah bisa menggunakan Waskita untuk analisis sentimen?**
**Jawab:** Waskita dirancang khusus untuk klasifikasi radikal/non-radikal. Untuk analisis sentimen, diperlukan model yang berbeda.

### **❓ Bagaimana cara backup data dan hasil klasifikasi?**
**Jawab:** Gunakan fitur export untuk backup hasil, dan lakukan backup database PostgreSQL secara berkala melalui Docker.

### **❓ Apakah Waskita dapat diintegrasikan dengan sistem lain?**
**Jawab:** Ya, Waskita menyediakan REST API yang dapat diintegrasikan dengan sistem eksternal. Dokumentasi API tersedia di menu Developer.

### **❓ Bagaimana cara menambah user baru?**
**Jawab:** Admin dapat menambah user baru melalui menu "User Management" di panel administrator.

---

## 9. DUKUNGAN DAN KONTAK

Jika Anda memerlukan bantuan lebih lanjut, silakan hubungi tim dukungan kami:

### 📧 **Email:** support@waskita.app
### 📞 **Telepon:** +62-21-1234-5678 (Senin-Jumat, 09:00-17:00 WIB)
### 🌐 **Website:** https://waskita.app/support
### 💬 **Live Chat:** Dukungan live chat tersedia di: https://waskita.app/chat (24/7)

### 📚 **Sumber Daya Tambahan:**
- **Dokumentasi Teknis:** https://docs.waskita.app
- **Video Tutorial:** https://youtube.com/waskita-tutorials
- **Community Forum:** https://forum.waskita.app
- **GitHub Repository:** https://github.com/Sansidam16/myapp

---

## 10. RIWAYAT REVISI

| **Versi** | **Tanggal** | **Perubahan** |
|-----------|-------------|---------------|
| **1.0.0** | 2024-01-15 | Rilis awal manual pengguna dengan fitur dasar |
| **1.1.0** | 2024-02-20 | Penambahan panduan web scraping dan troubleshooting |
| **1.2.0** | 2024-03-10 | Update fitur dark mode dan optimasi performa |
| **1.3.0** | 2024-04-05 | Penambahan multi-model classification dan API documentation |
| **1.4.0** | 2024-05-15 | Integrasi Docker Compose dan panduan deployment |
| **1.5.0** | 2024-06-20 | Penambahan fitur export hasil dan dashboard analytics |
| **2.0.0** | 2024-09-27 | Major update dengan UI baru, security enhancements, dan performance improvements |

---

**© 2024 Waskita - Sistem Klasifikasi Konten Radikal Media Sosial**  
**Dikembangkan dengan ❤️ untuk Indonesia yang lebih aman di dunia digital**