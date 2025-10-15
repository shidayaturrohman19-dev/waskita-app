# Models Directory

Folder ini berisi model machine learning yang digunakan oleh aplikasi Waskita untuk klasifikasi konten radikal.

## Struktur Folder

```
models/
├── embeddings/
│   └── wiki_word2vec_csv_updated.model  # Model Word2Vec untuk preprocessing text
└── navesbayes/
    ├── naive_bayes_model1.pkl           # Model Naive Bayes untuk klasifikasi
    ├── naive_bayes_model2.pkl           # Model Naive Bayes alternatif
    └── naive_bayes_model3.pkl           # Model Naive Bayes tambahan
```

## File Model yang Diperlukan

### 1. Word2Vec Model
- **File**: `embeddings/wiki_word2vec_csv_updated.model`
- **Fungsi**: Mengkonversi teks menjadi vektor numerik untuk preprocessing
- **Format**: Gensim Word2Vec model

### 2. Naive Bayes Models
- **File**: `navesbayes/naive_bayes_model1.pkl`
- **File**: `navesbayes/naive_bayes_model2.pkl`
- **File**: `navesbayes/naive_bayes_model3.pkl`
- **Fungsi**: Klasifikasi teks sebagai Radikal atau Non-Radikal
- **Format**: Scikit-learn pickle files

## Cara Mendapatkan Model

Model-model ini tidak disertakan dalam repository karena ukurannya yang besar. Untuk mendapatkan model:

1. **Hubungi pengembang** melalui kontak yang tersedia di CONTRIBUTING.md
2. **Download dari sumber resmi** jika tersedia
3. **Train model sendiri** menggunakan dataset yang sesuai

## Konfigurasi

Path model dikonfigurasi di `config.py`:
- `WORD2VEC_MODEL_PATH`
- `NAIVE_BAYES_MODEL1_PATH`
- `NAIVE_BAYES_MODEL2_PATH`
- `NAIVE_BAYES_MODEL3_PATH`

## Catatan Keamanan

- Pastikan model berasal dari sumber terpercaya
- Verifikasi integritas file sebelum digunakan
- Jangan commit file model ke repository (sudah ada di .gitignore)