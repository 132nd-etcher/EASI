[Setup]
AppName={#AppName}
AppVersion={#AssemblySemVer}
AppVerName={#FullSemVer}
AppUpdatesURL=https://github.com/132nd-etcher/EASI/releases
AppSupportURL=https://github.com/132nd-etcher/EASI/issues
VersionInfoVersion={#AssemblySemVer}
SetupIconFile={#SourcePath}{#AppIco}
DefaultDirName={pf}\{#AppName}
AppId={{5b6dab14-577b-48b8-953a-80c0112a2aee}
UninstallDisplayName={#AppName}
OutputDir={#SourcePath}{#OutputDir}
OutputBaseFilename={#AppName}_setup_{#FullSemVer}
ShowTasksTreeLines=True
AppPublisher=etcher
AppPublisherURL=etcher
DefaultGroupName={#AppName}
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
VersionInfoTextVersion={#FullSemVer}
VersionInfoCopyright=Copyright (C) 2016  etcher
VersionInfoProductName={#AppName}
VersionInfoProductVersion={#AssemblySemVer}
VersionInfoProductTextVersion={#InformationalVersion}
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
