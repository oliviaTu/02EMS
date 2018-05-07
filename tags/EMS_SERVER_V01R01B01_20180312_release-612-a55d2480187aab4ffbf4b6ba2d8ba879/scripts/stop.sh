#!/bin/sh

ps -ef | grep /opt/powercloud/ems/ems_server/software/ems/ems | grep -v grep | awk '{print $2}' | xargs kill -9