# Changelog

Format: [Keep a Changelog](https://keepachangelog.com). Versi mengikuti `app/config.py` (`VERSION`) dan `pyproject.toml`.
Tiap perubahan: catat di sini + naikkan versi lewat `uv run scripts/bump_version.py patch|minor|major`.

## [Unreleased]

## [0.1.0] - 2026-11-17

### Added
- Starter awal GUI pywebview: window, `Api` JS↔Python, settings JSON, logging, single instance.
- Struktur folder baku (`app/` + `app/web/`), path terpusat di `app/paths.py`.
- Build `scripts/build.py`: exe + `<Nama>_System/` + `<Nama>_Data/` + zip `<Nama> <Versi>.zip`.
- Skrip `bump_version.py` dan `rename_app.py`, smoke test `tests/test_smoke.py`.
- Dokumen README, ARCHITECTURE, CHANGELOG.
