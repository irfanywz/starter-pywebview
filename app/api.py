"""Jembatan JS -> Python. Semua method PUBLIC di class Api bisa dipanggil dari JS:
    await window.pywebview.api.nama_method(args)

Aturan: atribut internal pakai awalan underscore (pywebview mengekspos yang public).
Return value harus JSON-serializable.
"""
import os
import sys

from . import paths
from .config import APP_NAME, VERSION
from .logger import get_logger
from .settings import Settings


class Api:
    def __init__(self, settings: Settings | None = None):
        self._settings = settings or Settings()
        self._log = get_logger()

    # ---- info -------------------------------------------------------
    def app_info(self) -> dict:
        return {
            "name": APP_NAME,
            "version": VERSION,
            "frozen": paths.FROZEN,
            "data_dir": str(paths.DATA_DIR),
            "python": sys.version.split()[0],
        }

    def ping(self) -> str:
        return "pong"

    # ---- settings ---------------------------------------------------
    def get_settings(self) -> dict:
        return self._settings.all()

    def set_setting(self, key: str, value) -> bool:
        self._settings.set(key, value)
        return True

    # ---- system -----------------------------------------------------
    def open_data_folder(self) -> bool:
        paths.DATA_DIR.mkdir(parents=True, exist_ok=True)
        if sys.platform == "win32":
            os.startfile(paths.DATA_DIR)  # noqa: S606
        return True
