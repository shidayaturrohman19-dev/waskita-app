# ⚡ Quick Start Guide - Waskita

Panduan cepat untuk memulai development Waskita dalam 5 menit!

## 🎯 Pilih Workflow Anda

### 🛠️ Option 1: Local Development (Recommended untuk Development)
**Cocok untuk:** Development aktif, debugging, testing fitur baru

```bash
# 1. Clone & Setup
git clone https://github.com/kaptenusop/waskita.git
cd waskita
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt

# 2. Setup Database (Otomatis)
python setup_postgresql.py

# 3. Jalankan Aplikasi
python app.py
```

✅ **Selesai!** Aplikasi berjalan di `http://localhost:5000`

**Login:** `admin` / `admin123`

---

### 🐳 Option 2: Docker Deployment (Recommended untuk Production)
**Cocok untuk:** Production deployment, testing environment, demo

```bash
# 1. Clone Repository
git clone https://github.com/kaptenusop/waskita.git
cd waskita

# 2. Docker Build & Run
make fresh-build
# atau: .\fresh-build.ps1 (Windows)
# atau: docker-compose up --build -d
```

✅ **Selesai!** Aplikasi berjalan di `http://localhost:5000`

**Login:** `admin` / `admin123`

---

## 🔄 Hybrid Workflow: Local → Docker

**Untuk development yang kemudian di-deploy:**

```bash
# 1. Development Lokal
git clone https://github.com/kaptenusop/waskita.git
cd waskita
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
python setup_postgresql.py
python app.py  # Develop di sini

# 2. Deploy ke Docker
make build  # Deploy dengan data persistent
```

---

## 📋 Prasyarat

### Untuk Local Development:
- ✅ Python 3.11.x
- ✅ PostgreSQL 15+
- ✅ Git

### Untuk Docker:
- ✅ Docker Desktop
- ✅ Git

---

## 🚀 Next Steps

Setelah aplikasi berjalan:

1. **📖 Baca dokumentasi lengkap:** [dev-to-docker.md](dev-to-docker.md)
2. **🔧 Setup model ML:** [docs/MODEL_SETUP_GUIDE.md](docs/MODEL_SETUP_GUIDE.md)
3. **🔐 Konfigurasi keamanan:** [SECURITY.md](SECURITY.md)
4. **📚 Panduan lengkap:** [docs/USER_GUIDE_LENGKAP.md](docs/USER_GUIDE_LENGKAP.md)

---

## 🆘 Troubleshooting Cepat

### Local Development
```bash
# Database error?
python setup_postgresql.py  # Re-run setup

# Port 5000 sudah digunakan?
# Edit app.py, ganti port ke 5001
```

### Docker
```bash
# Container error?
docker-compose logs web

# Port conflict?
make clean && make build
```

---

## 📞 Bantuan

- **🐛 Issues:** [GitHub Issues](https://github.com/kaptenusop/waskita/issues)
- **📖 Docs:** [docs/](docs/)
- **🔄 Workflow:** [dev-to-docker.md](dev-to-docker.md)

**🎉 Happy Coding!**