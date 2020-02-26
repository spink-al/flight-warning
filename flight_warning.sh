#!/bin/bash
while true ; do
    # localhost or ip
    nc -w 30 localhost 33333 | python flight_warning_MLAT.py
    #nc -w 30 localhost 33333 | python3 flight_warning_MLAT.py
    sleep 5s 
done


