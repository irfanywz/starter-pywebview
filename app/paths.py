"""Semua path dihitung di sini. Modul lain TIDAK boleh menyusun path sendiri."""
import sys
from pathlib import Path

from .config import DATA_DIR_NAME

FROZEN = bool(getattr(sys, "frozen", False))

if FROZEN:
    # NamaAplikasi/NamaAplikasi.exe -> root = folder exe
    ROOT_DIR = Path(sys.executable).resolve().parent
    # _MEIPASS = NamaAplikasi_System/ (contents-directory PyInstaller)
    RESOURCE_DIR = Path(getattr(sys, "_MEIPASS", ROOT_DIR))
else:
    # dev: root = folder proyek (induk dari package app/)
    ROOT_DIR = Path(__file__).resolve().parent.parent
    RESOURCE_DIR = ROOT_DIR

DATA_DIR = ROOT_DIR / DATA_DIR_NAME
WEB_DIR = RESOURCE_DIR / "app" / "web"
INDEX_HTML = WEB_DIR / "index.html"

SETTINGS_FILE = DATA_DIR / "settings.json"
LOG_DIR = DATA_DIR / "logs"
WEBVIEW_STORAGE_DIR = DATA_DIR / "webview"  # cache/cookie WebView2 ikut portable


def ensure_dirs() -> None:
    for d in (DATA_DIR, LOG_DIR, WEBVIEW_STORAGE_DIR):
        d.mkdir(parents=True, exist_ok=True)
