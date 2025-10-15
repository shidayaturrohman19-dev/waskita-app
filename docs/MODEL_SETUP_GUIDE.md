# Panduan Setup Model Machine Learning

Dokumen ini menjelaskan cara mengkonfigurasi dan mendapatkan model machine learning yang diperlukan untuk aplikasi Waskita.

## 📋 Model yang Diperlukan

Aplikasi Waskita memerlukan 4 file model untuk berfungsi dengan baik:

### 1. Word2Vec Model
- **File**: `models/embeddings/wiki_word2vec_csv_updated.model`
- **Fungsi**: Preprocessing teks menjadi vektor numerik
- **Format**: Gensim Word2Vec model
- **Ukuran**: ~500MB - 1GB

### 2. Naive Bayes Models (3 model)
- **File 1**: `models/navesbayes/naive_bayes_model1.pkl`
- **File 2**: `models/navesbayes/naive_bayes_model2.pkl`
- **File 3**: `models/navesbayes/naive_bayes_model3.pkl`
- **Fungsi**: Klasifikasi teks sebagai Radikal/Non-Radikal
- **Format**: Scikit-learn pickle files
- **Ukuran**: ~10-50MB per file

## 🔧 Cara Setup

### Langkah 1: Buat Folder Models
```bash
# Folder sudah dibuat otomatis saat clone repository
# Struktur folder:
models/
├── embeddings/
│   └── .gitkeep
└── navesbayes/
    └── .gitkeep
```

### Langkah 2: Dapatkan File Model
Ada beberapa cara untuk mendapatkan file model:

#### Opsi A: Hubungi Pengembang (Recommended)
Hubungi pengembang melalui:
- **Email**: waskita.dev@gmail.com
- **Telegram**: @WaskitaDev
- **WhatsApp**: +62-XXX-XXXX-XXXX

#### Opsi B: Download dari Sumber Resmi
Jika tersedia link download resmi, akan diupdate di sini.

#### Opsi C: Train Model Sendiri
Untuk advanced users yang ingin melatih model sendiri:
1. Siapkan dataset training yang sesuai
2. Gunakan script training (akan disediakan di masa depan)
3. Simpan hasil model di folder yang tepat

### Langkah 3: Verifikasi Setup
```bash
# Jalankan aplikasi untuk test
python app.py

# Cek status model di dashboard
# Buka http://127.0.0.1:5000 dan login sebagai admin
```

## 🔍 Troubleshooting

### Error: Model file not found
```
FileNotFoundError: [Errno 2] No such file or directory: 'models/embeddings/wiki_word2vec_csv_updated.model'
```

**Solusi:**
1. Pastikan file model ada di path yang benar
2. Cek konfigurasi path di `.env.local`
3. Hubungi pengembang untuk mendapatkan file model

### Error: Model loading failed
```
Exception: Failed to load Word2Vec model
```

**Solusi:**
1. Pastikan file model tidak corrupt
2. Cek versi Gensim yang digunakan
3. Download ulang file model dari pengembang

### Error: Classification not working
```
AttributeError: 'NoneType' object has no attribute 'predict'
```

**Solusi:**
1. Pastikan semua 3 file Naive Bayes model tersedia
2. Cek format file (.pkl)
3. Restart aplikasi setelah menambah model

## ⚙️ Konfigurasi Environment

File `.env.local` harus berisi path model yang benar:

```env
# Model paths (sudah dikonfigurasi otomatis)
WORD2VEC_MODEL_PATH=models/embeddings/wiki_word2vec_csv_updated.model
NAIVE_BAYES_MODEL1_PATH=models/navesbayes/naive_bayes_model1.pkl
NAIVE_BAYES_MODEL2_PATH=models/navesbayes/naive_bayes_model2.pkl
NAIVE_BAYES_MODEL3_PATH=models/navesbayes/naive_bayes_model3.pkl
```

## 🔒 Keamanan Model

- **Verifikasi Sumber**: Pastikan model berasal dari sumber terpercaya
- **Checksum**: Verifikasi integritas file dengan checksum (akan disediakan)
- **Backup**: Simpan backup model di tempat aman
- **Update**: Update model secara berkala sesuai rekomendasi pengembang

## 📊 Performa Model

### Word2Vec Model
- **Akurasi**: Tergantung dataset training
- **Kecepatan**: ~100-1000 teks/detik
- **Memory**: ~500MB-1GB RAM

### Naive Bayes Models
- **Akurasi**: ~85-95% (tergantung dataset)
- **Kecepatan**: ~1000-10000 teks/detik
- **Memory**: ~10-50MB RAM per model

## 📞 Bantuan

Jika mengalami kesulitan dalam setup model:

1. **Baca dokumentasi** ini dengan teliti
2. **Cek troubleshooting** section di atas
3. **Hubungi pengembang** melalui kontak yang tersedia
4. **Buat issue** di GitHub dengan detail error

---

**Catatan**: Model ML tidak disertakan dalam repository karena ukurannya yang besar dan pertimbangan lisensi. Hubungi pengembang untuk mendapatkan akses.