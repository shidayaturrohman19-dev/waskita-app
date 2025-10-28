# PANDUAN PENGGUNA WASKITA

**Tujuan**: Dokumen ini memberikan instruksi lengkap untuk membantu pengguna akhir memahami dan menggunakan Waskita secara efisien. Panduan ini mencakup deskripsi fitur utama, prosedur penyiapan, panduan penggunaan, tips pemecahan masalah, dan informasi dukungan.

## 1. Perkenalan

Waskita adalah sistem berbasis web yang dirancang untuk mengklasifikasikan konten media sosial sebagai **Radikal** atau **Non-Radikal** menggunakan teknologi Machine Learning. Aplikasi ini menggunakan algoritma Naive Bayes yang telah dilatih dengan dataset khusus untuk mendeteksi konten radikal dengan tingkat akurasi tinggi.

Panduan ini bertujuan untuk memandu Anda melalui proses instalasi, penggunaan, dan pemeliharaan sistem Waskita secara menyeluruh.

## 2. Persyaratan Sistem

Sebelum menginstal dan menggunakan Waskita, pastikan komputer atau server Anda memenuhi persyaratan sistem berikut:

• **Sistem Operasi**: Windows 10/11, macOS 10.15+, atau Ubuntu 18.04+
• **Python**: Versi 3.11.x SAJA (TIDAK mendukung versi 3.12/3.13 karena masalah kompatibilitas dengan Gensim)
• **RAM**: Minimal 4GB (Direkomendasikan: 8GB atau lebih)
• **Penyimpanan**: Minimal 2GB ruang kosong
• **Docker**: Docker Desktop 4.0 atau lebih baru
• **Browser**: Chrome 90+, Firefox 88+, Safari 14+
## 3. Petunjuk Instalasi

Pada bagian ini, kami akan menjelaskan cara menginstal dan menyiapkan aplikasi Waskita pada sistem Anda. Terdapat dua metode instalasi yang dapat Anda pilih sesuai dengan kebutuhan dan kemampuan teknis Anda.

Waskita dapat diinstal dan dijalankan dengan dua cara: menggunakan Docker (direkomendasikan) atau instalasi lokal. Docker menyederhanakan proses instalasi dan menghindari masalah kompatibilitas, sementara instalasi lokal memberikan fleksibilitas lebih untuk pengembangan.

### **Instalasi dengan Docker (Direkomendasikan):**

Metode ini sangat disarankan karena lebih sederhana dan menghindari masalah kompatibilitas antar sistem:

