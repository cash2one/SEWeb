#!/bin/bash
    
if [ -f ~/.bash_profile ];
then
    . ~/.bash_profile
fi 

echo "stopping jhssd"
jhss_pid=$(netstat -anop | grep "0.0.0.0:9999" | awk '{print $7}' | awk -F '/' '{print $1}')
if [ -n "$jhss_pid" ];  
then
{
    kill -9 $jhss_pid
}
fi 
