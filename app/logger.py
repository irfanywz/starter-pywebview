import logging
import sys
from logging.handlers import RotatingFileHandler

from . import paths
from .config import APP_ID


def setup_logging() -> logging.Logger:
    paths.LOG_DIR.mkdir(parents=True, exist_ok=True)
    log = logging.getLogger(APP_ID)
    if log.handlers:
        return log
    log.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh = RotatingFileHandler(paths.LOG_DIR / "app.log", maxBytes=512_000, backupCount=3, encoding="utf-8")
    fh.setFormatter(fmt)
    log.addHandler(fh)
    if not paths.FROZEN:
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        log.addHandler(sh)

    def _excepthook(exc_type, exc, tb):
        log.error("Uncaught exception", exc_info=(exc_type, exc, tb))

    sys.excepthook = _excepthook
    return log


def get_logger() -> logging.Logger:
    return logging.getLogger(APP_ID)
