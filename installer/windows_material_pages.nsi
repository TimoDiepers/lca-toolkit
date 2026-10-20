# Post-install pages for the Windows installer (constructor `post_install_pages`).
# tools/make_installer.py fills in the suggested repository (SUGGESTED_MATERIAL_URL).
# Inserted as-is after the install step, before the finish page.
#
# Page 1: optionally add external resources from a git repository (any link the user pastes,
#         e.g. course material with an access token; prefilled with an example) into a
#         folder of the user's choice.
# Page 2 (only if page 1 was used): restore a Brightway project backup (.tar.gz) with bw2io.
# Silent installs (/S) skip custom pages, so neither step runs there.

Var MaterialCheckbox
Var MaterialUrlText
Var MaterialDirText
Var MaterialWanted
Var ProjectCheckbox
Var ProjectFileText

Page custom MaterialPageShow MaterialPageLeave
Page custom ProjectPageShow ProjectPageLeave

Function MaterialPageShow
    nsDialogs::Create 1018
    Pop $0
    ${If} $0 == error
        Abort
    ${EndIf}
    !insertmacro MUI_HEADER_TEXT "Additional resources" "Optionally add external resources from a git repository"
    SetShellVarContext current  # $DOCUMENTS of the logged-in user, also for all-users installs

    ${NSD_CreateLabel} 0 0 100% 28u "Do you want to add external resources from a git repository, e.g. teaching material, tutorials or the files of a study? Needs an internet connection; LCA Notebooks then opens in that folder."
    Pop $0
    ${NSD_CreateCheckbox} 0 30u 100% 12u "Download from this repository:"
    Pop $MaterialCheckbox
    ${NSD_Check} $MaterialCheckbox
    ${NSD_CreateText} 0 44u 100% 13u "@MATERIAL_URL@"
    Pop $MaterialUrlText
    ${NSD_CreateLabel} 0 59u 100% 10u "Paste the link you were given (it may contain an access token), or keep the example."
    Pop $0
    ${NSD_CreateLabel} 0 73u 100% 10u "Folder (a subfolder named like the repository is created inside it):"
    Pop $0
    ${NSD_CreateDirRequest} 0 85u 74% 13u "$DOCUMENTS"
    Pop $MaterialDirText
    ${NSD_CreateBrowseButton} 76% 84u 24% 15u "Browse..."
    Pop $0
    ${NSD_OnClick} $0 MaterialBrowse
    nsDialogs::Show
FunctionEnd

Function MaterialBrowse
    ${NSD_GetText} $MaterialDirText $0
    nsDialogs::SelectFolderDialog "Choose where to put the resources" $0
    Pop $0
    ${If} $0 != error
        ${NSD_SetText} $MaterialDirText $0
    ${EndIf}
FunctionEnd

Function MaterialPageLeave
    StrCpy $MaterialWanted 0
    ${NSD_GetState} $MaterialCheckbox $0
    ${If} $0 != ${BST_CHECKED}
        Return
    ${EndIf}
    ${NSD_GetText} $MaterialUrlText $3
    ${If} $3 == ""
        MessageBox MB_OK|MB_ICONEXCLAMATION "Please paste a repository link, or untick the box."
        Abort
    ${EndIf}
    ${NSD_GetText} $MaterialDirText $1
    GetDlgItem $2 $HWNDPARENT 1
    EnableWindow $2 0
    # nsExec logs the program's output, not the command line, so a token in $3 stays out of the log
    nsExec::ExecToLog '"$INSTDIR\python.exe" "$INSTDIR\share\lca-toolkit\launcher.py" fetch-material --url "$3" --parent "$1"'
    Pop $0
    EnableWindow $2 1
    ${If} $0 != 0
        MessageBox MB_RETRYCANCEL|MB_ICONEXCLAMATION "The resources could not be downloaded. Check the link and your internet connection, and that the folder doesn't already contain other files.$\r$\n$\r$\nRetry, or Cancel to skip this step." IDRETRY retry
        Return
        retry:
        Abort  # stay on the page
    ${EndIf}
    StrCpy $MaterialWanted 1
FunctionEnd

Function ProjectPageShow
    ${If} $MaterialWanted != 1
        Abort  # skip this page
    ${EndIf}
    nsDialogs::Create 1018
    Pop $0
    ${If} $0 == error
        Abort
    ${EndIf}
    !insertmacro MUI_HEADER_TEXT "Brightway project" "Optionally restore a project backup"

    ${NSD_CreateLabel} 0 0 100% 24u "If you already downloaded the project backup archive (.tar.gz) with the databases, it can be restored now, so it is directly available in Activity Browser and JupyterLab."
    Pop $0
    ${NSD_CreateCheckbox} 0 30u 100% 12u "I have the project backup file (.tar.gz)"
    Pop $ProjectCheckbox
    ${NSD_CreateFileRequest} 0 50u 74% 13u ""
    Pop $ProjectFileText
    ${NSD_CreateBrowseButton} 76% 49u 24% 15u "Browse..."
    Pop $0
    ${NSD_OnClick} $0 ProjectBrowse
    nsDialogs::Show
FunctionEnd

Function ProjectBrowse
    nsDialogs::SelectFileDialog open "" "Project backup (*.tar.gz)|*.tar.gz|All files (*.*)|*.*"
    Pop $0
    ${If} $0 != error
    ${AndIf} $0 != ""
        ${NSD_SetText} $ProjectFileText $0
        ${NSD_Check} $ProjectCheckbox
    ${EndIf}
FunctionEnd

Function ProjectPageLeave
    ${NSD_GetState} $ProjectCheckbox $0
    ${If} $0 != ${BST_CHECKED}
        Return
    ${EndIf}
    ${NSD_GetText} $ProjectFileText $1
    ${IfNot} ${FileExists} "$1"
        MessageBox MB_OK|MB_ICONEXCLAMATION "Please choose the project backup file (.tar.gz), or untick the box."
        Abort
    ${EndIf}
    StrCpy $3 ""
    restore:
    GetDlgItem $2 $HWNDPARENT 1
    EnableWindow $2 0
    nsExec::ExecToLog '"$INSTDIR\python.exe" "$INSTDIR\share\lca-toolkit\launcher.py" restore-project "$1" $3'
    Pop $0
    EnableWindow $2 1
    ${If} $0 == 3
        MessageBox MB_YESNO|MB_ICONQUESTION "A Brightway project with this name already exists. Overwrite it?" IDNO done
        StrCpy $3 "--overwrite"
        Goto restore
    ${ElseIf} $0 != 0
        MessageBox MB_OK|MB_ICONEXCLAMATION "The project could not be restored. Check that the file is a Brightway project backup (.tar.gz)."
        Abort
    ${EndIf}
    MessageBox MB_OK|MB_ICONINFORMATION "The project was restored."
    done:
    Return
FunctionEnd
