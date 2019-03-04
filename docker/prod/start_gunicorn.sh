#!/usr/bin/env bash

 . .env
 gunicorn manage:app --worker-class gevent -b 0.0.0.0:8000 --reload --log-syslog
