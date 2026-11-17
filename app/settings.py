"""Settings sederhana berbasis JSON di <Nama>_Data/settings.json."""
import json
import threading
from pathlib import Path
from typing import Any

from . import paths

DEFAULTS: dict[str, Any] = {
    "theme": "dark",
}


class Settings:
    def __init__(self, file: Path | None = None):
        self._file = file or paths.SETTINGS_FILE
        self._lock = threading.Lock()
        self._data: dict[str, Any] = dict(DEFAULTS)
        self._load()

    def _load(self) -> None:
        try:
            loaded = json.loads(self._file.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                self._data.update(loaded)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def _save(self) -> None:
        self._file.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._file.with_suffix(".tmp")
        tmp.write_text(json.dumps(self._data, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(self._file)

    def all(self) -> dict[str, Any]:
        with self._lock:
            return dict(self._data)

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._data[key] = value
            self._save()
