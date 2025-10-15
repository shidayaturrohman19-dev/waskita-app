# Contributing to Waskita

Terima kasih atas minat Anda untuk berkontribusi pada proyek Waskita! 🎉

## 🚀 Cara Berkontribusi

### 1. Fork Repository
```bash
# Fork repository ini melalui GitHub UI
# Kemudian clone fork Anda
git clone https://github.com/your-username/waskita.git
cd waskita
```

### 2. Setup Development Environment
```bash
# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# atau
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup database
python setup_postgresql.py

# Copy environment file
cp .env.example .env.local
```

### 3. Buat Feature Branch
```bash
git checkout -b feature/nama-fitur-anda
# atau
git checkout -b bugfix/nama-bug-yang-diperbaiki
```

### 4. Lakukan Perubahan
- Ikuti coding standards yang ada
- Tambahkan tests untuk fitur baru
- Update dokumentasi jika diperlukan
- Pastikan semua tests pass

### 5. Commit & Push
```bash
git add .
git commit -m "feat: deskripsi singkat perubahan"
git push origin feature/nama-fitur-anda
```

### 6. Buat Pull Request
- Buka GitHub dan buat Pull Request
- Berikan deskripsi yang jelas tentang perubahan
- Link ke issue yang terkait (jika ada)

## 📝 Coding Standards

### Python Code Style
- Gunakan **Black** untuk formatting: `black app/`
- Ikuti **PEP 8** guidelines
- Gunakan **type hints** untuk fungsi baru
- Dokumentasi dengan **docstrings**

### Commit Message Format
```
type(scope): deskripsi singkat

[optional body]

[optional footer]
```

**Types:**
- `feat`: fitur baru
- `fix`: perbaikan bug
- `docs`: perubahan dokumentasi
- `style`: formatting, missing semicolons, etc
- `refactor`: refactoring code
- `test`: menambah atau memperbaiki tests
- `chore`: maintenance tasks

**Contoh:**
```
feat(auth): tambah fitur reset password
fix(scraping): perbaiki error handling untuk API timeout
docs(readme): update installation guide
```

## 🧪 Testing

### Menjalankan Tests
```bash
# Unit tests
python -m pytest tests/

# Dengan coverage
python -m pytest --cov=app tests/

# Test specific file
python -m pytest tests/test_auth.py
```

### Menulis Tests
- Buat test file di folder `tests/`
- Gunakan naming convention: `test_*.py`
- Test semua edge cases
- Mock external dependencies

## 📚 Dokumentasi

### Update Dokumentasi
Jika perubahan Anda mempengaruhi:
- **API**: Update `docs/API_DOCUMENTATION.md`
- **User Guide**: Update `docs/USER_GUIDE_LENGKAP.md`
- **Setup**: Update `README.md`
- **Security**: Update `docs/SECURITY_GUIDE.md`

## 🐛 Melaporkan Bug

### Sebelum Melaporkan Bug
1. Cek apakah bug sudah dilaporkan di [Issues](https://github.com/your-username/waskita/issues)
2. Pastikan Anda menggunakan versi terbaru
3. Coba reproduce bug di environment yang bersih

### Template Bug Report
```markdown
**Deskripsi Bug**
Deskripsi singkat dan jelas tentang bug.

**Langkah Reproduce**
1. Buka halaman '...'
2. Klik pada '....'
3. Scroll ke bawah '....'
4. Lihat error

**Expected Behavior**
Deskripsi tentang apa yang seharusnya terjadi.

**Screenshots**
Jika applicable, tambahkan screenshots.

**Environment:**
- OS: [e.g. Windows 10, Ubuntu 20.04]
- Python Version: [e.g. 3.11.0]
- Browser: [e.g. Chrome 91.0]

**Additional Context**
Tambahkan context lain tentang masalah ini.
```

## 💡 Mengusulkan Fitur

### Template Feature Request
```markdown
**Apakah feature request ini terkait dengan masalah? Jelaskan.**
Deskripsi jelas dan ringkas tentang masalahnya.

**Solusi yang Anda inginkan**
Deskripsi jelas dan ringkas tentang apa yang Anda inginkan.

**Alternatif yang sudah dipertimbangkan**
Deskripsi tentang solusi atau fitur alternatif yang sudah Anda pertimbangkan.

**Additional context**
Tambahkan context atau screenshots lain tentang feature request.
```

## 🔒 Security Issues

Jika Anda menemukan vulnerability keamanan, **JANGAN** buat public issue. 
Hubungi tim development secara private melalui email atau Discord.

## 📞 Bantuan

Butuh bantuan? Hubungi kami melalui:
- **GitHub Discussions**: Untuk pertanyaan umum
- **GitHub Issues**: Untuk bug reports dan feature requests
- **Email**: [your-email@domain.com]

## 🙏 Terima Kasih

Kontribusi Anda sangat berarti untuk pengembangan Waskita. Setiap kontribusi, baik besar maupun kecil, sangat dihargai!

---

**Happy Coding!** 🚀