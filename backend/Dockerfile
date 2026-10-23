# Dockerfile untuk backend Laravel dengan FrankenPHP (Soal 5a & Soal 7 Bonus +10)
# Menggunakan image resmi dengan tag versi jelas (bukan latest)
FROM dunglas/frankenphp:1.4-php8.3

# Pasang ekstensi PHP yang dibutuhkan Laravel
RUN install-php-extensions \
    pdo_mysql \
    bcmath \
    intl \
    zip \
    opcache

# Salin binary composer dari image resmi
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /app

# PENTING (Docker Layer Cache): Salin composer.json & composer.lock
# dan pasang dependensi SEBELUM menyalin seluruh kode aplikasi (Soal 5a)
COPY composer.json composer.lock ./
RUN composer install --no-dev --optimize-autoloader --no-scripts --no-autoloader

# Salin seluruh kode aplikasi (tanpa .env / secrets)
COPY . .

# Generate autoloader teroptimasi setelah kode aplikasi ada
RUN composer dump-autoload --optimize

# Konfigurasi permission storage, cache, dan entrypoint script
RUN chown -R www-data:www-data storage bootstrap/cache \
    && chmod -R 775 storage bootstrap/cache \
    && chmod +x /app/docker-entrypoint.sh

# Atur variabel lingkungan FrankenPHP agar melayani port 8000
ENV SERVER_NAME=":8000"

EXPOSE 8000

# Server aplikasi dijalankan memakai FrankenPHP via entrypoint script (Soal 7)
ENTRYPOINT ["/app/docker-entrypoint.sh"]
