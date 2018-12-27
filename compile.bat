cd .
::pyinstaller --clean t4app.spec
::del /f /q /s build
::del /f /q /s dist

rd /s /q build
rd /s /q dist
pyinstaller t4app.spec

xcopy dist\MRX-T4 installer /e /h
copy t4app.iss installer
pause