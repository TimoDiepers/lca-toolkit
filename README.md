# LCA Toolkit

Single-click installers for [Brightway](https://docs.brightway.dev)-based life cycle assessment. After installing you get two programs:

<table>
  <tr>
    <td align="center" width="50%">
      <img src="recipe/shortcuts/icons/lca-notebooks.svg" width="72" alt=""><br>
      <b>LCA Notebooks</b><br><br>
      Brightway as Code in Python Notebooks. Bundles <a href="https://jupyter.org">JupyterLab</a> & <a href="https://docs.brightway.dev">Brightway 2.5</a>.
    </td>
    <td align="center" width="50%">
      <img src="recipe/shortcuts/icons/lca-browser.svg" width="72" alt=""><br>
      <b>LCA Browser</b><br><br>
      Point-and-click LCA Graphical Interface. Bundles <a href="https://github.com/LCA-ActivityBrowser/activity-browser">Activity Browser 3 (beta)</a>.
    </td>
  </tr>
</table>

Both programs use the same Python environment and the same Brightway projects, so a
project you create in one shows up in the other.

## Download

<!-- The links point to the newest GitHub release (assets with stable names, added by the
     release job in .github/workflows/build.yml). They work once the first v* tag has been
     released, and only for people who can see the repository while it is private. -->

| Your computer | Download |
|---|---|
| **Windows** 10 or 11 (64-bit) | [**LCA-Toolkit-Windows-x86_64.exe**](https://github.com/TimoDiepers/lca-toolkit/releases/latest/download/LCA-Toolkit-Windows-x86_64.exe) |
| **Mac with Apple Silicon** (M1, M2, M3, M4, …), macOS 13 or newer | [**LCA-Toolkit-macOS-arm64.pkg**](https://github.com/TimoDiepers/lca-toolkit/releases/latest/download/LCA-Toolkit-macOS-arm64.pkg) |
| **Mac with Intel processor**, macOS 13 or newer | [**LCA-Toolkit-macOS-x86_64.pkg**](https://github.com/TimoDiepers/lca-toolkit/releases/latest/download/LCA-Toolkit-macOS-x86_64.pkg) |
| **Linux** (64-bit, e.g. Ubuntu 22.04 or newer) | [**LCA-Toolkit-Linux-x86_64.sh**](https://github.com/TimoDiepers/lca-toolkit/releases/latest/download/LCA-Toolkit-Linux-x86_64.sh) |

Older versions: [all releases](https://github.com/TimoDiepers/lca-toolkit/releases).

- You need about **3 GB** of free disk space (Linux: about **5.5 GB**).
- The installation itself works offline. Downloading notebooks (optional, see
  [below](#additional-resources-and-project-backup)) needs internet.
- **Which Mac do I have?** Apple menu → *About This Mac*: "Chip: Apple M…" means Apple
  Silicon, "Processor: … Intel …" means Intel.

## Installing on Windows

1. Double-click the downloaded `.exe`.
2. Windows shows **"Windows protected your PC"**. This appears because the installer is
   not signed with a paid certificate. Click **More info**, then **Run anyway**.
3. Click through the installer:
   - **Just Me** (default, recommended) needs no admin rights. **All Users** needs an
     admin password.
   - If your Windows user name contains a space, change the install folder to e.g.
     `C:\lca-toolkit`.
4. Optionally add **external resources** from a git repository (e.g. teaching material)
   and restore a **project backup**, see [below](#additional-resources-and-project-backup).
5. Start **LCA Browser** or **LCA Notebooks** from the Start Menu or the desktop.

## Installing on macOS

1. Double-click the downloaded `.pkg`. macOS says *Apple could not verify
   "LCA-Toolkit-….pkg" is free of malware…*. This appears because the installer isn't
   signed by an Apple developer account. Click **Done** (not "Move to Trash").
2. Open **System Settings → Privacy & Security**, scroll down to
   *"LCA-Toolkit-….pkg" was blocked…* and click **Open Anyway**. Enter your Mac password
   and confirm **Open Anyway** again. The installer starts.
3. At *Installation Type* / *Destination*, choose:
   - **Install for me only** (recommended, no admin password needed), or
   - **Install for all users of this computer** (needs an admin password).
4. Finish the installer. Near the end, small windows ask whether to add **external
   resources** from a git repository (e.g. teaching material) and restore a **project backup**, see
   [below](#additional-resources-and-project-backup). They may appear behind the installer window.
5. Start **LCA Browser** or **LCA Notebooks**. The easiest way is Spotlight: press
   ⌘ Space, type **LCA**, pick one with the arrow keys and press Enter.
   - "Install for me only": the apps are in the *Applications* folder **inside your home
     folder** (Finder → Go → Home → Applications), not the main Applications folder.
   - "Install for all users": the apps are in the normal *Applications* folder.
   - Tip: while an app runs, right-click its Dock icon → Options → **Keep in Dock**.

## Installing on Linux

The Linux installer is a script you run in a terminal (no admin rights needed):

```bash
cd ~/Downloads
bash LCA-Toolkit-Linux-x86_64.sh
```

1. Press Enter to accept the install location (`~/lca-toolkit`), or type another one.
2. Answer the questions about **external resources** and the **project backup** in the terminal
   (see [below](#additional-resources-and-project-backup)). For the backup, type or paste the path of
   the `.tar.gz` file.
3. Start **LCA Browser** or **LCA Notebooks** from your desktop's application menu
   (category *Science* / *Education*). They can take a few seconds to appear in the menu.

For all users: `sudo bash LCA-Toolkit-Linux-x86_64.sh` and choose e.g.
`/opt/lca-toolkit`. The menu entries then appear for everyone.

## Additional resources and project backup

At the end of the installation you're asked:

1. **Add external resources from a git repository?** For example teaching material,
   tutorials or the files of a study. The link field is prefilled with
   [Brightway from the ground up](https://github.com/brightway-lca/from-the-ground-up), an
   introduction to Brightway. If you were given a link, paste it there instead. Then
   choose a folder (default: *Documents*). The repository is downloaded into a subfolder
   named like it, and LCA Notebooks then always opens there.
2. **Do you already have the project backup (`.tar.gz`)?** Only asked if you downloaded
   something in step 1. If you were given one, choose the file. It is restored so the project is
   directly available in LCA Browser and LCA Notebooks. Large projects can take a few
   minutes. If a project with the same name exists, you're asked whether to overwrite it.

Both are optional.

## Using the programs

- **LCA Notebooks** opens JupyterLab in your web browser, plus a terminal window with its
  log. Keep that window open while you work, and close it to stop JupyterLab. It opens in
  the downloaded folder from step 1 if there is one, otherwise in the `LCA-Notebooks` folder in
  your home folder.
- **LCA Browser** and LCA Notebooks use the same Brightway projects, so a project you
  create in one shows up in the other.
- **ecoinvent** is not included (license). Import it in LCA Browser with your own
  ecoinvent account.

## Updating

Download the new installer and run it like the first time, with the same choice ("Just
Me" / "for me only", or all users). It detects the existing installation and asks whether
to **replace** it. Your notebooks, teaching material and Brightway projects are kept. Close
LCA Browser and LCA Notebooks first.

## Uninstalling

- **Windows:** Settings → Apps → Installed apps → "LCA-Toolkit" → ⋯ → Uninstall.
- **Linux:** `rm -rf ~/lca-toolkit ~/.local/share/applications/*lca-toolkit*` (all-users
  install: `sudo rm -rf /opt/lca-toolkit /usr/share/applications/*lca-toolkit*`).
- **macOS:** move the two apps **LCA Browser** and **LCA Notebooks** to the Trash (in
  *Applications* in your home folder, or the main *Applications* folder). Then, in Finder,
  press ⇧⌘G, go to `~/Library/lca-toolkit` ("for me only") or `/Library/lca-toolkit` ("for
  all users"), and move that folder to the Trash.

This keeps your notebooks, the teaching material and your Brightway projects. To remove
those too, delete:

| What | Windows | macOS | Linux |
|---|---|---|---|
| Teaching material | the folder you chose (default `Documents\<material>`) | the folder you chose (default `~/Documents/<material>`) | the folder you chose (default `~/Documents/<material>`) |
| Default notebook folder | `%USERPROFILE%\LCA-Notebooks` | `~/LCA-Notebooks` | `~/LCA-Notebooks` |
| Brightway projects ⚠️ shared with any other Brightway installation | `%LOCALAPPDATA%\pylca\Brightway3` | `~/Library/Application Support/Brightway3` | `~/.local/share/Brightway3` |
| Settings | `%APPDATA%\lca-toolkit` | `~/Library/Application Support/lca-toolkit` | `~/.config/lca-toolkit` |

## Troubleshooting

- **macOS: nothing happens / "blocked" when opening the installer.** Use *Open Anyway*
  in System Settings → Privacy & Security (step 2 above).
- **Windows: "Directory … is not empty".** The folder contains something that isn't an LCA
  Toolkit installation. Choose another folder.
- **Windows: the installer refuses a path with spaces.** Choose e.g. `C:\lca-toolkit`.
- **Linux: "File or directory already exists".** The folder contains something that isn't
  an LCA Toolkit installation. Choose another location.
- **LCA Notebooks closed / the browser tab says the server is gone.** You closed the
  terminal window. Start LCA Notebooks again.
- **Download from the git repository failed during installation.** Check the link and your internet
  connection and run the installer again (choose *Replace*).

---

# For maintainers

Everything below is about building and changing the installers.

**How the toolkit is put together:**
- **Brightway 2.5** (bw2data, bw2calc, bw2io, …), **Activity Browser 3** (newest beta) and
  **JupyterLab** go into one self-contained environment.
- The two shortcuts above are created at install time.
- At the end, the installer offers to add external resources from a git repository and to
  restore a Brightway project backup (see *Additional resources step*).

| Platform (pixi name) | Installer file | Fast sparse solver | Qt / PySide6 from |
|---|---|---|---|
| Windows x64 (`win-64`) | `LCA-Toolkit-<version>-Windows-x86_64.exe` | pypardiso (Intel MKL) | conda-forge |
| macOS Apple Silicon (`osx-arm64`) | `LCA-Toolkit-<version>-macOS-arm64.pkg` | scikit-umfpack (SuiteSparse) | conda-forge |
| macOS Intel (`osx-64`) | `LCA-Toolkit-<version>-macOS-x86_64.pkg` | scikit-umfpack (SuiteSparse) | **PyPI** |
| Linux x64 (`linux-64`) | `LCA-Toolkit-<version>-Linux-x86_64.sh` | pypardiso (Intel MKL) | conda-forge |

Activity Browser needs Qt WebEngine. conda-forge has no `qt6-webengine` for `osx-64`, so on
Intel Macs PySide6 comes from PyPI: its universal2 wheels bundle their own Qt including
WebEngine (macOS 13+). That's also why `matplotlib-base` is used instead of `matplotlib`,
which would pull in a second Qt from conda-forge.

## What gets installed where

The Windows and macOS installers let the user choose **"Just me"** (no admin rights
needed, the default) or **"All users"** (admin password required). On Linux, running the
installer with `sudo` and an install location such as `/opt/lca-toolkit` does the same:

| | Software (environment) | Shortcuts |
|---|---|---|
| Windows, just me | `%USERPROFILE%\lca-toolkit` | Start Menu → *LCA Toolkit*, plus desktop |
| Windows, all users | `%ALLUSERSPROFILE%\lca-toolkit` (usually `C:\ProgramData\lca-toolkit`) | Start Menu (all users) |
| macOS, just me | `~/Library/lca-toolkit` | `~/Applications` |
| macOS, all users | `/Library/lca-toolkit` | `/Applications` |
| Linux, just me | `~/lca-toolkit` (asked during install) | `~/.local/share/applications` (application menu) |
| Linux, all users (`sudo`) | e.g. `/opt/lca-toolkit` | `/usr/share/applications` |

For every user:
- JupyterLab opens in the downloaded repository's folder if the user added one (see *Additional resources step*). Otherwise it opens in `LCA-Notebooks` in the home folder (`%USERPROFILE%\LCA-Notebooks` or `~/LCA-Notebooks`).
- Brightway projects are kept in Brightway's default data directory, which Activity Browser and JupyterLab share.
- JupyterLab only offers the toolkit's own Python kernel and starts it without asking. Kernels from other Python setups (in `~/Library/Jupyter`, `~/.local/share/jupyter`, `%APPDATA%\jupyter`) are hidden there, because they lack the toolkit's packages.
- On macOS, the environment folder belongs to the installing user even for "all users", so that user can still `pip install` extra packages.

The installer does not touch `PATH`, shell init files or the registry's "default Python",
so it can't interfere with other Python/conda installations.

---

## Repository layout

| Path | What it is | Edit it when … |
|---|---|---|
| `pixi.toml` | **Single source of truth** for the environment (conda-forge + PyPI dependencies), plus the build tooling environment and tasks | you add/remove/pin packages |
| `pixi.lock` | Exact versions for every package on every platform, generated by pixi | never by hand; regenerate with `pixi lock` / `pixi update` |
| `tools/make_installer.py` | Turns `pixi.lock` into a constructor installer (see *How the build works*) | you rename the toolkit or change installer options |
| `recipe/shortcuts/menu.json` | Shortcut definitions (menuinst format): names, icons, commands | you rename, change what a shortcut runs, or add a shortcut |
| `recipe/shortcuts/icons/` | Shortcut icons: `*.svg` sources, generated `*.icns` / `*.ico` (committed) | you change an icon (then `pixi run -e build icons`) |
| `tools/make_icons.py` | Renders the SVGs to `.icns` / `.ico` | you change icon sizes or margins |
| `launcher/launcher.py` | Shipped into the env: starts JupyterLab in the right folder with only the toolkit kernel; clones/updates the external-resources repository; restores project backups | you change what the LCA Notebooks shortcut or the material steps do |
| `launcher/jupyterlab_overrides.json` | Shipped as JupyterLab's `overrides.json`: default settings (auto-start the kernel) | you want other JupyterLab defaults |
| `installer/windows_material_pages.nsi`, `installer/macos_material_dialogs.sh`, `installer/linux_material_prompts.sh` | Installer steps "add external resources from a git repository" + project restore | you change those dialogs |
| `tools/run_constructor.py`, `installer/macos_checks_before_install.sh` | constructor with our patches: replace an existing installation instead of refusing (see *Updating installations*) | you change the update behaviour, or constructor changes the patched code |
| `tests/test_launcher.py` | Tests the launcher's material + restore steps in an installed env | — |
| `recipe/shortcuts/recipe.yaml` | rattler-build recipe for the tiny `lca-toolkit-shortcuts` conda package that carries `menu.json` and the icons | you rename the shortcut package; bump its version whenever `menu.json` or an icon changes |
| `tests/smoke.py` | Checks an *installed* environment: solver active, Qt WebEngine, AB, JupyterLab, AB starts headless | you add packages that should be verified |
| `.github/workflows/build.yml` | CI: builds all four installers, installs them on fresh runners, runs the tests, publishes releases | you change platforms or release flow |
| `build/` (git-ignored) | Build outputs: rendered `construct.yaml`, downloaded wheels, final installers | — |
| `.superpowers/` (git-ignored) | Scratch files from design sessions (icon mockups) | — |

---

## How the build works

```
pixi.toml ──pixi lock──▶ pixi.lock
                            │
        tools/make_installer.py (per platform)
                            │
      ┌─────────────────────┼──────────────────────────────┐
      ▼                     ▼                              ▼
 conda packages        PyPI wheels                  shortcuts package
 → exact specs in      → downloaded + sha256-       (recipe/shortcuts: menu.json
   construct.yaml        checked, bundled as          + icons, built by
                         extra_files, installed       rattler-build into
                         offline by post_install      build/channel)
      └─────────────────────┼──────────────────────────────┘
                            ▼
                 constructor → .exe / .pkg
```

1. **`pixi.toml` → `pixi.lock`.** pixi resolves the conda-forge packages and the PyPI
   packages together, so the combination is known to be consistent, per platform.
2. **Shortcut package.** `pixi run -e build build-shortcuts` builds
   `recipe/shortcuts` into a local channel (`build/channel`).
3. **`tools/make_installer.py`**, for the current OS:
   - converts each locked conda package into an exact spec (`name=version=build`);
   - downloads each locked PyPI wheel and checks it against the lock's sha256;
   - writes a `post_install` script that runs
     `pip install --no-index --no-deps -r requirements.txt` against the bundled wheels and
     then deletes them (plus the external-resources dialogs on macOS / prompts on Linux);
   - writes a macOS `pre_install` script that removes old shortcut apps (see *Shortcuts*);
   - adds `launcher.py` and the JupyterLab defaults as `extra_files`;
   - renders `build/<platform>/construct.yaml` and runs
     [constructor](https://github.com/conda/constructor).
4. **constructor** builds the installer. At install time, it unpacks the conda packages,
   runs `post_install` (PyPI wheels), and
   [menuinst](https://github.com/conda/menuinst) creates the shortcuts from `menu.json`.

The finished installer needs **no internet** during installation.

### Why not conda-only (or uv-only)?

- **Not conda-only:** the Activity Browser 3 beta is published on the `lca` conda channel,
  but those builds pull `bw_graph_tools 0.5` / `bw_functional` with `numpy<2` and, for the
  newest beta, an unsolvable `bw2io → pyecospold → lxml==4.9.3` chain. The PyPI wheels of
  the same AB version have none of these problems, so AB and Brightway come from PyPI.
- **Not uv/PyPI-only:** `scikit-umfpack` (the fast solver on macOS) has no wheels
  on PyPI, only an sdist that needs SuiteSparse and a compiler. conda-forge has prebuilt
  binaries, as well as Qt/WebEngine and MKL.

pixi is effectively "uv + conda-forge": it locks both kinds of packages together (and uses
uv internally for the PyPI part).

---

## Changing dependencies

All dependency changes happen in **`pixi.toml`**, followed by re-locking.

### Where to put a package

| Kind of package | Section in `pixi.toml` | Example |
|---|---|---|
| Compiled / non-Python libraries, anything on conda-forge that is heavy or binary | `[dependencies]` | `pandas = "*"`, `geopandas = ">=1"` |
| Only on some platforms | `[target.<platform>.dependencies]` (`win-64`, `osx-arm64`, `osx-64`, `linux-64`) | `pypardiso`, `scikit-umfpack`, `pyside6` |
| Pure-Python packages, or packages only on PyPI | `[pypi-dependencies]` | `bw_temporalis = "*"`, `premise = ">=2.2"` |

Rules of thumb:
- Prefer conda-forge for anything with compiled code. Every PyPI package must have a
  **wheel** for every platform; `make_installer.py` refuses sdists, because users can't
  compile.
- Don't list the same package in both sections. pixi uses the conda version and treats
  it as satisfying the PyPI requirement.

### Workflow

```bash
# 1. edit pixi.toml, e.g. add  bw_temporalis = "*"  under [pypi-dependencies]

# 2. re-lock and install into your local dev environment
pixi lock                 # or: pixi install

# 3. try it
pixi run ab               # Activity Browser
pixi run lab              # JupyterLab
pixi run python -c "import bw_temporalis"

# 4. (optional) build + test the installer for your own OS, see below

# 5. commit pixi.toml AND pixi.lock, push / open a PR → CI builds and tests all platforms
```

### Updating versions

```bash
pixi run update-ab                 # newest Activity Browser beta (= `pixi update activity-browser`)
pixi update bw2calc                # newest allowed version of one package
pixi update                        # everything (within the constraints in pixi.toml)
```

The `activity-browser` constraint in `pixi.toml` is a minimum (`>=3.0.0b…`). It must
contain a pre-release marker (`b`), or the resolver won't consider beta versions. The
manual CI run also updates AB to the newest beta by default (see *CI and releases*).

### Changing the Python version

Edit `python = "3.13.*"` in `pixi.toml` and re-lock. Check that `scikit-umfpack` and
`pypardiso` still resolve for that Python version on conda-forge.

### Adding a platform

Add it to `platforms` in `pixi.toml` (with its solver and Qt under `[target.<platform>…]`),
add it to `PLATFORMS`, `current_platform()` and `construct_yaml()` in
`tools/make_installer.py`, give `menu.json` a `platforms` block if needed, and add a job to
the CI matrix and copies to the release job. Activity Browser needs Qt WebEngine; check
conda-forge (`pixi search -p <platform> qt6-webengine`) or fall back to PySide6 wheels from
PyPI like `osx-64`.

---

## Additional resources step

At the end of every installation, users can add external resources (teaching material,
tutorials, the files of a study, …) from **any git repository** and restore a Brightway project backup. Nothing course-specific is built
into the installer:

1. "Do you want to add external resources from a git repository?" with a **free text field** for the link,
   prefilled with `SUGGESTED_MATERIAL_URL` in `tools/make_installer.py`
   ([Brightway from the ground up](https://github.com/brightway-lca/from-the-ground-up)),
   and a folder choice (default **Documents**). For a course, give students a link to
   paste, e.g. a read-only GitLab/GitHub token URL
   `https://name:token@git.example.org/course/material.git`. The repository is cloned into
   `<folder>/<repository name>`, and JupyterLab then opens there instead of `LCA-Notebooks`.
2. Only if they downloaded something in step 1: "Do you already have the project backup
   (`.tar.gz`)?" If they pick the file, it is restored with
   `bw2io.backup.restore_project_directory`, so the project is directly available in
   Activity Browser and JupyterLab. If a project with that name exists, users are asked
   whether to overwrite it.

To prefill a different repository, change `SUGGESTED_MATERIAL_URL`, or set
`MATERIAL_SUGGESTED_URL` for one build. It must not contain credentials, because it is
built into the installer (the build refuses such URLs).

> A link with a token ends up in the user's clone (`.git/config`), so `update-material`
> keeps working. Only hand out read-only tokens, and revoke them when the course ends.

Where this is implemented:
- **Windows:** two extra installer pages, `installer/windows_material_pages.nsi`
  (constructor `post_install_pages`).
- **macOS:** `.pkg` installers can't have custom pages without a compiled Installer
  plug-in, so `installer/macos_material_dialogs.sh` is appended to the post-install script
  and asks with AppleScript dialogs. The post-install script runs as root, so the dialogs,
  git and bw2io run as the logged-in user in their own session (`launchctl asuser` +
  `sudo -u`); a root `osascript` there fails silently. Dialog errors end up in
  `/var/log/install.log` (search for `postinstall`).
- **Linux:** the `.sh` installer runs in a terminal, so `installer/linux_material_prompts.sh`
  (appended to the post-install script) asks there, reading from `/dev/tty`. With `sudo`,
  git and bw2io run as the user who called sudo.
- Silent/unattended installs skip both steps (Windows `/S`; Linux `-b`; on macOS any
  command-line `installer -pkg …`, which constructor reports as `INSTALLER_UNATTENDED=1`).
- git runs with credential helpers and prompts switched off. A token, if any, is in the
  URL, and Windows' git would otherwise open a credential-helper window, which hangs
  unattended installs. The launcher never prints the URL, and git itself strips
  credentials from its messages, so tokens stay out of installer logs.
- The actual work is done by `launcher/launcher.py`, which is shipped into the environment
  at `share/lca-toolkit/launcher.py`:

  ```
  python launcher.py lab                          # what the LCA Notebooks shortcut runs
  python launcher.py fetch-material --url URL --parent DIR  # clone into DIR/<repo name>
  python launcher.py update-material              # git pull --ff-only (keeps users' edits safe)
  python launcher.py restore-project FILE [--overwrite]
  ```

  Where a user put the material is stored per user in
  `%APPDATA%\lca-toolkit\config.json` / `~/Library/Application Support/lca-toolkit/config.json`.

`git` is part of the environment for this, which adds about 115 MB unpacked on Windows.

---

## Updating installations

constructor refuses to install into a folder that already exists (macOS: "Chosen path
already exists!", Windows: "Directory … is not empty", Linux: "File or directory already
exists"). To let users update by simply running the new installer,
`tools/make_installer.py` runs constructor through `tools/run_constructor.py`, which
patches all three installer types:

- **Windows:** a patched copy of constructor's NSIS template (`nsis_template`). On the
  directory page, if the folder contains `Uninstall-LCA-Toolkit.exe` and
  `conda-meta\history`, the installer asks "Replace it?". On yes, it runs the old
  uninstaller silently (removing its shortcuts and registry entries) and deletes the folder.
- **macOS:** constructor's `checks_before_install.sh` (the pkg's very first script) is swapped
  for `installer/macos_checks_before_install.sh`. If the folder contains
  `conda-meta/history` and `_conda`, it asks "Replace?" in a dialog and then deletes the
  folder. The old apps are removed by the `pre_install` step anyway (see *Shortcuts*).
- **Linux:** constructor's `header.sh` (the start of the `.sh` installer) gets the same
  check: if the folder holds `conda-meta/history` and `_conda`, it asks "Replace?
  [yes|no]" in the terminal and deletes the folder. constructor's own `-u` (update into
  the existing folder) still works as before.
- Anything else in the way is still refused. Silent/command-line installs (Windows `/S`,
  `installer -pkg …`, Linux `-b`) replace without asking. CI tests this by installing twice.
- Only the software folder is replaced. Notebooks, teaching material, Brightway projects
  and settings live elsewhere and are kept.
- If constructor changes the patched code, `run_constructor.py` fails the build with an
  assertion instead of silently shipping an unpatched installer. Update the copied text
  there, or compare the macOS script with constructor's `osx/checks_before_install.sh`.

---

## Renaming / rebranding

The name "LCA Toolkit" appears in these places, so keep them in sync:

| What | Where |
|---|---|
| Installer title + file name, install folder, shortcut package name, macOS bundle-ID prefix | constants block at the top of `tools/make_installer.py` (`NAME`, `COMPANY`, `PREFIX_DIR`, `SHORTCUTS_PACKAGE`, `BUNDLE_ID_PREFIX`) |
| Shortcut package name | `recipe/shortcuts/recipe.yaml` (`package.name`) |
| Shortcut names, icons, Start Menu folder, macOS bundle names/IDs | `recipe/shortcuts/menu.json` |
| Icon artwork | `recipe/shortcuts/icons/*.svg` (then `pixi run -e build icons`) |
| Fallback notebook folder (`LCA-Notebooks`), config folder | `launcher/launcher.py` |
| Install folder + shortcut names checked in CI | `.github/workflows/build.yml` |
| Installer version | `version` in `pixi.toml` (`[workspace]`) |
| User-facing text, download links (repository URL) | top of `README.md` |

> ⚠️ Keep the macOS bundle identifiers in `menu.json` starting with `BUNDLE_ID_PREFIX`.
> The macOS pre-install step uses it to find and replace old shortcuts (see *Shortcuts*).

---

## Shortcuts (`recipe/shortcuts/menu.json`)

Each entry in `menu_items` becomes one shortcut. `command` is what runs, and the
`platforms.win` / `platforms.osx` blocks override it per OS. Placeholders such as
`{{ PREFIX }}` are filled in by menuinst at install time.
[menuinst docs](https://conda.github.io/menuinst/).

- **Windows** uses menuinst's own activation (`"activate": true`).
- **macOS** sets `"activate": false` and activates manually with
  `$PREFIX/_conda shell.bash activate`. menuinst only looks for a standalone conda named
  `_conda.exe`, but constructor installs it as `_conda` on macOS, so menuinst's activation
  would call a bare `conda` that doesn't exist on users' machines.
- menuinst refuses to overwrite an existing `.app` (`App already exists`), and the pkg
  still reports success. A `pre_install` script (written by `make_installer.py`)
  therefore deletes the apps whose bundle identifier starts with `BUNDLE_ID_PREFIX`
  before the shortcuts are created.
- LCA Notebooks uses `"terminal": true`. The terminal window shows the JupyterLab server
  log, and closing it stops JupyterLab.

The two shortcuts are **LCA Browser** (Activity Browser) and **LCA Notebooks**
(JupyterLab). The names start with "LCA" so that the part that matters survives when a
desktop or Launchpad cuts long names short.

**Icons** live in `recipe/shortcuts/icons/`: one SVG per shortcut is the source, the
`.icns` (macOS) and `.ico` (Windows) next to it are generated from it and committed:

```bash
pixi run -e build icons     # after editing an SVG; then commit the .icns/.ico too
```

`tools/make_icons.py` drops the element with `id="label"` (the "LCA" lettering) at sizes
below 48 px, and adds Apple's usual margin to the macOS version. The lettering is stored as
outlines, not text, so it renders the same without any fonts installed. `menu.json` points at
the icons with `{{ MENU_DIR }}/<name>.{{ ICON_EXT }}`.

To add a shortcut (e.g. a second notebook folder, or a plain Python prompt), copy an entry,
change `name`, `icon`, `command` and the macOS `CFBundleName`/`CFBundleIdentifier`. Then rebuild.
Bump `context.version` in `recipe/shortcuts/recipe.yaml` when you change `menu.json`.

---

## Building locally

Builds the installer for the OS you are on (macOS → `.pkg`, Windows → `.exe`):

```bash
pixi run -e build installer
# → build/<platform>/installer/LCA-Toolkit-<version>-….pkg / .exe
```

Render the inputs only, without running constructor (also works for the other platform):

```bash
pixi run -e build python tools/make_installer.py --platform win-64 --no-build
# inspect build/win-64/construct.yaml, post_install.bat, requirements.txt
```

The shortcut package is rebuilt from scratch for every build (`build/channel` is deleted
first, and its stale copy is dropped from constructor's download cache), so changes to
`menu.json`, the icons or `recipe.yaml` are always picked up.

To prefill a different repository in the additional resources step (see *Additional resources step*):

```bash
MATERIAL_SUGGESTED_URL="https://github.com/org/repo.git" pixi run -e build installer
```

### Testing an installer locally

macOS (no admin rights needed):

```bash
installer -pkg build/osx-*/installer/*.pkg -target CurrentUserHomeDirectory
~/Library/lca-toolkit/bin/python tests/smoke.py --launch
~/Library/lca-toolkit/bin/python tests/test_launcher.py   # material + project restore
# clean up:
rm -rf ~/Library/lca-toolkit ~/Applications/"LCA Browser.app" ~/Applications/"LCA Notebooks.app"
# all-users variant: sudo installer -pkg … -target /   → /Library/lca-toolkit, /Applications
```

Windows (PowerShell):

```powershell
Start-Process .\build\win-64\installer\LCA-Toolkit-*.exe -Wait -ArgumentList '/S','/InstallationType=JustMe',"/D=$env:USERPROFILE\lca-toolkit"
& "$env:USERPROFILE\lca-toolkit\python.exe" tests\smoke.py --launch
& "$env:USERPROFILE\lca-toolkit\python.exe" tests\test_launcher.py
```

Linux:

```bash
bash build/linux-64/installer/*.sh -b -p ~/lca-toolkit     # -b: batch mode, no questions
~/lca-toolkit/bin/python tests/smoke.py --launch
~/lca-toolkit/bin/python tests/test_launcher.py
```

These silent/command-line installs skip the external-resources questions. To try those,
double-click the installer instead (Linux: run it without `-b`).

---

## CI and releases

`.github/workflows/build.yml` runs one job per platform: `macos-14` (Apple Silicon),
`macos-15-intel` (Intel Mac), `windows-latest` and `ubuntu-latest`. Each job:

1. builds the installer (`pixi run -e build installer`),
2. installs it silently on the runner: "just me", then again over that installation
   (checks that it is replaced), then "all users",
3. runs `tests/smoke.py --launch` with the installed Python (checks the solver, Qt
   WebEngine, AB and JupyterLab imports, and that AB stays up for 30 s headless) and
   `tests/test_launcher.py` (material download/update, project restore), and checks that
   the shortcuts (and the macOS icon) exist,
4. uploads the installers (and the `pixi.lock` used) as workflow artifacts.

A job is cancelled after 45 minutes; a normal run takes 10–20.

Triggers (a plain push to `main` does **not** build):
- **pull requests**: build + test with the committed `pixi.lock`;
- **manual run** (Actions → *Build installers* → *Run workflow*): updates Activity Browser
  to the newest beta first (checkbox, on by default). The lock used is in the artifact;
- **tag `v*`**: build + test with the committed `pixi.lock`, then publish all four
  installers as a GitHub release, plus copies without the version in the file name
  (`LCA-Toolkit-Windows-x86_64.exe`, `LCA-Toolkit-macOS-arm64.pkg`,
  `LCA-Toolkit-macOS-x86_64.pkg`, `LCA-Toolkit-Linux-x86_64.sh`). The download links at
  the top of this README point to those via `releases/latest/download/…`. See *Making a
  release* below.

### Making a release

A tag build never updates packages itself; it uses exactly what `pixi.lock` says. So bring
the lock up to date first, commit it, then tag:

```bash
git pull

# 1. update packages (pick what you need, see "Updating versions")
pixi run update-ab        # newest Activity Browser beta
pixi update               # or: everything, within the constraints in pixi.toml

# 2. check it locally (optional, but catches most problems before CI)
pixi run python tests/smoke.py --launch
pixi run -e build installer        # builds the installer for your own OS

# 3. bump the version in pixi.toml (semantic versioning, see below), e.g. 0.1.0 → 0.2.0

# 4. commit + push, then test-build exactly this lock (no AB update) and wait for green
git commit -am "Release 0.2.0: newest AB beta"
git push
gh workflow run build.yml -f update-ab=false    # or: Actions → Run workflow, untick the box

# 5. tag → CI builds + tests all platforms again and publishes the release
git tag v0.2.0
git push origin v0.2.0
```

After ~15 min the release appears under *Releases* with
the four `LCA-Toolkit-<version>-…` installers (plus the copies without version).
If any build or install test fails, nothing is published. Fix the problem, then move the
tag to the fixed commit (`git tag -f v0.2.0 && git push -f origin v0.2.0`) or use the
next patch version.

Versions follow [semantic versioning](https://semver.org): patch (`0.1.1`) for fixes and
updated packages, minor (`0.2.0`) for new features or dependencies, major for breaking
changes such as a new Python or Brightway generation. The build fails if the tag isn't
`v` + the `version` in `pixi.toml`, so file names and release always match.

Things to keep in mind:
- **Who can download it:** a release has the same visibility as the repository. While the
  repo is private, only collaborators can download it; share the files with students
  through your course platform instead, or make the repo public.
- **No course links or tokens are inside the installers.** Students paste their course
  link during installation, so the installers can be shared publicly.
- **Upgrading users** just run the new installer; it offers to replace the old
  installation (see *Updating installations* below).
- A manual run (Actions → *Run workflow*) gives the same installers as artifacts without
  publishing anything. Use it for test builds; the artifacts expire after 90 days.

---

## Known caveats

- **Unsigned installers.** macOS blocks the `.pkg` with *"Apple could not verify … is free
  of malware"*. Since macOS 15, right-click → Open no longer bypasses this, and users
  have to click **Open Anyway** in System Settings → Privacy & Security (see the install
  guide). Windows SmartScreen requires "More info → Run anyway". Proper signing needs an Apple Developer ID and a
  Windows code-signing certificate, plus extra constructor settings
  (`signing_identity_name`, `notarization_identity_name`, `signing_certificate`).
- **Windows paths with spaces.** constructor refuses install paths with spaces. If the
  user name contains one, choose e.g. `C:\lca-toolkit` in the installer.
- **ecoinvent** can't be bundled (license). Users import it in Activity Browser with
  their own ecoinvent account.
- **Size:** the installers are about 0.5 GB (Apple Silicon), 0.8 GB (Intel Mac, Windows) and 0.8 GB (Linux). Installed, the environment takes about 2–3 GB; the Linux installer wants about 5.5 GB free while installing (Intel MKL is large there).
