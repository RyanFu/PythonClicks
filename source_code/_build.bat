@echo off

set name=_main


rd /s /q dist

pyinstaller -F -w -i resources/ssr.ico %name%.py
del /s /q /f %name%.spec
rd /s /q build
rd /s /q __pycache__

xcopy /s/e .\resources .\dist\resources\*

pause