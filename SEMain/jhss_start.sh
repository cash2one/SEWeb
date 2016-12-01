#!/bin/bash

if [ -f ~/.bash_profile ];
then
    . ~/.bash_profile
fi
dt=`date +%Y-%m-%d`
echo "starting jhssd"
nohup python /home/v-wxb-chai/workspace/webserver/SEMain/app.py >> /home/v-wxb-chai/workspace/webserver/SEMain/logs/log.$dt 2>&1 &
