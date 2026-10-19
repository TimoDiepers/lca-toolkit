# Optional post-install pages for the Windows installer (constructor `post_install_pages`).
# Only included when the installer is built with MATERIAL_GIT_URL set; tools/make_installer.py
# replaces @MATERIAL_NAME@. Inserted as-is after the install step, before the finish page.
#
# Page 1: download the teaching material (git clone) into a folder of the user's choice.
# Page 2 (only if page 1 was used): restore a Brightway project backup (.tar.gz) with bw2io.
# Silent installs (/S) skip custom pages, so neither step runs there.

Var MaterialCheckbox
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
    !insertmacro MUI_HEADER_TEXT "@MATERIAL_NAME@ material" "Optionally download the teaching material"
    SetShellVarContext current  # $DOCUMENTS of the logged-in user, also for all-users installs

    ${NSD_CreateLabel} 0 0 100% 24u "Download the @MATERIAL_NAME@ notebooks and files now (needs an internet connection). JupyterLab will open in this folder."
    Pop $0
    ${NSD_CreateCheckbox} 0 30u 100% 12u "Download the @MATERIAL_NAME@ material"
    Pop $MaterialCheckbox
    ${NSD_Check} $MaterialCheckbox
    ${NSD_CreateLabel} 0 50u 100% 10u "Folder (a subfolder $\"@MATERIAL_NAME@$\" is created inside it):"
    Pop $0
    ${NSD_CreateDirRequest} 0 62u 74% 13u "$DOCUMENTS"
    Pop $MaterialDirText
    ${NSD_CreateBrowseButton} 76% 61u 24% 15u "Browse..."
    Pop $0
    ${NSD_OnClick} $0 MaterialBrowse
    nsDialogs::Show
FunctionEnd

Function MaterialBrowse
    ${NSD_GetText} $MaterialDirText $0
    nsDialogs::SelectFolderDialog "Choose where to put the @MATERIAL_NAME@ folder" $0
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
    ${NSD_GetText} $MaterialDirText $1
    GetDlgItem $2 $HWNDPARENT 1
    EnableWindow $2 0
    nsExec::ExecToLog '"$INSTDIR\python.exe" "$INSTDIR\share\lca-toolkit\launcher.py" fetch-material --parent "$1"'
    Pop $0
    EnableWindow $2 1
    ${If} $0 != 0
        MessageBox MB_RETRYCANCEL|MB_ICONEXCLAMATION "The @MATERIAL_NAME@ material could not be downloaded (no internet connection, or the folder already contains other files).$\r$\n$\r$\nRetry, or Cancel to skip this step." IDRETRY retry
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
