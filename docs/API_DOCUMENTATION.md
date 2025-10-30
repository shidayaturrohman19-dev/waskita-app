# 🚀 API DOCUMENTATION - WASKITA

**Waskita REST API** menyediakan akses programatis ke sistem klasifikasi konten media sosial dengan teknologi Machine Learning. API ini mendukung autentikasi, upload data, web scraping, klasifikasi AI, dan export hasil.

---

## 📋 DAFTAR ISI

1. [Informasi Umum](#informasi-umum)
2. [Autentikasi](#autentikasi)
3. [Endpoint Dashboard](#endpoint-dashboard)
4. [Endpoint Data Management](#endpoint-data-management)
5. [Endpoint Web Scraping](#endpoint-web-scraping)
6. [Endpoint Klasifikasi AI](#endpoint-klasifikasi-ai)
7. [Endpoint Admin](#endpoint-admin)
8. [Endpoint Sistem](#endpoint-sistem)
9. [Error Handling](#error-handling)
10. [Rate Limiting](#rate-limiting)

---

## 🌐 INFORMASI UMUM

### Base URL
```
http://localhost:5000
```

### Content Type
```
Content-Type: application/json
```

### Response Format
Semua response menggunakan format JSON dengan struktur:
```json
{
  "status": "success|error",
  "message": "Pesan response",
  "data": {...},
  "timestamp": "2024-01-01T00:00:00Z"
}
```

---

## 🔐 AUTENTIKASI

### Login
**POST** `/login`

Login ke sistem dengan username dan password.

**Request Body:**
```json
{
  "username": "[username]",
  "password": "[password]",
  "remember": false
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Login berhasil",
  "data": {
    "user_id": "[user_id]",
    "username": "[username]",
    "role": "[role]",
    "last_login": "[timestamp]"
  }
}
```

### Logout
**GET** `/logout`

Logout dari sistem dan hapus session.

**Response:**
```json
{
  "status": "success",
  "message": "Logout berhasil"
}
```

### Registrasi OTP
**POST** `/otp/register-request`

Daftar akun baru dengan verifikasi OTP email.

**Request Body:**
```json
{
  "username": "[new_username]",
  "email": "[user@example.com]",
  "password": "[password]",
  "confirm_password": "[password]",
  "full_name": "[Full Name]",
  "organization": "[Organization Name]"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "OTP telah dikirim ke email Anda",
  "data": {
    "request_id": "[request_id]",
    "email": "[user@example.com]",
    "expires_at": "[timestamp]"
  }
}
```

---

## 📊 ENDPOINT DASHBOARD

### Dashboard Statistics
**GET** `/dashboard`

Mendapatkan statistik dashboard utama.

**Response:**
```json
{
  "status": "success",
  "data": {
    "statistics": {
      "total_upload": "[Dinamis]",
      "total_scraping": "[Dinamis]",
      "total_cleaned": "[Dinamis]",
      "total_classified": "[Dinamis]"
    },
    "platform_distribution": {
      "Twitter": "[%]",
      "Facebook": "[%]",
      "Instagram": "[%]",
      "TikTok": "[%]"
    },
    "recent_activities": [
      {
        "id": "[id]",
        "user": "[username]",
        "action": "[Action Type]",
        "timestamp": "[timestamp]",
        "details": "[Activity details]"
      }
    ],
    "system_status": {
      "word2vec_model": "[status]",
      "naive_bayes_models": "[X/X]",
      "database": "[status]"
    }
  }
}
```

---

## 📁 ENDPOINT DATA MANAGEMENT

### Upload Dataset
**POST** `/data/upload`

Upload file CSV/XLSX untuk klasifikasi.

**Request (multipart/form-data):**
```
file: [CSV/XLSX file]
dataset_name: "[Dataset Name]"
description: "[Dataset description]"
```

**Response:**
```json
{
  "status": "success",
  "message": "File berhasil diupload",
  "data": {
    "upload_id": "[upload_id]",
    "filename": "[filename.csv]",
    "total_records": "[count]",
    "duplicates_found": "[count]",
    "valid_records": "[count]"
  }
}
```

### Get Raw Data
**GET** `/api/raw_data`

Mendapatkan daftar data mentah yang diupload.

**Query Parameters:**
- `page`: Nomor halaman (default: 1)
- `per_page`: Jumlah data per halaman (default: [X])
- `search`: Kata kunci pencarian

**Response:**
```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": "[id]",
        "content": "[Contoh teks konten]",
        "username": "[username]",
        "url": "[https://example.com]",
        "platform": "[Platform]",
        "created_at": "[timestamp]"
      }
    ],
    "pagination": {
      "page": "[page]",
      "per_page": "[per_page]",
      "total": "[total]",
      "pages": "[pages]"
    }
  }
}
```

### Delete Raw Data
**DELETE** `/api/raw_data/<int:data_id>`

Hapus data mentah berdasarkan ID.

**Response:**
```json
{
  "status": "success",
  "message": "Data berhasil dihapus"
}
```

### Bulk Delete Data
**POST** `/api/dataset/bulk_delete`

Hapus multiple data sekaligus.

**Request Body:**
```json
{
  "data_ids": "[1, 2, 3, 4, 5]",
  "data_type": "[data_type]"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "[X] data berhasil dihapus"
}
```

---

## 🕷️ ENDPOINT WEB SCRAPING

### Start Scraping
**POST** `/start_scraping`

Memulai proses web scraping dari media sosial.

**Request Body:**
```json
{
  "platform": "twitter",
  "keyword": "machine learning",
  "max_results": 100,
  "date_from": "2024-01-01",
  "date_to": "2024-01-31",
  "dataset_name": "ML Research Data"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Scraping dimulai",
  "data": {
    "job_id": 456,
    "run_id": "scrape_20240101_123456",
    "platform": "twitter",
    "estimated_time": "5-10 minutes"
  }
}
```

### Scraping Progress
**GET** `/api/scraping/progress/<run_id>`

Monitor progress scraping real-time.

**Response:**
```json
{
  "status": "success",
  "data": {
    "run_id": "scrape_20240101_123456",
    "status": "running",
    "progress": 65,
    "current_step": "Processing results",
    "total_found": 85,
    "processed": 55,
    "estimated_remaining": "2 minutes"
  }
}
```

### Scraping Statistics
**GET** `/api/scraping/statistics`

Statistik scraping keseluruhan.

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_jobs": 25,
    "successful_jobs": 22,
    "failed_jobs": 3,
    "total_scraped": 5000,
    "platform_breakdown": {
      "Twitter": 2000,
      "Facebook": 1500,
      "Instagram": 1000,
      "TikTok": 500
    }
  }
}
```

### Map Scraping Data
**POST** `/api/scraping/map-data`

Mapping hasil scraping ke format yang diinginkan.

**Request Body:**
```json
{
  "job_id": 456,
  "mapping": {
    "username_field": "author.username",
    "content_field": "text",
    "url_field": "url",
    "date_field": "createdAt"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Data berhasil dimapping",
  "data": {
    "mapped_records": 85,
    "saved_records": 80,
    "duplicates_skipped": 5
  }
}
```

---

## 🧠 ENDPOINT KLASIFIKASI AI

### Manual Text Classification
**POST** `/api/classify_manual_text`

Klasifikasi teks manual menggunakan AI.

**Request Body:**
```json
{
  "text": "Contoh teks yang akan diklasifikasi",
  "models": ["model1", "model2", "model3"]
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "text": "Contoh teks yang akan diklasifikasi",
    "results": {
      "model1": {
        "prediction": "Non-Radikal",
        "probability_radikal": 0.25,
        "probability_non_radikal": 0.75,
        "confidence": "high"
      },
      "model2": {
        "prediction": "Non-Radikal",
        "probability_radikal": 0.30,
        "probability_non_radikal": 0.70,
        "confidence": "medium"
      },
      "model3": {
        "prediction": "Non-Radikal",
        "probability_radikal": 0.20,
        "probability_non_radikal": 0.80,
        "confidence": "high"
      }
    },
    "consensus": {
      "final_prediction": "Non-Radikal",
      "agreement_score": 1.0,
      "average_confidence": 0.75
    }
  }
}
```

### Batch Classification
**POST** `/api/classify_data`

Klasifikasi batch data menggunakan AI.

**Request Body:**
```json
{
  "data_type": "clean_data",
  "data_ids": [1, 2, 3, 4, 5],
  "models": ["model1", "model2", "model3"]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Klasifikasi batch dimulai",
  "data": {
    "job_id": "classify_20240101_123456",
    "total_items": 5,
    "estimated_time": "2-3 minutes"
  }
}
```

### Classification Results
**GET** `/api/classification_results`

Mendapatkan hasil klasifikasi.

**Query Parameters:**
- `page`: Nomor halaman
- `per_page`: Jumlah data per halaman
- `filter`: Filter berdasarkan prediksi (radikal/non-radikal)

**Response:**
```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "content": "Teks yang diklasifikasi",
        "model1_prediction": "Non-Radikal",
        "model1_prob_radikal": 0.25,
        "model1_prob_non_radikal": 0.75,
        "model2_prediction": "Non-Radikal",
        "model2_prob_radikal": 0.30,
        "model2_prob_non_radikal": 0.70,
        "model3_prediction": "Non-Radikal",
        "model3_prob_radikal": 0.20,
        "model3_prob_non_radikal": 0.80,
        "created_at": "2024-01-01T10:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 50,
      "total": 200,
      "pages": 4
    }
  }
}
```

### Export Classification Results
**POST** `/api/export/classification-results`

Export hasil klasifikasi ke CSV/Excel.

**Request Body:**
```json
{
  "format": "csv",
  "include_probabilities": true,
  "filter": {
    "prediction": "all",
    "date_from": "2024-01-01",
    "date_to": "2024-01-31"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Export berhasil",
  "data": {
    "download_url": "/downloads/classification_results_20240101.csv",
    "filename": "classification_results_20240101.csv",
    "total_records": 500,
    "file_size": "2.5 MB"
  }
}
```

### Model Performance
**GET** `/api/model_performance`

Mendapatkan performa model AI.

**Response:**
```json
{
  "status": "success",
  "data": {
    "model1": {
      "name": "Naive Bayes Model 1",
      "accuracy": 0.89,
      "precision": 0.87,
      "recall": 0.91,
      "f1_score": 0.89,
      "total_predictions": 1500
    },
    "model2": {
      "name": "Naive Bayes Model 2",
      "accuracy": 0.91,
      "precision": 0.90,
      "recall": 0.92,
      "f1_score": 0.91,
      "total_predictions": 1500
    },
    "model3": {
      "name": "Naive Bayes Model 3",
      "accuracy": 0.88,
      "precision": 0.86,
      "recall": 0.90,
      "f1_score": 0.88,
      "total_predictions": 1500
    },
    "ensemble": {
      "accuracy": 0.93,
      "consensus_rate": 0.85
    }
  }
}
```

---

## 📈 ENDPOINT DATASET MANAGEMENT

### Create Dataset
**POST** `/dataset/management`

Membuat dataset baru.

**Request Body:**
```json
{
  "name": "Dataset Penelitian",
  "description": "Dataset untuk penelitian klasifikasi konten",
  "category": "research"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Dataset berhasil dibuat",
  "data": {
    "dataset_id": 789,
    "name": "Dataset Penelitian",
    "created_at": "2024-01-01T10:00:00Z"
  }
}
```

### Dataset Details
**GET** `/api/dataset/<int:dataset_id>/details`

Mendapatkan detail dataset lengkap.

**Response:**
```json
{
  "status": "success",
  "data": {
    "dataset": {
      "id": 789,
      "name": "Dataset Penelitian",
      "description": "Dataset untuk penelitian klasifikasi konten",
      "created_at": "2024-01-01T10:00:00Z"
    },
    "statistics": {
      "raw_data_count": 500,
      "cleaned_data_count": 480,
      "classified_data_count": 450
    },
    "raw_data": [
      {
        "id": 1,
        "content": "Teks mentah",
        "username": "user123",
        "platform": "Twitter"
      }
    ],
    "cleaned_data": [
      {
        "id": 1,
        "original_content": "Teks mentah",
        "cleaned_content": "teks mentah",
        "cleaning_applied": ["remove_emoji", "lowercase"]
      }
    ],
    "classification_results": [
      {
        "id": 1,
        "content": "teks mentah",
        "prediction": "Non-Radikal",
        "probability": 0.85
      }
    ]
  }
}
```

### Clean Dataset
**POST** `/api/dataset/<int:dataset_id>/clean`

Membersihkan data dalam dataset.

**Request Body:**
```json
{
  "cleaning_options": {
    "remove_emoji": true,
    "remove_urls": true,
    "remove_mentions": true,
    "lowercase": true,
    "remove_special_chars": true
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Data cleaning dimulai",
  "data": {
    "job_id": "clean_20240101_123456",
    "total_items": 500,
    "estimated_time": "3-5 minutes"
  }
}
```

### Classify Dataset
**POST** `/api/dataset/<int:dataset_id>/classify`

Klasifikasi semua data dalam dataset.

**Request Body:**
```json
{
  "models": ["model1", "model2", "model3"],
  "batch_size": 100
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Klasifikasi dataset dimulai",
  "data": {
    "job_id": "classify_dataset_20240101_123456",
    "total_items": 480,
    "estimated_time": "10-15 minutes"
  }
}
```

### Delete Dataset
**DELETE** `/api/dataset/<int:dataset_id>`

Hapus dataset beserta semua data terkait.

**Response:**
```json
{
  "status": "success",
  "message": "Dataset berhasil dihapus"
}
```

---

## 👨‍💼 ENDPOINT ADMIN

### Registration Statistics
**GET** `/api/registration-stats`

Statistik registrasi pengguna (Admin only).

**Response:**
```json
{
  "status": "success",
  "data": {
    "pending": 5,
    "approved": 25,
    "rejected": 3,
    "expired": 2,
    "total": 35,
    "recent": 8
  }
}
```

### User Management
**GET** `/api/admin/users`

Daftar semua pengguna (Admin only).

**Response:**
```json
{
  "status": "success",
  "data": {
    "users": [
      {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin",
        "is_active": true,
        "last_login": "2024-01-01T10:00:00Z",
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

### Create User
**POST** `/api/admin/users`

Buat pengguna baru (Admin only).

**Request Body:**
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "password123",
  "role": "user",
  "full_name": "New User"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Pengguna berhasil dibuat",
  "data": {
    "user_id": 10,
    "username": "newuser"
  }
}
```

### Update User
**PUT** `/api/admin/users/<int:user_id>`

Update data pengguna (Admin only).

**Request Body:**
```json
{
  "email": "updated@example.com",
  "role": "admin",
  "is_active": true
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Data pengguna berhasil diupdate"
}
```

### Delete User
**DELETE** `/api/admin/users/<int:user_id>`

Hapus pengguna (Admin only).

**Response:**
```json
{
  "status": "success",
  "message": "Pengguna berhasil dihapus"
}
```

---

## 🔧 ENDPOINT SISTEM

### Health Check
**GET** `/api/health`

Cek status kesehatan sistem.

**Response:**
```json
{
  "status": "success",
  "data": {
    "system": "healthy",
    "database": "connected",
    "models": {
      "word2vec": "loaded",
      "naive_bayes": "3/3 loaded"
    },
    "memory_usage": "45%",
    "disk_usage": "60%",
    "uptime": "5 days, 10 hours"
  }
}
```

### System Status
**GET** `/api/status`

Status detail sistem dan komponen.

**Response:**
```json
{
  "status": "success",
  "data": {
    "application": {
      "name": "Waskita",
      "version": "1.0.0",
      "environment": "production"
    },
    "database": {
      "status": "connected",
      "total_records": 15000,
      "last_backup": "2024-01-01T02:00:00Z"
    },
    "machine_learning": {
      "word2vec_model": {
        "status": "loaded",
        "vocabulary_size": 50000,
        "vector_size": 300
      },
      "naive_bayes_models": {
        "model1": "loaded",
        "model2": "loaded", 
        "model3": "loaded"
      }
    },
    "external_services": {
      "apify_api": "connected",
      "email_service": "connected"
    }
  }
}
```

---

## ❌ ERROR HANDLING

### Error Response Format
```json
{
  "status": "error",
  "message": "Deskripsi error",
  "error_code": "ERROR_CODE",
  "details": {
    "field": "Specific error details"
  },
  "timestamp": "2024-01-01T10:00:00Z"
}
```

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request berhasil |
| 201 | Created - Resource berhasil dibuat |
| 400 | Bad Request - Request tidak valid |
| 401 | Unauthorized - Tidak terautentikasi |
| 403 | Forbidden - Tidak memiliki akses |
| 404 | Not Found - Resource tidak ditemukan |
| 422 | Unprocessable Entity - Validasi gagal |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Error server |

### Common Error Codes

| Error Code | Description |
|------------|-------------|
| `INVALID_CREDENTIALS` | Username/password salah |
| `INSUFFICIENT_PERMISSIONS` | Tidak memiliki permission |
| `VALIDATION_ERROR` | Data input tidak valid |
| `FILE_TOO_LARGE` | File melebihi batas ukuran |
| `UNSUPPORTED_FORMAT` | Format file tidak didukung |
| `MODEL_NOT_LOADED` | Model AI belum dimuat |
| `RATE_LIMIT_EXCEEDED` | Melebihi batas request |
| `EXTERNAL_API_ERROR` | Error dari API eksternal |

---

## ⚡ RATE LIMITING

### Limits per User Role

| Role | Requests per Hour | Requests per Day |
|------|-------------------|------------------|
| Admin | Unlimited | Unlimited |
| User | 200 | 500 |
| Guest | 50 | 100 |

### Rate Limit Headers
```
X-RateLimit-Limit: 200
X-RateLimit-Remaining: 150
X-RateLimit-Reset: 1640995200
```

### Rate Limit Exceeded Response
```json
{
  "status": "error",
  "message": "Rate limit exceeded",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "details": {
    "limit": 200,
    "remaining": 0,
    "reset_time": "2024-01-01T11:00:00Z"
  }
}
```

---

## 📝 CONTOH PENGGUNAAN

### Python Example
```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:5000"

# Login
login_data = {
    "username": "admin",
    "password": "admin123"
}
response = requests.post(f"{BASE_URL}/login", json=login_data)
session = requests.Session()

# Upload dataset
files = {'file': open('dataset.csv', 'rb')}
data = {
    'dataset_name': 'Test Dataset',
    'description': 'Dataset untuk testing'
}
response = session.post(f"{BASE_URL}/data/upload", files=files, data=data)

# Classify text
classify_data = {
    "text": "Contoh teks untuk klasifikasi",
    "models": ["model1", "model2", "model3"]
}
response = session.post(f"{BASE_URL}/api/classify_manual_text", json=classify_data)
result = response.json()
print(f"Prediction: {result['data']['consensus']['final_prediction']}")
```

### JavaScript Example
```javascript
// Login
const loginResponse = await fetch('/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'admin',
        password: 'admin123'
    })
});

// Get dashboard statistics
const dashboardResponse = await fetch('/dashboard');
const dashboardData = await dashboardResponse.json();
console.log('Total Upload:', dashboardData.data.statistics.total_upload);

// Classify text
const classifyResponse = await fetch('/api/classify_manual_text', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        text: 'Contoh teks untuk klasifikasi',
        models: ['model1', 'model2', 'model3']
    })
});
const classifyResult = await classifyResponse.json();
console.log('Prediction:', classifyResult.data.consensus.final_prediction);
```

---

## 🔒 KEAMANAN API

### Authentication
- Session-based authentication dengan CSRF protection
- Rate limiting per user dan IP address
- Input validation dan sanitization
- SQL injection protection

### Security Headers
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

### File Upload Security
- MIME type validation
- File size limits (50MB max)
- Virus scanning
- Secure filename generation

---

## 📞 DUKUNGAN

### Bantuan Teknis
- **Email**: [api-support@waskita.com](mailto:api-support@waskita.com)
- **Documentation**: Lihat folder `docs/` untuk panduan lengkap
- **GitHub Issues**: Report bug di repository GitHub

### API Versioning
- **Current Version**: v1
- **Deprecation Policy**: 6 bulan notice sebelum deprecated
- **Backward Compatibility**: Maintained untuk 1 tahun

---

**🎉 Selamat menggunakan Waskita API! Sistem klasifikasi konten media sosial yang powerful dan aman.**