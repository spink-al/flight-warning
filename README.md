# Original idea: 
flight-warning by Darren Enns <darethehair@gmail.com>

# flight_warning_MLAT.py

- Color console realtime display of Az/Alt of airplanes
- Sun/Moon transits prediction
- mlat
- python3-ready

## Needs python 2.7 or 3.7

## Needs python ephem:

pip install ephem

## Windows (not tested see win_lin_2019 branch):
WINDOWS_RUNME.BAT
(path to ncat)\ncat.exe (ip of dump1090 host) 30003 | (path to python 2.7)\python.exe flight_warning_MLAT.py

## Linux:

With merged feed from VRS and rebroadcast server on port 33333 use:

bash ./flight_warning.sh

for dump1090 on 30003 port:

nc (ip of dump1090 host) 30003 | python flight_warning_MLAT.py

## Edit with your lat/lon/elevation in flight_warning_conf.py:

MY_LAT="51.1234" #yourlatitude # (positive = north, negative = south) 

MY_LON="15.1234" #yourlongitude # (positive = east, negative = west) 

MY_ALT="90" #your antenna elevation in meters above sea level

out_path="/tmp/out.txt" # output file for dummy/_ASR_DUMMY2.py or AllSkyRadar https://github.com/spink-al/AllSkyRadar

out_path="/dev/null" # for no output

![alt text](https://github.com/spink-al/flight-warning/blob/master/Capture.JPG)


