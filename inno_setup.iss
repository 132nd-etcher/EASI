#define ApplicationName 'EASI'
#define ApplicationVersion '0.0.11.10867'
#define AppIco SourcePath + "\src\ui\resources\app.ico"
#define OutputDir SourcePath + "\build\release"

[Setup]
AppName={#ApplicationName}
AppVersion={#ApplicationVersion}
AppVerName={#ApplicationName} {#ApplicationVersion}
AppUpdatesURL=https://github.com/132nd-etcher/EASI/releases
AppSupportURL=https://github.com/132nd-etcher/EASI/issues
VersionInfoVersion={#ApplicationVersion}
SetupIconFile={#AppIco}
DefaultDirName={pf}\{#ApplicationName}
AppId={{5b6dab14-577b-48b8-953a-80c0112a2aee}
UninstallDisplayName={#ApplicationName}
OutputDir={#OutputDir}
OutputBaseFilename={#ApplicationName}_setup_{#ApplicationVersion}
ShowTasksTreeLines=True
AppPublisher=etcher
AppPublisherURL=etcher
DefaultGroupName={#ApplicationName}
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
VersionInfoTextVersion={#ApplicationName} {#ApplicationVersion}
VersionInfoCopyright=Copyright (C) 2016  etcher
VersionInfoProductName={#ApplicationName}
VersionInfoProductVersion={#ApplicationVersion}
VersionInfoProductTextVersion={#ApplicationName} {#ApplicationVersion}
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
