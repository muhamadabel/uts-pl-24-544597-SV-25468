#!/usr/bin/env python3
"""Script untuk menghasilkan Laporan UTS Konstruksi & Evolusi Perangkat Lunak format PDF."""

import pathlib
from PIL import Image as PImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
)

BASE = pathlib.Path(__file__).parent
BUKTI = BASE
OUT = BASE.parent / "laporan"
OUT.mkdir(exist_ok=True)

NIM = "24/544597/SV/25468 (NIU: 544597)"
NAMA = "Muhammad Abel Abhinaya Riananto"
PRODI = "D4 Teknologi Rekayasa Perangkat Lunak"
DEPARTEMEN = "Departemen Teknik Elektro dan Informatika, Sekolah Vokasi UGM"
MATKUL = "Konstruksi dan Evolusi Perangkat Lunak (SVPL261501)"
DOSEN = "Dr. Muhammad Fakhrurrifqi, S.Kom., M.Cs. & Galih Malela Damaraji, S.Pd., M.Eng."
TANGGAL = "15 Oktober 2026"
REPO_ORG = "https://github.com/KEPL2026/uts-p1-544597"
REPO_USER = "https://github.com/muhamadabel/uts-p1-544597"

ss = getSampleStyleSheet()

H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=14, leading=18, spaceAfter=8, textColor=colors.HexColor("#0f172a"))
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=11.5, leading=15, spaceBefore=10, spaceAfter=5, textColor=colors.HexColor("#2563eb"))
H3 = ParagraphStyle("H3", parent=ss["Heading3"], fontSize=10, leading=13.5, spaceBefore=6, spaceAfter=3, textColor=colors.HexColor("#1e293b"))
BODY = ParagraphStyle("BODY", parent=ss["BodyText"], fontSize=9, leading=13, textColor=colors.HexColor("#222222"))
BODY_BOLD = ParagraphStyle("BODY_BOLD", parent=BODY, fontName="Helvetica-Bold")
CAP = ParagraphStyle("CAP", parent=BODY, textColor=colors.HexColor("#555555"), fontSize=8, leading=10.5, spaceBefore=3, spaceAfter=8, alignment=1)
MONO = ParagraphStyle("MONO", parent=ss["Code"], fontName="Courier", fontSize=7.5, leading=10,
                      backColor=colors.HexColor("#f8fafc"), borderPadding=4, spaceBefore=2, spaceAfter=6)

def img(path, cap, w=16.0 * cm):
    p = BUKTI / path
    if not p.exists():
        return [Paragraph(f"[Gambar {path} tidak ditemukan]", CAP)]
    iw, ih = PImage.open(p).size
    h = w * ih / iw
    return [
        KeepTogether([
            Image(str(p), width=w, height=h),
            Paragraph(cap, CAP)
        ])
    ]

def cover():
    return [
        Spacer(1, 2.5 * cm),
        Paragraph(DEPARTEMEN.upper(), ParagraphStyle("dep", parent=BODY, fontSize=11, leading=14, alignment=1, fontName="Helvetica-Bold", textColor=colors.HexColor("#475569"))),
        Paragraph("UNIVERSITAS GADJAH MADA", ParagraphStyle("ugm", parent=BODY, fontSize=13, leading=16, alignment=1, fontName="Helvetica-Bold", textColor=colors.HexColor("#0f172a"))),
        Spacer(1, 1.8 * cm),
        Paragraph("LAPORAN UJIAN TENGAH SEMESTER", ParagraphStyle("j1", parent=H1, fontSize=18, leading=22, alignment=1, textColor=colors.HexColor("#0f172a"))),
        Paragraph("TAHUN AKADEMIK GASAL 2026/2027", ParagraphStyle("j2", parent=BODY, fontSize=12, leading=15, alignment=1, fontName="Helvetica-Bold")),
        Spacer(1, 0.5 * cm),
        Paragraph(MATKUL, ParagraphStyle("j3", parent=BODY, fontSize=11, leading=14, alignment=1, textColor=colors.HexColor("#334155"))),
        Spacer(1, 2.2 * cm),
        Table([
            ["Nama Mahasiswa", ":", NAMA],
            ["NIM / NIU", ":", NIM],
            ["Program Studi", ":", PRODI],
            ["Dosen Pengampu", ":", DOSEN],
            ["Tanggal Ujian", ":", TANGGAL],
            ["Sifat Ujian", ":", "Take Home (Waktu Pengerjaan 10 Hari)"],
            ["Tema Sistem", ":", "Sistem Manajemen Katalog Produk Toko"],
            ["Tautan Repositori", ":", REPO_ORG],
        ], colWidths=[3.5 * cm, 0.4 * cm, 12.1 * cm], style=TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9.5),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1e293b")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ])),
        PageBreak(),
    ]

