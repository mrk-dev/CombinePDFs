@echo off

REM installer for CombinePDFs program

echo Checking for install directory...
if NOT EXIST C:\tools mkdir C:\tools
if NOT EXIST C:\tools\CombinePDFs (
	echo Creating install directory
	mkdir C:\tools\CombinePDFs
)

echo Copying files into C:\tools\CombinePDFs
copy /y combine*.* C:\tools\CombinePDFs

echo Create Desktop shortcut
Powershell.exe -executionpolicy remotesigned -File  .\createshortcut.ps1 "%USERPROFILE%\Desktop\Combine PDfs.lnk" C:\tools\CombinePDFs\combine.exe "--window # #" C:\tools\CombinePDFs\combine.ico

pause

