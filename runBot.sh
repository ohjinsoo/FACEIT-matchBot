#!/bin/bash

PID_FILE=/tmp/faceit_bot.pid
[ -f $PID_FILE ] && kill -9 $(cat $PID_FILE) && rm $PID_FILE
echo "Starting FACEIT_BOT"
node src/index.js > /log/faceit_bot.log 2>&1 & echo $! >>$PID_FILE