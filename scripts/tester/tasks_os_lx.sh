#!/bin/bash
export PROJECT_BASE=/home/ubuntu/Escritorio/python_project
export PROJECT_APP=$PROJECT_BASE/python_apps
export APP_NAME=tasks
export LOG_LEVEL=DEBUG
export MAIL_LIST=$ADMIN_MAIL
export PAGER_LIST=$ADMIN_PGR
export DTM=`date '+%Y%m%d.%H.%M.%S'`
export DT=`date '+%Y%m%d'`
export LOG_DIR=$PROJECT_APP/log
export LOG_NAME="$APP_NAME"_${DT}".log"
export PYTHONINTR=$PROJECT_APP/virtual_environment/bin/python3.7
export PYTHONPATH=$PROJECT_APP/lib

$PYTHONINTR $PROJECT_APP/lib/apps/tasks.py B 1
