#!/bin/bash

# Script untuk inisialisasi admin user saat Docker container pertama kali dijalankan
# File: init_admin.sh

echo "=========================================="
echo "Waskita - Inisialisasi Admin User"
echo "=========================================="

# Tunggu database siap
echo "Menunggu database PostgreSQL siap..."
until pg_isready -h db -p 5432 -U waskita_user; do
  echo "Database belum siap, menunggu 2 detik..."
  sleep 2
done

echo "Database siap! Membuat admin user..."

# Jalankan script Python untuk membuat admin user
python /app/create_admin.py

echo "=========================================="
echo "Inisialisasi selesai!"
echo "=========================================="