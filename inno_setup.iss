[Setup]
AppName={#appname}
AppVersion={#version}
AppVerName={#versionfull}
AppUpdatesURL=https://github.com/132nd-etcher/EASI/releases
AppSupportURL=https://github.com/132nd-etcher/EASI/issues
VersionInfoVersion={#version}
SetupIconFile={#SourcePath}{#appico}
DefaultDirName={pf}\{#appname}
AppId={{5b6dab14-577b-48b8-953a-80c0112a2aee}
UninstallDisplayName={#appname}
OutputDir={#SourcePath}{#outputdir}
OutputBaseFilename={#appname}_setup_{#versionfull}
ShowTasksTreeLines=True
AppPublisher=etcher
AppPublisherURL=etcher
DefaultGroupName={#appname}
AlwaysShowGroupOnReadyPage=True
AlwaysShowDirOnReadyPage=True
DisableProgramGroupPage=auto
DisableWelcomePage=True
DisableReadyMemo=True
AppendDefaultGroupName=False
UninstallDisplayIcon={uninstallexe}
ShowLanguageDialog=no
MinVersion=0,6.1
VersionInfoCompany=etcher
VersionInfoDescription=Etcher's Automated Skin Installer
VersionInfoTextVersion={#versionfull}
VersionInfoCopyright=Copyright (C) 2016  etcher
VersionInfoProductName={#appname}
VersionInfoProductVersion={#version}
VersionInfoProductTextVersion={#versioninfo}
DisableReadyPage=True

[Files]
Source: "{#SourcePath}build\dist_windowed\EASI.exe"; DestDir: "{app}"; Flags: ignoreversion createallsubdirs recursesubdirs

[Run]
Filename: "{app}\easi.exe"; WorkingDir: "{app}"; Flags: nowait postinstall runascurrentuser; Description: "Start EASI ?"

[Icons]
Name: "{group}\Uninstall EASI"; Filename: "{uninstallexe}"; WorkingDir: "{app}"; IconFilename: "{app}\easi.exe"
Name: "{group}\EASI"; Filename: "{app}\easi.exe"; WorkingDir: "{app}"; IconFilename: "{app}\easi.exe"

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
