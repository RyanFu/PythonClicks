@echo off

%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit

E:
cd GitHub\Local_Projects\Python_Clicks\onmyoji

python _run.py

pause