# Waskita - Docker Deployment Guide

## Panduan Deployment Aplikasi Waskita dengan Docker

### Prasyarat
- Docker dan Docker Compose terinstall
- Port 80, 5000, 5432, dan 6379 tersedia

### Cara Deployment

1. **Clone repository dan masuk ke direktori**
   ```bash
   git clone <repository-url>
   cd Waskita
   ```

2. **Build dan jalankan dengan Docker Compose**
   ```bash
   docker-compose up -d --build
   ```

3. **Akses aplikasi**
   - URL: http://localhost
   - Aplikasi akan otomatis membuat user admin saat pertama kali dijalankan

### Kredensial Login Default

#### Admin User
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@waskita.com`
- **Role**: Administrator (akses penuh)

#### Test User
- **Username**: `testuser`
- **Password**: `test123`
- **Email**: `test@waskita.com`
- **Role**: User biasa

### Fitur Admin
Sebagai admin, Anda dapat:
- Mengelola semua dataset dan data
- Mengakses panel admin
- Melihat aktivitas semua pengguna
- Mengelola user lain
- Mengakses semua fitur klasifikasi

### Fitur User Biasa
Sebagai user biasa, Anda dapat:
- Upload dan scraping data
- Membersihkan data
- Melakukan klasifikasi
- Melihat hasil klasifikasi sendiri

### Services yang Berjalan

1. **waskita_app** - Aplikasi Flask utama (Port 5000)
2. **waskita_nginx** - Web server Nginx (Port 80)
3. **waskita_db** - Database PostgreSQL (Port 5432)
4. **waskita_redis** - Cache Redis (Port 6379)

### Perintah Docker Berguna

```bash
# Melihat status container
docker ps

# Melihat logs aplikasi
docker logs waskita_app

# Restart aplikasi
docker-compose restart web

# Stop semua services
docker-compose down

# Rebuild dan restart
docker-compose up -d --build
```

### Troubleshooting

#### Jika tidak bisa login:
1. Pastikan semua container berjalan: `docker ps`
2. Cek logs aplikasi: `docker logs waskita_app`
3. Restart container: `docker-compose restart web`

#### Jika admin user tidak ada:
```bash
# Jalankan script manual
docker exec -it waskita_app python create_admin.py
```

#### Reset database:
```bash
docker-compose down -v
docker-compose up -d --build
```

### Keamanan

⚠️ **PENTING**: Ganti password default setelah login pertama!

1. Login sebagai admin
2. Masuk ke Profile/Settings
3. Ganti password default
4. Update email jika diperlukan

### Konfigurasi Tambahan

File konfigurasi utama:
- `.env.docker` - Environment variables untuk Docker
- `docker-compose.yml` - Konfigurasi services
- `nginx.conf` - Konfigurasi web server

### Support

Jika mengalami masalah:
1. Cek logs: `docker logs waskita_app`
2. Pastikan semua port tersedia
3. Restart services: `docker-compose restart`

---

**Waskita Application** - Sistem Klasifikasi Konten Radikal
Dikembangkan dengan Flask, PostgreSQL, Redis, dan Nginx