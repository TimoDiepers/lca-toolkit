"""Build the LCA Toolkit installer for the current platform from pixi.lock.

The environment is defined in pixi.toml and pinned in pixi.lock. That lock
mixes conda-forge packages and PyPI wheels (Activity Browser + Brightway), but
constructor only understands conda packages, so this script:

1. turns the locked conda packages into exact constructor specs,
2. downloads (and hash-checks) the locked PyPI wheels and bundles them as extra files,
3. adds a post-install step that pip-installs those wheels offline (--no-index),
4. renders construct.yaml and runs constructor.

Run via `pixi run -e build installer` (after `build-shortcuts`, which the task does).
"""

from __future__ import annotations

import argparse
import hashlib
import platform
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LOCK = ROOT / "pixi.lock"
SHORTCUTS_CHANNEL = ROOT / "build" / "channel"

# --- Names --------------------------------------------------------------------
# Keep in sync with recipe/shortcuts/ (package name, menu.json) and the CI smoke test.
NAME = "LCA-Toolkit"  # installer title and file name
COMPANY = "LCA Toolkit"
PREFIX_DIR = "lca-toolkit"  # install folder in the user's home directory
SHORTCUTS_PACKAGE = "lca-toolkit-shortcuts"  # must match recipe/shortcuts/recipe.yaml
WHEEL_DIR_IN_PREFIX = "lca-toolkit-wheels"  # temporary, removed after post-install


def current_platform() -> str:
    if sys.platform == "win32":
        return "win-64"
    if sys.platform == "darwin" and platform.machine() == "arm64":
        return "osx-arm64"
    raise SystemExit(f"Unsupported build platform: {sys.platform}/{platform.machine()}")


def read_lock(plat: str) -> tuple[list[str], list[dict]]:
    lock = yaml.safe_load(LOCK.read_text())
    entries = lock["environments"]["default"]["packages"][plat]
    conda_urls = [e["conda"] for e in entries if "conda" in e]
    pypi_urls = {e["pypi"] for e in entries if "pypi" in e}
    pypi = [p for p in lock["packages"] if p.get("pypi") in pypi_urls]
    return conda_urls, pypi


def conda_spec(url: str) -> str:
    fn = url.rsplit("/", 1)[-1].removesuffix(".conda").removesuffix(".tar.bz2")
    name, version, build = fn.rsplit("-", 2)
    return f"{name}={version}={build}"


def download_wheels(pypi: list[dict], dest: Path) -> list[Path]:
    dest.mkdir(parents=True, exist_ok=True)
    wheels = []
    for pkg in pypi:
        url = pkg["pypi"]
        target = dest / url.rsplit("/", 1)[-1]
        if not target.name.endswith(".whl"):
            raise SystemExit(f"{pkg['name']} is locked as an sdist ({target.name}); only wheels can be bundled")
        if not target.exists():
            print(f"downloading {target.name}")
            urllib.request.urlretrieve(url, target)
        if pkg.get("sha256") and hashlib.sha256(target.read_bytes()).hexdigest() != pkg["sha256"]:
            target.unlink()
            raise SystemExit(f"sha256 mismatch for {target.name}")
        wheels.append(target)
    return wheels


def write_post_install(out: Path, plat: str, wheels: list[Path]) -> str:
    (out / "requirements.txt").write_text("".join(f"{w.name.split('-')[0]}=={w.name.split('-')[1]}\n" for w in wheels))
    pip_args = "--no-index --no-deps --disable-pip-version-check --no-warn-script-location"
    if plat == "win-64":
        script = out / "post_install.bat"
        script.write_text(
            "@echo off\r\n"
            f'"%PREFIX%\\python.exe" -m pip install {pip_args} '
            f'--find-links "%PREFIX%\\{WHEEL_DIR_IN_PREFIX}" -r "%PREFIX%\\{WHEEL_DIR_IN_PREFIX}\\requirements.txt"'
            " || exit /b 1\r\n"
            f'rmdir /s /q "%PREFIX%\\{WHEEL_DIR_IN_PREFIX}"\r\n'
        )
    else:
        script = out / "post_install.sh"
        script.write_text(
            "#!/bin/bash\nset -euo pipefail\n"
            f'"$PREFIX/bin/python" -m pip install {pip_args} '
            f'--find-links "$PREFIX/{WHEEL_DIR_IN_PREFIX}" -r "$PREFIX/{WHEEL_DIR_IN_PREFIX}/requirements.txt"\n'
            f'rm -rf "$PREFIX/{WHEEL_DIR_IN_PREFIX}"\n'
        )
    return script.name


