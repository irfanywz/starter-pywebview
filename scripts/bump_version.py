"""Naikkan versi di app/config.py + pyproject.toml, dan siapkan heading di CHANGELOG.md.

Pakai:  uv run scripts/bump_version.py patch|minor|major|X.Y.Z
Setelah itu isi catatan perubahan di bawah heading baru di CHANGELOG.md.
"""
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import CHANGELOG, PYPROJECT, read_config_value, write_config_value  # noqa: E402


def next_version(cur: str, arg: str) -> str:
    if re.fullmatch(r"\d+\.\d+\.\d+", arg):
        return arg
    major, minor, patch = map(int, cur.split("."))
    if arg == "major":
        return f"{major + 1}.0.0"
    if arg == "minor":
        return f"{major}.{minor + 1}.0"
    if arg == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise SystemExit("Argumen: patch | minor | major | X.Y.Z")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    cur = read_config_value("VERSION")
    new = next_version(cur, sys.argv[1])

    write_config_value("VERSION", new)
    text = PYPROJECT.read_text(encoding="utf-8")
    PYPROJECT.write_text(re.sub(r'^version = "[^"]+"', f'version = "{new}"', text, count=1, flags=re.M), encoding="utf-8")

    log = CHANGELOG.read_text(encoding="utf-8")
    heading = f"## [{new}] - {date.today().isoformat()}\n\n### Changed\n- (isi di sini)\n\n"
    if "## [Unreleased]" in log:
        log = log.replace("## [Unreleased]\n", f"## [Unreleased]\n\n{heading}".rstrip("\n") + "\n", 1)
    else:
        log += "\n" + heading
    CHANGELOG.write_text(log, encoding="utf-8")
    print(f"Versi {cur} -> {new}. Jangan lupa isi CHANGELOG.md.")


if __name__ == "__main__":
    main()
