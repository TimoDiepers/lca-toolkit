"""Build the LCA Toolkit installer for the current platform from pixi.lock.

The environment is defined in pixi.toml and pinned in pixi.lock. That lock
mixes conda-forge packages and PyPI wheels (Activity Browser + Brightway), but
constructor only understands conda packages, so this script:

1. turns the locked conda packages into exact constructor specs,
2. downloads (and hash-checks) the locked PyPI wheels and bundles them as extra files,
3. adds a post-install step that pip-installs those wheels offline (--no-index),
4. ships launcher/launcher.py (used by the JupyterLab shortcut) into the environment,
5. adds the optional "notebooks from a git repository" steps (see below),
6. renders construct.yaml and runs constructor (via tools/run_constructor.py, which lets the
   installers replace an existing installation instead of refusing).

Notebooks: at the end of the installation, users can download notebooks from any git
repository (a free text field, prefilled with SUGGESTED_MATERIAL_URL, e.g. to paste course
material with an access token) into a folder of their choice (default: Documents), and then
restore a Brightway project backup (.tar.gz) with bw2io. No URL or token is built into the
installer. Windows: extra installer pages (installer/windows_material_pages.nsi). macOS:
dialogs (installer/macos_material_dialogs.sh). Linux: terminal prompts
(installer/linux_material_prompts.sh).

Run via `pixi run -e build installer` (after `build-shortcuts`, which the task does).
"""

from __future__ import annotations

import argparse
import hashlib
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LOCK = ROOT / "pixi.lock"
LAUNCHER = ROOT / "launcher" / "launcher.py"
INSTALLER_DIR = ROOT / "installer"
SHARE_IN_PREFIX = "share/lca-toolkit"  # launcher.py; keep in sync with menu.json
# Prefilled in the installers' "download notebooks from a git repository" step. Users can
# paste any other link (e.g. course material with an access token). Override at build time
# with MATERIAL_SUGGESTED_URL (no credentials: it is built into the installer).
SUGGESTED_MATERIAL_URL = "https://github.com/brightway-lca/from-the-ground-up.git"
SHORTCUTS_CHANNEL = ROOT / "build" / "channel"

# --- Names --------------------------------------------------------------------
# Keep in sync with recipe/shortcuts/ (package name, menu.json) and the CI smoke test.
NAME = "LCA-Toolkit"  # installer title and file name
COMPANY = "LCA Toolkit"
PREFIX_DIR = "lca-toolkit"  # install folder in the user's home directory
SHORTCUTS_PACKAGE = "lca-toolkit-shortcuts"  # must match recipe/shortcuts/recipe.yaml
WHEEL_DIR_IN_PREFIX = "lca-toolkit-wheels"  # temporary, removed after post-install
BUNDLE_ID_PREFIX = "io.github.lca-toolkit."  # macOS CFBundleIdentifier prefix used in menu.json


PLATFORMS = ["osx-arm64", "osx-64", "win-64", "linux-64"]


def current_platform() -> str:
    machine = platform.machine().lower()
    if sys.platform == "win32":
        return "win-64"
    if sys.platform == "darwin":
        return "osx-arm64" if machine == "arm64" else "osx-64"
    if sys.platform.startswith("linux") and machine in ("x86_64", "amd64"):
        return "linux-64"
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


def suggested_material_url() -> str:
    url = os.environ.get("MATERIAL_SUGGESTED_URL", "").strip() or SUGGESTED_MATERIAL_URL
    if "@" in url.split("://", 1)[-1].split("/", 1)[0]:
        raise SystemExit("MATERIAL_SUGGESTED_URL must not contain credentials; it is built into the installer")
    return url


def render_template(path: Path, url: str) -> str:
    return path.read_text().replace("@MATERIAL_URL@", url)


def write_post_install(out: Path, plat: str, wheels: list[Path], material_url: str) -> str:
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
        dialogs = "linux_material_prompts.sh" if plat == "linux-64" else "macos_material_dialogs.sh"
        with script.open("a") as f:
            f.write(render_template(INSTALLER_DIR / dialogs, material_url))
    return script.name


