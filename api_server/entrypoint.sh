#!/bin/sh



# Check for RUN_FOR_EVER env variable.
if [ $RUN_FOR_EVER = "True" ]
    then
        tail -f /dev/null

elif [  $RUN_FOR_EVER = "False" ]
    then
        cd /usr/src/app && celery -A celery_app worker -l INFO --detach && python run.py
fi

