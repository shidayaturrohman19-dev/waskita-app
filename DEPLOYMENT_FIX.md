# Panduan Perbaikan Deployment - Model Path Issues

## 🚨 Masalah yang Ditemukan

### 1. Path Model Eksternal
- Model saat ini berada di luar folder aplikasi:
  - `d:/Project/apps/embeddings/` 
  - `d:/Project/apps/navesbayes/`
- Path hardcoded Windows tidak kompatibel dengan Docker/Linux
- Container tidak dapat mengakses path eksternal

### 2. Dockerfile dan Docker-compose Tidak Sesuai
- Dockerfile mencoba copy folder `models/` yang tidak ada
- Volume mapping mengarah ke folder yang tidak ada

## 💡 Solusi Rekomendasi

### **Solusi 1: Pindahkan Model ke Dalam Aplikasi (RECOMMENDED)**

#### Langkah 1: Buat Struktur Folder Model
```bash
cd d:\Project\apps\waskita
mkdir models
mkdir models\embeddings
mkdir models\navesbayes
```

#### Langkah 2: Copy Model Files
```bash
# Copy Word2Vec model
copy "d:\Project\apps\embeddings\*" "models\embeddings\"

# Copy Naive Bayes models  
copy "d:\Project\apps\navesbayes\*" "models\navesbayes\"
```

#### Langkah 3: Update config.py
```python
# Model paths - relative to app directory
WORD2VEC_MODEL_PATH = os.getenv('WORD2VEC_MODEL_PATH', 
    os.path.join(os.path.dirname(__file__), 'models', 'embeddings', 'wiki_word2vec_csv_updated.model'))
NAIVE_BAYES_MODEL1_PATH = os.getenv('NAIVE_BAYES_MODEL1_PATH', 
    os.path.join(os.path.dirname(__file__), 'models', 'navesbayes', 'naive_bayes_model1.pkl'))
NAIVE_BAYES_MODEL2_PATH = os.getenv('NAIVE_BAYES_MODEL2_PATH', 
    os.path.join(os.path.dirname(__file__), 'models', 'navesbayes', 'naive_bayes_model2.pkl'))
NAIVE_BAYES_MODEL3_PATH = os.getenv('NAIVE_BAYES_MODEL3_PATH', 
    os.path.join(os.path.dirname(__file__), 'models', 'navesbayes', 'naive_bayes_model3.pkl'))
```

#### Langkah 4: Update .env.example
```env
# Model Paths - relative paths for containerization
WORD2VEC_MODEL_PATH=models/embeddings/wiki_word2vec_csv_updated.model
NAIVE_BAYES_MODEL1_PATH=models/navesbayes/naive_bayes_model1.pkl
NAIVE_BAYES_MODEL2_PATH=models/navesbayes/naive_bayes_model2.pkl
NAIVE_BAYES_MODEL3_PATH=models/navesbayes/naive_bayes_model3.pkl
```

#### Langkah 5: Update Dockerfile
```dockerfile
# Copy project
COPY . .

# Models are now included in the project copy
# No need for separate COPY models/ command

# Create necessary directories
RUN mkdir -p uploads logs static/uploads
```

#### Langkah 6: Update docker-compose.yml
```yaml
web:
  build: .
  container_name: waskita_app
  environment:
    - FLASK_ENV=production
    - DATABASE_URL=postgresql://waskita_user:waskita_password@db:5432/waskita_prod
    - SECRET_KEY=your-production-secret-key-change-this
    - REDIS_URL=redis://redis:6379/0
    # Model paths for container
    - WORD2VEC_MODEL_PATH=/app/models/embeddings/wiki_word2vec_csv_updated.model
    - NAIVE_BAYES_MODEL1_PATH=/app/models/navesbayes/naive_bayes_model1.pkl
    - NAIVE_BAYES_MODEL2_PATH=/app/models/navesbayes/naive_bayes_model2.pkl
    - NAIVE_BAYES_MODEL3_PATH=/app/models/navesbayes/naive_bayes_model3.pkl
  volumes:
    - ./uploads:/app/uploads
    - ./logs:/app/logs
    # Remove models volume mapping - models are now in container
```

### **Solusi 2: External Volume Mounting (Alternative)**

#### Jika ingin tetap memisahkan model dari aplikasi:

```yaml
# docker-compose.yml
web:
  volumes:
    - ./uploads:/app/uploads
    - ./logs:/app/logs
    - ../embeddings:/app/models/embeddings
    - ../navesbayes:/app/models/navesbayes
  environment:
    - WORD2VEC_MODEL_PATH=/app/models/embeddings/wiki_word2vec_csv_updated.model
    - NAIVE_BAYES_MODEL1_PATH=/app/models/navesbayes/naive_bayes_model1.pkl
    - NAIVE_BAYES_MODEL2_PATH=/app/models/navesbayes/naive_bayes_model2.pkl
    - NAIVE_BAYES_MODEL3_PATH=/app/models/navesbayes/naive_bayes_model3.pkl
```

## 🚀 Untuk Hosting Production

### Cloud Deployment (AWS/GCP/Azure)
1. **Upload model files** ke cloud storage (S3, GCS, Azure Blob)
2. **Download models** saat container startup
3. **Environment variables** untuk cloud storage paths

### VPS/Dedicated Server
1. **Copy model files** ke server
2. **Mount volumes** dengan path yang benar
3. **Set environment variables** sesuai server path

## ✅ Verifikasi Deployment

### Test Local Docker
```bash
cd d:\Project\apps\waskita
docker-compose up --build
```

### Check Model Loading
- Akses `http://localhost:5000/dashboard`
- Periksa "Status Sistem" section
- Pastikan semua model "Loaded"

## 📝 Checklist Deployment

- [ ] Model files dipindah ke folder `models/`
- [ ] config.py diupdate dengan path relatif
- [ ] .env.example diupdate
- [ ] Dockerfile dibersihkan
- [ ] docker-compose.yml diupdate
- [ ] Test local Docker build
- [ ] Verifikasi model loading di dashboard
- [ ] Test klasifikasi berfungsi

## 🔒 Security Notes

- **Jangan commit** model files ke Git (file terlalu besar)
- **Gunakan .gitignore** untuk folder models/
- **Download models** saat deployment dari secure storage
- **Encrypt models** jika berisi data sensitif