# 🚀 PANDUAN DEPLOYMENT PRODUCTION - APLIKASI WASKITA

**Versi:** Production Ready v2.0  
**Tanggal:** Januari 2025  
**Status:** Enterprise-Level Security ✅  
**Target Environment:** Production Server

---

## 📋 DAFTAR ISI

1. [Persyaratan Sistem](#persyaratan-sistem)
2. [Persiapan Environment](#persiapan-environment)
3. [Konfigurasi Database](#konfigurasi-database)
4. [Deployment dengan Docker](#deployment-dengan-docker)
5. [Konfigurasi Web Server](#konfigurasi-web-server)
6. [SSL/TLS Setup](#ssltls-setup)
7. [Monitoring & Logging](#monitoring--logging)
8. [Backup & Recovery](#backup--recovery)
9. [Security Hardening](#security-hardening)
10. [Performance Optimization](#performance-optimization)
11. [Troubleshooting](#troubleshooting)

---

## 🖥️ PERSYARATAN SISTEM

### **Minimum Requirements:**
- **OS:** Ubuntu 20.04 LTS / CentOS 8 / RHEL 8
- **CPU:** 4 cores (2.4 GHz)
- **RAM:** 8 GB
- **Storage:** 100 GB SSD
- **Network:** 1 Gbps

### **Recommended Requirements:**
- **OS:** Ubuntu 22.04 LTS
- **CPU:** 8 cores (3.0 GHz)
- **RAM:** 16 GB
- **Storage:** 200 GB NVMe SSD
- **Network:** 10 Gbps

### **Software Dependencies:**
```bash
# Core Requirements
- Docker 24.0+
- Docker Compose 2.20+
- Nginx 1.20+
- PostgreSQL 14+ / MySQL 8.0+
- Redis 7.0+
- Python 3.9+

# Optional (Recommended)
- Certbot (Let's Encrypt)
- Prometheus + Grafana
- ELK Stack (Elasticsearch, Logstash, Kibana)
```

---

## 🔧 PERSIAPAN ENVIRONMENT

### **1. Update System**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git unzip

# CentOS/RHEL
sudo yum update -y
sudo yum install -y curl wget git unzip
```

### **2. Install Docker & Docker Compose**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### **3. Create Application Directory**
```bash
sudo mkdir -p /opt/waskita
sudo chown $USER:$USER /opt/waskita
cd /opt/waskita
```

### **4. Clone Repository**
```bash
git clone https://github.com/your-org/waskita.git .
# atau upload files secara manual
```

---

## 🗄️ KONFIGURASI DATABASE

### **Option 1: PostgreSQL (Recommended)**

#### **Install PostgreSQL:**
```bash
# Ubuntu/Debian
sudo apt install -y postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install -y postgresql-server postgresql-contrib
sudo postgresql-setup initdb
```

#### **Configure PostgreSQL:**
```bash
sudo -u postgres psql

-- Create database and user
CREATE DATABASE waskita_prod;
CREATE USER waskita_user WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE waskita_prod TO waskita_user;
ALTER USER waskita_user CREATEDB;
\q
```

#### **Security Configuration:**
```bash
# Edit postgresql.conf
sudo nano /etc/postgresql/14/main/postgresql.conf

# Add/modify these settings:
listen_addresses = 'localhost'
port = 5432
max_connections = 200
shared_buffers = 256MB
effective_cache_size = 1GB

# Edit pg_hba.conf
sudo nano /etc/postgresql/14/main/pg_hba.conf

# Add this line for application access:
local   waskita_prod    waskita_user                    md5
host    waskita_prod    waskita_user    127.0.0.1/32    md5
```

### **Option 2: MySQL (Alternative)**

#### **Install MySQL:**
```bash
# Ubuntu/Debian
sudo apt install -y mysql-server

# CentOS/RHEL
sudo yum install -y mysql-server
sudo systemctl start mysqld
sudo mysql_secure_installation
```

#### **Configure MySQL:**
```sql
-- Login to MySQL
sudo mysql -u root -p

-- Create database and user
CREATE DATABASE waskita_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'waskita_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON waskita_prod.* TO 'waskita_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## 🐳 DEPLOYMENT DENGAN DOCKER

### **1. Production Docker Compose**

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
      - DATABASE_URL=postgresql://waskita_user:your_secure_password@db:5432/waskita_prod
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - APIFY_API_TOKEN=${APIFY_API_TOKEN}
      - MAIL_SERVER=${MAIL_SERVER}
      - MAIL_PORT=${MAIL_PORT}
      - MAIL_USERNAME=${MAIL_USERNAME}
      - MAIL_PASSWORD=${MAIL_PASSWORD}
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
      - POSTGRES_PASSWORD=your_secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    networks:
      - waskita_network

  redis:
    image: redis:7-alpine
    container_name: waskita_redis
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass your_redis_password
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
      - ./nginx/sites-available:/etc/nginx/sites-available
      - ./ssl:/etc/nginx/ssl
      - ./logs/nginx:/var/log/nginx
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

### **2. Production Dockerfile**

Buat file `Dockerfile.prod`:

```dockerfile
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libpq-dev \
        libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads logs models static/uploads \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
```

### **3. Environment Variables**

Buat file `.env.prod`:

```bash
# Application
SECRET_KEY=your_very_long_and_secure_secret_key_here
FLASK_ENV=production
DEBUG=False

# Database
DATABASE_URL=postgresql://waskita_user:your_secure_password@db:5432/waskita_prod

# Redis
REDIS_URL=redis://:your_redis_password@redis:6379/0

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password

# Apify API
APIFY_API_TOKEN=your_apify_token

# Security
WTF_CSRF_TIME_LIMIT=3600
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# File Upload
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=/app/uploads

# Rate Limiting
RATELIMIT_STORAGE_URL=redis://:your_redis_password@redis:6379/1
```

### **4. Deploy Application**

```bash
# Load environment variables
source .env.prod

# Build and start services
docker-compose -f docker-compose.prod.yml up -d --build

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f app
```

---

## 🌐 KONFIGURASI WEB SERVER

### **Nginx Configuration**

Buat file `nginx/nginx.conf`:

```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    access_log /var/log/nginx/access.log main;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Security Headers
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';" always;

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    limit_req_zone $binary_remote_addr zone=api:10m rate=100r/m;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Include site configurations
    include /etc/nginx/sites-available/*;
}
```

Buat file `nginx/sites-available/waskita.conf`:

```nginx
upstream waskita_app {
    server app:5000;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Client upload limit
    client_max_body_size 20M;

    # Static files
    location /static/ {
        alias /app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Rate limiting for login
    location /login {
        limit_req zone=login burst=3 nodelay;
        proxy_pass http://waskita_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Rate limiting for API
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://waskita_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Main application
    location / {
        proxy_pass http://waskita_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check
    location /health {
        proxy_pass http://waskita_app;
        access_log off;
    }
}
```

---

## 🔒 SSL/TLS SETUP

### **Option 1: Let's Encrypt (Recommended)**

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal setup
sudo crontab -e
# Add this line:
0 12 * * * /usr/bin/certbot renew --quiet
```

### **Option 2: Self-Signed Certificate (Development)**

```bash
# Create SSL directory
mkdir -p ssl

# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/privkey.pem \
    -out ssl/fullchain.pem \
    -subj "/C=ID/ST=West Java/L=Bandung/O=Waskita/CN=your-domain.com"
```

---

## 📊 MONITORING & LOGGING

### **1. Application Monitoring**

Buat file `docker-compose.monitoring.yml`:

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: waskita_prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - waskita_network

  grafana:
    image: grafana/grafana:latest
    container_name: waskita_grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin_password
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana:/etc/grafana/provisioning
    networks:
      - waskita_network

  node_exporter:
    image: prom/node-exporter:latest
    container_name: waskita_node_exporter
    restart: unless-stopped
    ports:
      - "9100:9100"
    networks:
      - waskita_network

volumes:
  prometheus_data:
  grafana_data:

networks:
  waskita_network:
    external: true
```

### **2. Log Management**

Buat file `docker-compose.logging.yml`:

```yaml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.5.0
    container_name: waskita_elasticsearch
    restart: unless-stopped
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - waskita_network

  logstash:
    image: docker.elastic.co/logstash/logstash:8.5.0
    container_name: waskita_logstash
    restart: unless-stopped
    volumes:
      - ./logging/logstash.conf:/usr/share/logstash/pipeline/logstash.conf
      - ./logs:/logs
    depends_on:
      - elasticsearch
    networks:
      - waskita_network

  kibana:
    image: docker.elastic.co/kibana/kibana:8.5.0
    container_name: waskita_kibana
    restart: unless-stopped
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch
    networks:
      - waskita_network

volumes:
  elasticsearch_data:

networks:
  waskita_network:
    external: true
```

---

## 💾 BACKUP & RECOVERY

### **1. Database Backup Script**

Buat file `scripts/backup_db.sh`:

```bash
#!/bin/bash

# Configuration
DB_NAME="waskita_prod"
DB_USER="waskita_user"
BACKUP_DIR="/opt/waskita/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/waskita_backup_$DATE.sql"

# Create backup directory
mkdir -p $BACKUP_DIR

# PostgreSQL backup
docker exec waskita_db pg_dump -U $DB_USER -d $DB_NAME > $BACKUP_FILE

# Compress backup
gzip $BACKUP_FILE

# Remove backups older than 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: ${BACKUP_FILE}.gz"
```

### **2. Application Backup Script**

Buat file `scripts/backup_app.sh`:

```bash
#!/bin/bash

# Configuration
APP_DIR="/opt/waskita"
BACKUP_DIR="/opt/waskita/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/waskita_app_backup_$DATE.tar.gz"

# Create backup
tar -czf $BACKUP_FILE \
    --exclude='backups' \
    --exclude='logs' \
    --exclude='.git' \
    --exclude='__pycache__' \
    $APP_DIR

echo "Application backup completed: $BACKUP_FILE"
```

### **3. Automated Backup Cron**

```bash
# Edit crontab
sudo crontab -e

# Add these lines:
# Daily database backup at 2 AM
0 2 * * * /opt/waskita/scripts/backup_db.sh

# Weekly application backup on Sunday at 3 AM
0 3 * * 0 /opt/waskita/scripts/backup_app.sh
```

---

## 🛡️ SECURITY HARDENING

### **1. Firewall Configuration**

```bash
# Install UFW
sudo apt install -y ufw

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH
sudo ufw allow ssh

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow monitoring (optional, restrict to specific IPs)
sudo ufw allow from YOUR_MONITORING_IP to any port 9090
sudo ufw allow from YOUR_MONITORING_IP to any port 3000

# Enable firewall
sudo ufw enable
```

### **2. Fail2Ban Configuration**

```bash
# Install Fail2Ban
sudo apt install -y fail2ban

# Create custom configuration
sudo nano /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
action = iptables-multiport[name=ReqLimit, port="http,https", protocol=tcp]
logpath = /opt/waskita/logs/nginx/error.log
maxretry = 10
findtime = 600
bantime = 7200
```

### **3. System Hardening**

```bash
# Disable root login
sudo passwd -l root

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install security updates automatically
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# Set proper file permissions
sudo chmod 600 /opt/waskita/.env.prod
sudo chmod +x /opt/waskita/scripts/*.sh
```

---

## ⚡ PERFORMANCE OPTIMIZATION

### **1. Database Optimization**

```sql
-- PostgreSQL optimization
-- Edit postgresql.conf

# Memory settings
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB

# Connection settings
max_connections = 200
max_prepared_transactions = 200

# Checkpoint settings
checkpoint_completion_target = 0.9
wal_buffers = 16MB
```

### **2. Redis Configuration**

```bash
# Create redis.conf
sudo nano /opt/waskita/redis/redis.conf
```

```conf
# Memory optimization
maxmemory 256mb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000

# Security
requirepass your_redis_password
```

### **3. Application Performance**

```python
# Add to app.py for production
from flask_caching import Cache

# Configure caching
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL')
})

# Add caching to expensive operations
@cache.memoize(timeout=300)
def expensive_function():
    # Your expensive operation here
    pass
```

---

## 🔧 TROUBLESHOOTING

### **Common Issues & Solutions**

#### **1. Application Won't Start**

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs app

# Common fixes:
# - Check environment variables
# - Verify database connection
# - Check file permissions
# - Ensure all required files exist
```

#### **2. Database Connection Issues**

```bash
# Test database connection
docker exec -it waskita_db psql -U waskita_user -d waskita_prod

# Check database logs
docker-compose -f docker-compose.prod.yml logs db

# Verify network connectivity
docker network ls
docker network inspect waskita_network
```

#### **3. SSL Certificate Issues**

```bash
# Check certificate validity
openssl x509 -in ssl/fullchain.pem -text -noout

# Renew Let's Encrypt certificate
sudo certbot renew --dry-run

# Check Nginx configuration
sudo nginx -t
```

#### **4. Performance Issues**

```bash
# Monitor resource usage
docker stats

# Check application metrics
curl http://localhost:9090/metrics

# Analyze logs
tail -f logs/app.log
```

### **Health Check Commands**

```bash
# Application health
curl -f http://localhost/health

# Database health
docker exec waskita_db pg_isready -U waskita_user

# Redis health
docker exec waskita_redis redis-cli ping

# Nginx status
sudo systemctl status nginx
```

---

## 📞 SUPPORT & MAINTENANCE

### **Regular Maintenance Tasks**

#### **Daily:**
- ✅ Check application logs
- ✅ Monitor system resources
- ✅ Verify backup completion

#### **Weekly:**
- ✅ Review security logs
- ✅ Check SSL certificate expiry
- ✅ Update system packages
- ✅ Performance analysis

#### **Monthly:**
- ✅ Security audit
- ✅ Database optimization
- ✅ Backup restoration test
- ✅ Dependency updates

### **Emergency Contacts**

- **System Administrator:** admin@your-domain.com
- **Database Administrator:** dba@your-domain.com
- **Security Team:** security@your-domain.com
- **Development Team:** dev@your-domain.com

---

## 🏆 DEPLOYMENT CHECKLIST

### **Pre-Deployment:**
- [ ] Server requirements met
- [ ] SSL certificate obtained
- [ ] Environment variables configured
- [ ] Database setup completed
- [ ] Backup strategy implemented
- [ ] Monitoring configured
- [ ] Security hardening applied

### **Deployment:**
- [ ] Application deployed successfully
- [ ] Database migrations completed
- [ ] Static files served correctly
- [ ] SSL/HTTPS working
- [ ] All services running
- [ ] Health checks passing

### **Post-Deployment:**
- [ ] Monitoring alerts configured
- [ ] Backup tested
- [ ] Performance baseline established
- [ ] Security scan completed
- [ ] Documentation updated
- [ ] Team notified

---

**🎉 SELAMAT! Aplikasi Waskita telah berhasil di-deploy ke production dengan standar enterprise security.**

**📧 Untuk dukungan deployment, hubungi tim DevOps atau system administrator.**