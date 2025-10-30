# 🐳 PANDUAN SETUP DOCKER-FIRST WASKITA

Panduan setup sederhana untuk menjalankan aplikasi Waskita dengan Docker dalam satu langkah.

---

## 🚀 QUICK START (Rekomendasi)

### Setup Lengkap dengan Docker (5 Menit)
```bash
# 1. Clone repository
git clone https://github.com/shidayaturrohman19-dev/waskita-app.git
cd waskita-app

# 2. Setup environment
cp .env.example .env

# 3. Jalankan semua services (database, app, nginx)
docker-compose up -d

# 4. Tunggu hingga semua container ready (30-60 detik)
docker-compose logs -f

# 5. Akses aplikasi
# http://localhost:5000 (aplikasi langsung)
# http://localhost:80 (melalui nginx proxy)
```

**🎯 Login Default:**
- **Admin**: admin@waskita.com / admin123
- **User**: user@test.com / user123

**✅ SELESAI!** Aplikasi sudah siap digunakan dengan:
- ✅ Database PostgreSQL otomatis terkonfigurasi
- ✅ Admin user otomatis dibuat
- ✅ Sample data otomatis dimuat
- ✅ Semua dependencies terinstall
- ✅ Nginx reverse proxy aktif

---

## 🔧 KONFIGURASI ENVIRONMENT

### File .env (Opsional - Sudah ada default)
```bash
# Database (otomatis dibuat di Docker)
POSTGRES_DB=waskita_db
POSTGRES_USER=waskita_user
POSTGRES_PASSWORD=waskita_password123
DATABASE_URL=postgresql://waskita_user:waskita_password123@postgres:5432/waskita_db

# Application
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
WEB_PORT=5000

# Email OTP (opsional untuk development)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Redis (otomatis dikonfigurasi)
REDIS_URL=redis://redis:6379/0

# Docker Configuration
CREATE_SAMPLE_DATA=true
```

---

## 📋 PERINTAH DOCKER BERGUNA

### Manajemen Container
```bash
# Lihat status semua container
docker-compose ps

# Lihat logs aplikasi
docker-compose logs app

# Lihat logs database
docker-compose logs postgres

# Restart aplikasi
docker-compose restart app

# Stop semua services
docker-compose down

# Stop dan hapus semua data
docker-compose down -v
```

### Development Commands
```bash
# Masuk ke container aplikasi
docker-compose exec app bash

# Jalankan command di dalam container
docker-compose exec app python create_admin.py

# Update dependencies
docker-compose exec app pip install -r requirements.txt

# Rebuild container setelah perubahan code
docker-compose up --build
```

### Database Management
```bash
# Akses PostgreSQL
docker-compose exec postgres psql -U waskita_user -d waskita_db

# Backup database
docker-compose exec postgres pg_dump -U waskita_user waskita_db > backup.sql

# Restore database
docker-compose exec -T postgres psql -U waskita_user waskita_db < backup.sql
```

---

## 🔍 TROUBLESHOOTING

### Port Sudah Digunakan
```bash
# Cek port yang digunakan
netstat -tulpn | grep :5000
netstat -tulpn | grep :80

# Ganti port di docker-compose.yml
ports:
  - "5001:5000"  # Ganti 5000 ke 5001
```

### Container Tidak Bisa Start
```bash
# Lihat error logs
docker-compose logs

# Rebuild semua container
docker-compose down
docker-compose up --build

# Reset semua data
docker-compose down -v
docker system prune -f
docker-compose up --build
```

### Database Connection Error
```bash
# Pastikan PostgreSQL container running
docker-compose ps postgres

# Restart database
docker-compose restart postgres

# Cek database logs
docker-compose logs postgres
```

### Email OTP Tidak Terkirim
```bash
# Test email configuration
docker-compose exec app python -c "
from flask_mail import Mail, Message
from app import app
mail = Mail(app)
with app.app_context():
    msg = Message('Test', sender=app.config['MAIL_USERNAME'], recipients=['test@example.com'])
    msg.body = 'Test email'
    mail.send(msg)
    print('Email sent!')
"
```

---

## 🏗️ DEVELOPMENT WORKFLOW

