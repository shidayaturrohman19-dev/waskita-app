# install-build.ps1
# Script instalasi build Waskita yang sederhana dan user-friendly
# Menggantikan fresh-build.ps1 dengan pendekatan yang lebih intuitif

param(
    [switch]$Clean,
    [switch]$Production,
    [switch]$Help
)

if ($Help) {
    Write-Host "=== WASKITA INSTALL BUILD SCRIPT ===" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Script instalasi dan build aplikasi Waskita dengan Docker."
    Write-Host ""
    Write-Host "Parameter:"
    Write-Host "  -Clean       : Bersihkan data lama sebelum build (fresh install)"
    Write-Host "  -Production  : Build untuk production environment"
    Write-Host "  -Help        : Tampilkan bantuan ini"
    Write-Host ""
    Write-Host "Contoh penggunaan:"
    Write-Host "  .\install-build.ps1                # Build normal (development)"
    Write-Host "  .\install-build.ps1 -Clean         # Fresh install dengan data bersih"
    Write-Host "  .\install-build.ps1 -Production    # Build untuk production"
    Write-Host ""
    Write-Host "Setelah instalasi berhasil:"
    Write-Host "  - Akses: http://localhost:5000"
    Write-Host "  - Login: admin / admin123"
    Write-Host ""
    exit 0
}

Write-Host "=== WASKITA INSTALL BUILD ===" -ForegroundColor Cyan
Write-Host ""

# Check Docker installation
Write-Host "Memeriksa Docker installation..." -ForegroundColor Yellow
docker --version > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Docker tidak terinstall atau tidak berjalan!" -ForegroundColor Red
    Write-Host "Silakan install Docker Desktop terlebih dahulu." -ForegroundColor Yellow
    exit 1
}

docker-compose --version > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Docker Compose tidak tersedia!" -ForegroundColor Red
    Write-Host "Silakan install Docker Compose terlebih dahulu." -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Docker dan Docker Compose tersedia" -ForegroundColor Green

# Clean installation if requested
if ($Clean) {
    Write-Host ""
    Write-Host "=== MEMBERSIHKAN INSTALASI LAMA ===" -ForegroundColor Yellow
    Write-Host "Menghentikan container yang berjalan..." -ForegroundColor Gray
    docker-compose down --volumes --remove-orphans 2>$null
    
    Write-Host "Menghapus volume database lama..." -ForegroundColor Gray
    docker volume rm waskita_postgres_data -f 2>$null
    
    Write-Host "✓ Pembersihan selesai" -ForegroundColor Green
}

# Determine environment
$composeFile = "docker-compose.yml"
$envFile = ".env"

if ($Production) {
    Write-Host ""
    Write-Host "=== PRODUCTION BUILD ===" -ForegroundColor Magenta
    $composeFile = "docker-compose.prod.yml"
    $envFile = ".env.production"
    
    if (-not (Test-Path $envFile)) {
        Write-Host "Error: File $envFile tidak ditemukan!" -ForegroundColor Red
        Write-Host "Silakan buat file environment production terlebih dahulu." -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host ""
    Write-Host "=== DEVELOPMENT BUILD ===" -ForegroundColor Blue
}

# Check environment file
if (-not (Test-Path $envFile)) {
    Write-Host "Warning: File $envFile tidak ditemukan!" -ForegroundColor Yellow
    Write-Host "Menggunakan konfigurasi default..." -ForegroundColor Gray
}

# Build and start
Write-Host ""
Write-Host "=== MEMULAI BUILD & INSTALASI ===" -ForegroundColor Green
Write-Host "Building Docker images..." -ForegroundColor Yellow

if ($Production) {
    $env:COMPOSE_FILE = $composeFile
    docker-compose -f $composeFile up --build -d
} else {
    $env:CREATE_SAMPLE_DATA = "true"
    docker-compose up --build -d
}

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Error: Build gagal!" -ForegroundColor Red
    Write-Host "Periksa log error di atas untuk detail masalah." -ForegroundColor Yellow
    exit 1
}

# Wait for services to be ready
Write-Host ""
Write-Host "Menunggu services siap..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check if services are running
Write-Host "Memeriksa status services..." -ForegroundColor Yellow
$containers = docker-compose ps --services --filter "status=running"
if ($containers -match "app" -and $containers -match "db") {
    Write-Host "✓ Services berjalan dengan baik" -ForegroundColor Green
} else {
    Write-Host "Warning: Beberapa services mungkin belum siap" -ForegroundColor Yellow
    Write-Host "Gunakan 'docker-compose logs' untuk memeriksa detail" -ForegroundColor Gray
}

# Success message
Write-Host ""
Write-Host "=== INSTALASI BERHASIL! ===" -ForegroundColor Green
Write-Host ""

if ($Production) {
    Write-Host "🚀 PRODUCTION DEPLOYMENT SIAP" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "Akses aplikasi:"
    Write-Host "- HTTPS: https://yourdomain.com" -ForegroundColor Cyan
    Write-Host "- HTTP:  http://yourdomain.com" -ForegroundColor Cyan
} else {
    Write-Host "🎉 DEVELOPMENT ENVIRONMENT SIAP" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Akses aplikasi:"
    Write-Host "- Web App: http://localhost:5000" -ForegroundColor Cyan
    Write-Host "- Nginx:   http://localhost:80" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Default Login:" -ForegroundColor White
Write-Host "- Username: admin" -ForegroundColor Green
Write-Host "- Password: admin123" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  PENTING: Ubah password default setelah login pertama!" -ForegroundColor Yellow
Write-Host ""

# Useful commands
Write-Host "Commands berguna:" -ForegroundColor White
Write-Host "- Lihat logs:     docker-compose logs -f" -ForegroundColor Gray
Write-Host "- Stop services:  docker-compose down" -ForegroundColor Gray
Write-Host "- Restart:        docker-compose restart" -ForegroundColor Gray
Write-Host "- Status:         docker-compose ps" -ForegroundColor Gray
Write-Host ""

if ($Clean) {
    Write-Host "✨ Fresh installation dengan data bersih berhasil!" -ForegroundColor Green
} else {
    Write-Host "✨ Build berhasil! Aplikasi siap digunakan." -ForegroundColor Green
}