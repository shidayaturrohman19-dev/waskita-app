# 🔒 Panduan Keamanan Waskita

## ⚠️ PERINGATAN PENTING

**JANGAN PERNAH** menggunakan kredensial default di production! File ini berisi panduan keamanan yang harus diikuti sebelum deployment.

---

## 🔐 Kredensial Default

### Admin Default (HANYA UNTUK DEVELOPMENT)
- **Username**: `admin`
- **Email**: `admin@waskita.com`  
- **Password**: `admin123` (WAJIB DIGANTI!)

### Test User Default (HANYA UNTUK DEVELOPMENT)
- **Username**: `testuser`
- **Email**: `test@waskita.com`
- **Password**: `test123` (WAJIB DIGANTI!)

### Database Default (HANYA UNTUK DEVELOPMENT)
- **User**: `waskita_user`
- **Password**: `waskita_password` (WAJIB DIGANTI!)
- **Database**: `waskita_dev`

---

## 🛡️ Checklist Keamanan Production

### 1. Kredensial & Password
- [ ] Ganti password admin default
- [ ] Ganti password database
- [ ] Generate SECRET_KEY yang unik
- [ ] Generate WASKITA_API_KEY yang unik
- [ ] Ganti semua API tokens (Apify, Social Media)
- [ ] Gunakan password yang kuat (min 12 karakter, kombinasi huruf/angka/simbol)

### 2. Environment Variables
- [ ] Buat file `.env.production` terpisah
- [ ] Jangan commit file `.env*` ke repository
- [ ] Gunakan environment variables untuk semua kredensial
- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`

### 3. Database Security
- [ ] Gunakan SSL/TLS untuk koneksi database
- [ ] Batasi akses database hanya dari aplikasi
- [ ] Backup database secara berkala
- [ ] Monitor akses database

### 4. Web Security
- [ ] Gunakan HTTPS di production
- [ ] Set secure cookies (`SESSION_COOKIE_SECURE=True`)
- [ ] Enable CSRF protection
- [ ] Set proper CORS headers
- [ ] Implement rate limiting

### 5. File Security
- [ ] Validasi semua file upload
- [ ] Scan malware untuk file upload
- [ ] Batasi ukuran file upload
- [ ] Simpan file upload di lokasi yang aman

---

## 🔧 Konfigurasi Production

### Environment Variables (.env.production)
```bash
# Database - GANTI SEMUA KREDENSIAL!
DATABASE_URL=postgresql://your_db_user:your_secure_password@localhost:5432/waskita_prod
SECRET_KEY=your_very_long_and_random_secret_key_here

# Flask Production Settings
FLASK_ENV=production
FLASK_DEBUG=False

# Security Settings
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
WTF_CSRF_ENABLED=True

# API Keys - GANTI DENGAN YANG ASLI!
APIFY_API_TOKEN=your_real_apify_token
WASKITA_API_KEY=your_unique_api_key

# Social Media APIs (Optional)
TWITTER_API_KEY=your_twitter_key
FACEBOOK_APP_ID=your_facebook_id
# ... dst
```

### Generate Secret Key
```python
import secrets
print(secrets.token_urlsafe(32))
```

### Generate API Key
```python
import secrets
import string
alphabet = string.ascii_letters + string.digits
api_key = ''.join(secrets.choice(alphabet) for i in range(32))
print(f"waskita_api_{api_key}")
```

---

## 🚨 Incident Response

### Jika Kredensial Terekspos
1. **Segera ganti** semua password dan API keys
2. **Revoke** semua session aktif
3. **Monitor** log untuk aktivitas mencurigakan
4. **Audit** semua akses ke sistem
5. **Update** dokumentasi keamanan

### Monitoring
- Monitor log aplikasi untuk error dan akses tidak sah
- Set up alerting untuk login gagal berulang
- Monitor penggunaan API untuk anomali
- Backup database secara berkala

---

## 🔄 Tugas Keamanan Berkala

### Mingguan
- [ ] Review log files untuk anomali
- [ ] Check update security patches
- [ ] Monitor pola penggunaan API

### Bulanan
- [ ] Rotate API keys (jika memungkinkan)
- [ ] Review akses dan permissions pengguna
- [ ] Update dependencies dengan security patches

### Triwulanan
- [ ] Full security audit
- [ ] Penetration testing (jika memungkinkan)
- [ ] Review dan update security policies
- [ ] Test disaster recovery procedures

---

## 🚨 Incident Response

### Jika Credentials Terekspos
1. **Tindakan Segera:**
   - Rotate semua credentials yang terekspos
   - Generate SECRET_KEY baru
   - Ganti password database
   - Revoke dan generate ulang API keys

2. **Investigasi:**
   - Check log untuk aktivitas mencurigakan
   - Audit akses yang tidak authorized
   - Identifikasi scope of exposure

3. **Recovery:**
   - Update environment dengan credentials baru
   - Restart aplikasi dengan config baru
   - Monitor aktivitas abnormal
   - Dokumentasi incident untuk pembelajaran

---

## 📞 Kontak Keamanan

Jika menemukan masalah keamanan:
- **JANGAN** posting di public issue tracker
- Hubungi tim security secara langsung
- Email: security@waskita.com
- Ikuti responsible disclosure practices

---

## 📚 Referensi

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/security.html)

---

**⚠️ INGAT: Keamanan adalah tanggung jawab bersama. Selalu ikuti best practices dan jangan pernah mengabaikan peringatan keamanan!**