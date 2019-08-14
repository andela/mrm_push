#!/bin/bash
cd /app
export $(cat .env | xargs)
celery worker -A cworker.celery --loglevel=info & celery beat -A cworker.celery --schedule=/tmp/celerybeat-schedule --loglevel=INFO --pidfile=/tmp/celerybeat.pid