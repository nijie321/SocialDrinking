#!/bin/bash

network_connected=false

check_network(){
	if [[ -z `iwgetid` ]]; then
		echo 'waiting for network connection...'
		sleep 5
		return 1
	else
		return 0
	fi
}

for i in {1..3}; do
	# the success case
	if check_network; then
		$network_connected=true
		break
	else
		echo 'retrying ...'
	fi
done

# restart network interface
if [[ $network_connected == false ]]; then
	sudo ifdown --force wlan0
	sudo ifup wlan0
fi

if check_network; then
	continue
else
	echo -n "oops, looks like the pi was unable to connect to an available network. Do you wish to continue without network? [y/n]:"
fi

read ans

if [[ "$ans" == "y" ]]; then
	exit 0
else
	echo "shutting down..."
	sleep 3
	sudo shutdown now
fi
