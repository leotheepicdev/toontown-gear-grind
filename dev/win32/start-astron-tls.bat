@echo off
cd ../../lib/astron

rem Make required folders if they do not exist:
IF NOT EXIST databases mkdir databases
IF NOT EXIST databases/astrondb mkdir databases\astrondb

astrond --loglevel info --pretty config/astrond_tls_dev.yml
pause
