# 🐳 Panduan Export dan Copy Docker Waskita ke Komputer Lain

## 📋 Daftar Isi
1. [Persiapan Export](#persiapan-export)
2. [Export Docker Image](#export-docker-image)
3. [Export Docker Compose dan File Pendukung](#export-docker-compose-dan-file-pendukung)
4. [Transfer ke Komputer Lain](#transfer-ke-komputer-lain)
5. [Import dan Setup di Komputer Tujuan](#import-dan-setup-di-komputer-tujuan)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Persiapan Export

### 1. Pastikan Docker Berjalan dengan Baik
```bash
# Cek status container
docker ps

# Cek image yang tersedia
docker images
```

### 2. Stop Container (Opsional)
```bash
# Stop semua container jika diperlukan
docker-compose down
```

---

## 📦 Export Docker Image

### Metode 1: Export Image Waskita Saja
```bash
# Export image utama aplikasi
docker save -o waskita-app-latest.tar waskita-app:latest

# Cek ukuran file
dir waskita-app-latest.tar
```

### Metode 2: Export Semua Image yang Diperlukan
```bash
# Export semua image sekaligus
docker save -o waskita-complete.tar waskita-app:latest postgres:15 nginx:alpine redis:7-alpine

# Atau export satu per satu
docker save -o waskita-app.tar waskita-app:latest
docker save -o postgres-15.tar postgres:15
docker save -o nginx-alpine.tar nginx:alpine
docker save -o redis-7-alpine.tar redis:7-alpine
```

### Metode 3: Export dengan Kompresi (Recommended)
```bash
# Export dengan kompresi gzip untuk menghemat space
docker save waskita-app:latest | gzip > waskita-app-latest.tar.gz
docker save postgres:15 | gzip > postgres-15.tar.gz
docker save nginx:alpine | gzip > nginx-alpine.tar.gz
docker save redis:7-alpine | gzip > redis-7-alpine.tar.gz
```

---

## 📁 Export Docker Compose dan File Pendukung

### 1. Buat Folder Export
```bash
# Buat folder untuk export
mkdir waskita-export
cd waskita-export
```

### 2. Copy File-file Penting
```bash
# Copy file konfigurasi
copy ..\docker-compose.yml .
copy ..\Dockerfile .
copy ..\.env.example .
copy ..\nginx.conf .
copy ..\requirements.txt .

# Copy folder penting
xcopy ..\static static\ /E /I
xcopy ..\templates templates\ /E /I
xcopy ..\migrations migrations\ /E /I

# Copy file aplikasi
copy ..\app.py .
copy ..\routes.py .
copy ..\models.py .
copy ..\config.py .
copy ..\utils.py .
copy ..\scheduler.py .
```

### 3. Buat Script Setup Otomatis
Buat file `setup.bat`:
```batch
@echo off
echo ========================================
echo    WASKITA DOCKER SETUP SCRIPT
echo ========================================

echo [1/5] Loading Docker Images...
docker load -i waskita-app-latest.tar.gz
docker load -i postgres-15.tar.gz
docker load -i nginx-alpine.tar.gz
docker load -i redis-7-alpine.tar.gz

echo [2/5] Creating .env file...
copy .env.example .env

echo [3/5] Creating necessary directories...
mkdir uploads
mkdir logs
mkdir data
mkdir ssl

echo [4/5] Starting Docker Compose...
docker-compose up -d

echo [5/5] Checking container status...
timeout /t 10
docker ps

echo ========================================
echo    SETUP COMPLETED!
echo    Access: http://localhost:5000
echo ========================================
pause
```

---

## 💾 Transfer ke Komputer Lain

### Metode 1: USB/External Drive
```bash
# Copy semua file ke USB
xcopy waskita-export E:\waskita-backup\ /E /I
xcopy *.tar.gz E:\waskita-backup\
```

### Metode 2: Network Share
```bash
# Copy ke network drive
xcopy waskita-export \\server\share\waskita-backup\ /E /I
xcopy *.tar.gz \\server\share\waskita-backup\
```

### Metode 3: Cloud Storage (Google Drive, OneDrive, dll)
1. Upload folder `waskita-export` dan file `.tar.gz` ke cloud storage
2. Download di komputer tujuan

---

## 🔧 Import dan Setup di Komputer Tujuan

### 1. Persiapan Komputer Tujuan
```bash
# Install Docker Desktop (jika belum ada)
# Download dari: https://www.docker.com/products/docker-desktop

# Pastikan Docker berjalan
docker --version
docker-compose --version
```

### 2. Import Docker Images

#### Jika menggunakan file terkompresi:
```bash
# Load image dari file .tar.gz
docker load -i waskita-app-latest.tar.gz
docker load -i postgres-15.tar.gz
docker load -i nginx-alpine.tar.gz
docker load -i redis-7-alpine.tar.gz
```

#### Jika menggunakan file .tar biasa:
```bash
# Load image dari file .tar
docker load -i waskita-app-latest.tar
docker load -i postgres-15.tar
docker load -i nginx-alpine.tar
docker load -i redis-7-alpine.tar
```

### 3. Setup Aplikasi
```bash
# Masuk ke folder waskita-export
cd waskita-export

# Copy .env.example ke .env dan edit sesuai kebutuhan
copy .env.example .env
notepad .env

# Buat folder yang diperlukan
mkdir uploads
mkdir logs
mkdir data
mkdir ssl

# Jalankan aplikasi
docker-compose up -d
```

### 4. Verifikasi Setup
```bash
# Cek container berjalan
docker ps

# Cek logs jika ada masalah
docker-compose logs

# Test akses aplikasi
# Buka browser: http://localhost:5000
```

---

## 🛠️ Troubleshooting

### Problem 1: Port Sudah Digunakan
```bash
# Cek port yang digunakan
netstat -an | findstr :5000
netstat -an | findstr :80
netstat -an | findstr :5432

# Solusi: Ubah port di docker-compose.yml
# Contoh: "5001:5000" untuk port 5001
```

### Problem 2: Image Tidak Ditemukan
```bash
# Cek image yang ter-load
docker images

# Load ulang jika perlu
docker load -i waskita-app-latest.tar.gz
```

### Problem 3: Database Connection Error
```bash
# Cek container database
docker logs waskita_db

# Restart database
docker-compose restart db

# Cek environment variables
docker exec waskita_app env | grep DATABASE
```

### Problem 4: Permission Error (Linux/Mac)
```bash
# Set permission untuk folder
chmod -R 755 uploads/
chmod -R 755 logs/
chmod -R 755 static/
```

---

## 📝 Checklist Export/Import

### ✅ Checklist Export:
- [ ] Docker images ter-export dengan baik
- [ ] File docker-compose.yml tersedia
- [ ] File .env.example tersedia
- [ ] Folder static dan templates ter-copy
- [ ] File aplikasi utama ter-copy
- [ ] Script setup.bat dibuat
- [ ] Semua file ter-compress/ter-archive

### ✅ Checklist Import:
- [ ] Docker Desktop terinstall di komputer tujuan
- [ ] Semua image ter-load dengan sukses
- [ ] File .env dikonfigurasi dengan benar
- [ ] Folder uploads, logs, data dibuat
- [ ] docker-compose up berjalan tanpa error
- [ ] Aplikasi dapat diakses di browser
- [ ] Database connection berfungsi
- [ ] Upload file berfungsi normal

---

## 🎯 Tips Optimasi

### 1. Mengurangi Ukuran Export
```bash
# Hapus cache dan temporary files sebelum export
docker system prune -f

# Export hanya layer yang diperlukan
docker save waskita-app:latest | gzip -9 > waskita-app-optimized.tar.gz
```

### 2. Backup Data
```bash
# Backup database jika ada data penting
docker exec waskita_db pg_dump -U waskita_user waskita_prod > backup.sql

# Backup uploads folder
xcopy uploads uploads-backup\ /E /I
```

### 3. Automated Backup Script
Buat file `backup.bat`:
```batch
@echo off
set BACKUP_DATE=%date:~-4,4%%date:~-10,2%%date:~-7,2%
set BACKUP_DIR=waskita-backup-%BACKUP_DATE%

mkdir %BACKUP_DIR%
docker save waskita-app:latest | gzip > %BACKUP_DIR%\waskita-app.tar.gz
xcopy docker-compose.yml %BACKUP_DIR%\
xcopy .env.example %BACKUP_DIR%\
xcopy uploads %BACKUP_DIR%\uploads\ /E /I

echo Backup completed: %BACKUP_DIR%
```

---

## 🔐 Keamanan

### 1. Jangan Export File Sensitif
- Jangan sertakan file `.env` dengan password asli
- Gunakan `.env.example` sebagai template
- Hapus file log yang berisi informasi sensitif

### 2. Enkripsi File Export (Opsional)
```bash
# Encrypt file dengan 7-Zip
7z a -p waskita-encrypted.7z waskita-export\
```

---

**📞 Support:** Jika mengalami masalah, periksa log container dengan `docker-compose logs` atau hubungi administrator sistem.