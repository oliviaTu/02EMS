#!/bin/sh
num=$(ps -ef |grep /opt/powercloud/ems/ems_server/software/ems/ems | grep -v grep)
if [ "$num" ]; then
	echo "sysmanage is running"
	exit 0
fi

prog_path=/opt/powercloud/ems/ems_server/software/ems/ems
nohup ${prog_path} > /opt/powercloud/ems/ems_server/run/ems.file 2>&1 &
if [ $? -ne 0 ]
then
	echo "start ems failed"
else
	echo "start ems success"
fi