# 🔄 Panduan GitHub: Ganti Akun & Push Repository

Panduan lengkap untuk mengganti akun GitHub dan memastikan repository siap di-push dengan aman.

## 📊 Status Repository Saat Ini

### ✅ **Files yang AMAN untuk di-push:**

#### Modified Files (Sudah ada, perlu update):
- ✅ `.env.example` - Template konfigurasi (aman)
- ✅ `README.md` - Dokumentasi utama
- ✅ `app.py` - Aplikasi utama
- ✅ `docs/USER_GUIDE_LENGKAP.md` - Dokumentasi
- ✅ `requirements.txt` - Dependencies
- ✅ `routes.py` - Routes aplikasi
- ✅ `static/css/custom.css` - Styling
- ✅ `templates/` - Template HTML
- ✅ `utils.py` - Utilities

#### New Files (Belum ada di repository):
- ✅ `README_OTP.md` - Dokumentasi OTP
- ✅ `SETUP_EMAIL_GMAIL.md` - Setup email
- ✅ `config_otp.py` - Konfigurasi OTP
- ✅ `dev-to-docker.md` - Workflow guide
- ✅ `email_service.py` - Service email
- ✅ `models_otp.py` - Model OTP
- ✅ `otp_routes.py` - Routes OTP
- ✅ `quick-start.md` - Quick start guide
- ✅ `security_logger.py` - Security logging
- ✅ `static/js/` - JavaScript files
- ✅ `templates/admin/` - Template admin baru
- ✅ `templates/auth/` - Template auth baru

### ❌ **Files yang TIDAK BOLEH di-push:**

#### Environment Files (Sudah di .gitignore):
- ❌ `.env` - **BERBAHAYA! Berisi kredensial asli**
- ❌ `.env.local` - **BERBAHAYA! Berisi kredensial development**
- ❌ `.env.docker` - **BERBAHAYA! Berisi kredensial Docker**

#### Other Sensitive Files:
- ❌ `uploads/` - File upload user
- ❌ `logs/` - Log files
- ❌ `__pycache__/` - Python cache
- ❌ `venv/` - Virtual environment
- ❌ `*.pyc` - Compiled Python files

### 🛡️ **Verifikasi .gitignore:**
✅ File `.gitignore` sudah dikonfigurasi dengan benar untuk mengecualikan:
```
.env
.env.local
.env.docker
.env.production
*.env
uploads/
logs/
__pycache__/
venv/
```

---

## 🔄 Panduan Ganti Akun GitHub

### **Step 1: Backup Repository Lokal**
```bash
# Backup current state
git add .
git commit -m "backup: save current state before account change"
```

### **Step 2: Konfigurasi Git dengan Akun Baru**

#### Option A: Global Configuration (Untuk semua repository)
```bash
# Set username dan email baru
git config --global user.name "USERNAME_BARU"
git config --global user.email "email_baru@example.com"

# Verifikasi konfigurasi
git config --global --list | findstr user
```

#### Option B: Local Configuration (Hanya untuk repository ini)
```bash
# Set username dan email untuk repository ini saja
git config user.name "USERNAME_BARU"
git config user.email "email_baru@example.com"

# Verifikasi konfigurasi
git config --list | findstr user
```

### **Step 3: Buat Repository Baru di GitHub**

1. **Login ke akun GitHub baru**
2. **Klik "New Repository"**
3. **Isi detail repository:**
   - Repository name: `waskita` (atau nama lain)
   - Description: `Sistem Klasifikasi Konten Radikal Media Sosial`
   - Visibility: `Public` atau `Private`
   - ❌ **JANGAN** centang "Initialize with README" (karena sudah ada)

### **Step 4: Update Remote URL**

```bash
# Hapus remote lama
git remote remove origin

# Tambah remote baru
git remote add origin https://github.com/USERNAME_BARU/NAMA_REPOSITORY.git

# Verifikasi remote baru
git remote -v
```

### **Step 5: Push ke Repository Baru**

```bash
# Push semua branch
git push -u origin main

# Jika ada error, force push (hati-hati!)
git push -u origin main --force
```

---

## 🚀 Langkah-langkah Push yang Aman

### **Pre-Push Checklist:**

#### 1. **Verifikasi Files yang Akan di-Push**
```bash
# Cek status git
git status

# Cek diff untuk memastikan tidak ada kredensial
git diff --cached
```

