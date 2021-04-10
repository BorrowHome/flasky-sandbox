currentpath = createobject("Scripting.FileSystemObject").GetFolder(".").Path

set WshShell=WScript.CreateObject("WScript.Shell")
strDesktop=WshShell.SpecialFolders("Desktop")
' strDesktop="c:/sandbox"
set oShellLink=WshShell.CreateShortcut(strDesktop & "\start.lnk")
oShellLink.TargetPath=currentpath & "\start.bat"
oShellLink.WindowStyle=1
' oShellLink.Hotkey="CTRL+SHIFT+E"
' oShellLink.IconLocation="c:\mydocumentfolder\icon.ico,0"
oShellLink.Description="start server and waitress_manage exe"
oShellLink.WorkingDirectory=currentpath
oShellLink.Save

set stopShellLink=WshShell.CreateShortcut(strDesktop & "\stop.lnk")
stopShellLink.TargetPath=currentpath & "\stop.bat"
stopShellLink.WindowStyle=1
' stopShellLink.Hotkey="CTRL+SHIFT+E"
' oShellLink.IconLocation="c:\mydocumentfolder\icon.ico,0"
stopShellLink.Description="stop server and waitress_manage exe"
stopShellLink.WorkingDirectory=currentpath
stopShellLink.Save