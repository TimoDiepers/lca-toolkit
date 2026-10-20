"""Helper shipped inside the installed environment (at share/lca-toolkit/launcher.py).

Used by the JupyterLab shortcut and by the installers' optional post-install steps:

    python launcher.py lab [jupyter args...]       start JupyterLab in the right folder
    python launcher.py fetch-material --url URL --parent DIR
                                                    clone a git repository (e.g. course material)
                                                    into DIR/<repository name>
    python launcher.py update-material              git pull the teaching material
    python launcher.py restore-project FILE [--overwrite]
                                                    restore a Brightway project backup (.tar.gz)

Exit codes: 0 ok, 1 error, 3 project already exists (rerun with --overwrite).

The material is any git repository the user names during installation (the installers
suggest a default, see tools/make_installer.py). Its URL may contain an access token, so it
is never printed. Where a user put the material is stored per user in config.json (see
config_path()); JupyterLab then opens there.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

PREFIX = Path(sys.prefix)
DEFAULT_NOTEBOOK_DIR = Path.home() / "LCA-Notebooks"
EXIT_PROJECT_EXISTS = 3


def config_path() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return base / "lca-toolkit" / "config.json"


def load_config() -> dict:
    try:
        return json.loads(config_path().read_text())
    except (OSError, ValueError):
        return {}


def save_config(**values) -> None:
    cfg = load_config() | values
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cfg, indent=2))


def git_exe() -> str:
    candidates = [PREFIX / "Library" / "bin" / "git.exe", PREFIX / "Library" / "cmd" / "git.exe", PREFIX / "bin" / "git"]
    for c in candidates:
        if c.is_file():
            return str(c)
    found = shutil.which("git")
    if not found:
        raise SystemExit("git not found in the environment")
    return found


def run_git(*args: str) -> int:
    # The token is in the URL, so git never needs to ask. Disable credential helpers and
    # prompts: conda-forge's Windows git otherwise pops up a credential-helper selector
    # (and hangs forever when nobody can click it).
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never")
    return subprocess.run([git_exe(), "-c", "credential.helper=", *args], env=env).returncode


def repo_name(url: str) -> str:
    """Folder name for a clone: the last path part of the URL, without .git (as git does)."""
    path = urlsplit(url).path if "://" in url else url.rsplit(":", 1)[-1]
    return path.rstrip("/").rsplit("/", 1)[-1].removesuffix(".git")


def fetch_material(url: str, parent: Path, branch: str | None = None) -> int:
    url = url.strip()
    name = repo_name(url)
    if not name:
        print("That doesn't look like a git repository link.", file=sys.stderr)
        return 1
    dest = parent.expanduser() / name
    if (dest / ".git").is_dir():
        print(f"Teaching material already present in {dest}")
    elif dest.exists() and any(dest.iterdir()):
        print(f"{dest} exists and is not empty; choose another folder.", file=sys.stderr)
        return 1
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        rc = run_git("clone", *(["--branch", branch] if branch else []), url, str(dest))
        if rc:
            return rc
    save_config(material_dir=str(dest))
    print(f"Material in {dest}")
    return 0


def update_material() -> int:
    target = load_config().get("material_dir")
    if not target or not (Path(target) / ".git").is_dir():
        print("No teaching material installed.", file=sys.stderr)
        return 1
    # --ff-only: never merge into (or overwrite) the user's own edits
    return run_git("-C", target, "pull", "--ff-only")


def restore_project(archive: Path, overwrite: bool) -> int:
    import bw2data as bd
    from bw2io.backup import restore_project_directory

    try:
        name = restore_project_directory(archive, overwrite_existing=overwrite)
    except ValueError as err:
        if "already exists" in str(err):
            print(err, file=sys.stderr)
            return EXIT_PROJECT_EXISTS
        raise
    print(f"Restored Brightway project {name!r} into {bd.projects.dir.parent}")
    return 0


def lab(extra: list[str]) -> int:
    target = load_config().get("material_dir")
    notebook_dir = Path(target) if target and Path(target).is_dir() else DEFAULT_NOTEBOOK_DIR
    notebook_dir.mkdir(parents=True, exist_ok=True)
    args = [
        f"--ServerApp.root_dir={notebook_dir}",
        # only this environment's kernel: hides kernels from other Python setups in
        # ~/Library/Jupyter or %APPDATA%\jupyter, which lack the toolkit's packages
        "--KernelSpecManager.allowed_kernelspecs=python3",
    ]
    return subprocess.run([sys.executable, "-m", "jupyterlab", *args, *extra]).returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("lab")
    fetch = sub.add_parser("fetch-material")
    fetch.add_argument("--url", required=True, help="git URL; may contain an access token")
    fetch.add_argument("--parent", type=Path, required=True)
    fetch.add_argument("--branch")
    sub.add_parser("update-material")
    restore = sub.add_parser("restore-project")
    restore.add_argument("archive", type=Path)
    restore.add_argument("--overwrite", action="store_true")
    args, extra = parser.parse_known_args()

    if args.cmd == "lab":
        return lab(extra)
    if extra:
        parser.error(f"unrecognized arguments: {' '.join(extra)}")
    if args.cmd == "fetch-material":
        return fetch_material(args.url, args.parent, args.branch)
    if args.cmd == "update-material":
        return update_material()
    return restore_project(args.archive, args.overwrite)


if __name__ == "__main__":
    sys.exit(main())
