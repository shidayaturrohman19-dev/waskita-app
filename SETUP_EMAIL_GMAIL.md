# 📧 Panduan Setup Email Gmail untuk Sistem OTP Waskita

## Status Integrasi Email

✅ **Sistem OTP sudah diintegrasikan dengan Gmail** - Namun perlu konfigurasi manual

❌ **Belum dikonfigurasi** - Perlu setup Gmail App Password dan environment variables

## 🔧 Langkah-langkah Setup Gmail

### 1. **Persiapan Akun Gmail**

#### A. Aktifkan 2-Factor Authentication
1. Buka [Google Account Settings](https://myaccount.google.com/)
2. Pilih **Security** di menu kiri
3. Aktifkan **2-Step Verification**
4. Ikuti instruksi untuk setup (SMS/Authenticator App)

#### B. Generate App Password
1. Setelah 2FA aktif, kembali ke **Security**
2. Cari **App passwords** (mungkin perlu scroll)
3. Klik **App passwords**
4. Pilih **Mail** sebagai app
5. Pilih **Other (Custom name)** sebagai device
6. Ketik: `Waskita OTP System`
7. Klik **Generate**
8. **SIMPAN** 16-digit password yang muncul (contoh: `abcd efgh ijkl mnop`)

### 2. **Konfigurasi File .env**

Edit file `.env` di root project:

```env
# Gmail SMTP Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False

# Gmail Account - GANTI DENGAN MILIK ANDA
MAIL_USERNAME=your-actual-gmail@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop
MAIL_DEFAULT_SENDER=your-actual-gmail@gmail.com

# Admin Email - GANTI DENGAN EMAIL ADMIN
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_EMAILS=admin1@yourdomain.com,admin2@yourdomain.com
```

### 3. **Contoh Konfigurasi Lengkap**

```env
# Contoh dengan Gmail nyata
MAIL_USERNAME=waskita.system@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop
MAIL_DEFAULT_SENDER=waskita.system@gmail.com

# Admin yang akan menerima OTP
ADMIN_EMAIL=admin.waskita@gmail.com
ADMIN_EMAILS=admin.waskita@gmail.com,supervisor@company.com
```

## 🧪 Testing Email Configuration

### 1. **Test Konfigurasi**
```bash
cd "d:\TelU\Matkul\Semester IV\Waskita"
python -c "from config_otp import OTPConfig; errors = OTPConfig.validate_config(); print('Config:', 'OK' if not errors else errors)"
```

### 2. **Test Pengiriman Email**
```python
# Buat file test_email.py
from email_service import EmailService

service = EmailService()
success, error = service.send_email(
    to_email="test@example.com",
    subject="Test Email Waskita",
    html_content="<h1>Test berhasil!</h1>"
)

print(f"Email sent: {success}")
if error:
    print(f"Error: {error}")
```

## 🔒 Keamanan Gmail

### **App Password vs Regular Password**
- ✅ **Gunakan App Password** (16 digit) - Lebih aman
- ❌ **Jangan gunakan password biasa** - Tidak akan berfungsi dengan 2FA

### **Batasan Gmail**
- **Limit harian**: 500 email per hari untuk akun gratis
- **Rate limit**: Maksimal 100 email per jam
- **Spam protection**: Hindari mengirim email berulang ke alamat yang sama

## 📋 Checklist Setup

- [ ] Akun Gmail sudah ada
- [ ] 2-Factor Authentication aktif
- [ ] App Password sudah di-generate
- [ ] File `.env` sudah dikonfigurasi dengan benar
- [ ] `MAIL_USERNAME` diisi dengan Gmail lengkap
- [ ] `MAIL_PASSWORD` diisi dengan 16-digit App Password
- [ ] `ADMIN_EMAIL` diisi dengan email admin yang valid
- [ ] Test konfigurasi berhasil
- [ ] Test pengiriman email berhasil

## 🚨 Troubleshooting

### **Error: "Username and Password not accepted"**
```
Solusi:
1. Pastikan 2FA sudah aktif
2. Gunakan App Password, bukan password biasa
3. Cek MAIL_USERNAME format: user@gmail.com (lengkap)
```

### **Error: "SMTPAuthenticationError"**
```
Solusi:
1. Regenerate App Password baru
2. Pastikan tidak ada spasi di App Password
3. Coba login manual ke Gmail untuk memastikan akun tidak terkunci
```

### **Error: "Connection refused"**
```
Solusi:
1. Cek koneksi internet
2. Pastikan MAIL_SERVER=smtp.gmail.com
3. Pastikan MAIL_PORT=587
4. Pastikan MAIL_USE_TLS=True
```

### **Email tidak sampai**
```
Solusi:
1. Cek folder Spam/Junk di email penerima
2. Pastikan email penerima valid
3. Cek quota Gmail (max 500/hari)
4. Tunggu beberapa menit (delay Gmail)
```

## 📧 Alternatif Email Provider

Jika tidak ingin menggunakan Gmail, bisa menggunakan:

### **Outlook/Hotmail**
```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
```

### **Yahoo Mail**
```env
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=True
```

### **Custom SMTP**
```env
MAIL_SERVER=mail.yourdomain.com
MAIL_PORT=587
MAIL_USE_TLS=True
```

## 🎯 Rekomendasi Production

### **Untuk Production Environment:**
1. **Gunakan email domain sendiri** (bukan Gmail)
2. **Setup DKIM/SPF records** untuk deliverability
3. **Gunakan email service** seperti SendGrid/Mailgun
4. **Monitor email quota** dan delivery rates
5. **Setup email templates** yang professional

### **Konfigurasi Production:**
```env
# Production dengan domain sendiri
MAIL_SERVER=smtp.yourdomain.com
MAIL_USERNAME=noreply@yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com
BASE_URL=https://waskita.yourdomain.com
```

## 📞 Support

Jika masih ada masalah:
1. Cek log aplikasi di `waskita.log`
2. Test manual dengan script Python
3. Verifikasi semua environment variables
4. Pastikan firewall tidak memblokir port 587

---

**Catatan Penting**: 
- Jangan commit file `.env` ke Git (sudah ada di `.gitignore`)
- Simpan App Password di tempat yang aman
- Ganti semua password default sebelum production