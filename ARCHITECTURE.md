# ARCHITECTURE

Dokumen ini ditulis agar AI/developer lain bisa langsung paham. Baca ini dulu sebelum mengubah kode.

## Gambaran
Aplikasi desktop: **pywebview** menampilkan UI web lokal (`app/web/`) di window native. Logika bisnis di Python. JS memanggil Python lewat `window.pywebview.api.<method>()`. Tanpa server HTTP, tanpa npm/bundler.

## Struktur folder (baku, jangan diubah antar aplikasi)
```
main.py                 Entry point (hanya memanggil app.window.run)
app/
  config.py             APP_NAME, VERSION, nama folder, ukuran window  <- identitas app
  paths.py              SEMUA path (dev vs frozen). Modul lain wajib pakai ini
  window.py             run(): setup, single instance, create_window, webview.start
  api.py                class Api: method public = bisa dipanggil dari JS
  settings.py           Settings: JSON di <Nama>_Data/settings.json
  logger.py             Logging ke <Nama>_Data/logs/app.log + excepthook global
  single_instance.py    Cegah aplikasi dibuka ganda (socket localhost)
  web/                  index.html, style.css, app.js (frontend)
assets/icon.ico         Icon exe (dipakai saat build)
scripts/
  build.py              PyInstaller + folder Data + zip
  bump_version.py       Naikkan versi (config.py + pyproject.toml) + heading CHANGELOG
  rename_app.py         Ganti APP_NAME
  _common.py            Helper baca/tulis config
tests/test_smoke.py     Smoke test (tanpa GUI)
```

## Alur runtime
`main.py` → `window.run()` → `paths.ensure_dirs()` → `setup_logging()` → `single_instance.acquire()` → `webview.create_window(url=index.html, js_api=Api())` → `webview.start(storage_path=<Data>/webview)`.
Di JS, tunggu event `pywebviewready` sebelum memanggil `api()` (lihat `app/web/app.js`).

## Path: dev vs exe
| | dev (`uv run main.py`) | exe (frozen) |
|---|---|---|
| `ROOT_DIR` | folder proyek | folder `Nama.exe` |
| `DATA_DIR` | `<proyek>/Nama_Data` | `<folder exe>/Nama_Data` |
| `RESOURCE_DIR` | folder proyek | `Nama_System/` (`sys._MEIPASS`) |

Semua data user (settings, log, cache WebView2) HARUS di `DATA_DIR` agar aplikasi portable. Jangan menulis ke `Nama_System/`.

## Build & distribusi
`scripts/build.py` memakai PyInstaller `--onedir --windowed --contents-directory <Nama>_System` (menggantikan `_internal` tanpa perlu rename manual), lalu membuat `<Nama>_Data/` kosong, lalu zip `release/<Nama> <Versi>.zip` dengan root folder `<Nama>/` (tanpa versi). `app/web` dibundel via `--add-data`.

## Konvensi
- Identitas app hanya di `app/config.py`; jangan hardcode nama/versi di tempat lain. `pyproject.toml` disinkronkan oleh skrip (dites di smoke test).
- Atribut internal di `Api` diawali underscore (pywebview mengekspos semua atribut public). Return value JSON-serializable.
- Frontend polos HTML/CSS/JS; tema lewat `data-theme` + CSS variable.
- Dependency di `pyproject.toml` pakai batas minimum (`>=`).
- Tiap perubahan: update `CHANGELOG.md` + naikkan versi (`bump_version.py`).
- UI dibuat sederhana: form dan input seminimal mungkin.

## Cara menambah fitur
1. Python: tambah method public di `app/api.py` (logika besar → modul baru di `app/`).
2. JS: panggil `await window.pywebview.api.nama_method(...)` di `app/web/app.js`.
3. Data baru → simpan di `DATA_DIR` lewat `paths.py`.
4. Update CHANGELOG, bump versi.

## Ide lanjutan (belum diimplementasi)
Tray icon, autostart Windows, simpan posisi window, custom titlebar frameless, version info di exe.
