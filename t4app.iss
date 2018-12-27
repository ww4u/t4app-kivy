; -- Example1.iss --
; Demonstrates copying 3 files and creating an icon.

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

#define appVersion "0.0.0.1"
#define appPublisher "MEGAROBO Technology"

[Setup]
AppName=MRX-T4
AppVersion={#appVersion}
AppPublisher={#appPublisher}
DefaultDirName={pf}\MRX-T4
DefaultGroupName=MEGAROBO Technology
UninstallDisplayIcon={app}\MRX-T4
Compression=lzma2
SolidCompression=yesOutputBaseFilename= "MRX-T4 {#appVersion}"
PrivilegesRequired= admin

;OutputDir=userdocs:Inno Setup Examples Output

[Files]
Source: "*.exe"; DestDir: "{app}"
Source: "*.dll"; DestDir: "{app}"
Source: "*.pyd"; DestDir: "{app}"
Source: "*.zip"; DestDir: "{app}"
Source: "*.md"; DestDir: "{app}"
Source: "*.ini"; DestDir: "{app}"
Source: "*.kv"; DestDir: "{app}"
Source: "*.txt"; DestDir: "{app}"
Source: "*.exe.manifest"; DestDir: "{app}"
Source: "*.py"; DestDir: "{app}"

Source: "__pycache__\*"; DestDir: "{app}\__pycache__"; Flags: recursesubdirs 
Source: "cache\*"; DestDir: "{app}\cache"; Flags: recursesubdirs 
Source: "docutils\*"; DestDir: "{app}\docutils"; Flags: recursesubdirs
Source: "image\*"; DestDir: "{app}\image"; Flags: recursesubdirs

Source: "Include\*"; DestDir: "{app}\Include"; Flags: recursesubdirs
Source: "kivy\*"; DestDir: "{app}\kivy"; Flags: recursesubdirs
Source: "kivy_install\*"; DestDir: "{app}\kivy_install"; Flags: recursesubdirs
Source: "win32com\*"; DestDir: "{app}\win32com"; Flags: recursesubdirs

[Dirs]
Name: "{app}\cache"
Name: "{app}\script"

[UninstallDelete]
Type: filesandordirs; Name: "{app}\cache"
Type: filesandordirs; Name: "{app}\script"

[Run]
;Filename: "{app}\driver\MRH-USBCAN_Device\InstallDriver.exe"; Description: "The Driver"
;Filename: "{app}\driver\niruntime\LVRTE2017SP1_f1Patchstd.exe"; Description: "Labivew run time"

; packages
                                   
[UninstallRun] 
;Filename: "{app}\uregsrv.bat"; Parameters: "{app}"; Flags: runascurrentuser

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional Icons"; 

[Icons]
Name: "{commondesktop}\MRX-T4"; Filename: "{app}\mrx-t4.exe"; Tasks: desktopicon

Name: "{group}\MRX-T4"; Filename: "{app}\mrx-t4.exe"
Name: "{group}\Uninstall MRX-T4"; Filename: "{uninstallexe}"