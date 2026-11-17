"""Ganti nama aplikasi (APP_NAME di app/config.py + name di pyproject.toml).

Pakai:  uv run scripts/rename_app.py "Nama Baru"
Folder/zip/exe otomatis mengikuti APP_NAME saat build.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import PYPROJECT, write_config_value  # noqa: E402


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        raise SystemExit(__doc__)
    name = sys.argv[1].strip()
    if re.search(r'[\\/:*?"<>|]', name):
        raise SystemExit('Nama tidak boleh mengandung \\ / : * ? " < > |')
    write_config_value("APP_NAME", name)
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    text = PYPROJECT.read_text(encoding="utf-8")
    PYPROJECT.write_text(re.sub(r'^name = "[^"]+"', f'name = "{slug}"', text, count=1, flags=re.M), encoding="utf-8")
    print(f'APP_NAME = "{name}". Catat di CHANGELOG.md lalu naikkan versi bila perlu.')


if __name__ == "__main__":
    main()
