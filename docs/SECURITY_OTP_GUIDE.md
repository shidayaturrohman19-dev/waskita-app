# 🔐 Panduan Keamanan & OTP Waskita

Panduan lengkap untuk keamanan aplikasi dan sistem OTP (One-Time Password) Waskita.

## ⚠️ Peringatan Keamanan Penting

### Default Credentials (WAJIB DIGANTI!)
**Development Only - JANGAN gunakan di production:**
- **Admin**: `[username]` / `[password]`
- **Database**: `[db_user]` / `[db_password]`
- **Test User**: `[test_username]` / `[test_password]`

### 🚨 Checklist Keamanan Production

#### Wajib Sebelum Deploy
- [ ] **Ganti semua password default**
- [ ] **Generate SECRET_KEY yang unik**
- [ ] **Setup HTTPS/SSL certificate**
- [ ] **Konfigurasi firewall yang proper**
- [ ] **Gunakan environment variables untuk kredensial**
- [ ] **Jangan commit file `.env*` ke repository**
- [ ] **Setup backup database otomatis**
- [ ] **Aktifkan logging dan monitoring**

#### Generate Secure Credentials
```bash
# Generate SECRET_KEY (32 bytes)
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"

# Generate strong password ([X] karakter)
python -c "import secrets, string; chars = string.ascii_letters + string.digits + '!@#$%^&*'; print(''.join(secrets.choice(chars) for _ in range([X])))"

# Generate database password
python -c "import secrets, string; chars = string.ascii_letters + string.digits; print('DB_PASSWORD=' + ''.join(secrets.choice(chars) for _ in range([X])))"
```

---

## 📧 Sistem OTP (One-Time Password)

### Overview
Sistem OTP Waskita menggunakan email untuk verifikasi registrasi user baru dengan kode 6 digit yang berlaku 10 menit.

### Fitur OTP System
- ✅ **Email verification** untuk registrasi user baru
- ✅ **[X]-digit OTP code** dengan expiry [X] menit
- ✅ **Rate limiting** untuk mencegah spam
- ✅ **Secure token generation** menggunakan `secrets` module
- ✅ **Gmail SMTP integration** dengan App Password
- ✅ **Automatic cleanup** expired OTP codes

### Struktur File OTP
```
├── email_service.py          # Core email functionality
├── otp_service.py           # OTP generation & validation
├── templates/
│   └── email/
│       └── otp_verification.html  # Email template
└── static/
    └── css/
        └── email.css        # Email styling
```

---

## 🛠️ Setup Gmail untuk OTP

### 1. Persiapan Akun Gmail

