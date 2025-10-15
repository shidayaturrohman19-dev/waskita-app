# Batasan Apify Actor untuk Scraping

## Twitter Actor: kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest

### Batasan Akun Gratis
Berdasarkan dokumentasi resmi Apify, actor ini memiliki batasan khusus untuk akun gratis:

1. **Batasan Jumlah Tweet**: Akun gratis dibatasi dalam jumlah tweet yang dapat di-scrape
2. **Batasan 200 Tweet**: Kemungkinan besar batasan default adalah 200 tweet per run untuk akun gratis
3. **Pricing Model**: $0.25 per 1000 tweets untuk akun berbayar

### Solusi untuk Mengatasi Batasan

#### Opsi 1: Upgrade ke Akun Berbayar
- Upgrade akun Apify ke plan berbayar
- Akan menghilangkan batasan 200 tweet
- Biaya: $0.25 per 1000 tweets

#### Opsi 2: Multiple Search Queries (Implementasi Saat Ini)
- Bagi scraping menjadi beberapa query dengan rentang waktu lebih kecil
- Contoh: Bagi per minggu atau per hari jika diperlukan
- Setiap query akan mendapat maksimal 200 tweet

#### Opsi 3: Ganti Actor Twitter
Alternatif actor yang bisa digunakan:
- `apidojo/tweet-scraper` - $0.30 per 1000 tweets
- `clockworks/twitter-scraper` - Gratis dengan batasan
- `vdrmota/twitter-scraper` - Alternatif lain

### Parameter yang Benar untuk Actor Saat Ini

```json
{
  "searchTerms": ["keyword since:2024-01-01 until:2024-01-31"],
  "lang": "in",
  "sort": "Latest"
}
```

### Catatan Penting
- Parameter `maxTweets` tidak didukung oleh actor ini
- Batasan 200 tweet kemungkinan adalah hard limit dari Apify untuk akun gratis
- Untuk mendapatkan lebih dari 200 tweet, perlu upgrade akun atau ganti actor