1. Unduh paket instalasi dari [repository Waskita](https://github.com/username/waskita).
2. Buka terminal atau command prompt dan jalankan perintah `git clone https://github.com/username/waskita.git`.
3. Masuk ke direktori proyek dengan perintah `cd waskita`.
4. Salin file konfigurasi dengan perintah `cp .env.example .env.docker` dan sesuaikan pengaturan jika diperlukan.
5. Jalankan perintah `docker-compose up -d --build` untuk membangun dan menjalankan aplikasi.
6. Akses aplikasi di browser melalui alamat `http://localhost:5000`.

### **Instalasi Lokal:**

Metode ini cocok untuk pengembang atau pengguna yang ingin melakukan kustomisasi lebih lanjut:

1. Unduh paket instalasi dari [repository Waskita](https://github.com/username/waskita).
2. Buka terminal atau command prompt dan jalankan perintah `git clone https://github.com/username/waskita.git`.
3. Masuk ke direktori proyek dengan perintah `cd waskita`.
4. Buat virtual environment dengan perintah `python -m venv venv` dan aktifkan.
5. Instal semua dependensi dengan perintah `pip install -r requirements.txt`.
6. Salin file konfigurasi dengan perintah `cp .env.example .env.local` dan sesuaikan pengaturan.
7. Jalankan aplikasi dengan perintah `python app.py`.

## 4. Memulai

Setelah berhasil menginstal aplikasi Waskita, bagian ini akan memandu Anda untuk mulai menggunakan sistem. Ikuti langkah-langkah berikut untuk memulai penggunaan aplikasi:

1. **Menjalankan Aplikasi**: Luncurkan aplikasi dengan menjalankan perintah `docker-compose up -d --build` (jika menggunakan Docker) atau `python app.py` (jika instalasi lokal).
2. **Autentikasi**: Masuk dengan kredensial Anda jika sudah memiliki akun, atau daftar sebagai pengguna baru melalui halaman registrasi.
3. **Konfigurasi Awal**: Ikuti panduan penyiapan untuk mengonfigurasi preferensi awal sesuai kebutuhan Anda.
## 5. Ikhtisar Fitur

Aplikasi Waskita menyediakan berbagai fitur canggih untuk membantu Anda mengklasifikasikan konten media sosial. Berikut adalah fitur-fitur utama yang tersedia dalam sistem:

• **Upload Dataset**: Mengimpor data dari file CSV/XLSX untuk dianalisis
• **Web Scraping**: Secara otomatis mengambil data dari berbagai platform media sosial
• **Data Cleaning**: Pembersihan otomatis konten (emoji, tautan, karakter khusus)
• **Klasifikasi AI**: Menggunakan 3 model Naive Bayes untuk mencapai akurasi tinggi
• **Analisis Probabilitas**: Menampilkan tingkat kepercayaan klasifikasi (0-100%)
• **Export Hasil**: Mengunduh hasil analisis dalam format CSV/Excel
• **Multi-User**: Sistem berbasis peran (Admin & User) untuk manajemen akses
• **Dark/Light Mode**: Antarmuka yang dapat disesuaikan sesuai preferensi pengguna

## 6. Petunjuk Penggunaan

Bagian ini menjelaskan langkah-langkah terperinci untuk menggunakan fitur-fitur utama aplikasi Waskita. Ikuti panduan ini untuk memaksimalkan penggunaan sistem.

### **Upload Dataset**

Fitur ini memungkinkan Anda mengimpor data dari file CSV atau XLSX untuk dianalisis oleh sistem:

1. **Persiapan File**: Pastikan file Anda dalam format CSV atau XLSX dan memiliki kolom `content` yang berisi teks yang akan dianalisis.
2. **Proses Upload**: Buka menu `Data Management` → `Upload Dataset`, pilih file dari komputer Anda, beri nama dataset, dan klik tombol `Upload`.
3. **Validasi Data**: Sistem akan secara otomatis memvalidasi format file dan mendeteksi duplikasi data sebelum mengimpor.

### **Web Scraping**

Fitur ini memungkinkan Anda mengumpulkan data secara otomatis dari berbagai platform media sosial:

1. **Setup Scraping**: Buka menu `Data Management` → `Web Scraping`, pilih platform (Twitter, Facebook, dll.), masukkan kata kunci pencarian, atur rentang tanggal, dan tentukan jumlah maksimal data.
2. **Mulai Scraping**: Klik tombol `Start Scraping` untuk memulai proses pengambilan data.
3. **Monitoring**: Pantau kemajuan dan hasil scraping secara real-time melalui indikator progres yang ditampilkan.

### **Data Cleaning**

Fitur ini membersihkan data mentah agar siap untuk proses klasifikasi:

1. **Akses Data Cleaning**: Buka menu `Data Management` → `Clean Data` dan pilih dataset yang ingin dibersihkan.
2. **Proses Otomatis**: Sistem akan secara otomatis membersihkan emoji, URL, mention, dan karakter khusus dari teks.
3. **Terapkan Perubahan**: Klik tombol `Apply Cleaning` untuk menyimpan data yang sudah dibersihkan ke dalam sistem.

### **Klasifikasi**

Fitur ini menganalisis data yang telah dibersihkan untuk mengklasifikasikannya sebagai Radikal atau Non-Radikal:

1. **Pilih Data**: Buka menu `Classification` → `Classify Data` dan pilih data yang sudah dibersihkan.
2. **Mulai Klasifikasi**: Klik tombol `Start Classification` untuk memulai proses analisis.
3. **Lihat Hasil**: Hasil klasifikasi akan ditampilkan dalam bentuk tabel beserta tingkat probabilitas untuk setiap entri data.
## 7. Panduan Mengatasi Masalah

Dalam penggunaan aplikasi Waskita, Anda mungkin mengalami beberapa kendala teknis. Bagian ini menyediakan solusi untuk masalah umum yang mungkin Anda hadapi. Jika Anda mengalami masalah, silakan periksa tabel di bawah ini untuk menemukan kemungkinan penyebab dan solusinya:

| Masalah | Penyebab | Solusi |
| --- | --- | --- |
| Gagal login | Password salah | Periksa kembali password Anda atau gunakan fitur lupa password untuk mengatur ulang. |
| Upload gagal | Format file salah | Pastikan file dalam format CSV atau XLSX dan memiliki struktur kolom yang benar. |
| Scraping error | Koneksi internet terputus | Periksa koneksi internet Anda dan coba lagi setelah koneksi stabil. |
| Klasifikasi lambat | Dataset terlalu besar | Gunakan dataset yang lebih kecil atau pecah menjadi beberapa bagian untuk pemrosesan lebih cepat. |

## 8. Pertanyaan yang Sering Diajukan (FAQ)

Berikut adalah jawaban untuk pertanyaan yang sering diajukan oleh pengguna Waskita. Jika pertanyaan Anda tidak terjawab di sini, silakan hubungi tim dukungan kami.

• **Apakah aplikasi ini gratis?**
  Ya, Waskita adalah aplikasi open-source yang dapat digunakan secara gratis. Anda dapat mengunduh, menginstal, dan menggunakan semua fiturnya tanpa biaya.

• **Berapa akurasi model klasifikasi?**
  Akurasi model berkisar antara 85-92% tergantung pada jenis konten dan kualitas data pelatihan. Sistem menggunakan tiga model Naive Bayes independen untuk meningkatkan akurasi melalui voting mayoritas.

• **Bisakah menambah platform scraping lain?**
  Ya, sistem dirancang secara modular sehingga memungkinkan untuk menambahkan platform media sosial baru dengan mudah. Pengembang dapat mengintegrasikan API baru ke dalam sistem yang ada.

• **Apakah data aman dan privat?**
  Ya, semua data disimpan secara lokal di server Anda dan tidak dikirim ke pihak ketiga. Waskita memprioritaskan keamanan dan privasi data pengguna.

## 9. Dukungan dan Kontak

Jika Anda memerlukan bantuan lebih lanjut atau memiliki pertanyaan yang tidak terjawab dalam panduan ini, silakan hubungi tim dukungan kami melalui:

• **Email**: support@waskita.com
• **Situs Web**: https://github.com/waskita
• **Forum Komunitas**: Bergabunglah dengan forum diskusi kami untuk berbagi pengalaman dan mendapatkan bantuan dari pengguna lain.

## 10. Riwayat Revisi

Tabel di bawah ini mencatat perubahan yang dilakukan pada aplikasi Waskita dari waktu ke waktu. Pastikan Anda selalu menggunakan versi terbaru untuk mendapatkan fitur dan perbaikan keamanan terkini.

| Versi | Tanggal | Perubahan |
| --- | --- | --- |
| 1.0.0 | 2024-05-20 | Rilis awal aplikasi dengan fitur dasar klasifikasi konten. |