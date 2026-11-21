Set shell = CreateObject("WScript.Shell")
shell.Run "cmd /c cd /d """ & CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & """ && python index.py", 0S