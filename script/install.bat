@echo off
@echo create resultinfo 
set filepath=%~dp0
set shelddisc=%~d0
echo %filepath%
echo %shelddisc%

set result_dir="c:/sandbox"

echo %result_dir%

mkdir %result_dir%
echo mkdir success
"%SystemRoot%/System32/WScript.exe" install.vbs
echo make link file success
copy start_link.bat %result_dir%
copy stop_link.bat %result_dir%
echo copy done
echo install done
pause 