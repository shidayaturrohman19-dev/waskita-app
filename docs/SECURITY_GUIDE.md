# Panduan Keamanan Aplikasi Waskita

## 1. Environment Variables dan Credentials

### Setup Environment Variables

1. **Copy file template:**
   ```bash
   cp .env.example .env
   ```

2. **Generate SECRET_KEY yang kuat:**
   ```python
   import secrets
   print(secrets.token_urlsafe(32))
   ```

3. **Update credentials di file .env:**
   - `SECRET_KEY`: Gunakan key yang di-generate di atas
   - `DATABASE_PASSWORD`: Ganti dengan password database yang kuat
   - `APIFY_API_TOKEN`: Masukkan token Apify API yang valid
   - `MAIL_USERNAME` & `MAIL_PASSWORD`: Credentials email yang valid

### Credentials yang Wajib Diisi

#### Development Environment:
- `SECRET_KEY`
- `DATABASE_URL`
- `TEST_DATABASE_URL`

#### Production Environment:
- Semua credentials di atas
- `APIFY_API_TOKEN` (jika menggunakan scraping)
- `MAIL_USERNAME` & `MAIL_PASSWORD` (jika menggunakan email)

## 2. Database Security

### Password Database
- Gunakan password yang kuat (minimal 12 karakter)
- Kombinasi huruf besar, kecil, angka, dan simbol
- Jangan gunakan password default seperti 'postgres' atau '123456'

### Connection Security
- Gunakan SSL/TLS untuk koneksi database di production
- Batasi akses database hanya dari IP yang diperlukan
- Gunakan user database khusus dengan privilege minimal

## 3. API Keys Security

### Apify API Token
- Simpan di environment variable `APIFY_API_TOKEN`
- Jangan commit ke repository
- Rotate token secara berkala
- Monitor penggunaan API untuk deteksi anomali

### Social Media API Keys
- Simpan semua keys di environment variables
- Gunakan scope/permission minimal yang diperlukan
- Implement rate limiting untuk mencegah abuse

## 4. Session Security

### Production Settings
- `SESSION_COOKIE_SECURE=True` (HTTPS only)
- `SESSION_COOKIE_HTTPONLY=True` (prevent XSS)
- `SESSION_COOKIE_SAMESITE='Strict'` (CSRF protection)
- `PERMANENT_SESSION_LIFETIME=24 hours` (auto logout)

### Development Settings
- `SESSION_COOKIE_SECURE=False` (allow HTTP)
- Other settings sama dengan production

## 5. File Security

### .env File
- **JANGAN** commit file `.env` ke repository
- Pastikan `.env` ada di `.gitignore`
- Set permission file: `chmod 600 .env` (Linux/Mac)
- Backup `.env` secara terpisah dan aman

### Upload Security
- Validasi tipe file yang diupload
- Scan file untuk malware (jika memungkinkan)
- Batasi ukuran file (saat ini 16MB)
- Simpan file upload di direktori yang tidak executable

## 6. Logging Security

### Sensitive Data
- **JANGAN** log password, API keys, atau data sensitif
- Mask/redact data sensitif dalam log
- Gunakan log level yang sesuai (INFO, WARNING, ERROR)

### Log Files
- Protect log files dengan permission yang tepat
- Rotate log files secara berkala
- Monitor log untuk aktivitas mencurigakan

## 7. Deployment Security

### Docker Security
- Jangan run container sebagai root user
- Gunakan multi-stage build untuk minimize attack surface
- Scan image untuk vulnerabilities
- Update base image secara berkala

### Production Checklist
- [ ] SECRET_KEY di-generate dengan aman
- [ ] Database password diganti dari default
- [ ] Semua API keys valid dan aktif
- [ ] SSL/HTTPS dikonfigurasi
- [ ] Firewall dikonfigurasi dengan benar
- [ ] Monitoring dan alerting aktif
- [ ] Backup strategy sudah ada
- [ ] Log monitoring aktif

## 8. Incident Response

### Jika Credentials Terekspos
1. **Immediate Actions:**
   - Rotate semua credentials yang terekspos
   - Generate SECRET_KEY baru
   - Ganti password database
   - Revoke dan generate ulang API keys

2. **Investigation:**
   - Check log untuk aktivitas mencurigakan
   - Audit akses yang tidak authorized
   - Identify scope of exposure

3. **Recovery:**
   - Update semua environment dengan credentials baru
   - Restart aplikasi dengan config baru
   - Monitor untuk aktivitas abnormal
   - Document incident untuk pembelajaran

## 9. Regular Security Tasks

### Weekly
- Review log files untuk anomali
- Check untuk update security patches
- Monitor API usage patterns

### Monthly
- Rotate API keys (jika memungkinkan)
- Review user access dan permissions
- Update dependencies dengan security patches

### Quarterly
- Full security audit
- Penetration testing (jika memungkinkan)
- Review dan update security policies
- Backup dan test disaster recovery

## 10. Contact

Jika menemukan security issue:
- **JANGAN** post di public issue tracker
- Contact security team secara langsung
- Provide detailed information tentang vulnerability
- Follow responsible disclosure practices