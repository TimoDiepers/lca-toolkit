"""Run constructor with the LCA Toolkit's installer patches (called by make_installer.py).

Both patches let a user update by running the new installer over an existing installation:
constructor itself refuses a non-empty install folder. Only an existing installation of this
toolkit is replaced (after asking); any other folder is still refused.

- macOS: constructor has no option to replace its osx/checks_before_install.sh, so this
  swaps in installer/macos_checks_before_install.sh when constructor renders it.
- Windows: make_installer.py writes a patched copy of constructor's NSIS template
  (see patched_nsis_template) and passes it as `nsis_template`.

If constructor changes the patched code, the asserts below fail the build instead of
silently producing an installer without the patch.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAC_CHECKS = ROOT / "installer" / "macos_checks_before_install.sh"

NSIS_DIR_NOT_EMPTY = """\
Function OnDirectoryLeave
    ${If} ${IsNonEmptyDirectory} "$InstDir"
        ${Print} "::error:: Directory '$INSTDIR' is not empty, please choose a different location."
        MessageBox MB_OK|MB_ICONEXCLAMATION \\
            "Directory '$INSTDIR' is not empty,$\\n\\
             please choose a different location." \\
            /SD IDOK
        Abort
    ${EndIf}
"""

NSIS_REPLACE_EXISTING = """\
Function OnDirectoryLeave
    ${If} ${IsNonEmptyDirectory} "$InstDir"
        # LCA Toolkit patch (tools/run_constructor.py): replace an existing installation of
        # this toolkit instead of refusing. Silent installs (/S) replace without asking.
        ${If} ${FileExists} "$INSTDIR\\Uninstall-${NAME}.exe"
        ${AndIf} ${FileExists} "$INSTDIR\\conda-meta\\history"
            MessageBox MB_YESNO|MB_ICONQUESTION \\
                "${NAME} is already installed in '$INSTDIR'.$\\n$\\n\\
                 Replace it with version ${VERSION}? Your notebooks, teaching material and \\
                 Brightway projects are kept." \\
                /SD IDYES IDYES lca_replace_existing
            Abort
            lca_replace_existing:
            ${Print} "Removing the existing installation in $INSTDIR"
            ExecWait '"$INSTDIR\\Uninstall-${NAME}.exe" /S _?=$INSTDIR'
            RMDir /r "$INSTDIR"
            ${If} ${FileExists} "$INSTDIR\\*.*"
                ${Print} "::error:: Could not remove the existing installation in '$INSTDIR'."
                MessageBox MB_OK|MB_ICONSTOP \\
                    "The existing installation in '$INSTDIR' could not be removed completely.$\\n\\
                     Close Activity Browser and JupyterLab, then try again." \\
                    /SD IDOK
                Abort
            ${EndIf}
        ${Else}
            ${Print} "::error:: Directory '$INSTDIR' is not empty, please choose a different location."
            MessageBox MB_OK|MB_ICONEXCLAMATION \\
                "Directory '$INSTDIR' is not empty,$\\n\\
                 please choose a different location." \\
                /SD IDOK
            Abort
        ${EndIf}
    ${EndIf}
"""


def patched_nsis_template() -> str:
    from constructor import winexe

    tmpl = Path(winexe.NSIS_DIR, "main.nsi.tmpl").read_text()
    assert tmpl.count(NSIS_DIR_NOT_EMPTY) == 1, "constructor's OnDirectoryLeave changed; update tools/run_constructor.py"
    return tmpl.replace(NSIS_DIR_NOT_EMPTY, NSIS_REPLACE_EXISTING)


def main() -> int:
    from constructor import osxpkg
    from constructor.main import main as constructor_main

    original = osxpkg.move_script

    def move_script(src, dst, info, **kwargs):
        if Path(src).name == "checks_before_install.sh":
            src = str(MAC_CHECKS)
        return original(src, dst, info, **kwargs)

    osxpkg.move_script = move_script
    return constructor_main(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