def write_pre_install_osx(out: Path) -> str:
    # menuinst refuses to overwrite an existing .app ("App already exists"), and the pkg still
    # reports success, so reinstalls/updates would keep stale shortcuts. Remove our own apps
    # (matched by bundle identifier from menu.json) before the shortcuts are created.
    script = out / "pre_install.sh"
    script.write_text(
        "#!/bin/bash\n"
        'case "$PREFIX" in\n'
        '    /Library/*) apps=/Applications ;;\n'
        '    *) apps="$(dirname "$(dirname "$PREFIX")")/Applications" ;;  # ~/Library/<x> -> ~/Applications\n'
        "esac\n"
        'for app in "$apps"/*.app; do\n'
        '    id=$(/usr/libexec/PlistBuddy -c "Print :CFBundleIdentifier" "$app/Contents/Info.plist" 2>/dev/null)\n'
        f'    case "$id" in {BUNDLE_ID_PREFIX}*) rm -rf "$app" ;; esac\n'
        "done\n"
        "exit 0\n"
    )
    return script.name


def construct_yaml(
    plat: str, version: str, specs: list[str], wheels: list[Path], post_install: str
) -> dict:
    extra_files = [{f"wheels/{w.name}": f"{WHEEL_DIR_IN_PREFIX}/{w.name}"} for w in wheels]
    extra_files.append({"requirements.txt": f"{WHEEL_DIR_IN_PREFIX}/requirements.txt"})
    extra_files.append({"launcher.py": f"{SHARE_IN_PREFIX}/launcher.py"})
    # JupyterLab defaults for this environment (start the kernel without asking)
    extra_files.append({"jupyterlab_overrides.json": "share/jupyter/lab/settings/overrides.json"})
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
            "default_prefix_all_users": f"%ALLUSERSPROFILE%\\{PREFIX_DIR}",
            "register_python_default": False,
            # constructor's template, patched to offer replacing an existing installation
            "nsis_template": "main.nsi.tmpl",
        }
        cfg["post_install_pages"] = ["material_pages.nsi"]
    elif plat == "linux-64":
        cfg |= {
            "installer_type": "sh",
            "installer_filename": f"{NAME}-{version}-Linux-x86_64.sh",
            # all users: run the installer with sudo and choose e.g. /opt/lca-toolkit
            "default_prefix": f"$HOME/{PREFIX_DIR}",
        }
    else:
        arch = "arm64" if plat == "osx-arm64" else "x86_64"
        cfg |= {
            "installer_type": "pkg",
            "installer_filename": f"{NAME}-{version}-macOS-{arch}.pkg",
            # "Install for me only" -> ~/Library/<pkg_name>, shortcuts in ~/Applications;
            # "Install for all users" (admin) -> /Library/<pkg_name>, shortcuts in /Applications.
            # Without the Library component a system install would target / (read-only on macOS).
            "pkg_name": PREFIX_DIR,
            "default_location_pkg": "Library",
            "pre_install": "pre_install.sh",
            "pkg_domains": {"enable_anywhere": False, "enable_currentUserHome": True, "enable_localSystem": True},
        }
    return cfg


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--platform", default=current_platform(), choices=PLATFORMS)
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
    material_url = suggested_material_url()
    shutil.copy(LAUNCHER, out / "launcher.py")
    shutil.copy(LAUNCHER.parent / "jupyterlab_overrides.json", out / "jupyterlab_overrides.json")
    if args.platform == "win-64":
        (out / "material_pages.nsi").write_text(
            render_template(INSTALLER_DIR / "windows_material_pages.nsi", material_url)
        )
    post_install = write_post_install(out, args.platform, wheels, material_url)
    if args.platform.startswith("osx-"):
        write_pre_install_osx(out)
    elif args.platform == "win-64":
        from run_constructor import patched_nsis_template

        (out / "main.nsi.tmpl").write_text(patched_nsis_template())
    (out / "construct.yaml").write_text(
        yaml.safe_dump(
            construct_yaml(args.platform, args.version, specs, wheels, post_install), sort_keys=False
        )
    )
    print(
        f"rendered {out / 'construct.yaml'}: {len(specs)} conda packages, {len(wheels)} wheels, "
        f"suggested notebooks repository: {material_url}"
    )

    if not args.no_build:
        # run_constructor.py = constructor + our "replace an existing installation" patches
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / "run_constructor.py"), str(out),
             "--output-dir", str(out / "installer"), "--platform", args.platform],
            check=True,
        )


def _workspace_version() -> str:
    import tomllib

    return tomllib.loads((ROOT / "pixi.toml").read_text())["workspace"]["version"]


if __name__ == "__main__":
    main()
