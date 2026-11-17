import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "app" / "config.py"
PYPROJECT = ROOT / "pyproject.toml"
CHANGELOG = ROOT / "CHANGELOG.md"


def read_config_value(key: str) -> str:
    m = re.search(rf'^{key} = "([^"]+)"', CONFIG.read_text(encoding="utf-8"), re.M)
    if not m:
        raise SystemExit(f"{key} tidak ditemukan di app/config.py")
    return m.group(1)


def write_config_value(key: str, value: str) -> None:
    text = CONFIG.read_text(encoding="utf-8")
    text = re.sub(rf'^{key} = "[^"]+"', f'{key} = "{value}"', text, count=1, flags=re.M)
    CONFIG.write_text(text, encoding="utf-8")