story = cover()

# 1. Ringkasan & Identitas Sistem
story += [
    Paragraph("1. Ringkasan Sistem dan Identitas Repositori", H1),
    Paragraph(
        "Laporan ini mendokumentasikan implementasi lengkap sistem perangkat lunak untuk Ujian Tengah Semester mata kuliah "
<<<<<<< HEAD
        "Konstruksi dan Evolusi Perangkat Lunak (SVPL261501). Sistem yang dibangun mengadopsi tema <b>Sistem Manajemen Katalog Produk Toko</b> "
        "(entitas <code>Product</code>), yaitu platform inventaris ritel untuk mendata dan mengelola barang dagangan toko (pakaian, alas kaki, "
        "aksesoris, elektronik, dan perlengkapan). Tema ini orisinal dan bebas dari duplikasi tugas-tugas praktikum sebelumnya.",
=======
        "Konstruksi dan Evolusi Perangkat Lunak. Sistem yang dibangun mengadopsi tema <b>Production Gear &amp; Equipment Management "
        "(Sistem Manajemen Inventaris Peralatan Produksi Multimedia)</b>, yaitu platform inventaris peralatan rekaman dan studio (kamera, lensa, pencahayaan, audio, dan stabilizer). "
        "Tema ini orisinal dan berbeda dari tema tugas-tugas praktikum sebelumnya.",
>>>>>>> origin/main
        BODY
    ),
    Spacer(1, 0.2 * cm),
    Table([
        ["Komponen", "Spesifikasi Teknologi", "Keterangan"],
        ["Backend", "Laravel 11, PHP 8.3, Laravel Sanctum", "RESTful API dengan token autentikasi, 10 feature tests"],
        ["App Server", "FrankenPHP v1.4 (Caddy Server Engine)", "Nilai tambahan (+10) pengganti PHP-FPM / artisan serve"],
        ["Frontend", "Vue.js 3, Vite, Axios Client", "Single Page Application (SPA), reactive table & modal CRUD"],
        ["Reverse Proxy", "Nginx 1.27 Alpine", "Serving file statis & proxy pass internal ke backend:8000"],
        ["Database", "MySQL 8.0 Community Server", "Named volume persistence (uts_toko_db_data)"],
        ["CI/CD", "GitHub Actions (.github/workflows/ci.yml)", "Pipeline test, build, dan deploy Docker image ke GHCR"],
        ["Repositori", REPO_ORG, "Publik di GitHub Organization KEPL2026 & Akun Personal"],
    ], colWidths=[2.5 * cm, 6.5 * cm, 7.0 * cm], style=TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ])),
    Spacer(1, 0.4 * cm),
]

