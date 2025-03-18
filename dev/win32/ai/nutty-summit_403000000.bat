@echo off
cd ../../..


rem Define some constants for our AI server:
set MAX_CHANNELS=999999
set STATESERVER=4002
set ASTRON_IP=127.0.0.1:7101
set EVENTLOGGER_IP=127.0.0.1:7197
set WANT_RANDOM_INVASIONS=0
set WANT_INVASIONS_ONLY=1

set DISTRICT_NAME=Nutty Summit
set BASE_CHANNEL=403000000

set /P PYTHON_PATH=<PYTHON_PATH

cls

:main
%PYTHON_PATH% -m toontown.ai.AIStart --base-channel %BASE_CHANNEL% ^
               --max-channels %MAX_CHANNELS% --stateserver %STATESERVER% ^
               --astron-ip %ASTRON_IP% --eventlogger-ip %EVENTLOGGER_IP% --want-random-invasions %WANT_RANDOM_INVASIONS% --want-invasions-only %WANT_INVASIONS_ONLY% ^
               --district-name "%DISTRICT_NAME%"
pause
goto :main