### 1. Development dengan Hot Reload
```bash
# Clone dan setup
git clone https://github.com/shidayaturrohman19-dev/waskita-app.git
cd waskita-app

# Setup environment
cp .env.example .env

# Jalankan dengan volume mounting untuk hot reload
docker-compose -f docker-compose.dev.yml up
```

### 2. Testing
```bash
# Run unit tests
docker-compose exec app python -m pytest

# Run security tests
docker-compose exec app python run_security_tests.py

# Run performance tests
docker-compose exec app python -m pytest tests/test_performance.py
```

### 3. Production Deployment
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# Monitor production
docker-compose -f docker-compose.prod.yml logs -f
```

---

## 📊 MONITORING & HEALTH CHECK

### Health Check Endpoints
```bash
# Application health
curl http://localhost:5000/health

# Database health
docker-compose exec app python -c "
from app import db
try:
    db.engine.execute('SELECT 1')
    print('Database: OK')
except:
    print('Database: ERROR')
"

# Redis health
docker-compose exec redis redis-cli ping
```

### Performance Monitoring
```bash
# Container resource usage
docker stats

# Application metrics
curl http://localhost:5000/metrics

# Database performance
docker-compose exec postgres psql -U waskita_user -d waskita_db -c "
SELECT query, calls, total_time, mean_time 
FROM pg_stat_statements 
ORDER BY total_time DESC LIMIT 10;
"
```

---

## 🔒 KEAMANAN PRODUCTION

### Environment Variables Production
```bash
# Generate secure secrets
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
DB_PASSWORD=$(python -c "import secrets, string; print(''.join(secrets.choices(string.ascii_letters + string.digits, k=20)))")

# Update .env untuk production
echo "SECRET_KEY=$SECRET_KEY" >> .env.prod
echo "POSTGRES_PASSWORD=$DB_PASSWORD" >> .env.prod
echo "FLASK_ENV=production" >> .env.prod
```

### SSL/HTTPS Setup
```bash
# Generate SSL certificate
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365

