[Setup]
AppName=TTS Studio
AppVersion=1.0
AppPublisher=Bobur Xoshimjanov
DefaultDirName={autopf}\TTS Studio
DefaultGroupName=TTS Studio
OutputBaseFilename=TTS-Studio-Setup
OutputDir=installer_output
Compression=lzma2
SolidCompression=yes
DisableProgramGroupPage=yes

[Files]
Source: "dist\TTS Studio\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\TTS Studio"; Filename: "{app}\TTS Studio.exe"
Name: "{autodesktop}\TTS Studio"; Filename: "{app}\TTS Studio.exe"

[Run]
Filename: "{app}\TTS Studio.exe"; Description: "Launch TTS Studio"; Flags: nowait postinstall skipifsilent