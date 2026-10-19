# Installing the LCA Toolkit

The LCA Toolkit installs **Activity Browser** and **JupyterLab** with **Brightway**, the
open-source LCA framework. You need about 3 GB of free disk space. No internet connection
is needed during installation.

## Windows

1. Download `LCA-Toolkit-…-Windows-x86_64.exe`.
2. Double-click it. If Windows shows "Windows protected your PC", click
   **More info → Run anyway**.
3. Click through the installer. "Just Me" (default) needs no admin rights, and
   "All Users" needs an admin password.
   If your user name contains a space, change the install folder to `C:\lca-toolkit`.
4. Start **LCA Browser** (Activity Browser) or **LCA Notebooks** (JupyterLab) from the
   Start Menu or the desktop.

## macOS (Apple Silicon: M1 or newer)

1. Download `LCA-Toolkit-…-macOS-arm64.pkg`.
2. Double-click it. macOS says *Apple could not verify "LCA-Toolkit-….pkg" is free of
   malware…*, because the installer isn't signed by an Apple developer account.
   Click **Done** (not "Move to Trash").
3. Open **System Settings → Privacy & Security**, scroll down to the message
   *"LCA-Toolkit-….pkg" was blocked…* and click **Open Anyway**. Enter your Mac password
   and confirm **Open Anyway** again. The installer starts.
4. At *Installation Type* / *Destination*, choose:
   - **Install for me only** (recommended, no admin password needed), or
   - **Install for all users of this computer** (needs an admin password; the apps then
     appear in the normal *Applications* folder).

   Then finish the installer.
5. Start **LCA Browser** (Activity Browser) or **LCA Notebooks** (JupyterLab). The easiest
   way is Spotlight: press ⌘ Space, type "LCA", and pick one with the arrow keys and Enter.
   - "Install for me only": the apps are in the *Applications* folder **inside your home
     folder** (Finder → Go → Home, or ⇧⌘H → Applications), not the main Applications
     folder.
   - "Install for all users": the apps are in the normal *Applications* folder.

   Tip: while an app runs, right-click its Dock icon → Options → Keep in Dock.

Not sure which Mac you have? Apple menu → *About This Mac*. "Chip: Apple M…" means
Apple Silicon. Macs with an Intel processor are not supported.

## Teaching material and project backup (if offered)

At the end of the installation you may be asked:

1. **Download the teaching material?** Choose a folder (default: *Documents*). The
   material is downloaded into a subfolder there, which needs an internet connection.
2. **Do you already have the project backup (`.tar.gz`)?** If you downloaded it already,
   choose the file. It is restored so the project is directly available in Activity
   Browser and JupyterLab. This can take a few minutes for large projects.

You can skip both and do them later.

## Using it

- **JupyterLab** opens in your browser. Keep the terminal window that opens with it open
  while you work, and close it to stop JupyterLab. It opens in the teaching material
  folder if you downloaded it, otherwise in the `LCA-Notebooks` folder in your home
  directory.
- **Activity Browser** and JupyterLab use the same Brightway projects, so a project you
  create in one shows up in the other.

## Uninstalling

- Windows: Settings → Apps → "LCA-Toolkit" → Uninstall.
- macOS: delete the two apps "LCA Browser" and "LCA Notebooks" and the software folder. In Finder, press
  ⇧⌘G and go to `~/Library/lca-toolkit` ("for me only") or `/Library/lca-toolkit` ("for all
  users"), then move that folder to the Trash.

To **update** to a new version, uninstall the old one first. The macOS installer stops
with "Chosen path already exists!" otherwise.

Your notebooks (`LCA-Notebooks`) and Brightway projects are kept in both cases.
