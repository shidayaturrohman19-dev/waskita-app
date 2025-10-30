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

## 🆘 SUPPORT

Jika mengalami masalah:
1. **Cek logs**: `docker-compose logs`
2. **Restart services**: `docker-compose restart`
3. **Reset environment**: `docker-compose down -v && docker-compose up --build`
4. **GitHub Issues**: Laporkan bug atau request fitur

---

**💡 TIP**: Gunakan Docker Desktop untuk GUI management yang lebih mudah di Windows/Mac.