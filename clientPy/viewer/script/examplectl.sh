#!/bin/sh
PYTHON_EXECUTE='python'

BASE_PATH=`pwd`/
EXECUTE_FILE=listener.py
PORT=2901
LOG_FILE=$BASE_PATH/log.stdout
WORKING_EXECUTE=$BASE_PATH/$EXECUTE_FILE
WORKING_HOME=`dirname $WORKING_EXECUTE`
cd $WORKING_HOME


echo "#############################################"
echo " execute working home : $WORKING_HOME"
echo "#############################################"

case $1 in
	'start')
		PID=`ps x | grep $EXECUTE_FILE | grep -v grep | awk '{print $1}'`
		if [ $PID ]; then
			kill -15 $PID
			if [ $? -eq 0 ]; then
				echo "listener is runiing with pid $PID"
				echo "kill and restart process"
			fi
		fi
		echo "======================================" >> $LOG_FILE
		$PYTHON_EXECUTE $WORKING_EXECUTE $PORT >> $LOG_FILE &
		PID=$!
		echo "listener started with pid $PID"
		;;
	'stop')
		STARTED=0
		PID=`ps x | grep $EXECUTE_FILE | grep -v grep | awk '{print $1}'`
		if [ $PID ]; then
			kill $PID
			if [ $? -eq 0 ]; then
				STARTED=1
			fi
		fi
		if [ $STARTED -eq 0 ]; then
			echo "listener is not running"
			exit 1
		fi
		kill -15 $PID
		echo "listner width pid $PID stopped"
		;;
	*)
		echo "$0 [ start | stop ]"
		;;
esac
