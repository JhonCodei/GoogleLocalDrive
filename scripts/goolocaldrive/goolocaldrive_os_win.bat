
REM Run Application

set PROJECT_BASE=%~dp0..\..\
set PROJECT_APP=%PROJECT_BASE%

REM Debug options
set LOG_LEVEL=DEBUG

REM Notification options
set MAIL_LIST=%ADMIN_MAIL%
set PAGER_LIST=%ADMIN_PGR%
REM export MAIL_ON_ERR=T
REM export PAGE_ON_ERR=T

REM For Timestamps
for /f "tokens=2-4 delims=/ " %%a in ("%DATE%") do (
    set "day=%%a"
    set "month=%%b"
    set "year=%%c"
)
set DTL=%year%-%month%-%day%
set LOG_DIR=%PROJECT_APP%/log/%DTL%
rem set LOG_DIR=%PROJECT_APP%/log

REM set PYTHONINTR=python
set PYTHONINTR=%PROJECT_APP%/virtual_environment/Scripts/python.exe
set PYTHONPATH=%PROJECT_APP%/lib

%PYTHONINTR% %PROJECT_APP%/lib/apps/goolocaldrive.py R


