"""Single instance lewat socket localhost (otomatis lepas saat proses mati)."""
import socket
import zlib

from .config import APP_ID

_sock: socket.socket | None = None


def acquire() -> bool:
    """True jika ini instance pertama, False jika sudah ada yang jalan."""
    global _sock
    port = 49152 + zlib.crc32(APP_ID.encode()) % 16000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
    except OSError:
        s.close()
        return False
    _sock = s  # simpan referensi supaya tidak di-GC
    return True
