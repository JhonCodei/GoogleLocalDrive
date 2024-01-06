#!/bin/bash
# Run Application
export PROJECT_BASE=$(dirname $0)

export PROJECT_APP=$PROJECT_BASE/../../

# Debug options
export LOG_LEVEL=DEBUG

# Notification options
export MAIL_LIST=$ADMIN_MAIL
export PAGER_LIST=$ADMIN_PGR
#export MAIL_ON_ERR=T
#export PAGE_ON_ERR=T

#For Timestamps
export DTM=`date '+%Y%m%d.%H.%M.%S'`
export DT=`date '+%Y-%m-%d'`

export LOG_DIR=$PROJECT_APP/log/$DT

#export LOG_FNAME=`basename $0`
#export LOG_NAME="${LOG_FNAME%.*}".${DTM}
export PYTHONINTR=$PROJECT_APP/virtual_environment/bin/python3
#$APP_BASE/PycharmProjects/venv/sms/bin/python3.6
export PYTHONPATH=$PROJECT_APP/lib

$PYTHONINTR $PROJECT_APP/lib/apps/goolocaldrive.py R