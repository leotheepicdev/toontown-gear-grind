@echo off
cd ../../lib/astron

rem Make required folders if they do not exist:
IF NOT EXIST databases mkdir databases
IF NOT EXIST databases/astrondb mkdir databases\astrondb

:main
astrond.exe --loglevel info --pretty config/astrond.yml
pause
goto :main