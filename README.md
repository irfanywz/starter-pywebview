# Starter (pywebview)

Base utama untuk aplikasi GUI **pywebview + Python** (UI = HTML/CSS/JS polos, logika = Python). Salin folder ini sebagai awal tiap aplikasi baru supaya struktur selalu sama.

## Persyaratan
- Windows 10/11 (WebView2 Runtime, sudah bawaan Win 11)
- [uv](https://docs.astral.sh/uv/)

## Perintah
```bash
uv sync                                   # install dependency
uv run main.py                            # jalankan (dev)
APP_DEBUG=1 uv run main.py                # dev + DevTools (PowerShell: $env:APP_DEBUG=1)
uv run pytest                             # smoke test
uv run scripts/build.py                   # build exe + zip
uv run scripts/bump_version.py patch      # naikkan versi (+ heading CHANGELOG)
uv run scripts/rename_app.py "Nama Baru"  # ganti nama aplikasi
```

## Hasil build
```
release/Starter 0.1.0.zip
└── Starter/                  <- root zip, tanpa versi
    ├── Starter.exe
    ├── Starter_System/       <- _internal PyInstaller (jangan diedit)
    └── Starter_Data/         <- semua data user (settings, log, cache webview)
```

## Membuat aplikasi baru dari starter
1. Salin folder, jalankan `rename_app.py "Nama Aplikasi"`.
2. Tambah method di `app/api.py`, tambah UI di `app/web/`.
3. Catat di `CHANGELOG.md`, jalankan `bump_version.py`, lalu `build.py`.

Detail desain ada di [ARCHITECTURE.md](ARCHITECTURE.md).
