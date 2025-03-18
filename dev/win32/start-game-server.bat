@echo off
cd ../..

set /P PYTHON_PATH=<PYTHON_PATH

%PYTHON_PATH% -m pip install -r requirements.txt

set TOONTOWN_GAMESERVER=game.geargrind.tech:6667

cls

:main
%PYTHON_PATH% -m toontown.toonbase.ToontownStart --debug-injector
pause
goto :main