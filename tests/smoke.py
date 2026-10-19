"""Smoke test for an installed LCA Toolkit environment (run with the env's own python).

Checks the fast sparse solver for the platform, the Qt WebEngine stack Activity Browser
needs, JupyterLab, and optionally that Activity Browser starts and stays up.
"""

import argparse
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--launch", action="store_true", help="also start Activity Browser headless for a while")
args = parser.parse_args()

import bw2calc  # noqa: E402

solver = "PYPARDISO" if sys.platform == "win32" else "UMFPACK"
assert getattr(bw2calc, solver), f"bw2calc is not using {solver}"
print(f"bw2calc {bw2calc.__version__}: {solver} active")

from importlib.metadata import version  # noqa: E402

from PySide6 import QtWebEngineWidgets  # noqa: E402,F401

import activity_browser  # noqa: E402,F401
import jupyterlab  # noqa: E402,F401

print("activity-browser", version("activity-browser"), "| jupyterlab", version("jupyterlab"))

if args.launch:
    scripts = Path(sys.prefix) / ("Scripts" if sys.platform == "win32" else "bin")
    exe = scripts / ("activity-browser.exe" if sys.platform == "win32" else "activity-browser")
    env = os.environ | {"QT_QPA_PLATFORM": "offscreen", "BRIGHTWAY2_DIR": tempfile.mkdtemp()}
    proc = subprocess.Popen([str(exe)], env=env)
    time.sleep(30)
    alive = proc.poll() is None
    proc.kill()
    assert alive, f"Activity Browser exited early with code {proc.returncode}"
    print("Activity Browser stayed up for 30 s")
