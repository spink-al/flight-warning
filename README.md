# flight-warning
Aircraft proximity detector from dump1090 feed

flight_warning.py
version 1.00

This program will send a Google mail message when an ADS-B data feed from
a dump1090 stream detects an aircraft within a set distance of a geographic point.

Copyright (C) 2015 Darren Enns <darethehair@gmail.com>

# flight_warning_winlin_term.py
Needs python ephem:
pip install ephem

Windows:
(path to ncat)\ncat.exe (ip of dump1090 host) 30003 | (path to python 2.7)\python.exe flight_warning_winlin_term.py

Linux:
nc (ip of dump1090 host) 30003 | python flight_warning_winlin_term.py
