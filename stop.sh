#!/bin/bash

PID=$(ps aux|grep 'uvicorn src.main:app'|grep -v grep|awk {'print $2'}|xargs)
echo "PID: $PID"
if [ -n "${PID}" ]
then
	kill -9 $PID
	echo "Killed Process"
else
	echo "No such process"
fi