# 2. Materi Uji CPMK1 (Soal 1): Backend Laravel RESTful API
story += [
    Paragraph("2. Backend RESTful API &amp; Autentikasi Sanctum (Soal 1 - CPMK 1)", H1),
    Paragraph(
        "Backend dibangun di dalam folder <code>backend/</code> menyediakan antarmuka RESTful API murni berformat JSON. "
        "Sesuai ketentuan butir soal nomor 1:",
        BODY
    ),
    Paragraph("<b>a. Autentikasi Token:</b> Menggunakan Laravel Sanctum. Endpoint login publik (<code>POST /api/login</code>) mengembalikan Bearer token. Seluruh endpoint resource lainnya wajib menyertakan token pada header permintaan (<code>Authorization: Bearer &lt;token&gt;</code>).", BODY),
    Paragraph("<b>b. CRUD Resource:</b> Resource <code>products</code> mengelola entitas produk toko dengan operasi lengkap: tampil semua (<code>GET /api/products</code>), tampil satu (<code>GET /api/products/{id}</code>), tambah (<code>POST /api/products</code>), ubah (<code>PUT /api/products/{id}</code>), dan hapus (<code>DELETE /api/products/{id}</code>).", BODY),
    Paragraph("<b>c. Format JSON &amp; Kode Status HTTP Standar:</b> Seluruh request dan response berformat JSON. Kode status yang dihasilkan: <b>201 Created</b> saat data berhasil dibuat, <b>422 Unprocessable Content</b> saat validasi gagal, dan <b>401 Unauthorized</b> saat token tidak disertakan atau kedaluwarsa.", BODY),
    Paragraph("<b>d. Postman Collection:</b> Kumpulan pengujian endpoint diekspor ke berkas <code>postman/UTS_KEPL_544597_Product_API.postman_collection.json</code> di dalam repositori.", BODY),
    Paragraph("<b>e. Automated Feature Tests:</b> Diimplementasikan 10 feature tests lengkap di <code>tests/Feature/ProductApiTest.php</code> mencakup uji token, validasi, dan operasi CRUD. Seluruh pengujian lulus hijau (10 passed, 41 assertions).", BODY),
    Spacer(1, 0.3 * cm),
]
story += img("ss-artisan-test.png", "Gambar 1. Hasil eksekusi php artisan test: 10 skenario feature test lulus hijau.")
story += img("ss-curl-api.png", "Gambar 2. Bukti respons HTTP API: 401 Unauthorized saat tanpa token, login token, validasi 422, dan 201 Created.")

# 3. Materi Uji CPMK1 (Soal 2): Frontend Vue.js
story += [
    PageBreak(),
    Paragraph("3. Frontend Vue.js &amp; Konsumsi API (Soal 2 - CPMK 1)", H1),
    Paragraph(
        "Aplikasi antarmuka frontend dikembangkan di dalam folder <code>frontend/</code> menggunakan framework Vue.js 3 "
        "dan bundler Vite. Arsitektur antarmuka dirancang bersih, intuitif, dan bebas dari dependensi yang tidak perlu:",
        BODY
    ),
    Paragraph("<b>a. Halaman Login &amp; Token Storage:</b> Komponen <code>LoginView.vue</code> menerima kredensial petugas toko, meminta token ke endpoint <code>/api/login</code>, lalu menyimpannya di <code>localStorage</code> (kunci <code>auth_token</code>). Interceptor Axios secara otomatis menyematkan token ini ke setiap request berikutnya.", BODY),
    Paragraph("<b>b. Operasi CRUD via Axios:</b> Komponen <code>ProductView.vue</code> memanfaatkan instance Axios terpusat (<code>src/api/axios.js</code>) untuk mengambil daftar produk, mengirim produk baru, memperbarui data, dan menghapus produk.", BODY),
    Paragraph("<b>c. Variabel Lingkungan:</b> URL endpoint tidak ditulis mati di dalam komponen, melainkan diatur melalui variabel lingkungan Vite <code>VITE_API_BASE_URL</code> pada berkas <code>.env.example</code> dan <code>.env</code>.", BODY),
    Spacer(1, 0.3 * cm),
]
story += img("ss-browser-ui.png", "Gambar 3. Antarmuka web Vue.js (http://localhost:3000) terhubung secara nyata ke API Laravel.")

