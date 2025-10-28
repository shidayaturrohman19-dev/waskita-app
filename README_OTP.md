# Sistem Autentifikasi OTP untuk Registrasi Pengguna

## Gambaran Umum

Sistem autentifikasi OTP (One-Time Password) ini dirancang untuk memberikan kontrol admin terhadap registrasi pengguna baru. Sebelum pengguna dapat mendaftar dan menggunakan aplikasi Waskita, admin harus menyetujui permintaan registrasi mereka melalui verifikasi OTP yang dikirim via email.

## Fitur Utama

### 1. **Registrasi dengan Persetujuan Admin**
- Pengguna mengajukan permintaan registrasi
- Admin menerima notifikasi email dengan OTP
- Admin memverifikasi dan menyetujui/menolak registrasi
- Pengguna mendapat notifikasi hasil persetujuan

### 2. **Sistem OTP yang Aman**
- OTP 6 digit yang di-generate secara acak
- Masa berlaku OTP dapat dikonfigurasi (default: 30 menit)
- Pembatasan percobaan OTP (default: 3 kali)
- Auto-cleanup untuk permintaan yang expired

### 3. **Panel Admin Komprehensif**
- Dashboard untuk melihat semua permintaan registrasi
- Filter berdasarkan status (pending, approved, rejected, expired)
- Riwayat lengkap email dan aktivitas
- Statistik registrasi real-time

### 4. **Notifikasi Email Otomatis**
- Email OTP ke admin saat ada permintaan baru
- Email konfirmasi ke pengguna saat registrasi disetujui
- Template email yang dapat dikustomisasi
- Retry mechanism untuk pengiriman email

## Struktur File

```
├── models_otp.py              # Model database untuk OTP system
├── otp_routes.py              # Routes untuk OTP authentication
├── email_service.py           # Service untuk pengiriman email
├── config_otp.py              # Konfigurasi OTP system
├── templates/
│   ├── register_request.html  # Form permintaan registrasi
│   ├── registration_status.html # Status permintaan registrasi
│   └── admin/
│       ├── pending_registrations.html # Dashboard admin
│       └── approve_registration.html  # Form persetujuan admin
└── README_OTP.md              # Dokumentasi ini
```

## Instalasi dan Konfigurasi

### 1. **Instalasi Dependencies**

Pastikan dependencies berikut sudah terinstall:

```bash
pip install flask-mail
```

### 2. **Konfigurasi Environment Variables**

Tambahkan konfigurasi berikut ke file `.env`:

```env
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Admin Configuration
ADMIN_EMAIL=admin@waskita.com
ADMIN_EMAILS=admin1@waskita.com,admin2@waskita.com

# OTP Configuration
OTP_LENGTH=6
OTP_EXPIRY_MINUTES=30
MAX_OTP_ATTEMPTS=3
LOCKOUT_DURATION_MINUTES=15

# Registration Configuration
REGISTRATION_ENABLED=True
AUTO_APPROVE_REGISTRATION=False

# Application URLs
BASE_URL=http://localhost:5000

# Email Notification Settings
SEND_EMAIL_NOTIFICATIONS=True
EMAIL_RETRY_ATTEMPTS=3
EMAIL_RETRY_DELAY_SECONDS=5
```

### 3. **Setup Gmail App Password**

Untuk menggunakan Gmail sebagai SMTP server:

1. Aktifkan 2-Factor Authentication di akun Gmail
2. Generate App Password di Google Account Settings
3. Gunakan App Password sebagai `MAIL_PASSWORD`

### 4. **Database Migration**

Jalankan migrasi database untuk membuat tabel baru:

```bash
flask db migrate -m "Add OTP authentication tables"
flask db upgrade
```

## Cara Penggunaan

### 1. **Untuk Pengguna (Registrasi)**

1. **Akses Form Registrasi**
   ```
   GET /otp/register-request
   ```

2. **Isi Form Registrasi**
   - Username (3-20 karakter, alphanumeric + underscore)
   - Email (format email valid)
   - Nama Lengkap
   - Password (minimal 8 karakter)
   - Konfirmasi Password
   - Persetujuan Terms & Conditions

3. **Cek Status Registrasi**
   ```
   GET /otp/registration-status/<request_id>
   ```

### 2. **Untuk Admin (Persetujuan)**

1. **Akses Dashboard Admin**
   ```
   GET /otp/admin/pending
   ```

2. **Review Permintaan Registrasi**
   - Lihat detail pengguna
   - Cek riwayat email
   - Filter berdasarkan status

3. **Proses Persetujuan**
   ```
   GET /otp/admin/approve/<request_id>
   ```
   - Masukkan OTP yang diterima via email
   - Tambahkan catatan admin (opsional)
   - Setujui atau tolak registrasi

## API Endpoints

