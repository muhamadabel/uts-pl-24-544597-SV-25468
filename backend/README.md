# Backend API - Katalog Produk Toko (Laravel 11 + FrankenPHP)

Modul backend berbasis RESTful API untuk Sistem Manajemen Katalog Produk Toko.

## Fitur Utama
1. **Autentikasi Token (Laravel Sanctum):**
   - `POST /api/login` (kredensial email & password, mengembalikan Bearer token)
   - `POST /api/logout` (mencabut token aktif, terproteksi)
   - `GET /api/user` (mendapatkan profil pengguna aktif, terproteksi)
2. **Resource CRUD Produk Toko (`/api/products`):**
   - `GET /api/products` (tampil semua dengan dukungan filter kategori dan pencarian)
   - `GET /api/products/{id}` (tampil detail satu produk)
   - `POST /api/products` (tambah produk baru, mengembalikan HTTP 201 Created)
   - `PUT /api/products/{id}` (perbarui data produk, mengembalikan HTTP 200 OK)
   - `DELETE /api/products/{id}` (hapus data produk, mengembalikan HTTP 200 OK)
3. **Kode Status HTTP Standar:**
   - `201 Created` saat data berhasil dibuat
   - `422 Unprocessable Content` saat validasi input gagal
   - `401 Unauthorized` saat request tidak menyertakan Bearer token valid
4. **Server Modern FrankenPHP (Bonus Nilai +10):**
   - Menjalankan Laravel menggunakan Caddy engine bawaan FrankenPHP.

## Menjalankan Pengujian Otomatis
```bash
php artisan test
```
Seluruh 10 skenario feature test diuji menggunakan SQLite in-memory database sehingga tidak memerlukan database eksternal dan dapat berjalan secara terisolasi pada CI pipeline.
