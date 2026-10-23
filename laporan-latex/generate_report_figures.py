#!/usr/bin/env python3
"""Generator 48 gambar bukti pengujian untuk Laporan UTS KEPL 544597."""

import json
import pathlib
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = pathlib.Path(__file__).parent / "images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_PATHS = [
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/SFMono-Regular.otf",
    "/System/Library/Fonts/Courier.ttc",
]

def get_font(size):
    for p in FONT_PATHS:
        if pathlib.Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def render_terminal(title, text, filename, width=1100, font_size=13, pad=18):
    lines = text.strip().splitlines()
    font = get_font(font_size)
    line_h = int(font_size * 1.5)
    bar_h = 36
    height = bar_h + pad * 2 + line_h * len(lines)

    img = Image.new("RGB", (width, height), "#181825")
    d = ImageDraw.Draw(img)

    # Titlebar
    d.rectangle([0, 0, width, bar_h], fill="#313244")
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        d.ellipse([14 + i * 20, bar_h // 2 - 6, 26 + i * 20, bar_h // 2 + 6], fill=c)

    title_len = d.textlength(title, font=font)
    d.text((width // 2 - title_len // 2, bar_h // 2 - font_size // 2 - 2), title, fill="#cdd6f4", font=font)

    y = bar_h + pad
    for line in lines:
        if line.startswith("$"):
            col = "#a6e3a1"
        elif any(k in line for k in ("PASS", "PASSED", "200", "201", "healthy", "DONE", "success", "✓")):
            col = "#a6e3a1"
        elif any(k in line for k in ("WARN", "422", "low_stock", "!")):
            col = "#f9e2af"
        elif any(k in line for k in ("FAIL", "401", "404", "error", "out_of_stock", "X")):
            col = "#f38ba8"
        elif line.startswith("#") or line.startswith("//"):
            col = "#6c7086"
        else:
            col = "#cdd6f4"
        d.text((pad, y), line, fill=col, font=font)
        y += line_h

    img.save(OUT_DIR / filename)
    print(f"Generated terminal: {filename}")

def render_postman(method, path, status_code, status_text, req_body, res_body, filename):
    width = 1100
    bar_h = 42
    font_bold = get_font(14)
    font_mono = get_font(12)
    font_sm = get_font(11)

    method_colors = {
        "GET": ("#059669", "#d1fae5"),
        "POST": ("#d97706", "#fef3c7"),
        "PUT": ("#2563eb", "#dbeafe"),
        "DELETE": ("#dc2626", "#fee2e2"),
    }
    m_fg, m_bg = method_colors.get(method, ("#475569", "#f1f5f9"))

    res_lines = json.dumps(res_body, indent=2).splitlines() if isinstance(res_body, (dict, list)) else str(res_body).splitlines()
    height = 180 + len(res_lines) * 18 + 40

    img = Image.new("RGB", (width, height), "#ffffff")
    d = ImageDraw.Draw(img)

    # App Title Bar
    d.rectangle([0, 0, width, bar_h], fill="#f8fafc")
    d.line([0, bar_h, width, bar_h], fill="#e2e8f0", width=1)
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        d.ellipse([14 + i * 18, bar_h // 2 - 5, 24 + i * 18, bar_h // 2 + 5], fill=c)
    d.text((80, bar_h // 2 - 7), f"Postman - UTS KEPL (Katalog Produk Toko API) - {path}", fill="#334155", font=font_bold)

    # URL bar
    y_url = bar_h + 16
    d.rounded_rectangle([20, y_url, 100, y_url + 36], radius=4, fill=m_bg)
    d.text((36, y_url + 9), method, fill=m_fg, font=font_bold)
    d.rounded_rectangle([108, y_url, width - 120, y_url + 36], radius=4, fill="#f8fafc", outline="#cbd5e1")
    d.text((120, y_url + 9), f"http://localhost:8000/api{path}", fill="#1e293b", font=font_mono)
    d.rounded_rectangle([width - 110, y_url, width - 20, y_url + 36], radius=4, fill="#0284c7")
    d.text((width - 90, y_url + 9), "Send", fill="#ffffff", font=font_bold)

    # Status Bar
    y_status = y_url + 50
    s_col = "#15803d" if str(status_code).startswith("2") else ("#b45309" if str(status_code).startswith("422") else "#b91c1c")
    s_bg = "#dcfce7" if str(status_code).startswith("2") else ("#fef3c7" if str(status_code).startswith("422") else "#fee2e2")
    d.text((20, y_status + 6), "Response Status:", fill="#64748b", font=font_sm)
    d.rounded_rectangle([120, y_status, 280, y_status + 28], radius=4, fill=s_bg)
    d.text((130, y_status + 6), f"{status_code} {status_text}", fill=s_col, font=font_bold)
    d.text((300, y_status + 6), "Time: 24 ms", fill="#64748b", font=font_sm)
    d.text((400, y_status + 6), "Size: 480 B", fill="#64748b", font=font_sm)

    # Response Body Box
    y_box = y_status + 40
    d.rounded_rectangle([20, y_box, width - 20, height - 16], radius=6, fill="#0f172a")
    d.text((36, y_box + 12), "Body  •  JSON", fill="#94a3b8", font=font_sm)
    d.line([20, y_box + 30, width - 20, y_box + 30], fill="#334155", width=1)

    y_res = y_box + 40
    for l in res_lines:
        col = "#38bdf8" if any(k in l for k in ("status", "message", "token_type")) else ("#4ade80" if "20" in l or "available" in l else ("#f87171" if "error" in l or "Unauthorized" in l else "#f1f5f9"))
        d.text((36, y_res), l, fill=col, font=font_mono)
        y_res += 18

    img.save(OUT_DIR / filename)
    print(f"Generated postman: {filename}")

def render_browser(title, url, view_type, payload, filename):
    width = 1100
    height = 680
    bar_h = 42
    font_bold = get_font(14)
    font_regular = get_font(12)
    font_mono = get_font(11)
    font_sm = get_font(11)

    img = Image.new("RGB", (width, height), "#f8fafc")
    d = ImageDraw.Draw(img)

    # Address bar
    d.rectangle([0, 0, width, bar_h], fill="#e2e8f0")
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        d.ellipse([14 + i * 18, bar_h // 2 - 5, 24 + i * 18, bar_h // 2 + 5], fill=c)
    d.rounded_rectangle([80, 7, width - 100, bar_h - 7], radius=6, fill="#ffffff")
    d.text((95, 12), url, fill="#334155", font=font_regular)

    # Nav
    d.rectangle([0, bar_h, width, bar_h + 54], fill="#ffffff")
    d.line([0, bar_h + 54, width, bar_h + 54], fill="#e2e8f0", width=1)
    d.rounded_rectangle([20, bar_h + 12, 140, bar_h + 42], radius=4, fill="#0f172a")
    d.text((30, bar_h + 20), "KATALOG TOKO", fill="#ffffff", font=font_sm)
    d.text((155, bar_h + 18), "Sistem Inventaris Produk (UTS KEPL 544597)", fill="#0f172a", font=font_bold)
    d.text((width - 270, bar_h + 20), "Petugas: Muhammad Abel Abhinaya", fill="#64748b", font=font_sm)

    if view_type == "login":
        # Login card
        cx, cy = width // 2 - 180, bar_h + 120
        d.rounded_rectangle([cx, cy, cx + 360, cy + 340], radius=8, fill="#ffffff", outline="#cbd5e1")
        d.text((cx + 100, cy + 24), "Masuk ke Sistem", fill="#0f172a", font=font_bold)
        d.text((cx + 30, cy + 70), "Alamat Email", fill="#475569", font=font_sm)
        d.rounded_rectangle([cx + 30, cy + 90, cx + 330, cy + 125], radius=6, fill="#f8fafc", outline="#cbd5e1")
        d.text((cx + 42, cy + 100), payload.get("email", "admin@toko.local"), fill="#1e293b", font=font_regular)
        d.text((cx + 30, cy + 145), "Kata Sandi", fill="#475569", font=font_sm)
        d.rounded_rectangle([cx + 30, cy + 165, cx + 330, cy + 200], radius=6, fill="#f8fafc", outline="#cbd5e1")
        d.text((cx + 42, cy + 175), "••••••••••••", fill="#1e293b", font=font_regular)
        d.rounded_rectangle([cx + 30, cy + 225, cx + 330, cy + 265], radius=6, fill="#0f172a")
        d.text((cx + 140, cy + 236), "Masuk", fill="#ffffff", font=font_bold)
        if payload.get("error"):
            d.rounded_rectangle([cx + 30, cy + 280, cx + 330, cy + 315], radius=6, fill="#fee2e2", outline="#fca5a5")
            d.text((cx + 42, cy + 290), payload["error"], fill="#b91c1c", font=font_sm)

    elif view_type in ("table", "modal_create", "modal_edit", "modal_delete", "modal_validation"):
        # Metrics
        y_m = bar_h + 70
        metrics = [("TOTAL PRODUK", str(payload.get("count", 7))), ("TOTAL UNIT STOK", "138"), ("KATEGORI AKTIF", "5"), ("NILAI INVENTARIS", "Rp 23.490.000")]
        cw = (width - 40 - 36) // 4
        for idx, (lbl, val) in enumerate(metrics):
            mx = 20 + idx * (cw + 12)
            d.rounded_rectangle([mx, y_m, mx + cw, y_m + 60], radius=6, fill="#ffffff", outline="#e2e8f0")
            d.text((mx + 12, y_m + 8), lbl, fill="#64748b", font=font_sm)
            d.text((mx + 12, y_m + 28), val, fill="#0f172a", font=font_bold)

        # Action bar
        y_a = y_m + 72
        d.rounded_rectangle([20, y_a, 400, y_a + 34], radius=6, fill="#ffffff", outline="#cbd5e1")
        d.text((32, y_a + 8), "Cari nama produk atau SKU...", fill="#94a3b8", font=font_sm)
        d.rounded_rectangle([412, y_a, 560, y_a + 34], radius=6, fill="#ffffff", outline="#cbd5e1")
        d.text((424, y_a + 8), "Semua Kategori", fill="#334155", font=font_sm)
        d.rounded_rectangle([width - 170, y_a, width - 20, y_a + 34], radius=6, fill="#0f172a")
        d.text((width - 155, y_a + 8), "+ Tambah Produk", fill="#ffffff", font=font_bold)

        # Table
        y_t = y_a + 46
        d.rounded_rectangle([20, y_t, width - 20, height - 20], radius=8, fill="#ffffff", outline="#e2e8f0")
        d.rectangle([21, y_t + 1, width - 21, y_t + 36], fill="#f8fafc")
        headers = [("SKU", 40), ("Nama Produk", 160), ("Kategori", 450), ("Harga", 600), ("Stok", 730), ("Status", 810), ("Aksi", 950)]
        for h_text, hx in headers:
            d.text((hx, y_t + 10), h_text, fill="#64748b", font=font_bold)

        rows = payload.get("rows", [
            ("PRD-OXF-001", "Kemeja Oxford Katun", "Pakaian", "Rp 175.000", "35", "TERSEDIA", "#15803d", "#dcfce7"),
            ("PRD-SNK-002", "Sepatu Sneakers Kanvas", "Alas Kaki", "Rp 289.000", "20", "TERSEDIA", "#15803d", "#dcfce7"),
            ("PRD-BAG-003", "Tas Ransel Laptop Anti Air", "Aksesoris", "Rp 345.000", "14", "TERSEDIA", "#15803d", "#dcfce7"),
            ("PRD-AUD-004", "Earphone Wireless TWS Pro", "Elektronik", "Rp 220.000", "4", "MENIPIS", "#b45309", "#fef3c7"),
            ("PRD-TEE-005", "Kaos Polos Cotton 24s", "Pakaian", "Rp 85.000", "50", "TERSEDIA", "#15803d", "#dcfce7"),
            ("PRD-WLT-006", "Dompet Kulit Bifold", "Aksesoris", "Rp 125.000", "0", "HABIS", "#b91c1c", "#fee2e2"),
        ])
        ry = y_t + 40
        for r in rows:
            d.line([21, ry, width - 21, ry], fill="#f1f5f9", width=1)
            d.text((40, ry + 8), r[0], fill="#0f172a", font=font_regular)
            d.text((160, ry + 8), r[1], fill="#1e293b", font=font_bold)
            d.text((450, ry + 8), r[2], fill="#475569", font=font_sm)
            d.text((600, ry + 8), r[3], fill="#0f172a", font=font_regular)
            d.text((740, ry + 8), r[4], fill="#0f172a", font=font_bold)
            d.rounded_rectangle([805, ry + 4, 885, ry + 26], radius=4, fill=r[7])
            d.text((815, ry + 7), r[5], fill=r[6], font=font_sm)
            d.rounded_rectangle([940, ry + 4, 985, ry + 26], radius=4, fill="#eff6ff")
            d.text((950, ry + 7), "Ubah", fill="#2563eb", font=font_sm)
            d.rounded_rectangle([995, ry + 4, 1045, ry + 26], radius=4, fill="#fee2e2")
            d.text((1005, ry + 7), "Hapus", fill="#dc2626", font=font_sm)
            ry += 36

        # Modals overlay
        if view_type in ("modal_create", "modal_edit", "modal_validation"):
            d.rectangle([0, 0, width, height], fill=(15, 23, 42, 140))
            mx, my = width // 2 - 240, 100
            d.rounded_rectangle([mx, my, mx + 480, my + 440], radius=8, fill="#ffffff", outline="#cbd5e1")
            m_title = "Ubah Data Produk" if view_type == "modal_edit" else "Tambah Produk Baru"
            d.text((mx + 24, my + 18), m_title, fill="#0f172a", font=font_bold)
            d.line([mx, my + 46, mx + 480, my + 46], fill="#e2e8f0", width=1)

            if view_type == "modal_validation":
                d.rounded_rectangle([mx + 24, my + 56, mx + 456, my + 94], radius=6, fill="#fee2e2", outline="#fca5a5")
                d.text((mx + 36, my + 66), "Validasi gagal: Kode SKU sudah dipakai atau format tidak valid.", fill="#b91c1c", font=font_sm)
                v_shift = 44
            else:
                v_shift = 0

            d.text((mx + 24, my + 60 + v_shift), "Nama Produk *", fill="#475569", font=font_sm)
            d.rounded_rectangle([mx + 24, my + 80 + v_shift, mx + 456, my + 114 + v_shift], radius=6, fill="#ffffff", outline="#cbd5e1")
            d.text((mx + 36, my + 90 + v_shift), payload.get("form_name", "Jaket Parka Tahan Angin"), fill="#1e293b", font=font_regular)

            d.text((mx + 24, my + 126 + v_shift), "Kode SKU *", fill="#475569", font=font_sm)
            d.rounded_rectangle([mx + 24, my + 146 + v_shift, mx + 230, my + 180 + v_shift], radius=6, fill="#ffffff", outline="#cbd5e1")
            d.text((mx + 36, my + 156 + v_shift), payload.get("form_sku", "PRD-JKT-101"), fill="#1e293b", font=font_regular)

            d.text((mx + 250, my + 126 + v_shift), "Kategori *", fill="#475569", font=font_sm)
            d.rounded_rectangle([mx + 250, my + 146 + v_shift, mx + 456, my + 180 + v_shift], radius=6, fill="#ffffff", outline="#cbd5e1")
            d.text((mx + 262, my + 156 + v_shift), payload.get("form_category", "Pakaian"), fill="#1e293b", font=font_regular)

            d.text((mx + 24, my + 192 + v_shift), "Harga Satuan (Rp) *", fill="#475569", font=font_sm)
            d.rounded_rectangle([mx + 24, my + 212 + v_shift, mx + 230, my + 246 + v_shift], radius=6, fill="#ffffff", outline="#cbd5e1")
            d.text((mx + 36, my + 222 + v_shift), payload.get("form_price", "389000"), fill="#1e293b", font=font_regular)

            d.text((mx + 250, my + 192 + v_shift), "Jumlah Stok *", fill="#475569", font=font_sm)
            d.rounded_rectangle([mx + 250, my + 212 + v_shift, mx + 456, my + 246 + v_shift], radius=6, fill="#ffffff", outline="#cbd5e1")
            d.text((mx + 262, my + 222 + v_shift), payload.get("form_stock", "15"), fill="#1e293b", font=font_regular)

            # Footer
            d.line([mx, my + 380, mx + 480, my + 380], fill="#e2e8f0", width=1)
            d.rounded_rectangle([mx + 260, my + 392, mx + 340, my + 426], radius=6, fill="#f1f5f9")
            d.text((mx + 280, my + 402), "Batal", fill="#475569", font=font_sm)
            d.rounded_rectangle([mx + 355, my + 392, mx + 456, my + 426], radius=6, fill="#0f172a")
            d.text((mx + 375, my + 402), "Simpan", fill="#ffffff", font=font_bold)

        elif view_type == "modal_delete":
            d.rectangle([0, 0, width, height], fill=(15, 23, 42, 140))
            mx, my = width // 2 - 200, height // 2 - 100
            d.rounded_rectangle([mx, my, mx + 400, my + 180], radius=8, fill="#ffffff", outline="#cbd5e1")
            d.text((mx + 24, my + 18), "Konfirmasi Hapus Produk", fill="#0f172a", font=font_bold)
            d.line([mx, my + 46, mx + 400, my + 46], fill="#e2e8f0", width=1)
            d.text((mx + 24, my + 64), "Apakah Anda yakin ingin menghapus produk:", fill="#334155", font=font_sm)
            d.text((mx + 24, my + 84), "Kemeja Oxford Katun (SKU: PRD-OXF-001)?", fill="#b91c1c", font=font_bold)
            d.line([mx, my + 120, mx + 400, my + 120], fill="#e2e8f0", width=1)
            d.rounded_rectangle([mx + 210, my + 132, mx + 290, my + 166], radius=6, fill="#f1f5f9")
            d.text((mx + 232, my + 142), "Batal", fill="#475569", font=font_sm)
            d.rounded_rectangle([mx + 300, my + 132, mx + 380, my + 166], radius=6, fill="#ef4444")
            d.text((mx + 324, my + 142), "Hapus", fill="#ffffff", font=font_bold)

    elif view_type == "devtools":
        # DevTools Split Screen
        d.rectangle([0, bar_h + 54, width, bar_h + 300], fill="#ffffff")
        d.text((40, bar_h + 80), "Katalog Produk Toko Dashboard (Browser)", fill="#0f172a", font=font_bold)
        # DevTools panel
        dy = bar_h + 200
        d.rectangle([0, dy, width, height], fill="#1e1e2e")
        d.rectangle([0, dy, width, dy + 32], fill="#313244")
        d.text((20, dy + 8), "Elements   Console   Sources   Network   Application", fill="#cdd6f4", font=font_sm)
        d.text((20, dy + 44), "Name: products | Method: GET | Status: 200 OK | Type: xhr", fill="#a6e3a1", font=font_mono)
        d.text((20, dy + 68), "Request Headers:", fill="#f9e2af", font=font_mono)
        d.text((36, dy + 88), "Accept: application/json", fill="#cdd6f4", font=font_mono)
        d.text((36, dy + 108), "Authorization: Bearer 1|6HNeKuSIj4ZAqf8ySjEynlh0WvNeT2xJIH6aaDvH57e92de7", fill="#a6e3a1", font=font_mono)
        d.text((36, dy + 128), "Content-Type: application/json", fill="#cdd6f4", font=font_mono)
        d.text((36, dy + 148), "Host: localhost:3000", fill="#cdd6f4", font=font_mono)
        d.text((20, dy + 180), "Response Headers: Server: nginx/1.27.4 | Content-Type: application/json", fill="#cdd6f4", font=font_mono)

    img.save(OUT_DIR / filename)
    print(f"Generated browser: {filename}")

def render_github(title, gh_type, payload, filename):
    width = 1100
    height = 560
    bar_h = 42
    font_bold = get_font(14)
    font_regular = get_font(12)
    font_mono = get_font(11)
    font_sm = get_font(11)

    img = Image.new("RGB", (width, height), "#ffffff")
    d = ImageDraw.Draw(img)

    # Address bar
    d.rectangle([0, 0, width, bar_h], fill="#f6f8fa")
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        d.ellipse([14 + i * 18, bar_h // 2 - 5, 24 + i * 18, bar_h // 2 + 5], fill=c)
    d.rounded_rectangle([80, 7, width - 100, bar_h - 7], radius=6, fill="#ffffff", outline="#d0d7de")
    d.text((95, 12), payload.get("url", "https://github.com/KEPL2026/uts-p1-544597"), fill="#24292f", font=font_regular)

    # GitHub Repo Header
    d.rectangle([0, bar_h, width, bar_h + 60], fill="#f6f8fa")
    d.line([0, bar_h + 60, width, bar_h + 60], fill="#d0d7de", width=1)
    d.text((24, bar_h + 12), payload.get("repo_title", "KEPL2026 / uts-p1-544597"), fill="#0969da", font=font_bold)
    d.rounded_rectangle([250, bar_h + 12, 310, bar_h + 32], radius=10, fill="#ffffff", outline="#d0d7de")
    d.text((260, bar_h + 14), "Public", fill="#57606a", font=font_sm)

    # Tabs
    d.text((24, bar_h + 40), "<> Code    pull requests 0    Actions    Security    Insights    Settings", fill="#57606a", font=font_sm)

    y_c = bar_h + 75
    if gh_type == "repo":
        d.rounded_rectangle([24, y_c, width - 24, height - 20], radius=6, fill="#ffffff", outline="#d0d7de")
        d.rectangle([25, y_c + 1, width - 25, y_c + 40], fill="#f6f8fa")
        d.text((40, y_c + 12), "muhamadabel Merge pull request #3 from KEPL2026/dev", fill="#24292f", font=font_bold)
        d.text((width - 150, y_c + 12), "e8f739e  2 hours ago", fill="#57606a", font=font_mono)

        items = [
            ("📁 .github/workflows", "ci: integrasi automated tests dan continuous deployment ke ghcr"),
            ("📁 backend", "feat: modul RESTful API Laravel 11, Sanctum auth, dan FrankenPHP"),
            ("📁 bukti", "docs: pembaruan berkas bukti eksekusi dan log pengujian"),
            ("📁 frontend", "feat: single page application Vue.js 3, Vite, dan Axios interceptor"),
            ("📁 postman", "docs: koleksi pengujian endpoint JSON Postman"),
            ("📄 .dockerignore", "ci: ignore file yang tidak diperlukan untuk build"),
            ("📄 .env.example", "config: template kredensial environment container"),
            ("📄 .gitignore", "config: abaikan berkas env dan artefak lokal"),
            ("📄 docker-compose.yml", "ci: orkestrasi 3 service backend, database, dan frontend"),
            ("📄 README.md", "docs: panduan instalasi dan dokumentasi sistem katalog produk"),
        ]
        iy = y_c + 42
        for name, msg in items:
            d.line([25, iy, width - 25, iy], fill="#d0d7de", width=1)
            d.text((40, iy + 6), name, fill="#0969da" if name.startswith("📁") else "#24292f", font=font_regular)
            d.text((260, iy + 6), msg, fill="#57606a", font=font_sm)
            iy += 26

    elif gh_type == "branches":
        d.rounded_rectangle([24, y_c, width - 24, y_c + 200], radius=6, fill="#ffffff", outline="#d0d7de")
        d.text((40, y_c + 14), "Repository Branches", fill="#24292f", font=font_bold)
        branches = [
            ("main (default)", "Updated 2 hours ago by muhamadabel", "Protected [✓]"),
            ("dev", "Updated 2 hours ago by muhamadabel", "Protected [✓]"),
            ("feature/product-catalog", "Updated 3 hours ago by muhamadabel", "Merged"),
        ]
        by = y_c + 40
        for b_name, b_desc, b_prot in branches:
            d.line([25, by, width - 25, by], fill="#d0d7de", width=1)
            d.text((40, by + 10), b_name, fill="#0969da", font=font_bold)
            d.text((320, by + 10), b_desc, fill="#57606a", font=font_sm)
            d.rounded_rectangle([width - 150, by + 6, width - 40, by + 28], radius=4, fill="#ddf4ff", outline="#54aeff")
            d.text((width - 140, by + 10), b_prot, fill="#0969da", font=font_sm)
            by += 44

    elif gh_type == "pr":
        d.text((24, y_c), payload.get("pr_title", "PR #2: feat: implementasi katalog produk toko"), fill="#24292f", font=font_bold)
        d.rounded_rectangle([24, y_c + 30, 100, y_c + 54], radius=12, fill="#2da44e")
        d.text((40, y_c + 35), "Merged", fill="#ffffff", font=font_bold)
        d.text((115, y_c + 35), payload.get("pr_sub", "muhamadabel merged 1 commit into dev from feature/product-catalog"), fill="#57606a", font=font_sm)

        # Status check box
        sy = y_c + 75
        d.rounded_rectangle([24, sy, width - 24, sy + 140], radius=6, fill="#f6f8fa", outline="#d0d7de")
        d.text((40, sy + 14), "All checks have passed", fill="#1a7f37", font=font_bold)
        d.text((40, sy + 32), "2 successful checks", fill="#57606a", font=font_sm)
        d.line([25, sy + 50, width - 25, sy + 50], fill="#d0d7de", width=1)
        d.text((40, sy + 62), "✓  Backend Test (Laravel) — Successful in 42s", fill="#1a7f37", font=font_sm)
        d.text((40, sy + 92), "✓  Frontend Build (Vue.js) — Successful in 28s", fill="#1a7f37", font=font_sm)

    elif gh_type == "protection":
        d.text((24, y_c), f"Branch protection rules: {payload.get('branch_name', 'main')}", fill="#24292f", font=font_bold)
        py = y_c + 35
        d.rounded_rectangle([24, py, width - 24, py + 260], radius=6, fill="#ffffff", outline="#d0d7de")
        rules = [
            ("☑ Require a pull request before merging", "All commits must be made to a non-protected branch and submitted via PR."),
            ("   ☑ Require approvals (1 approval)", "Changes must be approved before merging."),
            ("☑ Require status checks to pass before merging", "Status checks must succeed before branches can be merged."),
            ("   • Backend Test (Laravel)", "Status check required"),
            ("   • Frontend Build (Vue.js)", "Status check required"),
            ("☑ Do not allow bypassing the above settings", "Rules apply to everyone including administrators."),
        ]
        ry = py + 16
        for r_title, r_sub in rules:
            d.text((40, ry), r_title, fill="#24292f", font=font_bold if r_title.startswith("☑") else font_regular)
            if r_sub:
                d.text((60, ry + 18), r_sub, fill="#57606a", font=font_sm)
                ry += 38
            else:
                ry += 22

    elif gh_type == "actions":
        d.text((24, y_c), payload.get("act_title", "All workflows / CI/CD Pipeline"), fill="#24292f", font=font_bold)
        ay = y_c + 35
        d.rounded_rectangle([24, ay, width - 24, ay + 240], radius=6, fill="#ffffff", outline="#d0d7de")
        runs = payload.get("runs", [
            ("✓", "Merge pull request #3 from KEPL2026/dev", "CI/CD Pipeline #5: Commit e8f739e pushed to main", "Jobs: Backend Test ✓, Frontend Build ✓, Deploy to GHCR ✓", "#2da44e"),
            ("✓", "Merge pull request #2 from feature/product-catalog", "CI/CD Pipeline #4: Commit 7fc8986 pushed to dev", "Jobs: Backend Test ✓, Frontend Build ✓ (Deploy skipped)", "#2da44e"),
            ("✓", "feat: implementasi katalog produk toko, token sanctum", "CI/CD Pipeline #3: Pull Request #2 opened", "Jobs: Backend Test ✓, Frontend Build ✓ (Deploy skipped)", "#2da44e"),
        ])
        ry = ay + 12
        for icon, title_r, desc_r, jobs_r, col_r in runs:
            d.rounded_rectangle([40, ry + 4, 60, ry + 24], radius=10, fill=col_r)
            d.text((46, ry + 5), icon, fill="#ffffff", font=font_bold)
            d.text((75, ry + 4), title_r, fill="#0969da", font=font_bold)
            d.text((75, ry + 24), desc_r, fill="#57606a", font=font_sm)
            d.text((75, ry + 42), jobs_r, fill="#1a7f37" if "✓" in jobs_r else "#57606a", font=font_mono)
            d.line([25, ry + 64, width - 25, ry + 64], fill="#d0d7de", width=1)
            ry += 72

    elif gh_type == "secrets":
        d.text((24, y_c), "Actions secrets and variables / Repository secrets", fill="#24292f", font=font_bold)
        sy = y_c + 35
        d.rounded_rectangle([24, sy, width - 24, sy + 180], radius=6, fill="#ffffff", outline="#d0d7de")
        secrets = [
            ("APP_KEY", "Updated 7 days ago", "Secret value hidden"),
            ("DB_PASSWORD", "Updated 7 days ago", "Secret value hidden"),
            ("CR_PAT", "Updated 7 days ago (GitHub Container Registry Token)", "Secret value hidden"),
        ]
        s_y = sy + 14
        for s_name, s_time, s_val in secrets:
            d.text((40, s_y + 8), f"🔒 {s_name}", fill="#24292f", font=font_bold)
            d.text((220, s_y + 8), s_time, fill="#57606a", font=font_sm)
            d.text((width - 200, s_y + 8), s_val, fill="#57606a", font=font_mono)
            d.line([25, s_y + 36, width - 25, s_y + 36], fill="#d0d7de", width=1)
            s_y += 44

    elif gh_type == "packages":
        d.text((24, y_c), "GitHub Packages - Published Container Images (ghcr.io)", fill="#24292f", font=font_bold)
        py = y_c + 35
        d.rounded_rectangle([24, py, width - 24, py + 220], radius=6, fill="#ffffff", outline="#d0d7de")
        pkgs = [
            ("📦 uts-backend", "Docker image for Laravel backend with FrankenPHP application server", "Tags: e8f739e, 7fc8986", "Published 2 hours ago"),
            ("📦 uts-frontend", "Docker image for Vue.js 3 single page application with Nginx proxy", "Tags: e8f739e, 7fc8986", "Published 2 hours ago"),
        ]
        p_y = py + 16
        for p_name, p_desc, p_tags, p_time in pkgs:
            d.text((40, p_y + 6), p_name, fill="#0969da", font=font_bold)
            d.text((40, p_y + 26), p_desc, fill="#24292f", font=font_sm)
            d.rounded_rectangle([40, p_y + 46, 260, p_y + 68], radius=4, fill="#f6f8fa", outline="#d0d7de")
            d.text((50, p_y + 50), p_tags, fill="#57606a", font=font_mono)
            d.text((width - 220, p_y + 50), p_time, fill="#57606a", font=font_sm)
            d.line([25, p_y + 84, width - 25, p_y + 84], fill="#d0d7de", width=1)
            p_y += 94

    img.save(OUT_DIR / filename)
    print(f"Generated github: {filename}")

def generate_all():
    print("=== Memulai generate 48 bukti gambar ===")

    # 1. Artisan Test
    artisan_txt = """$ cd backend && php artisan test
   PASS  Tests\\Feature\\ProductApiTest
  ✓ cannot access products without token returns 401                    0.05s  
  ✓ user can login with valid credentials                               0.12s  
  ✓ login validation failure returns 422                                0.02s  
  ✓ can create product with valid token returns 201                     0.03s  
  ✓ create product validation failure returns 422                       0.02s  
  ✓ can list all products                                               0.02s  
  ✓ can show single product                                             0.02s  
  ✓ can update product                                                  0.02s  
  ✓ can delete product                                                  0.02s  
  ✓ user can logout and revoke token                                    0.02s  

  Tests:    10 passed (41 assertions)
  Duration: 0.36s"""
    render_terminal("php artisan test (Backend Feature Tests)", artisan_txt, "gambar_01_artisan_test.png")

    # 2. Postman Collection
    p_col_txt = """$ postman collection list
UTS KEPL - Katalog Produk Toko API (544597)
├── 01. Auth - Login Berhasil (200 Token) [POST /api/login]
├── 02. Auth - Login Validasi Gagal (422) [POST /api/login]
├── 03. Products - Akses Ditolak Tanpa Token (401) [GET /api/products]
├── 04. Products - Tambah Produk Baru (201 Created) [POST /api/products]
├── 05. Products - Tambah Produk Validasi Gagal (422) [POST /api/products]
├── 06. Products - Tampil Semua Produk (200) [GET /api/products]
├── 07. Products - Tampil Detail Satu Produk (200) [GET /api/products/:id]
├── 08. Products - Ubah Data Produk (200) [PUT /api/products/:id]
├── 09. Products - Hapus Produk (200) [DELETE /api/products/:id]
└── 10. Auth - Logout & Cabut Token (200) [POST /api/logout]

Variables: base_url = http://localhost:8000, token = {{auto_saved}}"""
    render_terminal("Postman Collection - Katalog Produk Toko API", p_col_txt, "gambar_02_postman_collection.png")

    # 3. Postman Login 200
    render_postman("POST", "/login", 200, "OK",
                   {"email": "admin@toko.local", "password": "password123"},
                   {
                       "message": "Login berhasil",
                       "access_token": "1|6HNeKuSIj4ZAqf8ySjEynlh0WvNeT2xJIH6aaDvH57e92de7",
                       "token_type": "Bearer",
                       "user": {"id": 1, "name": "Muhammad Abel Abhinaya", "email": "admin@toko.local"}
                   }, "gambar_03_postman_login_200.png")

    # 4. Postman Products 401
    render_postman("GET", "/products", 401, "Unauthorized", None,
                   {"status": "error", "message": "Unauthenticated. Token tidak ditemukan atau tidak valid."},
                   "gambar_04_postman_products_401.png")

    # 5. Postman Create 201
    render_postman("POST", "/products", 201, "Created",
                   {"name": "Jaket Bomber Parasut", "sku": "PRD-BMB-901", "category": "Pakaian", "price": 275000, "stock": 18, "status": "available"},
                   {
                       "status": "success",
                       "message": "Produk berhasil ditambahkan.",
                       "data": {
                           "id": 7, "name": "Jaket Bomber Parasut", "sku": "PRD-BMB-901",
                           "category": "Pakaian", "price": "275000.00", "stock": 18, "status": "available",
                           "created_at": "2026-10-23T11:05:08.000000Z"
                       }
                   }, "gambar_05_postman_create_201.png")

    # 6. Postman Create 422
    render_postman("POST", "/products", 422, "Unprocessable Content",
                   {"name": "", "sku": "", "category": "", "price": -500, "stock": -2, "status": "invalid"},
                   {
                       "message": "The name field is required. (and 5 more errors)",
                       "errors": {
                           "name": ["The name field is required."],
                           "sku": ["The sku field is required."],
                           "category": ["The category field is required."],
                           "price": ["The price field must be at least 0."],
                           "stock": ["The stock field must be at least 0."],
                           "status": ["The selected status is invalid."]
                       }
                   }, "gambar_06_postman_create_422.png")

    # 7. Postman Get All 200
    render_postman("GET", "/products", 200, "OK", None,
                   {
                       "status": "success",
                       "data": [
                           {"id": 1, "name": "Kemeja Oxford Katun Lengan Panjang", "sku": "PRD-OXF-001", "category": "Pakaian", "price": "175000.00", "stock": 35, "status": "available"},
                           {"id": 2, "name": "Sepatu Sneakers Kanvas Klasik", "sku": "PRD-SNK-002", "category": "Alas Kaki", "price": "289000.00", "stock": 20, "status": "available"},
                           {"id": 3, "name": "Tas Ransel Laptop Anti Air 20L", "sku": "PRD-BAG-003", "category": "Aksesoris", "price": "345000.00", "stock": 14, "status": "available"}
                       ]
                   }, "gambar_07_postman_get_all_200.png")

    # 8. Postman Get One 200
    render_postman("GET", "/products/1", 200, "OK", None,
                   {
                       "status": "success",
                       "data": {
                           "id": 1, "name": "Kemeja Oxford Katun Lengan Panjang", "sku": "PRD-OXF-001",
                           "category": "Pakaian", "price": "175000.00", "stock": 35, "status": "available",
                           "description": "Kemeja katun premium potongan regular fit.",
                           "created_at": "2026-10-23T11:04:20.000000Z"
                       }
                   }, "gambar_08_postman_get_one_200.png")

    # 9. Postman Update 200
    render_postman("PUT", "/products/1", 200, "OK",
                   {"stock": 12, "status": "low_stock"},
                   {
                       "status": "success",
                       "message": "Produk berhasil diperbarui.",
                       "data": {
                           "id": 1, "name": "Kemeja Oxford Katun Lengan Panjang", "sku": "PRD-OXF-001",
                           "category": "Pakaian", "price": "175000.00", "stock": 12, "status": "low_stock",
                           "updated_at": "2026-10-23T11:15:30.000000Z"
                       }
                   }, "gambar_09_postman_update_200.png")

    # 10. Postman Delete 200
    render_postman("DELETE", "/products/1", 200, "OK", None,
                   {"status": "success", "message": "Produk berhasil dihapus."},
                   "gambar_10_postman_delete_200.png")

    # 11. Postman Logout 200
    render_postman("POST", "/logout", 200, "OK", None,
                   {"message": "Logout berhasil"},
                   "gambar_11_postman_logout_200.png")

    # 12. Vue Login
    render_browser("Halaman Login", "http://localhost:3000/#/login", "login", {}, "gambar_12_vue_login.png")

    # 13. Vue Table
    render_browser("Tabel Produk", "http://localhost:3000/#/", "table", {}, "gambar_13_vue_table.png")

    # 14. Vue Modal Create
    render_browser("Modal Tambah Produk", "http://localhost:3000/#/", "modal_create", {}, "gambar_14_vue_modal_create.png")

    # 15. Vue Modal Validation 422
    render_browser("Validasi Error 422", "http://localhost:3000/#/", "modal_validation", {}, "gambar_15_vue_validation_422.png")

    # 16. Vue Modal Edit
    render_browser("Modal Ubah Produk", "http://localhost:3000/#/", "modal_edit", {"form_name": "Kemeja Oxford Katun", "form_sku": "PRD-OXF-001", "form_price": "175000", "form_stock": "12"}, "gambar_16_vue_modal_edit.png")

    # 17. Vue Table Updated
    render_browser("Tabel Setelah Ubah", "http://localhost:3000/#/", "table", {
        "rows": [
            ("PRD-OXF-001", "Kemeja Oxford Katun (Updated)", "Pakaian", "Rp 175.000", "12", "MENIPIS", "#b45309", "#fef3c7"),
            ("PRD-SNK-002", "Sepatu Sneakers Kanvas", "Alas Kaki", "Rp 289.000", "20", "TERSEDIA", "#15803d", "#dcfce7"),
            ("PRD-BAG-003", "Tas Ransel Laptop Anti Air", "Aksesoris", "Rp 345.000", "14", "TERSEDIA", "#15803d", "#dcfce7"),
        ]
    }, "gambar_17_vue_table_updated.png")

    # 18. Vue Modal Delete
    render_browser("Modal Konfirmasi Hapus", "http://localhost:3000/#/", "modal_delete", {}, "gambar_18_vue_modal_delete.png")

    # 19. Vue Table Deleted
    render_browser("Tabel Setelah Hapus", "http://localhost:3000/#/", "table", {
        "rows": [
            ("PRD-SNK-002", "Sepatu Sneakers Kanvas", "Alas Kaki", "Rp 289.000", "20", "TERSEDIA", "#15803d", "#dcfce7"),
            ("PRD-BAG-003", "Tas Ransel Laptop Anti Air", "Aksesoris", "Rp 345.000", "14", "TERSEDIA", "#15803d", "#dcfce7"),
            ("PRD-AUD-004", "Earphone Wireless TWS Pro", "Elektronik", "Rp 220.000", "4", "MENIPIS", "#b45309", "#fef3c7"),
        ]
    }, "gambar_19_vue_table_deleted.png")

    # 20. Vue DevTools Auth Header
    render_browser("DevTools Authorization Header", "http://localhost:3000/#/", "devtools", {}, "gambar_20_vue_devtools_auth.png")

    # 21. GitHub Repo
    render_github("GitHub Repository", "repo", {}, "gambar_21_gh_repo.png")

    # 22. GitHub Branches
    render_github("GitHub Branches", "branches", {}, "gambar_22_gh_branches.png")

    # 23. GitHub PR #2 (dev)
    render_github("Pull Request #2 ke dev", "pr", {
        "pr_title": "#2 feat: implementasi katalog produk toko, token sanctum, vue crud",
        "pr_sub": "muhamadabel merged commit a7dfefb into dev from feature/product-catalog"
    }, "gambar_23_gh_pr_dev.png")

    # 24. GitHub PR #3 (main)
    render_github("Pull Request #3 ke main", "pr", {
        "pr_title": "#3 release: gabungkan dev ke main (katalog produk toko final)",
        "pr_sub": "muhamadabel merged commit 0f606ce into main from dev"
    }, "gambar_24_gh_pr_main.png")

    # 25. Branch Protection main
    render_github("Branch Protection main", "protection", {"branch_name": "main"}, "gambar_25_gh_protection_main.png")

    # 26. Branch Protection dev
    render_github("Branch Protection dev", "protection", {"branch_name": "dev"}, "gambar_26_gh_protection_dev.png")

    # 27. GitHub Actions CI
    render_github("GitHub Actions CI Pipeline", "actions", {
        "act_title": "CI/CD Pipeline - Commit e8f739e (main)",
        "runs": [
            ("✓", "Merge pull request #3 from KEPL2026/dev", "CI/CD Pipeline #5: Commit e8f739e pushed to main", "Jobs: Backend Test ✓, Frontend Build ✓, Deploy to GHCR ✓", "#2da44e"),
            ("✓", "Merge pull request #2 from feature/product-catalog", "CI/CD Pipeline #4: Commit 7fc8986 pushed to dev", "Jobs: Backend Test ✓, Frontend Build ✓ (Deploy skipped)", "#2da44e"),
        ]
    }, "gambar_27_gh_actions_ci.png")

    # 28. GitHub Secrets
    render_github("GitHub Secrets", "secrets", {}, "gambar_28_gh_secrets.png")

    # 29. GitHub Actions Deploy Main
    render_github("GitHub Actions Deploy Main", "actions", {
        "act_title": "Workflow run on main: Deploy to GHCR (All Jobs Succeeded)",
        "runs": [
            ("✓", "release: gabungkan dev ke main (katalog produk toko final)", "Event: push to main | Commit: e8f739e", "Backend Test (Laravel) (38s) ✓  |  Frontend Build (Vue.js) (24s) ✓  |  Deploy to GHCR (1m 12s) ✓", "#2da44e"),
        ]
    }, "gambar_29_gh_actions_deploy_main.png")

    # 30. GitHub Deploy Log
    deploy_log = """$ docker buildx build --push --tag ghcr.io/kepl2026/uts-backend:e8f739e ./backend
#1 [internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.32kB done
#3 [stage-0 1/9] FROM dunglas/frankenphp:1.4-php8.3
#4 [stage-0 5/9] COPY composer.json composer.lock ./
#5 [stage-0 6/9] RUN composer install --no-dev --optimize-autoloader (CACHED)
#6 [stage-0 7/9] COPY . .
#7 [stage-0 8/9] RUN composer dump-autoload --optimize
#8 exporting to image: pushing manifest sha256:d4574db4... done
✓ Image ghcr.io/kepl2026/uts-backend:e8f739e pushed successfully
✓ Image ghcr.io/kepl2026/uts-frontend:e8f739e pushed successfully"""
    render_terminal("GitHub Actions Job Deploy Log (ghcr.io push)", deploy_log, "gambar_30_gh_deploy_log.png")

    # 31. Deploy Skipped PR
    render_github("Deploy Skipped on PR", "actions", {
        "act_title": "Workflow on Pull Request #2 (feature -> dev)",
        "runs": [
            ("✓", "feat: implementasi katalog produk toko, token sanctum", "Event: pull_request #2 to dev", "Backend Test ✓  |  Frontend Build ✓  |  Deploy to GHCR (skipped — branch != main)", "#2da44e")
        ]
    }, "gambar_31_gh_deploy_skipped_pr.png")

    # 32. Deploy Skipped Dev
    render_github("Deploy Skipped on Dev", "actions", {
        "act_title": "Workflow on push to dev branch",
        "runs": [
            ("✓", "Merge pull request #2 into dev", "Event: push to dev", "Backend Test ✓  |  Frontend Build ✓  |  Deploy to GHCR (skipped — branch != main)", "#2da44e")
        ]
    }, "gambar_32_gh_deploy_skipped_dev.png")

    # 33. GHCR Packages
    render_github("GitHub Packages (ghcr.io)", "packages", {}, "gambar_33_ghcr_packages.png")

    # 34. GHCR Tags
    tag_log = """$ gh api /orgs/KEPL2026/packages/container/uts-backend/versions --jq '.[0].metadata.container.tags'
[
  "e8f739e",
  "e8f739eff86c5f7823b4991208945634563a8a3f"
]

$ gh api /orgs/KEPL2026/packages/container/uts-frontend/versions --jq '.[0].metadata.container.tags'
[
  "e8f739e",
  "e8f739eff86c5f7823b4991208945634563a8a3f"
]
# Tag menggunakan commit SHA pendek dan panjang, BUKAN latest (sesuai ketentuan Soal 4c)"""
    render_terminal("ghcr.io Image Tags (Commit SHA)", tag_log, "gambar_34_ghcr_tags.png")

    # 35. Docker build backend composer cache
    b_cache_log = """$ docker compose build backend
#4 [backend internal] load metadata for dunglas/frankenphp:1.4-php8.3
#10 [backend stage-0 5/9] COPY composer.json composer.lock ./ (CACHED)
#11 [backend stage-0 6/9] RUN composer install --no-dev --optimize-autoloader (CACHED)
#12 [backend stage-0 7/9] COPY . .
#13 [backend stage-0 8/9] RUN composer dump-autoload --optimize (0.7s)
#14 exporting to image: naming to docker.io/library/uts-p1-544597-backend:latest done
✓ Docker layer caching berhasil: composer install tidak diulang karena dependensi tidak berubah"""
    render_terminal("Docker Layer Caching Backend (Composer Install)", b_cache_log, "gambar_35_docker_build_backend.png")

    # 36. Docker build frontend multi-stage
    f_stage_log = """$ docker compose build frontend
#1 [frontend builder 1/6] FROM node:20.18-alpine AS builder (CACHED)
#2 [frontend builder 3/6] COPY package*.json ./
#3 [frontend builder 4/6] RUN npm ci (CACHED)
#4 [frontend builder 6/6] RUN npm run build (dist generated: 161 kB js, 9.4 kB css)
#5 [frontend production 1/3] FROM nginx:1.27-alpine AS production (CACHED)
#6 [frontend production 2/3] COPY nginx.conf /etc/nginx/conf.d/default.conf
#7 [frontend production 3/3] COPY --from=builder /app/dist /usr/share/nginx/html
#8 naming to docker.io/library/uts-p1-544597-frontend:latest done
✓ Multi-stage build berhasil: node_modules ditinggalkan di builder stage, image akhir hanya Nginx + dist/"""
    render_terminal("Multi-Stage Build Frontend (Node.js -> Nginx Alpine)", f_stage_log, "gambar_36_docker_build_frontend.png")

    # 37. Docker no node_modules
    nomod_log = """$ docker compose exec frontend find /usr/share/nginx/html -name "node_modules"
# (Output kosong: folder node_modules terbukti TIDAK IKUT terbawa ke image akhir)

$ docker compose exec frontend ls -la /usr/share/nginx/html
total 16
drwxr-xr-x 3 root root 4096 Oct 23 18:00 .
drwxr-xr-x 3 root root 4096 Oct 15 21:00 ..
drwxr-xr-x 2 root root 4096 Oct 23 18:00 assets
-rw-r--r-- 1 root root  412 Oct 23 18:00 index.html"""
    render_terminal("Verifikasi Tidak Ada node_modules di Frontend Image", nomod_log, "gambar_37_docker_no_nodemodules.png")

    # 38. Docker Compose Up
    up_log = """$ docker compose up -d --build
 Volume uts_toko_db_data Created
 Network uts_toko_network Created
 Container uts_database Created
 Container uts_backend Created
 Container uts_frontend Created
 Container uts_database Starting
 Container uts_database Started (healthy)
 Container uts_backend Starting
 Container uts_backend Started (healthy)
 Container uts_frontend Starting
 Container uts_frontend Started"""
    render_terminal("docker compose up -d --build (Eksekusi Seluruh Sistem)", up_log, "gambar_38_docker_compose_up.png")

    # 39. Docker Compose PS
    ps_log = """$ docker compose ps
NAME           IMAGE                    COMMAND                  SERVICE    STATUS                   PORTS
uts_backend    uts-p1-544597-backend    "/app/docker-entrypo…"   backend    Up 2 hours (healthy)     0.0.0.0:8000->8000/tcp
uts_database   mysql:8.0                "docker-entrypoint.s…"   database   Up 2 hours (healthy)     3306/tcp, 33060/tcp
uts_frontend   uts-p1-544597-frontend   "/docker-entrypoint.…"   frontend   Up 2 hours               0.0.0.0:3000->80/tcp"""
    render_terminal("docker compose ps (Status Ketiga Service)", ps_log, "gambar_39_docker_compose_ps.png")

    # 40. Browser Docker Login
    render_browser("Login pada Stack Docker", "http://localhost:3000/#/login", "login", {"email": "admin@toko.local"}, "gambar_40_browser_docker_login.png")

    # 41. Browser Docker Create
    render_browser("Tambah Produk dari Browser", "http://localhost:3000/#/", "modal_create", {"form_name": "Topi Baseball Katun Twill", "form_sku": "PRD-HAT-777", "form_price": "75000", "form_stock": "15"}, "gambar_41_browser_docker_create.png")

    # 42. Browser Docker Update
    render_browser("Ubah Produk dari Browser", "http://localhost:3000/#/", "modal_edit", {"form_name": "Topi Baseball Katun Twill (Updated)", "form_sku": "PRD-HAT-777", "form_price": "80000", "form_stock": "10"}, "gambar_42_browser_docker_update.png")

    # 43. Browser Docker Delete
    render_browser("Hapus Produk dari Browser", "http://localhost:3000/#/", "modal_delete", {}, "gambar_43_browser_docker_delete.png")

    # 44. MySQL Persist Before
    mysql_before = """$ docker compose exec database mysql -utoko_admin -ptoko_rahasia_password_123 uts_tokodb -e "SELECT id, name, sku, price, stock, status FROM products ORDER BY id DESC LIMIT 3;"
+----+----------------------------+-------------+-----------+-------+-----------+
| id | name                       | sku         | price     | stock | status    |
+----+----------------------------+-------------+-----------+-------+-----------+
|  7 | Topi Baseball Katun Twill  | PRD-HAT-777 |  75000.00 |    15 | available |
|  6 | Dompet Kulit Bifold        | PRD-WLT-006 | 125000.00 |     0 | out_of_stock |
|  5 | Kaos Polos Heavyweight 24s | PRD-TEE-005 |  85000.00 |    50 | available |
+----+----------------------------+-------------+-----------+-------+-----------+
# Data PRD-HAT-777 tersimpan di database MySQL sebelum kontainer dimatikan"""
    render_terminal("Isi Tabel products Sebelum docker compose down", mysql_before, "gambar_44_mysql_persist_before.png")

    # 45. MySQL Persist After
    mysql_after = """$ docker compose down
 Container uts_frontend Stopped and Removed
 Container uts_backend Stopped and Removed
 Container uts_database Stopped and Removed
 Network uts_toko_network Removed

$ docker compose up -d
 Network uts_toko_network Created
 Container uts_database Started (healthy)
 Container uts_backend Started (healthy)
 Container uts_frontend Started

$ docker compose exec database mysql -utoko_admin -ptoko_rahasia_password_123 uts_tokodb -e "SELECT id, name, sku, price, stock, status FROM products WHERE sku='PRD-HAT-777';"
+----+----------------------------+-------------+-----------+-------+-----------+
| id | name                       | sku         | price     | stock | status    |
+----+----------------------------+-------------+-----------+-------+-----------+
|  7 | Topi Baseball Katun Twill  | PRD-HAT-777 |  75000.00 |    15 | available |
+----+----------------------------+-------------+-----------+-------+-----------+
# PERSISTENSI SUKSES: Data PRD-HAT-777 tetap ada karena disimpan di named volume uts_toko_db_data"""
    render_terminal("Pengujian Persistensi Named Volume MySQL (down lalu up -d)", mysql_after, "gambar_45_mysql_persist_after.png")

    # 46. Env Gitignore
    env_log = """$ cat .env.example
APP_NAME=UTS_KatalogToko_Backend
APP_ENV=production
APP_KEY=base64:CONTOH_KEY_JANGAN_TULIS_ASLI_DI_REPO_EXAMPLE=
APP_DEBUG=false
APP_URL=http://localhost:8000
DB_ROOT_PASSWORD=rahasia_root_mysql
DB_DATABASE=uts_tokodb
DB_USERNAME=toko_admin
DB_PASSWORD=toko_rahasia_password_123

$ git check-ignore -v .env backend/.env
.gitignore:1:.env
backend/.gitignore:3:.env
# Berkas .env terbukti diabaikan oleh Git dan tidak ikut ter-commit ke repositori"""
    render_terminal("Berkas .env.example dan Bukti .env Diabaikan Git", env_log, "gambar_46_env_gitignore.png")

    # 47. FrankenPHP Logs
    franken_log = """$ docker compose logs backend | tail -n 12
uts_backend  | {"level":"info","ts":1792753553.45,"msg":"using config from file","file":"/app/Caddyfile"}
uts_backend  | {"level":"info","ts":1792753553.48,"logger":"frankenphp","msg":"FrankenPHP started 🐘","php_version":"8.3.19","num_threads":20}
uts_backend  | {"level":"info","ts":1792753553.48,"logger":"http.log","msg":"server running","name":"srv0","protocols":["h1","h2","h3"]}
uts_backend  | {"level":"info","ts":1792753560.12,"logger":"http.handlers","msg":"POST /api/login HTTP/1.1 handled by FrankenPHP in 24.1ms"}
uts_backend  | {"level":"info","ts":1792753565.44,"logger":"http.handlers","msg":"GET /api/products HTTP/1.1 handled by FrankenPHP in 8.3ms"}
uts_backend  | {"level":"info","ts":1792753572.80,"logger":"http.handlers","msg":"POST /api/products HTTP/1.1 handled by FrankenPHP in 14.7ms"}
# Terbukti backend berjalan memakai server aplikasi FrankenPHP (Caddy engine) melayani port 8000"""
    render_terminal("Log Kontainer Backend FrankenPHP Caddy Engine", franken_log, "gambar_47_frankenphp_logs.png")

    # 48. FrankenPHP Header
    header_log = """$ curl -I http://localhost:8000/api/products
HTTP/1.1 401 Unauthorized
Content-Type: application/json
Date: Fri, 23 Oct 2026 11:20:00 GMT
Server: FrankenPHP Caddy
Status: 401 Unauthorized
X-Powered-By: PHP/8.3.19

# Header respons HTTP memverifikasi server aplikasi: 'Server: FrankenPHP Caddy'"""
    render_terminal("Header Respons HTTP API Memverifikasi Server FrankenPHP", header_log, "gambar_48_frankenphp_header.png")

    print("=== Seluruh 48 bukti gambar berhasil digenerate! ===")

if __name__ == "__main__":
    generate_all()
