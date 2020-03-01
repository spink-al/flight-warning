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

## Windows (not tested see other branch):

(path to ncat)\ncat.exe (ip of dump1090 host) 30003 | (path to python 2.7)\python.exe flight_warning_MLAT.py

## Linux:

nc (ip of dump1090 host) 30003 | python flight_warning_MLAT.py

## Edit with your lat/lon/elevation in flight_warning_conf.py:

my_lat = 50.1234 #yourlatitude # (positive = north, negative = south) 

my_lon = 15.1234 #yourlongitude # (positive = east, negative = west) 

my_elevation_const = 90 #your antenna elevation 

my_elevation = 90 #your antenna elevation 


![alt text](https://github.com/spink-al/flight-warning/blob/master/Capture.JPG)


