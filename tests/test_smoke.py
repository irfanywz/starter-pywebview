"""Smoke test: `uv run pytest`. Tidak membuka window."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import config, paths  # noqa: E402
from app.settings import Settings  # noqa: E402


def test_version_in_sync_with_pyproject():
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert re.search(r'^version = "([^"]+)"', text, re.M).group(1) == config.VERSION


def test_changelog_has_current_version():
    assert f"[{config.VERSION}]" in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")


def test_web_files_exist():
    for name in ("index.html", "style.css", "app.js"):
        assert (paths.WEB_DIR / name).is_file()


def test_data_dir_name():
    assert paths.DATA_DIR.name == f"{config.APP_NAME}_Data"


def test_settings_roundtrip(tmp_path):
    f = tmp_path / "s.json"
    s = Settings(f)
    assert s.get("theme") == "dark"
    s.set("theme", "light")
    assert Settings(f).get("theme") == "light"
