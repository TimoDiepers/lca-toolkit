# Installing the LCA Toolkit

The LCA Toolkit installs **Activity Browser** and **JupyterLab** with **Brightway**, the
open-source LCA framework. You need about 3 GB of free disk space. No internet connection
is needed during installation.

## Windows

1. Download `LCA-Toolkit-…-Windows-x86_64.exe`.
2. Double-click it. If Windows shows "Windows protected your PC", click
   **More info → Run anyway**.
3. Click through the installer with the default options ("Just Me").
   If your user name contains a space, change the install folder to `C:\lca-toolkit`.
4. Start **Activity Browser (LCA Toolkit)** or **JupyterLab (LCA Toolkit)** from the
   Start Menu or the desktop.

## macOS (Apple Silicon: M1 or newer)

1. Download `LCA-Toolkit-…-macOS-arm64.pkg`.
2. **Right-click** the file → **Open** → **Open** (a plain double-click is blocked because
   the installer isn't signed).
3. Choose "Install for me only" and finish the installer.
4. Start **Activity Browser (LCA Toolkit)** or **JupyterLab (LCA Toolkit)** from
   *Applications* in your home folder (Finder → Go → Home → Applications), or with
   Spotlight (⌘ Space).

Not sure which Mac you have? Apple menu → *About This Mac*. "Chip: Apple M…" means
Apple Silicon. Macs with an Intel processor are not supported.

## Using it

- **JupyterLab** opens in your browser. Keep the terminal window that opens with it open
  while you work, and close it to stop JupyterLab. Your notebooks are saved in the
  `LCA-Notebooks` folder in your home directory.
- **Activity Browser** and JupyterLab use the same Brightway projects, so a project you
  create in one shows up in the other.

## Uninstalling

- Windows: Settings → Apps → "LCA-Toolkit" → Uninstall.
- macOS: delete the `lca-toolkit` folder in your home directory and the two
  "(LCA Toolkit)" apps in `~/Applications`.

Your notebooks (`LCA-Notebooks`) and Brightway projects are kept in both cases.