# Update nginx configuration
# Edit nginx/nginx.conf untuk enable SSL
```

---

## 📚 DOKUMENTASI LANJUTAN

- **[🔒 Security Guide](SECURITY_COMPREHENSIVE_GUIDE.md)** - Panduan keamanan lengkap
- **[👤 User Guide](USER_GUIDE_LENGKAP.md)** - Panduan penggunaan aplikasi
- **[📡 API Documentation](API_DOCUMENTATION.md)** - Dokumentasi API endpoints
- **[🚀 Deployment Guide](DEPLOYMENT_GUIDE.md)** - Panduan deployment production

---

## 📚 PANDUAN PENGGUNA LENGKAP

### 🎯 Dashboard Utama

#### Statistik Real-time
Dashboard menampilkan 4 metrik utama:
- **📤 Data Upload**: Total data yang diupload manual
- **🕷️ Data Scraping**: Total data dari web scraping  
- **🧹 Data Cleaned**: Total data yang sudah dibersihkan
- **🧠 Terklasifikasi**: Total data yang sudah diklasifikasi

#### Quick Actions
- **Upload Data**: Upload file CSV/XLSX
- **Scraping Data**: Scraping dari media sosial
- **Kelola Dataset**: Manajemen dataset
- **Klasifikasi**: Klasifikasi konten AI

#### Status Sistem
- **Word2Vec Model**: Status model embedding
- **Naive Bayes Models**: Status 3 model klasifikasi (x/3)
- **Database Connection**: Status koneksi database

### 📊 Fitur Utama

#### 1. 📤 Upload Dataset

**Format File yang Didukung:**
- **CSV**: Dengan encoding UTF-8, UTF-8-BOM, Latin1
- **Excel**: Format .xlsx dan .xls
- **Kolom Wajib**: `content` (berisi teks yang akan diklasifikasi)
- **Kolom Opsional**: `username`, `url`, `platform`

**Langkah Upload:**
1. Dashboard → Upload Data
2. Pilih file dan upload
3. Sistem otomatis validasi format dan duplikasi
4. Review data preview sebelum konfirmasi
5. Data disimpan dengan timestamp

**Validasi Keamanan:**
- File size maksimal 50MB
- MIME type validation
- Content scan untuk malware
- Duplicate check otomatis

#### 2. 🕷️ Web Scraping

**Platform yang Didukung:**
- Twitter/X, Facebook, Instagram, TikTok

**Setup Scraping:**
1. Dapatkan Apify API token
2. Tambahkan `APIFY_API_TOKEN` ke `.env`
3. Pilih platform dan input keyword
4. Set parameters (jumlah data, rentang tanggal)
5. Monitor progress real-time

#### 3. 🧹 Data Cleaning

**Proses Otomatis:**
- Remove emoji, URLs, mentions, hashtags
- Clean special characters dan angka
- Normalize text (lowercase, trim)
- Indonesian stopwords removal
- Tokenization untuk Word2Vec

#### 4. 🧠 Klasifikasi AI

**Model Machine Learning:**
- **Word2Vec**: Model embedding 300 dimensi
- **3 Naive Bayes Models**: Untuk validasi silang

**Proses Klasifikasi:**
1. Pilih dataset yang sudah dibersihkan
2. Pilih model yang akan digunakan
3. Batch process otomatis
4. Monitor progress real-time
5. Review hasil dengan probabilitas

**Output Klasifikasi:**
- Prediksi: Radikal / Non-Radikal
- Probabilitas untuk setiap kategori
- Confidence score model

#### 5. 📁 Export Hasil

**Format Export:**
- CSV dan Excel (.xlsx)
- Include: teks asli, hasil klasifikasi, probabilitas semua model

#### 6. 📈 Dataset Management

**Fitur Management:**
- Create dataset baru
- View details (raw, cleaned, classified)
- Statistics lengkap per dataset
- Delete dataset beserta data terkait

### 🔐 Keamanan & Autentikasi

#### Sistem OTP Email
- Registrasi dengan verifikasi email OTP 6 digit
- OTP berlaku 10 menit
- Admin approval untuk user baru

#### Role-Based Access
- **Admin**: Akses penuh + approve user baru
- **User**: Akses fitur klasifikasi dan data management
- **Security**: Rate limiting 500 request/hari, 200/jam

#### Fitur Keamanan
- CSRF Protection
- Input validation dan sanitasi
- File upload security dengan virus scan
- Security headers otomatis
- Activity logging

### 📱 Antarmuka Pengguna

#### Responsive Design
- Desktop: Layout penuh dengan sidebar
- Tablet: Layout adaptif dengan collapsible menu
- Mobile: Layout mobile-first dengan bottom navigation

#### Accessibility
- Screen reader support dengan ARIA labels
- Keyboard navigation penuh
- High contrast mode
- Font scaling hingga 200%

#### Modern UI Features
- Real-time updates dengan progress bars
- Interactive charts dengan Chart.js
- Modal dialogs untuk detail data
- Toast notifications yang elegant

### 💡 Tips Penggunaan

#### Workflow Optimal
1. **Setup**: Login → Check model status di dashboard
2. **Data Input**: Upload dataset ATAU scraping dari media sosial
3. **Preprocessing**: Otomatis cleaning saat upload/scraping
4. **Classification**: Pilih dataset → Run klasifikasi
5. **Analysis**: Review hasil di dashboard dan dataset details
6. **Export**: Download hasil untuk analisis lanjutan

#### Best Practices
- **Dataset Size**: Optimal 100-10,000 data per batch
- **Keyword Scraping**: Gunakan keyword spesifik untuk hasil relevan
- **Model Validation**: Gunakan 3 model untuk validasi silang
- **Regular Backup**: Export hasil secara berkala
- **Monitor Resources**: Check RAM usage saat proses besar

#### Interpretasi Hasil
- **Probabilitas > 70%**: Prediksi sangat yakin
- **Probabilitas 50-70%**: Prediksi cukup yakin
- **Probabilitas < 50%**: Prediksi kurang yakin, perlu review manual
- **Konsensus Model**: Jika 2-3 model setuju, hasil lebih akurat

---

## 🚀 DEPLOYMENT PRODUKSI

### Persyaratan Sistem Produksi

#### Minimum Requirements
- **CPU**: 2 cores (4 cores recommended)
- **RAM**: 4GB (8GB recommended untuk ML models)
- **Storage**: 20GB SSD (50GB recommended)
- **OS**: Ubuntu 20.04+ / CentOS 8+ / Debian 11+

#### Software Dependencies
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Nginx**: 1.18+ (untuk reverse proxy)
- **PostgreSQL**: 13+ (recommended) atau MySQL 8.0+
- **Redis**: 6.0+ (untuk caching dan sessions)

### Production Docker Setup

#### 1. Persiapan Server
```bash
# Update system
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git unzip

