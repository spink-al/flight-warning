@echo off
echo ########################################################################
echo Edit path to ncat, python, ip, port in flight_warning_MLAT.BAT !!! 
echo ########################################################################

timeout 5
ncat.exe -w 5 127.0.0.1 33333 | python.exe flight_warning_MLAT.py
