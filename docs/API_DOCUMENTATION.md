# Waskita API Documentation

## Scraping API Endpoint

### POST /api/v1/scraping/start

Endpoint ini digunakan untuk memulai proses scraping data dari media sosial secara programatis tanpa memerlukan CSRF token.

#### Authentication
- **Method**: API Key
- **Header**: `X-API-Key`
- **Value**: Gunakan nilai dari `WASKITA_API_KEY` di file `.env`

#### Request Headers
```
Content-Type: application/json
X-API-Key: waskita_api_key_2024_secure_token_v1
```

#### Request Body
```json
{
    "platform": "twitter|facebook|instagram|tiktok",
    "keywords": "kata kunci untuk scraping",
    "start_date": "2024-01-01",  // Optional, format: YYYY-MM-DD
    "end_date": "2024-12-31",    // Optional, format: YYYY-MM-DD
    "max_results": 25            // Optional, default: 25, max: 100
}
```

#### Response Success (200)
```json
{
    "success": true,
    "message": "Scraping started successfully",
    "job_id": "4cbe6bc4-1098-4c7d-86d5-ed2ddbd0bd20",
    "run_id": "apify_run_id_here",
    "platform": "twitter",
    "keywords": "test",
    "max_results": 5,
    "results_count": 25,
    "preview_data": [
        {
            "content": "Sample tweet content...",
            "author": "username",
            "created_at": "2024-01-01T10:00:00Z",
            "url": "https://twitter.com/username/status/123456789"
        }
        // ... up to 3 preview results
    ]
}
```

#### Response Error (400)
```json
{
    "success": false,
    "message": "Platform tidak valid. Gunakan: twitter, facebook, instagram, atau tiktok"
}
```

#### Response Error (401)
```json
{
    "success": false,
    "message": "Invalid API key"
}
```

#### Response Error (500)
```json
{
    "success": false,
    "message": "Error message here"
}
```

### Example Usage

#### cURL
```bash
curl -X POST http://localhost:5000/api/v1/scraping/start \
  -H "Content-Type: application/json" \
  -H "X-API-Key: waskita_api_key_2024_secure_token_v1" \
  -d '{
    "platform": "twitter",
    "keywords": "machine learning",
    "max_results": 10
  }'
```

#### PowerShell
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/v1/scraping/start" `
  -Method POST `
  -Headers @{
    "X-API-Key"="waskita_api_key_2024_secure_token_v1"; 
    "Content-Type"="application/json"
  } `
  -Body '{"platform": "twitter", "keywords": "AI", "max_results": 5}'
```

#### Python
```python
import requests

url = "http://localhost:5000/api/v1/scraping/start"
headers = {
    "Content-Type": "application/json",
    "X-API-Key": "waskita_api_key_2024_secure_token_v1"
}
data = {
    "platform": "twitter",
    "keywords": "data science",
    "max_results": 20
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### Security Notes

1. **API Key**: Simpan API key dengan aman dan jangan expose di repository publik
2. **Rate Limiting**: Endpoint ini tidak memiliki rate limiting, gunakan dengan bijak
3. **CSRF Protection**: Endpoint ini exempt dari CSRF protection untuk kemudahan integrasi API
4. **Authentication**: Hanya request dengan API key yang valid yang akan diproses

### Platform Support

- **Twitter**: Scraping tweets berdasarkan keyword
- **Facebook**: Scraping posts publik
- **Instagram**: Scraping posts dan stories publik
- **TikTok**: Scraping video dan komentar publik

### Limitations

- Maximum results per request: 100
- API key harus dikonfigurasi di file `.env`
- Memerlukan konfigurasi Apify API token yang valid
- Data yang di-scrape tergantung pada ketersediaan dan kebijakan platform