!include "LogicLib.nsh"
!include "MUI2.nsh"

Name "Inclutel-1.0.0"
OutFile "Inclutel-Setup.exe"
InstallDir "$PROGRAMFILES\Inclutel"
InstallDirRegKey HKCU "Software\Inclutel" ""

!define MUI_ABORTWARNING

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "Spanish"

Section "Instalar"
    SetOutPath "$INSTDIR"

    ; Incluye todos los archivos y carpetas dentro de la carpeta principal Inclutel
    File /r "*"

    ; Crea los accesos directos
    CreateDirectory "$SMPROGRAMS\Inclutel"
    CreateShortCut "$SMPROGRAMS\Inclutel\Inclutel.lnk" "$INSTDIR\Inclutel.exe"
    CreateShortCut "$DESKTOP\Inclutel.lnk" "$INSTDIR\Inclutel.exe"

    ; Escribe la ruta de instalación en el registro
    WriteRegStr HKCU "Software\Inclutel" "Install_Dir" "$INSTDIR"
SectionEnd

Function .onInit
FunctionEnd