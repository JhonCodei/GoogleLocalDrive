REM Run Application

set PROJECT_BASE=C:\Users\Programmer\Desktop\Projects\PYTHON\NATIVO
set PROJECT_APP=%PROJECT_BASE%/python_apps

REM Debug options
set LOG_LEVEL=DEBUG

REM Notification options
SET MAIL_LIST=%ADMIN_MAIL%
SET PAGER_LIST=%ADMIN_PGR%
REM export MAIL_ON_ERR=T
REM export PAGE_ON_ERR=T

REM For Timestamps
REM export DTM=`date '+%Y%m%d.%H.%M.%S'`
REM export DT=`date '+%Y%m%d'`
SET DTL=%DATE:~6,8%-%DATE:~3,2%-%DATE:~0,2%
SET LOG_DIR=%PROJECT_APP%/log/%DTL%
REM export LOG_NAME=`basename $0`.${DTM}

REM set PYTHONINTR=python
set PYTHONINTR=%PROJECT_APP%/virtual_environment/Scripts/python.exe
set PYTHONPATH=%PROJECT_APP%/lib

%PYTHONINTR% %PROJECT_APP%/lib/apps/makeproject.py Z