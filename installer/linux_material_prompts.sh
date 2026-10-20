
# --- Optional notebooks (git repository) + project restore -------------------------------
# Appended to post_install.sh by tools/make_installer.py, which fills in the suggested
# repository (SUGGESTED_MATERIAL_URL); users can paste any other link, e.g. course material
# with a token.
# The Linux installer is a shell script that runs in a terminal, so this asks there. Batch installs (-b) skip it. If the installer runs with sudo,
# git/bw2io run as the user who called sudo, so files and projects belong to them.
set +e
[[ "${INSTALLER_UNATTENDED:-0}" == "1" ]] && exit 0
[[ -r /dev/tty ]] || exit 0

user=${SUDO_USER:-$(id -un)}
home=$(getent passwd "$user" | cut -d: -f6)
launcher=("$PREFIX/bin/python" "$PREFIX/share/lca-toolkit/launcher.py")
as_user() { if [[ $(id -u) == 0 && -n "${SUDO_USER:-}" ]]; then sudo -H -u "$SUDO_USER" "$@"; else "$@"; fi; }
ask() { local reply; printf "%s " "$1" > /dev/tty; read -r reply < /dev/tty; printf "%s" "$reply"; }

printf "\n" > /dev/tty
url="@MATERIAL_URL@"
printf "Optionally download notebooks from a git repository, e.g. your course material.\n" > /dev/tty
printf "LCA Notebooks then opens in that folder. Needs an internet connection.\n" > /dev/tty
answer=$(ask "Download notebooks? [yes|no] (default: yes) >>>")
[[ -z "$answer" || "$answer" =~ ^[Yy] ]] || exit 0
while true; do
    reply=$(ask "Repository link (paste the link you were given, or press Enter for $url) >>>")
    url=${reply:-$url}
    parent=$(ask "Folder to put it in (a subfolder named like the repository is created) [$home/Documents] >>>")
    parent=${parent:-$home/Documents}
    parent=${parent/#\~/$home}
    as_user "${launcher[@]}" fetch-material --url "$url" --parent "$parent" && break
    retry=$(ask "Download failed (check the link and your internet connection, and that the folder has no other files). Try again? [yes|no] (default: yes) >>>")
    [[ -z "$retry" || "$retry" =~ ^[Yy] ]] || exit 0
done

answer=$(ask "Do you already have the project backup archive (.tar.gz) with the databases? Enter its path to restore it, or press Enter to skip >>>")
[[ -n "$answer" ]] || exit 0
archive=${answer/#\~/$home}
as_user "${launcher[@]}" restore-project "$archive"
rc=$?
if [[ $rc == 3 ]]; then
    answer=$(ask "A Brightway project with this name already exists. Overwrite it? [yes|no] (default: no) >>>")
    [[ "$answer" =~ ^[Yy] ]] || exit 0
    as_user "${launcher[@]}" restore-project "$archive" --overwrite
    rc=$?
fi
if [[ $rc == 0 ]]; then
    printf "The project was restored.\n" > /dev/tty
else
    printf "The project could not be restored. Check that the file is a Brightway project backup (.tar.gz).\n" > /dev/tty
fi
exit 0