# 4. Materi Uji CPMK2 (Soal 3): Manajemen GitHub & CI Pipeline
story += [
    PageBreak(),
    Paragraph("4. Manajemen Repositori GitHub &amp; CI Pipeline (Soal 3 - CPMK 2)", H1),
    Paragraph(
        "Seluruh kode sumber dikelola dalam repositori GitHub <code>uts-p1-544597</code> dengan struktur folder "
        "terpisah: <code>backend/</code> untuk aplikasi Laravel dan <code>frontend/</code> untuk aplikasi Vue.js.",
        BODY
    ),
    Paragraph("<b>a. Strategi Branching:</b> Diterapkan tiga lapis branch: <code>main</code> (produksi), <code>dev</code> (integrasi pengembangan), dan branch fitur <code>feature/product-catalog</code>. Perubahan kode hanya dapat masuk melalui Pull Request.", BODY),
    Paragraph("<b>b. Branch Protection Rules:</b> Perlindungan cabang dipasang pada branch <code>main</code> dan <code>dev</code>. Aturan mewajibkan Pull Request sebelum penggabungan dan status check <b>Backend Test (Laravel)</b> serta <b>Frontend Build (Vue.js)</b> wajib berstatus lulus hijau.", BODY),
    Paragraph("<b>c. Pipeline CI GitHub Actions:</b> Dibuat berkas <code>.github/workflows/ci.yml</code> yang menjalankan job pengujian unit/feature Laravel (<code>php artisan test</code>) dan job build aplikasi frontend (<code>npm ci</code> &amp; <code>npm run build</code>).", BODY),
    Spacer(1, 0.3 * cm),
]
story += img("ss-git-graph.png", "Gambar 4. Riwayat cabang Git (git log --graph --oneline) menunjukkan alur branch feature, dev, dan main.")
story += img("ss-pull-request.png", "Gambar 5. Pull Request dari branch fitur ke dev pada antarmuka GitHub CLI.")
story += img("ss-branch-protection.png", "Gambar 6. Bukti pengaturan Branch Protection pada GitHub yang mewajibkan status check CI lulus.")

# 5. Materi Uji CPMK3 (Soal 4): Continuous Deployment ke GHCR
story += [
    PageBreak(),
    Paragraph("5. Continuous Deployment ke GHCR (Soal 4 - CPMK 3)", H1),
    Paragraph(
        "Pipeline pengiriman otomatis (Continuous Deployment) dikonfigurasi pada workflow GitHub Actions dengan "
        "menambahkan job <code>deploy</code>:",
        BODY
    ),
    Paragraph("<b>a. Aturan Eksekusi Job Deploy:</b> Job deploy hanya berjalan saat terjadi event <code>push</code> pada branch <code>main</code> (menggunakan sintaks kondisi <code>if: github.ref == 'refs/heads/main' &amp;&amp; github.event_name == 'push'</code>). Untuk Pull Request atau branch lainnya, workflow secara otomatis berhenti setelah job pengujian dan build selesai.", BODY),
    Paragraph("<b>b. GitHub Secrets:</b> Kredensial rahasia seperti <code>APP_KEY</code> dan <code>DB_PASSWORD</code> dikonfigurasi melalui GitHub Secrets (Settings &rarr; Secrets and variables &rarr; Actions) sehingga tidak pernah tersimpan di repositori publik.", BODY),
    Paragraph("<b>c. Build &amp; Push ke GHCR:</b> Job deploy membangun image Docker backend dan frontend, kemudian mengunggahnya ke GitHub Container Registry (<code>ghcr.io</code>). Tag image menggunakan nomor commit SHA pendek (<code>sha_short</code>), bukan tag <code>latest</code>, untuk menjamin keterlacakan versi build.", BODY),
    Spacer(1, 0.4 * cm),
    Paragraph("6. Dockerfile Multi-Stage &amp; Keamanan Kontainer (Soal 5 - CPMK 4 &amp; 5)", H1),
    Paragraph(
        "Dockerfile dirancang mengikuti standar keamanan dan efisiensi kontainerisasi modern:",
        BODY
    ),
    Paragraph("<b>a. backend/Dockerfile:</b> Menggunakan image dasar resmi FrankenPHP versi spesifik (<code>dunglas/frankenphp:1.4-php8.3</code>). Berkas <code>composer.json</code> dan <code>composer.lock</code> disalin dan dipasang sebelum kode aplikasi disalin, sehingga memanfaatkan Docker Layer Caching secara optimal.", BODY),
    Paragraph("<b>b. frontend/Dockerfile:</b> Menerapkan <i>multi-stage build</i>. Tahap pertama (<code>node:20.18-alpine</code>) memasang dependensi dan menghasilkan berkas statis (<code>npm run build</code>). Tahap kedua menyajikan berkas hasil kompilasi menggunakan <code>nginx:1.27-alpine</code>. Image produksi akhir bersih tanpa menyertakan <code>node_modules</code>.", BODY),
    Paragraph("<b>c. Berkas .dockerignore &amp; Keamanan Secrets:</b> Setiap folder dilengkapi berkas <code>.dockerignore</code> untuk mengecualikan berkas sensitif (<code>.env</code>, kredensial) dan folder dependensi lokal.", BODY),
    Spacer(1, 0.4 * cm),
]

