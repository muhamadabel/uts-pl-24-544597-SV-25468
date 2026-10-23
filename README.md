# UTS Konstruksi & Evolusi Perangkat Lunak (SVPL261501)
**Nama:** Muhammad Abel Abhinaya Riananto  
**NIM:** 24/544597/SV/25468 (NIU: 544597)  
**Program Studi:** D4 Teknologi Rekayasa Perangkat Lunak  
**Departemen:** Teknik Elektro dan Informatika, Sekolah Vokasi, Universitas Gadjah Mada  
**Tema:** Sistem Manajemen Katalog Produk Toko

---

## Deskripsi Sistem
Sistem manajemen katalog produk toko ritel berbasis arsitektur decoupled (SPA + RESTful API):
- **Backend:** Laravel 11 dengan autentikasi token Laravel Sanctum dan server aplikasi modern FrankenPHP (Caddy engine).
- **Frontend:** Vue.js 3 + Vite dengan Axios interceptor dan reverse proxy Nginx multi-stage build.
- **Database:** MySQL 8.0 dengan persistensi Docker named volume.
- **CI/CD:** GitHub Actions dengan automated test Laravel, build Vue.js, dan continuous deployment ke GitHub Container Registry (GHCR).

---

## Menjalankan Sistem (Docker Compose)

### 1. Salin Konfigurasi Environment
```bash
cp .env.example .env
```

### 2. Jalankan Seluruh Container
```bash
docker compose up -d --build
```
*(Seluruh migrasi basis data dan seeding 6 produk sampel otomatis dijalankan pada saat container backend melakukan booting pertama kali).*

### 3. Akses Aplikasi
- **Frontend Web UI:** [http://localhost:3000](http://localhost:3000)
- **Backend API:** [http://localhost:8000/api](http://localhost:8000/api)
- **Akun Default Petugas Toko:**
  - Email: `admin@toko.local`
  - Password: `password123`

---

## Pengujian Otomatis

### Backend Feature Tests (10 Skenario Uji)
```bash
cd backend
php artisan test
```

### Frontend Build
```bash
cd frontend
npm ci
npm run build
```
