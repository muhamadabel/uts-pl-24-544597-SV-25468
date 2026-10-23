#!/bin/sh
set -e

echo "=== Memulai Inisialisasi Backend Laravel (FrankenPHP) ==="

# Tunggu sampai service MySQL siap menerima koneksi
echo "Menghubungkan ke basis data MySQL ($DB_HOST:$DB_PORT)..."
while ! php -r "try { new PDO('mysql:host='.getenv('DB_HOST').';port='.getenv('DB_PORT', 3306).';dbname='.getenv('DB_DATABASE'), getenv('DB_USERNAME'), getenv('DB_PASSWORD')); exit(0); } catch (Exception \$e) { exit(1); }"; do
    echo "Menunggu MySQL siap..."
    sleep 2
done

echo "MySQL terhubung! Menjalankan migrasi basis data..."
php artisan migrate --force

echo "Menjalankan seeder awal data produk toko..."
php artisan db:seed --force

echo "Menjalankan server aplikasi FrankenPHP pada port 8000..."
exec frankenphp run --config /app/Caddyfile
