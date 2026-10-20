"""Test the launcher's notebooks (git) and project-restore steps (run with the installed env's python).

Uses a temporary Brightway directory (BRIGHTWAY2_DIR), a temporary folder for the notebooks
and a temporary home/AppData for the launcher's config, so it never touches real projects or
settings. Clones the public repository the installers suggest by default.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

work = Path(tempfile.mkdtemp())
(work / "bw").mkdir()
(work / "home").mkdir()
os.environ["BRIGHTWAY2_DIR"] = str(work / "bw")
# keep the launcher's per-user config.json out of the real home/AppData
os.environ["HOME"] = os.environ["APPDATA"] = str(work / "home")
os.environ.pop("XDG_CONFIG_HOME", None)
launcher = Path(sys.prefix) / "share" / "lca-toolkit" / "launcher.py"


def run(*args) -> int:
    return subprocess.run([sys.executable, str(launcher), *map(str, args)]).returncode


URL = "https://github.com/brightway-lca/from-the-ground-up.git"  # SUGGESTED_MATERIAL_URL
assert run("fetch-material", "--url", URL, "--parent", work / "My Documents") == 0
assert (work / "My Documents" / "from-the-ground-up" / ".git").is_dir()
assert run("update-material") == 0
assert run("fetch-material", "--url", "https://user:token@example.invalid/x/repo.git", "--parent", work) != 0
print("notebooks: fetch + update ok")

import bw2data as bd  # noqa: E402
import bw2io as bi  # noqa: E402

bd.projects.set_current("launcher-test")
bd.Database("toy").write({("toy", "a"): {"name": "a", "exchanges": []}})
archive = bi.backup_project_directory("launcher-test", dir_backup=str(work))
bd.projects.set_current("default")
bd.projects.delete_project("launcher-test", delete_dir=True)

assert run("restore-project", archive) == 0
assert run("restore-project", archive) == 3, "expected 'project exists' exit code"
assert run("restore-project", archive, "--overwrite") == 0
bd.projects.set_current("launcher-test")
assert len(bd.Database("toy")) == 1
print("project restore: ok")
