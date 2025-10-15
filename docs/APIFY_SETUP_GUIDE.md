# Panduan Setup Apify API untuk Waskita

## Langkah-langkah Setup Apify API

### 1. Membuat Akun Apify
1. Kunjungi [https://apify.com](https://apify.com)
2. Klik "Sign Up" untuk membuat akun baru
3. Verifikasi email Anda
4. Login ke dashboard Apify

### 2. Mendapatkan API Token
1. Setelah login, kunjungi [https://console.apify.com/settings/integrations](https://console.apify.com/settings/integrations)
2. Di bagian "API tokens", klik "Create new token"
3. Berikan nama untuk token (contoh: "Waskita App")
4. Copy token yang dihasilkan (format: `apify_api_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)

### 3. Konfigurasi Environment Variables

#### Untuk Development (file `.env`):
```bash
# Apify API Configuration
APIFY_API_TOKEN=apify_api_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
APIFY_BASE_URL=https://api.apify.com/v2

# Apify Actor IDs (sudah dikonfigurasi)
APIFY_TWITTER_ACTOR=CJdippxWmn9uRfooo
APIFY_FACEBOOK_ACTOR=apify/facebook-scraper
APIFY_INSTAGRAM_ACTOR=apify/instagram-scraper
APIFY_TIKTOK_ACTOR=clockworks/free-tiktok-scraper
```

#### Untuk Docker (file `.env.docker`):
```bash
# Apify API Configuration
APIFY_API_TOKEN=apify_api_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
APIFY_BASE_URL=https://api.apify.com/v2
```

### 4. Restart Aplikasi
Setelah mengkonfigurasi token:

#### Development:
```bash
# Stop aplikasi jika sedang berjalan
# Restart aplikasi
python app.py
```

#### Docker:
```bash
# Stop containers
docker-compose down

# Rebuild dan restart
docker-compose up -d --build
```

### 5. Testing Scraping
1. Login ke aplikasi Waskita
2. Pergi ke menu "Data Management" > "Scraping Data"
3. Pilih platform (Twitter, Facebook, Instagram, atau TikTok)
4. Masukkan kata kunci
5. Klik "Mulai Scraping"

### Troubleshooting

#### Error: "User was not found or authentication token is not valid"
- **Penyebab**: Token API tidak valid atau belum dikonfigurasi
- **Solusi**: 
  1. Pastikan token sudah benar di file environment
  2. Restart aplikasi setelah mengubah token
  3. Cek apakah token masih aktif di dashboard Apify

#### Error: "Failed to start actor"
- **Penyebab**: Actor ID tidak valid atau tidak tersedia
- **Solusi**:
  1. Cek apakah Actor ID masih aktif di Apify Store
  2. Update Actor ID jika diperlukan

#### Error: "Scraping timeout"
- **Penyebab**: Proses scraping memakan waktu terlalu lama
- **Solusi**:
  1. Kurangi jumlah maksimal hasil
  2. Gunakan kata kunci yang lebih spesifik

### Informasi Penting

#### Biaya Apify
- Apify menggunakan sistem kredit
- Setiap scraping menggunakan kredit berdasarkan jumlah data
- Akun gratis mendapat kredit terbatas per bulan
- Monitor penggunaan kredit di dashboard Apify

#### Batasan Platform
- **Twitter**: Maksimal 100 tweet per request
- **Facebook**: Tergantung pada ketersediaan data publik
- **Instagram**: Maksimal 50 post per request
- **TikTok**: Maksimal 25 video per request

#### Best Practices
1. Gunakan kata kunci yang spesifik untuk hasil yang relevan
2. Batasi jumlah hasil untuk menghemat kredit
3. Monitor penggunaan kredit secara berkala
4. Backup token API di tempat yang aman

### Support
Jika mengalami masalah:
1. Cek log aplikasi untuk detail error
2. Verifikasi konfigurasi environment variables
3. Pastikan koneksi internet stabil
4. Hubungi administrator sistem jika diperlukan