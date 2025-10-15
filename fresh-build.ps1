# fresh-build.ps1
# Script untuk melakukan fresh build Docker dengan menghapus semua data
# WARNING: Script ini akan menghapus SEMUA data yang ada!

param(
    [switch]$Force,
    [switch]$Help
)

if ($Help) {
    Write-Host "=== FRESH BUILD SCRIPT ===" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Script ini akan melakukan fresh build Docker dengan menghapus SEMUA data."
    Write-Host ""
    Write-Host "Parameter:"
    Write-Host "  -Force    : Skip konfirmasi, langsung eksekusi"
    Write-Host "  -Help     : Tampilkan bantuan ini"
    Write-Host ""
    Write-Host "Contoh penggunaan:"
    Write-Host "  .\fresh-build.ps1         # Normal dengan konfirmasi"
    Write-Host "  .\fresh-build.ps1 -Force  # Langsung eksekusi tanpa konfirmasi"
    Write-Host ""
    exit 0
}

Write-Host "=== WASKITA FRESH BUILD SCRIPT ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "WARNING: Script ini akan menghapus SEMUA data berikut:" -ForegroundColor Red
Write-Host "- Volume postgres_data (DATABASE)" -ForegroundColor Yellow
Write-Host "- Semua container yang sedang berjalan" -ForegroundColor Yellow
Write-Host ""

if (-not $Force) {
    $confirmation = Read-Host "Apakah Anda yakin ingin melanjutkan? (y/N)"
    if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
        Write-Host "Operasi dibatalkan." -ForegroundColor Green
        exit 0
    }
}

Write-Host ""
Write-Host "=== MEMULAI FRESH BUILD ===" -ForegroundColor Green

# Step 1: Stop dan hapus semua container
Write-Host "1. Menghentikan dan menghapus container..." -ForegroundColor Yellow
docker-compose down --volumes --remove-orphans
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Gagal menghentikan container" -ForegroundColor Red
    exit 1
}

# Step 2: Hapus volume database
Write-Host "2. Menghapus volume database..." -ForegroundColor Yellow
docker volume rm waskita_postgres_data -f 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   Volume database berhasil dihapus" -ForegroundColor Green
} else {
    Write-Host "   Volume database tidak ditemukan atau sudah dihapus" -ForegroundColor Gray
}

# Step 3: Build dan jalankan container
Write-Host "3. Building dan menjalankan container..." -ForegroundColor Yellow
$env:CREATE_SAMPLE_DATA = "true"
docker-compose up --build -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Gagal build atau menjalankan container" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== FRESH BUILD SELESAI ===" -ForegroundColor Green
Write-Host ""
Write-Host "Aplikasi sedang starting up..." -ForegroundColor Cyan
Write-Host "Tunggu beberapa saat untuk inisialisasi database dan admin user."
Write-Host ""
Write-Host "Akses aplikasi di:" -ForegroundColor White
Write-Host "- Web App: http://localhost:5000" -ForegroundColor Cyan
Write-Host "- Nginx:   http://localhost:80" -ForegroundColor Cyan
Write-Host ""
Write-Host "Default Login:" -ForegroundColor White
Write-Host "- Admin: admin / admin123" -ForegroundColor Green
Write-Host "- User:  testuser / testuser123" -ForegroundColor Green
Write-Host ""
Write-Host "Untuk melihat logs: docker-compose logs -f" -ForegroundColor Gray
Write-Host "Untuk stop: docker-compose down" -ForegroundColor Gray