#!/bin/bash

mypath="/home/v-wxb-chai/workspace/webserver/SEMain/logs"
l=$(ls ${mypath})
list=($l)
newfile=${mypath}"/unionLogs"
bl=0

if [ -f $newfile ]
then
	echo "exists"
	bl=1
else
	touch $newfile
fi

if [ 1 -eq $bl ]
then
	echo "return"
else

	for s in ${list[*] }
	do
		ss=${s:0:3} 
		if [ $ss == "log" ]
		then 
			`cat $s > $newfile`
		fi
	done
fi

date

