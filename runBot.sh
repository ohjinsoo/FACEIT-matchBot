#!/bin/bash

PID_FILE=/tmp/faceit_bot.pid
[ -f $PID_FILE ] && kill -9 $(cat $PID_FILE) && rm $PID_FILE
echo "Starting FACEIT_BOT"
pipenv run python3.6 ./bot.py > /var/log/faceit_bot.log 2>&1 & echo $! >>$PID_FILE
