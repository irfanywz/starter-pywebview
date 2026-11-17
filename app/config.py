"""Satu-satunya tempat identitas aplikasi. Diubah lewat scripts/rename_app.py & scripts/bump_version.py."""
import re

APP_NAME = "Starter"
VERSION = "0.1.0"

# Turunan otomatis, jangan diedit manual
APP_ID = re.sub(r"[^a-z0-9]+", "-", APP_NAME.lower()).strip("-")
DATA_DIR_NAME = f"{APP_NAME}_Data"      # semua data user
SYSTEM_DIR_NAME = f"{APP_NAME}_System"  # hasil PyInstaller (_internal di-rename)

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 680
WINDOW_MIN_SIZE = (720, 480)
