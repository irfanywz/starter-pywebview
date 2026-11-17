"""Build exe + bundle zip.   Pakai: uv run scripts/build.py

Hasil:
  build/dist/<Nama>/<Nama>.exe
  build/dist/<Nama>/<Nama>_System/   (= _internal PyInstaller, di-rename lewat --contents-directory)
  build/dist/<Nama>/<Nama>_Data/     (folder data, kosong di awal)
  release/<Nama> <Versi>.zip         (root folder di dalam zip = "<Nama>" tanpa versi)
"""
import os
import shutil
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, read_config_value  # noqa: E402

import PyInstaller.__main__  # noqa: E402

NAME = read_config_value("APP_NAME")
VERSION = read_config_value("VERSION")
SYSTEM_DIR = f"{NAME}_System"
DATA_DIR = f"{NAME}_Data"

BUILD = ROOT / "build"
DIST = BUILD / "dist"
RELEASE = ROOT / "release"
APP_DIST = DIST / NAME


def build_exe() -> None:
    shutil.rmtree(BUILD, ignore_errors=True)
    args = [
        str(ROOT / "main.py"),
        "--name", NAME,
        "--noconfirm", "--clean",
        "--onedir", "--windowed",
        "--contents-directory", SYSTEM_DIR,
        "--distpath", str(DIST),
        "--workpath", str(BUILD / "work"),
        "--specpath", str(BUILD),
        "--add-data", f"{ROOT / 'app' / 'web'}{os.pathsep}app/web",
    ]
    icon = ROOT / "assets" / "icon.ico"
    if icon.is_file():
        args += ["--icon", str(icon)]
    PyInstaller.__main__.run(args)
    (APP_DIST / DATA_DIR).mkdir(exist_ok=True)


def make_zip() -> Path:
    RELEASE.mkdir(exist_ok=True)
    zip_path = RELEASE / f"{NAME} {VERSION}.zip"
    zip_path.unlink(missing_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(APP_DIST.rglob("*")):
            arc = Path(NAME) / p.relative_to(APP_DIST)  # root folder = NAME saja
            if p.is_dir():
                z.write(p, arc.as_posix() + "/")
            else:
                z.write(p, arc.as_posix())
    return zip_path


if __name__ == "__main__":
    build_exe()
    out = make_zip()
    print(f"\nSelesai: {out}")