#### Aktifkan 2-Factor Authentication
1. Buka [Google Account Settings](https://myaccount.google.com/)
2. Pilih **Security** di sidebar kiri
3. Cari **2-Step Verification** dan aktifkan
4. Ikuti langkah verifikasi (SMS/Authenticator app)

#### Generate App Password
1. Setelah 2FA aktif, kembali ke **Security**
2. Pilih **App passwords** (mungkin perlu login ulang)
3. Pilih **Mail** sebagai app
4. Pilih **Other (Custom name)** sebagai device
5. Ketik nama: `Waskita OTP System`
6. Klik **Generate**
7. **Simpan 16-digit password** yang muncul (format: xxxx xxxx xxxx xxxx)

### 2. Konfigurasi Environment

Edit file `.env` atau `.env.local`:
```env
# Gmail SMTP Configuration for OTP
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-digit-app-password

# OTP Configuration
OTP_EXPIRY_MINUTES=[X]
OTP_LENGTH=[X]
MAX_OTP_ATTEMPTS=[X]
```

### 3. Testing Email Setup
```bash
# Test koneksi SMTP
python -c "
from email_service import test_smtp_connection
result = test_smtp_connection()
print('✅ SMTP OK' if result else '❌ SMTP Failed')
"

# Test pengiriman OTP
python -c "
from otp_service import send_otp_email
result = send_otp_email('test@example.com', 'Test User')
print('✅ OTP Sent' if result else '❌ OTP Failed')
"
```

---

## 🔧 Konfigurasi OTP System

### Environment Variables
```env
# Required - Gmail SMTP
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-gmail@gmail.com
MAIL_PASSWORD=your-app-password

# Optional - OTP Settings
OTP_EXPIRY_MINUTES=10        # Default: 10 menit
OTP_LENGTH=6                 # Default: 6 digit
MAX_OTP_ATTEMPTS=3           # Default: 3 percobaan
MAIL_DEFAULT_SENDER=your-gmail@gmail.com
```

### Database Schema
```sql
-- OTP codes disimpan di tabel users
ALTER TABLE users ADD COLUMN otp_code VARCHAR(6);
ALTER TABLE users ADD COLUMN otp_expires_at TIMESTAMP;
ALTER TABLE users ADD COLUMN otp_attempts INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;
```

---

## 🚀 Implementasi OTP

### 1. Registrasi User dengan OTP
```python
# Route: /register
@app.route('/register', methods=['POST'])
def register():
    # 1. Validasi input
    # 2. Check email sudah ada atau belum
    # 3. Generate OTP code
    # 4. Kirim email OTP
    # 5. Simpan user dengan status unverified
    # 6. Redirect ke halaman verifikasi
```

### 2. Verifikasi OTP
```python
# Route: /verify-otp
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    # 1. Validasi OTP code
    # 2. Check expiry time
    # 3. Check attempts limit
    # 4. Aktivasi user account
    # 5. Clear OTP data
```

### 3. Resend OTP
```python
# Route: /resend-otp
@app.route('/resend-otp', methods=['POST'])
def resend_otp():
    # 1. Check rate limiting
    # 2. Generate new OTP
    # 3. Update database
    # 4. Kirim email baru
```

---

## 🛡️ Security Best Practices

### OTP Security
- **Rate Limiting**: Max 3 percobaan per 10 menit
- **Secure Generation**: Menggunakan `secrets.randbelow()` 
- **Short Expiry**: Default 10 menit
- **Single Use**: OTP dihapus setelah digunakan
- **No Logging**: OTP code tidak di-log untuk keamanan

### Email Security
- **App Password**: Jangan gunakan password Gmail asli
- **TLS Encryption**: Semua komunikasi SMTP terenkripsi
- **Sender Verification**: Validasi sender email
- **Template Security**: HTML email di-sanitize

### Database Security
- **Hashed Passwords**: Menggunakan bcrypt
- **Prepared Statements**: Mencegah SQL injection
- **Connection Pooling**: Limit koneksi database
- **Backup Encryption**: Backup database terenkripsi

---

## 🔍 Troubleshooting

### Email Issues
```bash
# Check Gmail settings
# 1. 2FA harus aktif
# 2. App Password harus benar (16 digit)
# 3. "Less secure app access" harus OFF (gunakan App Password)

# Test SMTP connection
telnet smtp.gmail.com 587
# Harus connect ke port 587

# Check firewall
# Port 587 (SMTP TLS) harus terbuka untuk outbound
```

### OTP Issues
```bash
# Check OTP generation
python -c "
import secrets
otp = str(secrets.randbelow(1000000)).zfill(6)
print(f'Sample OTP: {otp}')
"

# Check database OTP storage
# Pastikan kolom otp_code, otp_expires_at ada di tabel users

# Check email template
# File templates/email/otp_verification.html harus ada
```

### Common Errors
- **535 Authentication failed**: App Password salah atau 2FA tidak aktif
- **Connection timeout**: Firewall block port 587
- **OTP expired**: User terlalu lama input OTP (>10 menit)
- **Too many attempts**: User salah input OTP >3 kali

---

## 📊 Monitoring & Logging

### OTP Metrics
- Total OTP sent per hari
- Success rate verifikasi
- Average verification time
- Failed attempts per user

### Security Logs
```python
# Log security events
import logging

# Setup security logger
security_logger = logging.getLogger('security')
security_logger.info(f'OTP sent to {email}')
security_logger.warning(f'Failed OTP attempt from {ip}')
security_logger.error(f'Suspicious activity: {details}')
```

### Alerts
- Multiple failed OTP attempts
- Unusual email sending patterns
- Database connection issues
- SMTP authentication failures

---

## 🎯 Production Checklist

### Pre-deployment
- [ ] Test OTP flow end-to-end
- [ ] Verify email deliverability
- [ ] Check rate limiting works
- [ ] Test with real Gmail account
- [ ] Verify HTTPS certificate
- [ ] Setup monitoring alerts

### Post-deployment
- [ ] Monitor OTP success rates
- [ ] Check email delivery logs
- [ ] Verify security logs
- [ ] Test backup/restore
- [ ] Monitor performance metrics

Sistem OTP dan keamanan Waskita siap untuk production! 🔐✅