def construct_yaml(plat: str, version: str, specs: list[str], wheels: list[Path], post_install: str) -> dict:
    extra_files = [{f"wheels/{w.name}": f"{WHEEL_DIR_IN_PREFIX}/{w.name}"} for w in wheels]
    extra_files.append({"requirements.txt": f"{WHEEL_DIR_IN_PREFIX}/requirements.txt"})
    cfg = {
        "name": NAME,
        "version": version,
        "company": COMPANY,
        "channels": [SHORTCUTS_CHANNEL.as_uri(), "conda-forge"],
        "specs": specs + [SHORTCUTS_PACKAGE],
        "menu_packages": [SHORTCUTS_PACKAGE],
        "extra_files": extra_files,
        "post_install": post_install,
        # Self-contained: no PATH, shell-init or registry changes on the user's machine.
        "initialize_conda": False,
        "initialize_by_default": False,
        "register_python": False,
    }
    if plat == "win-64":
        cfg |= {
            "installer_type": "exe",
            "installer_filename": f"{NAME}-{version}-Windows-x86_64.exe",
            # Must differ from the notebook folder (LCA-Notebooks) the JupyterLab shortcut opens.
            "default_prefix": f"%USERPROFILE%\\{PREFIX_DIR}",
            "register_python_default": False,
        }
    else:
        cfg |= {
            "installer_type": "pkg",
            "installer_filename": f"{NAME}-{version}-macOS-arm64.pkg",
            "pkg_name": PREFIX_DIR,  # .pkg installs to ~/<pkg_name>
            "pkg_domains": {"enable_anywhere": False, "enable_currentUserHome": True, "enable_localSystem": False},
        }
    return cfg


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--platform", default=current_platform(), choices=["osx-arm64", "win-64"])
    parser.add_argument("--version", default=_workspace_version())
    parser.add_argument("--no-build", action="store_true", help="only render inputs, don't run constructor")
    args = parser.parse_args()

    if not any(SHORTCUTS_CHANNEL.glob(f"noarch/{SHORTCUTS_PACKAGE}-*.conda")):
        raise SystemExit("shortcut package missing; run `pixi run -e build build-shortcuts` first")

    out = ROOT / "build" / args.platform
    if out.exists():
        shutil.rmtree(out / "installer", ignore_errors=True)
    out.mkdir(parents=True, exist_ok=True)

    conda_urls, pypi = read_lock(args.platform)
    specs = [conda_spec(u) for u in conda_urls]
    wheels = download_wheels(pypi, out / "wheels")
    post_install = write_post_install(out, args.platform, wheels)
    (out / "construct.yaml").write_text(
        yaml.safe_dump(construct_yaml(args.platform, args.version, specs, wheels, post_install), sort_keys=False)
    )
    print(f"rendered {out / 'construct.yaml'}: {len(specs)} conda packages, {len(wheels)} wheels")

    if not args.no_build:
        subprocess.run(
            ["constructor", str(out), "--output-dir", str(out / "installer"), "--platform", args.platform],
            check=True,
        )


def _workspace_version() -> str:
    import tomllib

    return tomllib.loads((ROOT / "pixi.toml").read_text())["workspace"]["version"]


if __name__ == "__main__":
    main()
