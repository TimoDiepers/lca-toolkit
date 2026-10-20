
# --- Optional external resources (git repository) + project restore ---------------------
# Appended to post_install.sh by tools/make_installer.py, which fills in the suggested
# repository (SUGGESTED_MATERIAL_URL); users can paste any other link, e.g. course material
# with a token.
# macOS .pkg installers can't have custom pages without a compiled Installer plug-in, so this
# asks with AppleScript dialogs, the same way constructor's own scripts show alerts. pkg scripts run as root; git/bw2io run as the
# logged-in user so files and Brightway projects end up owned by (and visible to) them.
set +e
[[ "${INSTALLER_UNATTENDED:-0}" == "1" ]] && exit 0

user=$(stat -f%Su /dev/console)
uid=$(id -u "$user")
home=$(dscl . -read "/Users/$user" NFSHomeDirectory | awk '{print $2}')
launcher=("$PREFIX/bin/python" "$PREFIX/share/lca-toolkit/launcher.py")
as_user() { sudo -H -u "$user" "$@"; }
# Dialogs must run in the user's GUI session: a root osascript from the pkg's postinstall
# fails silently there. `activate` brings the dialog in front of the Installer window.
# Errors (incl. "User canceled") go to /var/log/install.log.
ask() { launchctl asuser "$uid" sudo -H -u "$user" osascript -e "activate" -e "$1"; }

url="@MATERIAL_URL@"
while true; do
    # The text field is prefilled with the example (or the link from a previous attempt).
    reply=$(ask "set r to display dialog \"Do you want to add external resources from a git repository, e.g. teaching material, tutorials or the files of a study? Paste the link you were given (it may contain an access token), or keep the example. Needs an internet connection; LCA Notebooks then opens in that folder.\" default answer \"$url\" buttons {\"Skip\", \"Download\"} default button \"Download\" with title \"Additional resources\"
if button returned of r is \"Download\" then return text returned of r
return \"\"") || exit 0
    [[ -n "$reply" ]] || exit 0
    url=$reply
    parent=$(ask "POSIX path of (choose folder with prompt \"Choose where to put the resources (a subfolder named like the repository is created):\" default location POSIX file \"$home/Documents\")") || exit 0
    as_user "${launcher[@]}" fetch-material --url "$url" --parent "$parent" && break
    retry=$(ask 'button returned of (display dialog "The resources could not be downloaded. Check the link and your internet connection, and that the folder does not already contain other files." buttons {"Skip", "Try again"} default button "Try again" with icon caution)')
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