### Public Endpoints

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/otp/register-request` | Form permintaan registrasi |
| POST | `/otp/register-request` | Submit permintaan registrasi |
| GET | `/otp/registration-status/<id>` | Cek status registrasi |
| GET | `/otp/api/registration-status/<id>` | API status registrasi |

### Admin Endpoints (Login Required)

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/otp/admin/pending` | Dashboard permintaan pending |
| GET | `/otp/admin/approve/<id>` | Form persetujuan registrasi |
| POST | `/otp/admin/approve/<id>` | Proses persetujuan/penolakan |
| GET | `/otp/admin/history` | Riwayat semua registrasi |
| POST | `/otp/admin/resend-otp/<id>` | Kirim ulang OTP |
| GET | `/otp/admin/api/stats` | API statistik registrasi |

## Model Database

### 1. **RegistrationRequest**
```python
- id: Primary key
- username: Username yang diminta
- email: Email pengguna
- full_name: Nama lengkap
- password_hash: Hash password
- otp_code: Kode OTP 6 digit
- otp_expires_at: Waktu expired OTP
- status: pending/approved/rejected/expired
- admin_notes: Catatan dari admin
- created_at: Waktu permintaan dibuat
- processed_at: Waktu diproses admin
- processed_by: Admin yang memproses
```

### 2. **AdminNotification**
```python
- id: Primary key
- registration_request_id: FK ke RegistrationRequest
- admin_email: Email admin yang dinotifikasi
- notification_type: Jenis notifikasi
- is_read: Status baca notifikasi
- created_at: Waktu notifikasi dibuat
```

### 3. **OTPEmailLog**
```python
- id: Primary key
- registration_request_id: FK ke RegistrationRequest
- recipient_email: Email penerima
- email_type: Jenis email (otp_notification/approval_notification)
- is_sent: Status pengiriman
- error_message: Pesan error jika gagal
- created_at: Waktu pengiriman
```

## Keamanan

### 1. **Validasi Input**
- Username: Alphanumeric + underscore, 3-20 karakter
- Email: Format email valid, unique
- Password: Minimal 8 karakter, kombinasi huruf dan angka
- OTP: 6 digit angka

### 2. **Rate Limiting**
- Maksimal 3 percobaan OTP per permintaan
- Lockout 15 menit setelah percobaan gagal
- Auto-cleanup permintaan expired

### 3. **CSRF Protection**
- Semua form dilindungi CSRF token
- Validasi referrer untuk admin endpoints

### 4. **Authorization**
- Admin endpoints memerlukan login
- Validasi admin role untuk akses sensitive

## Monitoring dan Logging

### 1. **Email Logs**
- Semua pengiriman email dicatat
- Status berhasil/gagal dengan error message
- Retry attempts tracking

### 2. **Activity Logs**
- Permintaan registrasi baru
- Persetujuan/penolakan admin
- OTP generation dan verification

### 3. **Statistics**
- Total permintaan per status
- Rata-rata waktu proses
- Success rate pengiriman email

## Troubleshooting

### 1. **Email Tidak Terkirim**
```python
# Cek konfigurasi SMTP
from config_otp import OTPConfig
errors = OTPConfig.validate_config()
if errors:
    print("Configuration errors:", errors)
```

### 2. **OTP Expired**
- Cek `OTP_EXPIRY_MINUTES` di environment
- Admin dapat mengirim ulang OTP
- Auto-cleanup akan menghapus permintaan expired

### 3. **Database Issues**
```bash
# Reset database jika diperlukan
flask db downgrade
flask db upgrade
```

### 4. **Permission Issues**
- Pastikan admin memiliki role yang tepat
- Cek `ADMIN_EMAILS` di konfigurasi

## Customization

### 1. **Email Templates**
Template email dapat dikustomisasi di `email_service.py`:
- `get_otp_email_template()`: Template OTP untuk admin
- `get_approval_email_template()`: Template konfirmasi untuk user

### 2. **OTP Configuration**
Sesuaikan di `config_otp.py`:
- Panjang OTP (4-8 digit)
- Masa berlaku (5-120 menit)
- Maksimal percobaan (1-10 kali)

### 3. **UI Customization**
Template HTML dapat dimodifikasi:
- Bootstrap 4 + AdminLTE theme
- Custom CSS untuk styling
- JavaScript untuk interaktivity

## Maintenance

### 1. **Cleanup Otomatis**
Sistem akan otomatis membersihkan:
- Permintaan expired (setelah 24 jam)
- Permintaan completed (setelah 7 hari)
- Email logs lama

### 2. **Backup Recommendations**
- Backup database secara berkala
- Simpan konfigurasi email
- Monitor disk space untuk logs

### 3. **Performance Monitoring**
- Monitor penggunaan email quota
- Cek response time admin dashboard
- Track success rate registrasi

## Support

Untuk pertanyaan atau issues:
1. Cek logs di `waskita.log`
2. Validasi konfigurasi dengan `OTPConfig.validate_config()`
3. Test email connectivity dengan test endpoint
4. Review database untuk data inconsistency

---

**Catatan**: Sistem ini dirancang untuk memberikan kontrol penuh kepada admin terhadap registrasi pengguna sambil tetap memberikan pengalaman yang user-friendly bagi calon pengguna.