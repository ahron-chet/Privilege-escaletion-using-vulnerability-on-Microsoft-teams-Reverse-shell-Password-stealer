set WshShell = WScript.CreateObject("WScript.Shell")'
WshShell.Run "cmd"
WScript.Sleep 100 
WshShell.AppActivate "C:\Windows\system32\cmd.exe" 
WScript.Sleep 100 
WshShell.SendKeys "runas /user:administrator $path"
WshShell.SendKeys "{ENTER}" 
WshShell.SendKeys "$password"
WshShell.SendKeys "{ENTER}"
