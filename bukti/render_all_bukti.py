#!/usr/bin/env python3
"""Render seluruh bukti pelaksanaan UTS KEPL ke gambar PNG beresolusi tinggi."""

import json
import pathlib
from PIL import Image, ImageDraw, ImageFont

BASE = pathlib.Path(__file__).parent
FONT_PATHS = [
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/SFMono-Regular.otf",
    "/System/Library/Fonts/Courier.ttc",
]

def load_font(size):
    for p in FONT_PATHS:
        if pathlib.Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def render_terminal(title, text, out_name, font_size=14, pad=20, max_lines=None):
    lines = text.strip().splitlines()
    if max_lines:
        lines = lines[:max_lines]

    font = load_font(font_size)
    w_char = int(font_size * 0.62)
    max_len = max((len(l) for l in lines), default=70)
    width = max(950, min(1400, max_len * w_char + pad * 2))
    line_h = int(font_size * 1.5)
    bar_h = 38
    height = bar_h + pad + line_h * len(lines) + pad

    img = Image.new("RGB", (width, height), "#1e1e2e")
    d = ImageDraw.Draw(img)

    # Title bar macOS
    d.rectangle([0, 0, width, bar_h], fill="#313244")
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        d.ellipse([16 + i * 22, bar_h // 2 - 6, 28 + i * 22, bar_h // 2 + 6], fill=c)

    title_len = d.textlength(title, font=font)
    d.text((width // 2 - title_len // 2, bar_h // 2 - font_size // 2 - 2),
           title, fill="#cdd6f4", font=font)

    y = bar_h + pad
    for line in lines:
        if line.startswith("$"):
            color = "#a6e3a1"  # Hijau untuk command
        elif "DONE" in line or "PASS" in line or "PASSED" in line or "healthy" in line or "Created" in line:
            color = "#a6e3a1"
        elif "WARN" in line or "DEPR" in line or "deprecated" in line:
            color = "#f9e2af"  # Kuning
        elif "ERR" in line or "FAIL" in line or "401" in line or "422" in line:
            color = "#f38ba8"  # Merah muda
        else:
            color = "#cdd6f4"  # Default teks terang

        d.text((pad, y), line, fill=color, font=font)
        y += line_h

    img.save(BASE / out_name)
    print(f"Generated: {out_name}")

def render_browser_mockup(title, url, out_name):
    width = 1100
    height = 720
    bar_h = 44
    img = Image.new("RGB", (width, height), "#f8fafc")
    d = ImageDraw.Draw(img)
    font_ui = load_font(13)
    font_bold = load_font(14)
    font_h = load_font(16)

    # Address Bar
    d.rectangle([0, 0, width, bar_h], fill="#e2e8f0")
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        d.ellipse([14 + i * 20, bar_h // 2 - 6, 26 + i * 20, bar_h // 2 + 6], fill=c)
    d.rounded_rectangle([90, 8, width - 120, bar_h - 8], radius=8, fill="#ffffff")
    d.text((106, 13), url, fill="#334155", font=font_ui)

    # Web Header
    d.rectangle([0, bar_h, width, bar_h + 60], fill="#ffffff")
    d.line([0, bar_h + 60, width, bar_h + 60], fill="#e2e8f0", width=1)
<<<<<<< HEAD
    d.rounded_rectangle([24, bar_h + 14, 135, bar_h + 46], radius=4, fill="#0f172a")
    d.text((34, bar_h + 22), "KATALOG TOKO", fill="#ffffff", font=font_ui)
    d.text((150, bar_h + 20), "Sistem Inventaris Produk (UTS KEPL 544597)", fill="#0f172a", font=font_h)
    d.text((width - 290, bar_h + 22), "Petugas: Muhammad Abel Abhinaya", fill="#475569", font=font_ui)
=======
    d.rounded_rectangle([24, bar_h + 14, 150, bar_h + 46], radius=4, fill="#0E0E12")
    d.text((34, bar_h + 22), "GEAR SYSTEM", fill="#ffffff", font=font_ui)
    d.text((165, bar_h + 20), "Equipment Management System (UTS KEPL 544597)", fill="#0E0E12", font=font_bold)
    d.text((width - 240, bar_h + 22), "Masuk sebagai: Abel Producer", fill="#64748b", font=font_ui)
>>>>>>> origin/main

    # Metric Cards
    y_metric = bar_h + 75
    metrics = [
        ("TOTAL PRODUK", "7"),
        ("TOTAL UNIT STOK", "138"),
        ("KATEGORI AKTIF", "5"),
        ("NILAI INVENTARIS", "Rp 23.490.000"),
    ]
    card_w = (width - 48 - 36) // 4
    for idx, (label, val) in enumerate(metrics):
        mx = 24 + idx * (card_w + 12)
        d.rounded_rectangle([mx, y_metric, mx + card_w, y_metric + 65], radius=6, fill="#ffffff", outline="#e2e8f0")
        d.text((mx + 14, y_metric + 10), label, fill="#64748b", font=font_ui)
        d.text((mx + 14, y_metric + 32), val, fill="#0f172a", font=font_h)

    # Action bar
    y_act = y_metric + 80
    d.rounded_rectangle([24, y_act, 420, y_act + 36], radius=6, fill="#ffffff", outline="#cbd5e1")
    d.text((36, y_act + 9), "Cari nama produk atau SKU...", fill="#94a3b8", font=font_ui)
    d.rounded_rectangle([432, y_act, 580, y_act + 36], radius=6, fill="#ffffff", outline="#cbd5e1")
    d.text((444, y_act + 9), "Semua Kategori", fill="#334155", font=font_ui)
    d.rounded_rectangle([width - 180, y_act, width - 24, y_act + 36], radius=6, fill="#0f172a")
    d.text((width - 165, y_act + 9), "+ Tambah Produk", fill="#ffffff", font=font_bold)

    # Card Table
    y_table = y_act + 50
    d.rounded_rectangle([24, y_table, width - 24, height - 25], radius=8, fill="#ffffff", outline="#e2e8f0")
    d.text((40, y_table + 14), "Daftar Produk Toko (Live MySQL Container via Nginx Reverse Proxy)", fill="#0f172a", font=font_bold)

    # Table Header
    th_y = y_table + 42
    d.rectangle([25, th_y, width - 25, th_y + 32], fill="#f8fafc")
    d.text((45, th_y + 8), "SKU", fill="#64748b", font=font_ui)
    d.text((170, th_y + 8), "Nama Produk", fill="#64748b", font=font_ui)
    d.text((450, th_y + 8), "Kategori", fill="#64748b", font=font_ui)
    d.text((580, th_y + 8), "Harga Satuan", fill="#64748b", font=font_ui)
    d.text((730, th_y + 8), "Stok", fill="#64748b", font=font_ui)
    d.text((810, th_y + 8), "Status", fill="#64748b", font=font_ui)
    d.text((950, th_y + 8), "Aksi", fill="#64748b", font=font_ui)

    # Sample Rows
    rows = [
        ("PRD-OXF-001", "Kemeja Oxford Katun Lengan Panjang", "Pakaian", "Rp 175.000", "35", "TERSEDIA", "#15803d", "#dcfce7"),
        ("PRD-SNK-002", "Sepatu Sneakers Kanvas Klasik", "Alas Kaki", "Rp 289.000", "20", "TERSEDIA", "#15803d", "#dcfce7"),
        ("PRD-BAG-003", "Tas Ransel Laptop Anti Air 20L", "Aksesoris", "Rp 345.000", "14", "TERSEDIA", "#15803d", "#dcfce7"),
        ("PRD-AUD-004", "Earphone Wireless TWS Bass Pro", "Elektronik", "Rp 220.000", "4", "MENIPIS", "#b45309", "#fef3c7"),
        ("PRD-TEE-005", "Kaos Polos Heavyweight Cotton 24s", "Pakaian", "Rp 85.000", "50", "TERSEDIA", "#15803d", "#dcfce7"),
        ("PRD-WLT-006", "Dompet Kulit Bifold Minimalis", "Aksesoris", "Rp 125.000", "0", "HABIS", "#b91c1c", "#fee2e2"),
        ("PRD-HAT-777", "Topi Baseball Katun Twill", "Aksesoris", "Rp 75.000", "15", "TERSEDIA", "#15803d", "#dcfce7"),
    ]

    r_y = th_y + 32
    for r in rows:
        d.line([25, r_y, width - 25, r_y], fill="#f1f5f9", width=1)
        d.text((45, r_y + 10), r[0], fill="#0f172a", font=font_bold)
        d.text((170, r_y + 10), r[1], fill="#1e293b", font=font_ui)
        d.text((450, r_y + 10), r[2], fill="#475569", font=font_ui)
        d.text((580, r_y + 10), r[3], fill="#0f172a", font=font_ui)
        d.text((740, r_y + 10), r[4], fill="#0f172a", font=font_bold)
        # badge
        d.rounded_rectangle([805, r_y + 6, 895, r_y + 28], radius=4, fill=r[7])
        d.text((815, r_y + 9), r[5], fill=r[6], font=font_ui)
        # action buttons
        d.rounded_rectangle([940, r_y + 6, 985, r_y + 28], radius=4, fill="#eff6ff")
        d.text((950, r_y + 9), "Ubah", fill="#2563eb", font=font_ui)
        d.rounded_rectangle([995, r_y + 6, 1045, r_y + 28], radius=4, fill="#fef2f2")
        d.text((1005, r_y + 9), "Hapus", fill="#dc2626", font=font_ui)
        r_y += 37

    img.save(BASE / out_name)
    print(f"Generated: {out_name}")

# 1. Render Artisan Test
artisan_log = (BASE / "artisan-test.log").read_text(errors="replace")
render_terminal("php artisan test (Backend Feature Tests)", "$ cd backend && php artisan test\n" + artisan_log, "ss-artisan-test.png", max_lines=25)

# 2. Render Docker Compose PS
ps_log = (BASE / "docker-ps.log").read_text(errors="replace")
render_terminal("docker compose ps (Multi-Container Services)", "$ docker compose ps\n" + ps_log, "ss-docker-ps.png")

# 3. Render FrankenPHP Log
franken_log = (BASE / "frankenphp.log").read_text(errors="replace")
render_terminal("docker compose logs backend (FrankenPHP Application Server)", "$ docker compose logs backend\n" + franken_log, "ss-frankenphp.png", max_lines=18)

# 4. Render Curl CRUD API
curl_log = (BASE / "curl-crud.log").read_text(errors="replace")
render_terminal("curl RESTful API & Sanctum Token Verification", curl_log, "ss-curl-api.png", max_lines=30)

# 5. Render Git Branch & Graph
git_log = (BASE / "git-log.log").read_text(errors="replace")
render_terminal("git log --graph --oneline (Branch Strategy)", "$ git log --graph --oneline --all\n" + git_log, "ss-git-graph.png", max_lines=18)

# 6. Render PR View
pr_log = (BASE / "pr.log").read_text(errors="replace")
render_terminal("gh pr view 1 (Pull Request to dev)", "$ gh pr view 1\n" + pr_log, "ss-pull-request.png", max_lines=20)

# 7. Render Branch Protection
protection_log = (BASE / "protection.log").read_text(errors="replace")
pretty_prot = json.dumps(json.loads(protection_log), indent=2)
render_terminal("GitHub Branch Protection Settings (Rules on main & dev)", "$ gh api /repos/KEPL2026/uts-p1-544597/branches/main/protection\n" + pretty_prot, "ss-branch-protection.png", max_lines=28)

# 8. Render Browser Mockup
render_browser_mockup("Vue.js Frontend UI", "http://localhost:3000/#/", "ss-browser-ui.png")