# 6. Materi Uji CPMK6 & CPMK7 (Soal 6): Docker Compose Orkestrasi
story += [
    PageBreak(),
    Paragraph("7. Orkestrasi Docker Compose (Soal 6 - CPMK 6 &amp; 7)", H1),
    Paragraph(
        "Seluruh sistem berjalan secara utuh dengan satu perintah <code>docker compose up -d --build</code> "
        "melalui berkas konfigurasi <code>docker-compose.yml</code> di akar repositori:",
        BODY
    ),
    Paragraph("<b>a. Tiga Service Terintegrasi:</b> Terdiri atas <code>uts_database</code> (MySQL 8.0), <code>uts_backend</code> (Laravel + FrankenPHP pada port 8000), dan <code>uts_frontend</code> (Vue + Nginx pada port 3000).", BODY),
    Paragraph("<b>b. Service Discovery Internal:</b> Komunikasi antar-kontainer menggunakan nama service dalam Docker Network bridge (<code>uts_toko_network</code>), yaitu backend menghubungi database pada host <code>database:3306</code> dan Nginx meneruskan request API ke host <code>backend:8000</code>.", BODY),
    Paragraph("<b>c. Persistensi Data Volume:</b> Direktori basis data dipetakan ke Docker named volume <code>uts_toko_db_data</code>. Terbukti bahwa saat kontainer dimatikan dan dihapus dengan <code>docker compose down</code> lalu dinyalakan kembali dengan <code>docker compose up -d</code>, seluruh data produk yang dibuat tetap tersimpan utuh.", BODY),
    Paragraph("<b>d. Variabel Lingkungan:</b> Kredensial dibaca dari berkas <code>.env</code> lokal yang tidak di-commit ke Git. Disediakan berkas <code>.env.example</code> sebagai panduan konfigurasi.", BODY),
    Spacer(1, 0.3 * cm),
]
story += img("ss-docker-ps.png", "Gambar 7. Output perintah docker compose ps: ketiga kontainer berstatus aktif dan sehat.")

# 7. Nilai Tambahan FrankenPHP (Soal 7)
story += [
    Spacer(1, 0.2 * cm),
    Paragraph("8. Nilai Tambahan (+10): Implementasi FrankenPHP Application Server (Soal 7)", H1),
    Paragraph(
        "Untuk memenuhi tantangan nilai tambahan, backend Laravel dijalankan menggunakan <b>FrankenPHP</b> sebagai server "
        "aplikasi, menggantikan server bawaan PHP-FPM / Nginx konvensional atau <code>php artisan serve</code>:",
        BODY
    ),
    Paragraph("<b>a. Image Dasar Jelas:</b> Menggunakan tag versi <code>dunglas/frankenphp:1.4-php8.3</code> (bukan latest).", BODY),
    Paragraph("<b>b. Integrasi Compose:</b> Kontainer backend berjalan berdampingan dengan service database dan frontend pada jaringan bridge yang sama.", BODY),
    Paragraph("<b>c. Bukti Eksekusi:</b> Log kontainer backend (<code>docker compose logs backend</code>) menunjukkan server FrankenPHP aktif melayani port 8000 dengan mesin Caddy. Log membuktikan request API dilayani langsung oleh FrankenPHP.", BODY),
    Spacer(1, 0.3 * cm),
]
story += img("ss-frankenphp.png", "Gambar 8. Bukti log kontainer backend membuktikan eksekusi FrankenPHP dan server Caddy pada port 8000.")

