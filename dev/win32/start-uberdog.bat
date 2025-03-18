@echo off
cd ../..

set /P PYTHON_PATH=<PYTHON_PATH

rem Define some constants for our UberDOG server:
set MAX_CHANNELS=999999
set STATESERVER=4002
set ASTRON_IP=127.0.0.1:7101
set EVENTLOGGER_IP=127.0.0.1:7197

rem Get the user input:
set /P BASE_CHANNEL="Base channel (DEFAULT: 1000000): " || ^
set BASE_CHANNEL=1000000

cls

:main
%PYTHON_PATH% -m toontown.uberdog.UDStart --base-channel %BASE_CHANNEL% ^
               --max-channels %MAX_CHANNELS% --stateserver %STATESERVER% ^
               --astron-ip %ASTRON_IP% --eventlogger-ip %EVENTLOGGER_IP%
pause
goto :main