# Install Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create application directory
sudo mkdir -p /opt/waskita
sudo chown $USER:$USER /opt/waskita
cd /opt/waskita
```

#### 2. Clone dan Setup
```bash
# Clone repository
git clone https://github.com/your-org/waskita.git .

# Copy production environment
cp .env.example .env.production

# Edit production environment
nano .env.production
```

#### 3. Production Environment Variables
```bash
# Database Configuration
DATABASE_URL=postgresql://waskita_user:SECURE_PASSWORD@db:5432/waskita_prod
REDIS_URL=redis://:REDIS_PASSWORD@redis:6379/0

# Security
SECRET_KEY=your-super-secure-secret-key-here
FLASK_ENV=production
DEBUG=False

# Email Configuration (untuk OTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# API Keys
APIFY_API_TOKEN=your-apify-token

# Security Headers
SECURITY_HEADERS=True
RATE_LIMITING=True
```

#### 4. Production Docker Compose
Buat file `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
    container_name: waskita_app
    restart: unless-stopped
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://waskita_user:${DB_PASSWORD}@db:5432/waskita_prod
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
      - ./models:/app/models
    depends_on:
      - db
      - redis
    networks:
      - waskita_network

  db:
    image: postgres:14-alpine
    container_name: waskita_db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=waskita_prod
      - POSTGRES_USER=waskita_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    networks:
      - waskita_network

  redis:
    image: redis:7-alpine
    container_name: waskita_redis
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - waskita_network

  nginx:
    image: nginx:alpine
    container_name: waskita_nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    networks:
      - waskita_network

volumes:
  postgres_data:
  redis_data:

networks:
  waskita_network:
    driver: bridge
```

#### 5. Deploy ke Produksi
```bash
# Build dan start services
docker-compose -f docker-compose.prod.yml up -d --build

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f app
```

### SSL/TLS Configuration

#### 1. Install Certbot (Let's Encrypt)
```bash
sudo apt install -y certbot python3-certbot-nginx

# Generate SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

#### 2. Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://app:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Monitoring & Maintenance

#### 1. Health Checks
```bash
# Check application health
curl -f http://localhost/health || exit 1

# Check database connection
docker-compose -f docker-compose.prod.yml exec db pg_isready

# Check Redis
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping
```

#### 2. Backup Strategy
```bash
# Database backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U waskita_user waskita_prod > backup_$(date +%Y%m%d_%H%M%S).sql

# Files backup
tar -czf uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz uploads/
```

#### 3. Log Management
```bash
# View application logs
docker-compose -f docker-compose.prod.yml logs -f app

# Rotate logs (add to crontab)
0 2 * * * docker-compose -f /opt/waskita/docker-compose.prod.yml exec app logrotate /etc/logrotate.conf
```

### Security Hardening

#### 1. Firewall Configuration
```bash
# UFW (Ubuntu)
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Fail2ban untuk SSH protection
sudo apt install -y fail2ban
```

#### 2. Docker Security
```bash
# Run containers as non-root user
# Set resource limits
# Use secrets for sensitive data
# Regular security updates
```

#### 3. Application Security
- Change default admin credentials immediately
- Enable rate limiting
- Configure CSRF protection
- Set secure session cookies
- Use HTTPS only
- Regular security audits

### Performance Optimization

#### 1. Database Optimization
```sql
-- PostgreSQL tuning
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
SELECT pg_reload_conf();
```

#### 2. Redis Configuration
```bash
# Redis memory optimization
maxmemory 512mb
maxmemory-policy allkeys-lru
```

#### 3. Application Tuning
- Enable gzip compression
- Use CDN untuk static files
- Database connection pooling
- Caching strategies
- Async processing untuk heavy tasks

---

Jika mengalami masalah:
1. **Cek logs**: `docker-compose logs`
2. **Restart services**: `docker-compose restart`
3. **Reset environment**: `docker-compose down -v && docker-compose up --build`
4. **GitHub Issues**: Laporkan bug atau request fitur

---

**💡 TIP**: Gunakan Docker Desktop untuk GUI management yang lebih mudah di Windows/Mac.