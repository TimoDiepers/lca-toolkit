
# --- Optional teaching material + project restore ---------------------------------------
# Appended to post_install.sh by tools/make_installer.py when MATERIAL_GIT_URL is set
# (@MATERIAL_NAME@ is replaced). macOS .pkg installers can't have custom pages without a
# compiled Installer plug-in, so this asks with AppleScript dialogs, the same way
# constructor's own scripts show alerts. pkg scripts run as root; git/bw2io run as the
# logged-in user so files and Brightway projects end up owned by (and visible to) them.
set +e
[[ "${INSTALLER_UNATTENDED:-0}" == "1" ]] && exit 0

user=$(stat -f%Su /dev/console)
home=$(dscl . -read "/Users/$user" NFSHomeDirectory | awk '{print $2}')
launcher=("$PREFIX/bin/python" "$PREFIX/share/lca-toolkit/launcher.py")
as_user() { sudo -H -u "$user" "$@"; }
ask() { osascript -e "tell application (path to frontmost application as text)" -e "$1" -e "end tell" 2>/dev/null; }

answer=$(ask 'button returned of (display dialog "Also download the @MATERIAL_NAME@ teaching material? This needs an internet connection. JupyterLab will then open in this folder." buttons {"Skip", "Download"} default button "Download" with title "@MATERIAL_NAME@")')
[[ "$answer" == "Download" ]] || exit 0
while true; do
    parent=$(ask "POSIX path of (choose folder with prompt \"Choose where to put the @MATERIAL_NAME@ folder:\" default location POSIX file \"$home/Documents\")") || exit 0
    as_user "${launcher[@]}" fetch-material --parent "$parent" && break
    retry=$(ask 'button returned of (display dialog "The @MATERIAL_NAME@ material could not be downloaded (no internet connection, or the folder already contains other files)." buttons {"Skip", "Try again"} default button "Try again" with icon caution)')
    [[ "$retry" == "Try again" ]] || exit 0
done

answer=$(ask 'button returned of (display dialog "Do you already have the project backup archive (.tar.gz) with the databases? It can be restored now, so it is directly available in Activity Browser and JupyterLab." buttons {"No", "Choose file…"} default button "Choose file…" with title "Brightway project")')
[[ "$answer" == "Choose file…" ]] || exit 0
archive=$(ask "POSIX path of (choose file with prompt \"Choose the project backup (.tar.gz):\" default location POSIX file \"$home/Downloads\")") || exit 0
as_user "${launcher[@]}" restore-project "$archive"
rc=$?
if [[ $rc == 3 ]]; then
    answer=$(ask 'button returned of (display dialog "A Brightway project with this name already exists. Overwrite it?" buttons {"Keep existing", "Overwrite"} default button "Keep existing" with icon caution)')
    [[ "$answer" == "Overwrite" ]] || exit 0
    as_user "${launcher[@]}" restore-project "$archive" --overwrite
    rc=$?
fi
if [[ $rc == 0 ]]; then
    ask 'display dialog "The project was restored." buttons {"OK"} default button "OK"' >/dev/null
else
    ask 'display dialog "The project could not be restored. Check that the file is a Brightway project backup (.tar.gz)." buttons {"OK"} default button "OK" with icon caution' >/dev/null
fi
exit 0
