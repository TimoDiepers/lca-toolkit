#!/bin/bash
# Replaces constructor's osx/checks_before_install.sh (swapped in by tools/run_constructor.py;
# rendered with the same Jinja variables). Difference: if the chosen location already holds
# an LCA Toolkit installation, offer to replace it instead of refusing to install, so users
# can update by just running the new installer. Anything else in the way is still refused.
# Notebooks, teaching material and Brightway projects live outside this folder and are kept.
set -euo pipefail

PREFIX="$2/{{ pkg_name_lower }}"
echo "PREFIX=$PREFIX"

# Dialogs must run in the logged-in user's GUI session (this script runs as root).
user=$(stat -f%Su /dev/console)
uid=$(id -u "$user" 2>/dev/null || echo 0)
dialog() { launchctl asuser "$uid" sudo -H -u "$user" osascript -e "activate" -e "$1"; }
log() { logger -p "install.info" "$1" || echo "$1"; }

if [[ -e "$PREFIX" ]]; then
    if [[ -f "$PREFIX/conda-meta/history" && -e "$PREFIX/{{ conda_exe_name }}" ]]; then
        if [[ "${COMMAND_LINE_INSTALL:-0}" == "0" ]]; then
            answer=$(dialog "button returned of (display dialog \"{{ installer_name }} is already installed in '$PREFIX'.

Replace it with version {{ installer_version }}? Your notebooks, teaching material and Brightway projects are kept.\" buttons {\"Cancel installation\", \"Replace\"} default button \"Replace\" with title \"{{ installer_name }}\")") || answer=""
            if [[ "$answer" != "Replace" ]]; then
                log "Existing installation in '$PREFIX' kept; installation cancelled."
                exit 1
            fi
        fi
        # command-line installs (`installer -pkg …`) replace without asking, like Windows /S
        log "Removing the existing installation in '$PREFIX'"
        rm -rf "$PREFIX"
    else
        log "ERROR: {{ path_exists_error_text }}"
        dialog "display alert \"Chosen path already exists!\" message \"{{ path_exists_error_text }}\" as critical buttons {\"OK\"} default button \"OK\"" >/dev/null || true
        exit 1
    fi
fi

{%- if check_path_spaces %}
case "$PREFIX" in
    *\ * )
        log "ERROR: '$PREFIX' contains spaces!"
        dialog "display alert \"Chosen path contain spaces!\" message \"'$PREFIX' contains spaces. Please, relaunch the installer and choose another location in the Destination Select step.\" as critical buttons {\"OK\"} default button \"OK\"" >/dev/null || true
        exit 1
        ;;
esac
{%- endif %}

exit 0
