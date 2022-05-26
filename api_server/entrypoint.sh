#!/bin/sh

# Run alembic migrations on project startup.
cd /usr/src/app/db && alembic upgrade head
# Check for RUN_FOR_EVER env variable.
if [ $RUN_FOR_EVER = "True" ]
    then
        tail -f /dev/null

elif [  $RUN_FOR_EVER = "False" ]
    then
        cd /usr/src/app/ && celery -A app.celery_base:app worker -l INFO --detach && python run.py
fi
