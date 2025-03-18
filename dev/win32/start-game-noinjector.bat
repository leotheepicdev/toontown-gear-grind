@echo off
cd ../..

set /P PYTHON_PATH=<PYTHON_PATH

%PYTHON_PATH% -m pip install -r requirements.txt

cls

:main
%PYTHON_PATH% -m toontown.toonbase.ToontownStart
pause
goto :main