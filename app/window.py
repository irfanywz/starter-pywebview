"""Membuat window pywebview dan menjalankan aplikasi."""
import os
import sys

import webview

from . import paths, single_instance
from .api import Api
from .config import APP_NAME, WINDOW_HEIGHT, WINDOW_MIN_SIZE, WINDOW_WIDTH
from .logger import setup_logging


def run() -> None:
    paths.ensure_dirs()
    log = setup_logging()

    if not single_instance.acquire():
        log.info("Instance lain sudah berjalan, keluar.")
        sys.exit(0)

    debug = os.environ.get("APP_DEBUG") == "1"
    log.info("Start %s (frozen=%s, debug=%s)", APP_NAME, paths.FROZEN, debug)

    webview.create_window(
        APP_NAME,
        url=str(paths.INDEX_HTML),
        js_api=Api(),
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        min_size=WINDOW_MIN_SIZE,
    )
    webview.start(
        debug=debug,
        private_mode=False,
        storage_path=str(paths.WEBVIEW_STORAGE_DIR),
    )
    log.info("Exit")