# 8. Alur Aliran Data & Kendala Solusi
story += [
    PageBreak(),
    Paragraph("9. Penjelasan Alur Aliran Data (Data Flow)", H1),
    Paragraph(
        "Alur pergerakan data dari pengguna hingga ke penyimpanan basis data berjalan sebagai berikut:",
        BODY
    ),
    Paragraph(
        "<b>1. Interaksi Pengguna (Browser):</b> Pengguna mengakses antarmuka Vue di <code>http://localhost:3000</code>. "
        "Saat formulir tambah produk diisi dan tombol simpan ditekan, fungsi reaktif memicu pustaka Axios Client.",
        BODY
    ),
    Paragraph(
        "<b>2. Reverse Proxy Nginx:</b> Axios mengirimkan permintaan HTTP POST JSON ke path <code>/api/products</code> pada port 3000. "
        "Nginx kontainer frontend menerima permintaan tersebut dan secara transparan meneruskannya ke kontainer <code>backend:8000/api/products</code> "
        "melalui jaringan internal Docker (<code>uts_toko_network</code>), mengeliminasi kendala CORS antar host.",
        BODY
    ),
    Paragraph(
        "<b>3. Pemrosesan FrankenPHP &amp; Laravel Sanctum:</b> Server FrankenPHP menangkap request masuk. Middleware Laravel Sanctum "
        "memvalidasi header <code>Authorization: Bearer &lt;token&gt;</code> terhadap tabel <code>personal_access_tokens</code>. Jika token sah, "
        "request diteruskan ke <code>ProductController@store</code>.",
        BODY
    ),
    Paragraph(
        "<b>4. Validasi &amp; Eloquent ORM:</b> Controller memvalidasi tipe data, keunikan SKU, dan rentang nilai harga serta stok. "
        "Setelah validasi lolos, Eloquent ORM menjalankan query INSERT ke service <code>database:3306</code> (MySQL).",
        BODY
    ),
    Paragraph(
        "<b>5. Persistensi Named Volume:</b> MySQL menulis rekaman data ke dalam filesystem kontainer yang terikat pada Docker named volume "
        "<code>uts_toko_db_data</code> di host fisik.",
        BODY
    ),
    Paragraph(
        "<b>6. Respons JSON &amp; Reactive Update:</b> Laravel merespons dengan status <b>201 Created</b> dan payload JSON produk baru. "
        "Axios menerima data tersebut, memperbarui array reaktif <code>products.value</code> di Vue, dan tabel UI secara otomatis ter-refresh.",
        BODY
    ),
    Spacer(1, 0.4 * cm),
    Paragraph("10. Kendala yang Ditemui dan Solusi Penanganannya", H1),
    Table([
        ["No", "Kendala Teknis", "Penyebab Masalah", "Solusi Penanganan"],
        [
            "1",
            "CORS & Panggilan API Lintas Port",
            "Browser mengakses frontend di port 3000 sementara API di port 8000, menyebabkan pemblokiran Cross-Origin.",
            "Mengonfigurasi blok location /api/ pada nginx.conf frontend sebagai reverse proxy ke http://backend:8000/api/."
        ],
        [
            "2",
            "Permission Storage Laravel dalam Kontainer",
            "FrankenPHP berjalan di bawah pengguna www-data, sehingga gagal menulis log dan session cache.",
            "Menambahkan perintah chown -R www-data:www-data storage bootstrap/cache serta chmod 775 di Dockerfile backend."
        ],
        [
            "3",
            "Docker Layer Caching saat Build",
            "Perubahan kecil pada kode aplikasi menyebabkan composer install dan npm ci diulang dari awal.",
            "Memisahkan COPY composer.json/package.json sebelum COPY . . agar dependensi tersimpan di layer cache Docker."
        ],
        [
            "4",
            "Status 401 saat Permintaan Tanpa Token",
            "Laravel default mengarahkan unauthenticated request ke route web 'login', menghasilkan error route not found 500.",
            "Mendefinisikan exception handler di bootstrap/app.php yang merender respons JSON 401 eksplisit untuk API."
        ],
    ], colWidths=[0.8 * cm, 4.0 * cm, 5.0 * cm, 6.2 * cm], style=TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ])),
]

out_pdf = OUT / f"UTS_{NIM.split('/')[1]}_{NAMA.replace(' ', '')}.pdf"
doc = SimpleDocTemplate(
    str(out_pdf),
    pagesize=A4,
    leftMargin=2.2 * cm,
    rightMargin=2.2 * cm,
    topMargin=2.0 * cm,
    bottomMargin=2.0 * cm,
)
doc.build(story)
print(f"Laporan PDF berhasil dibuat: {out_pdf}")
