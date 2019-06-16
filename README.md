# Original idea: 
flight-warning by Darren Enns <darethehair@gmail.com>

# flight_warning_winlin_term.py

- Color console realtime display of Az/Alt of airplanes
- Sun/Moon transits prediction

Needs python ephem:

pip install ephem

Windows:

(path to ncat)\ncat.exe (ip of dump1090 host) 30003 | (path to python 2.7)\python.exe flight_warning_winlin_term.py

Linux:

nc (ip of dump1090 host) 30003 | python flight_warning_winlin_term.py

https://github.com/spink-al/flight-warning/blob/master/Capture.JPG
