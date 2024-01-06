REM Run Application

set PROJECT_BASE=#BASE DIRECTORY PROJECT
set PROJECT_APP=%PROJECT_BASE%/#PROJECT-FOLDER

REM Debug options
set LOG_LEVEL=DEBUG

REM Notification options
set MAIL_LIST=%ADMIN_MAIL%
set PAGER_LIST=%ADMIN_PGR%
#export MAIL_ON_ERR=T
#export PAGE_ON_ERR=T

#For Timestamps
REM export DTM=`date '+%Y%m%d.%H.%M.%S'`
REM export DT=`date '+%Y%m%d'`

set LOG_DIR=%PROJECT_APP%/log
REM export LOG_NAME=`basename $0`.${DTM}

#set PYTHONINTR=python
set PYTHONINTR=%PROJECT_APP%/virtual_environment/Scripts/python.exe

set PYTHONPATH=%PROJECT_APP%/lib

%PYTHONINTR% %PROJECT_APP%/lib/apps/{APP.py} {arg1} {arg2}