#### 2. **Pastikan .env Files Tidak Ter-track**
```bash
# Cek apakah .env files ter-track
git ls-files | findstr "\.env"

# Jika ada, hapus dari tracking (TANPA menghapus file)
git rm --cached .env
git rm --cached .env.local
git rm --cached .env.docker
```

#### 3. **Add Files yang Aman**
```bash
# Add semua files yang aman
git add .env.example
git add README.md
git add app.py
git add docs/
git add requirements.txt
git add routes.py
git add static/
git add templates/
git add utils.py
git add README_OTP.md
git add SETUP_EMAIL_GMAIL.md
git add config_otp.py
git add dev-to-docker.md
git add email_service.py
git add models_otp.py
git add otp_routes.py
git add quick-start.md
git add security_logger.py

# Atau add semua (karena .gitignore sudah melindungi)
git add .
```

#### 4. **Commit dengan Pesan yang Jelas**
```bash
git commit -m "feat: add OTP system, email service, and comprehensive documentation

- Add OTP-based registration system
- Add email service with Gmail integration
- Add comprehensive workflow documentation (dev-to-docker.md)
- Add quick start guide
- Add security logging
- Update admin panel with registration management
- Update authentication templates
- Add email setup guide"
```

#### 5. **Push ke Repository**
```bash
git push -u origin main
```

---

## 🔐 Keamanan & Best Practices

### **❌ JANGAN PERNAH Push:**
1. **File .env dengan kredensial asli**
2. **Password atau API keys**
3. **Database credentials**
4. **Email passwords**
5. **Secret keys production**

### **✅ SELALU Push:**
1. **File .env.example dengan placeholder**
2. **Source code aplikasi**
3. **Dokumentasi**
4. **Requirements.txt**
5. **Configuration templates**

### **🛡️ Verifikasi Keamanan:**
```bash
# Cek apakah ada kredensial yang ter-commit
git log --oneline -p | findstr -i "password\|secret\|key\|token"

# Jika ada, gunakan git filter-branch atau BFG untuk membersihkan history
```

---

## 🆘 Troubleshooting

### **Problem: Remote repository sudah ada**
```bash
# Solution: Force push (hati-hati!)
git push -u origin main --force
```

### **Problem: Authentication failed**
```bash
# Solution 1: Use Personal Access Token
# 1. Buat PAT di GitHub Settings > Developer settings > Personal access tokens
# 2. Use PAT sebagai password saat push

# Solution 2: Use SSH
ssh-keygen -t rsa -b 4096 -C "email_baru@example.com"
# Add SSH key ke GitHub account
```

### **Problem: File .env ter-push**
```bash
# Solution: Remove from history
git rm --cached .env
git commit -m "remove: .env file from tracking"
git push

# Untuk remove dari history (advanced):
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch .env' --prune-empty --tag-name-filter cat -- --all
```

### **Problem: Merge conflicts**
```bash
# Solution: Resolve conflicts
git status
# Edit conflicted files
git add .
git commit -m "resolve: merge conflicts"
git push
```

---

## 📋 Quick Commands Summary

### **Setup Akun Baru:**
```bash
# 1. Konfigurasi git
git config user.name "USERNAME_BARU"
git config user.email "email_baru@example.com"

# 2. Update remote
git remote set-url origin https://github.com/USERNAME_BARU/REPO_BARU.git

# 3. Push
git add .
git commit -m "initial: setup repository with new account"
git push -u origin main
```

### **Verifikasi Keamanan:**
```bash
# Cek files yang akan di-push
git status

# Cek apakah .env ter-track
git ls-files | findstr "\.env"

# Cek remote
git remote -v

# Cek user config
git config --list | findstr user
```

---

## 🎯 Rekomendasi

### **Untuk Repository Baru:**
1. **Gunakan akun GitHub yang sesuai dengan project**
2. **Set repository sebagai Private jika berisi data sensitif**
3. **Buat README.md yang informatif**
4. **Setup branch protection rules**
5. **Enable security alerts**

### **Untuk Development:**
1. **Selalu gunakan .env.example sebagai template**
2. **Jangan pernah commit file .env asli**
3. **Gunakan environment variables untuk semua kredensial**
4. **Regular backup repository**
5. **Review commits sebelum push**

---

## 📞 Support

Jika mengalami masalah:
1. **Cek dokumentasi GitHub:** https://docs.github.com
2. **Cek .gitignore:** Pastikan file sensitif ter-exclude
3. **Backup dulu:** Sebelum operasi yang berisiko
4. **Test di branch terpisah:** Untuk perubahan besar

**🎉 Selamat! Repository Anda siap di-push dengan aman ke akun GitHub baru!**