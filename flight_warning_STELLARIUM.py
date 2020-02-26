#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
flight_warning.py
version 1.06

This program will send a Google mail message when an ADS-B data feed from
a dump1090 stream detects an aircraft within a set distance of a geographic point.
It will also send an email when the aircraft leaves that detection area.
As well, it will send a warning email if the trajectory of the plane is likely to
intersect the detection zone.

The appearance of the records sent to stdout look like this:

2015-07-27T17:46:16.715000-05,75827C,PAL118,49.88521,-100.47669,11887,186.8,295.6,3.5

The format is as follows:

datetime,icao_code,flight_code,latitude,longitude,elevation,distance,azimuth,altitude

The units of elevation and distance depend on settings within the code below (i.e. meters/kilometers
or feet/miles).

Copyright (C) 2015 Darren Enns <darethehair@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
USA.
"""

# import required libraries
#
import os
import sys
import datetime
import time
import math
# import ephem
import re
import requests
import subprocess
from math import atan2, sin, cos, acos, radians, degrees, atan, asin, sqrt, isnan

if os.name == 'nt':
	print os.name
	os.system('color')
else:
	print os.name

#
# set geographic location and elevation
#
#########################################################################
###################  ZMIEN TE DANE               ########################
#########################################################################

my_lat = 51.1234 #yourlatitude # (positive = north, negative = south)
my_lon = 14.12335 #yourlongitude # (positive = east, negative = west)
my_elevation_const = 90 #yourantennaelevation
IP_STELLARIUM = "192.168.3.104:8090"
LIMIT = 100 # Powyzej tej odleglosci w km nie wyswietlaj w Stellarium

#########################################################################
#########################################################################
#########################################################################





# my_elevation = 90 #yourantennaelevation

pressure = 1013

warning_distance = 149 # 149 #yourwarningradius # e.g. 200
alert_duplicate_minutes 			= 20
alert_distance 						= 15 ## Warning radius 1 Sound alert
xtd_tst 							= 20 ## Warning radius 2 Sound alert





print "Starting..."
started = datetime.datetime.now()

url_main = "http://"+str(IP_STELLARIUM)+"/api/"
url_status = "main/status"
response = requests.get(url_main + url_status)
url_command = 'scripts/direct'

deg = '\xb0'
earth_R = 6371
histdate = str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))

#
# initialize empty dictionaries
#
plane_dict = {}

# 
# set desired units
#
metric_units = True

aktual_t = datetime.datetime.now()
last_t = datetime.datetime.now() - datetime.timedelta(seconds=10) 
metar_t = datetime.datetime.now() - datetime.timedelta(minutes=20) 
gong_t = datetime.datetime.now()


#
# calculate time zone for ISO date/timestamp
#
timezone_hours = time.altzone/60/60

#
# define havesine great-circle-distance routine
# credit: http://www.movable-type.co.uk/scripts/latlong.html
#
def haversine(origin, destination):
	lat1, lon1 = origin
	lat2, lon2 = destination

	if (metric_units):
		radius = 6371 # km
	else:
		radius = 3959 # miles

	dlat = radians(lat2-lat1)
	dlon = radians(lon2-lon1)
	a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(radians(lat1)) * math.cos(radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	d = radius * c

	return d

#
# define cross-track error routine
# credit: http://www.movable-type.co.uk/scripts/latlong.html
#
def crosstrack(distance, azimuth, track):
	if (metric_units):
		radius = 6371 # km
	else:
		radius = 3959 # miles

	xtd = round(abs(math.asin(math.sin(float(distance)/radius) * math.sin(radians(float(azimuth) - float(track)))) * radius),1)

	return xtd



def gong():
	global gong_t
	aktual_gong_t = datetime.datetime.now()
	diff_gong_t = (aktual_gong_t - gong_t).total_seconds() 
	if (diff_gong_t > 2):
		gong_t = aktual_gong_t
		print '\a' ## TERMINAL GONG!
# time.sleep(5)
# gong()
def is_float_try(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def is_int_try(str):
    try:
		int(str)
		return True
    except ValueError:
        return False
def get_metar_press():
	return 1013

def clean_dict():
	for pentry in plane_dict:
		then2 = plane_dict[pentry][0]
		now2 = datetime.datetime.now()
		diff_minutes2 = (now2 - then2).total_seconds() / 60.
		
		if (diff_minutes2 > 1):
			del plane_dict[pentry]
			break

def aktualizuj_stellarium():
	global last_t

	
	diff_t = (aktual_t - last_t).total_seconds()
	## Update freq 1=1s, 0=realtime 
	if (diff_t > 3):
		last_t = aktual_t

		stel_command = 'CustomObjectMgr.removeCustomObjects();'+\
		'CustomObjectMgr.setMarkersSize("3");'
		command_post = requests.post(url_main + url_command, data={'code': str(stel_command)})
		
		sub_txt1 = ""
		for pentry in plane_dict:
			if (is_float_try(plane_dict[pentry][5])):
				if (plane_dict[pentry][5] < int(LIMIT)):
					stel_command = ''
					if plane_dict[pentry][1] != "":
						sub_txt0 = str(plane_dict[pentry][1])
					else:
						sub_txt0 = str(pentry)
					if (plane_dict[pentry][12] == 'WARNING' and plane_dict[pentry][9] != "RECEDING"):
						sub_txt1 = ">["+str( plane_dict[pentry][13])+"km]"
					else:
						sub_txt1 = ""
							
					stel_command += 'CustomObjectMgr.addCustomObjectAltAzi("'+sub_txt0+' ' +str(plane_dict[pentry][5])+"km" +str(sub_txt1)+' ", "'+str(plane_dict[pentry][7])+'","'+str(plane_dict[pentry][6])+'", true);'
					tmp_licz = 0
					for poz in plane_dict[pentry][15]:
						stel_command += 'CustomObjectMgr.addCustomObjectAltAzi("'+str(" ")+' ", "'+str(plane_dict[pentry][16][tmp_licz])+'","'+str(poz)+'", true);'
						tmp_licz += 1
					command_post = requests.post(url_main + url_command, data={'code': str(stel_command)})
		    
		lastline=str(datetime.datetime.time(datetime.datetime.now()))
		lastline+= " --- "
		lastline+= str(len (plane_dict))
		lastline+= " --- "
		lastline+= str(int(diff_t))
		lastline+= " --- "+ str(pressure)+"hPa"
		lastline+= " Started: "+str(started)
		print lastline

	#return #moon_alt, moon_az, sun_alt, sun_az ## przeniesc na koniec, moonaltyazy w while, sleep na start albo startdatetime 1970

aktualizuj_stellarium()
#
# loop through all records from dump1090 port 10003 input stream on stdin
#
while True:
	line=sys.stdin.readline()
	aktual_t = datetime.datetime.now()

	if line in ['\n', '\r\n']:
		plane_dict.clear()     # remove all entries in dict
		print ''		
		with open(out_path,'w') as tsttxt:
			tsttxt.write('')
	else:
		#
		# divide input line into parts and extract desired values
		#
		parts = line.split(",")
		type = parts[1].strip()
		icao = parts[4].strip()
		date = parts[6].strip()
		time = parts[7].strip()
		date_time_local = datetime.datetime.strptime(date + " " + time, '%Y/%m/%d %H:%M:%S.%f')
		date_time_iso = datetime.datetime.strftime(date_time_local, '%Y-%m-%dT%H:%M:%S.%f') + str("%+d" % (-timezone_hours)).zfill(3)
		
		#
		# check age of newest icao record, compare to newly-input value, and kill dictionary if too old (i.e. start fresh history)
		#
		if (icao in plane_dict):
		    then = plane_dict[icao][0]
		    now = datetime.datetime.now()
		    diff_minutes = (now - then).total_seconds() / 60.
		    # if (diff_minutes > alert_duplicate_minutes):
		    if (diff_minutes > alert_duplicate_minutes):
				del plane_dict[icao]
				
		#
		# if type 1 record then extract datetime/flight and create or update dictionary
		#
		if (type == "1"): # this record type contains the aircraft 'flight' identifier
			flight = parts[10].strip()

			if (icao not in plane_dict): 
				plane_dict[icao] = [date_time_local, flight, "", "", "", "", "", "", "", "", "", "", "", "", "", [], [], "", "", "", "", "", "", "", "", "", "", "", ""]
			else:
				plane_dict[icao][0] = date_time_local
				plane_dict[icao][1] = flight
		#
		# if type 5 flight elevation
		#
		if (type == "5"): 
			flight = parts[10].strip()
			elevation = parts[11].strip()
			if is_int_try(elevation):
				elevation=int(elevation)
				# print elevation
				if elevation > 6500:
					pressure = int(get_metar_press())
					elevation = elevation + ((1013 - pressure)*30)
					my_elevation = my_elevation_const
				else:
					my_elevation = 90# -90 ## taka sama wysokość punktu obserwacji n.p.m jak pas na EPPO
				# powyzsze tu nic nie robi
				if (metric_units):
					elevation = float((elevation * 0.3048)) # convert elevation feet to meters
				else:
					elevation = ""
			if (icao not in plane_dict): 
				# if flight != '':
				plane_dict[icao] = [date_time_local, flight, "", "", elevation, "", "", "", "", "", "", "", "", "", "", [], [], "", "", "", "", "", "", "", "", "", "", "", ""]
			else:
				plane_dict[icao][4] = elevation 
				plane_dict[icao][0] = date_time_local
				if flight != '':
					plane_dict[icao][1] = flight
				
					

		#
		# if type 4 record then extract speed/track
		#
		if (type == "4"): # this record type contains the aircraft 'track' & 'velocity' identifier
			velocity = parts[12].strip()
			track = parts[13].strip()
			if is_int_try(velocity):
				velocity_kmh = round(int(velocity)*1.852)
			else:
				velocity = 900
			
			if (icao not in plane_dict): 
				plane_dict[icao] = [date_time_local, "", "", "", "", "", "", "", "", "", "", track,  "", "", velocity, [], [], "", "", "", "", "", "", "", "", "", "", "", ""]
			
			else:
				plane_dict[icao][0] = date_time_local
				plane_dict[icao][11] = track
				plane_dict[icao][14] = velocity_kmh
				

		#
		# if type 3 record then extract datetime/elevation/lat/lon, calculate distance/azimuth/altitude, and create or update dictionary
		#
		if (type == "3"): # this record type contains the aircraft 'ICAO' identifier, lat/lon, and elevation
			elevation = parts[11].strip() # assumes dump1090 is outputting elevation in feet 
			if is_int_try(elevation):
				elevation=int(elevation)
				if elevation > 6500:
					pressure = int(get_metar_press())
					elevation = elevation + ((1013 - pressure)*30)
					my_elevation = my_elevation_const
				else:
					my_elevation = 90 #-90 ## taka sama wysokość punktu obserwacji n.p.m jak pas na EPPO
				if (metric_units):
					elevation = float((elevation * 0.3048)) # convert elevation feet to meters
				else:
					elevation = ""
			elevation_units = "ft"
			distance_units = "mi"
			# if (metric_units):
				# elevation = int(round(elevation * 0.3048)) # convert elevation feet to meters
				#elevation_units = "m"
				# distance_units = "km"

			#print parts[14], parts
			try:
				plane_lat = float(parts[14])
			except:
				plane_lat = ''
				#pass
			try:
				plane_lon = float(parts[15])
			except:
				plane_lon = ''
				#pass
			if not plane_lat == '':
				if not plane_lon == '':
					distance = round(haversine((my_lat, my_lon), (plane_lat, plane_lon)),1)
					azimuth = atan2(sin(radians(plane_lon-my_lon))*cos(radians(plane_lat)), cos(radians(my_lat))*sin(radians(plane_lat))-sin(radians(my_lat))*cos(radians(plane_lat))*cos(radians(plane_lon-my_lon)))
					azimuth = round(((degrees(azimuth) + 360) % 360),1)
					if distance == 0:
						distance = 0.01	
					altitude = degrees(atan((elevation - my_elevation)/(distance*1000))) # distance converted from kilometers to meters to match elevation
					# if (not metric_units):
						# altitude = degrees(atan((elevation - my_elevation)/(distance*5280))) # distance converted from miles to feet to match elevation
					altitude = round(altitude,1)
					
					if (icao not in plane_dict): 
						plane_dict[icao] = [date_time_local, "", plane_lat, plane_lon, elevation, distance, azimuth, altitude, "", "", distance, "", "", "", "", [], [], "", "", "", "", "", "", "", "", "", "", "", ""]
						plane_dict[icao][15] = []
						plane_dict[icao][16] = []	
						plane_dict[icao][15].append(azimuth)
						plane_dict[icao][16].append(altitude)				
					else:
						#
						# figure out if plane is approaching/holding/receding
						#
						min_distance = plane_dict[icao][10]

						if (distance < min_distance):
							plane_dict[icao][9] = "APPROACHING"
							plane_dict[icao][10] = distance
						elif (distance > min_distance):
							plane_dict[icao][9] = "RECEDING"
						else:
							plane_dict[icao][9] = "HOLDING"

						plane_dict[icao][0] = date_time_local
						plane_dict[icao][2] = plane_lat
						plane_dict[icao][3] = plane_lon
						plane_dict[icao][4] = elevation 
						plane_dict[icao][5] = distance 
						plane_dict[icao][6] = azimuth 
						plane_dict[icao][7] = altitude 
						
						# if plane_dict[icao][33] == '':
							# plane_dict[icao][33] = str(plane_dict[icao][6])
						
						# if plane_dict[icao][34] == '':
							# plane_dict[icao][34] = str(plane_dict[icao][7])
						
						if plane_dict[icao][17] == '':
							plane_dict[icao][17] = date_time_local
						
						then = plane_dict[icao][17]
						now = datetime.datetime.now()
						diff_seconds = (now - then).total_seconds()
						if (diff_seconds > 6):
							
							plane_dict[icao][17] = date_time_local

							poz_az = str(plane_dict[icao][6])
							poz_alt = str(plane_dict[icao][7])

							plane_dict[icao][15].append(poz_az)
							plane_dict[icao][16].append(poz_alt)				
				#		
				# if matched record between type 1/3  occurs, log stats to stdout and also email if entering/leaving detection zone
				#

		if ((type == "1" or type == "3" or type == "4") and (icao in plane_dict and plane_dict[icao][2] != "" and plane_dict[icao][11] != "")):

			flight 			= plane_dict[icao][1]
			plane_lat 		= plane_dict[icao][2]
			plane_lon 		= plane_dict[icao][3]
			elevation 		= plane_dict[icao][4]
			distance 		= plane_dict[icao][5]
			azimuth 		= plane_dict[icao][6]
			altitude 		= plane_dict[icao][7]
			track 			= plane_dict[icao][11]
			warning 		= plane_dict[icao][12]
			direction 		= plane_dict[icao][9]
			# elevation_feet 	= int(round(int(round(elevation / 0.3048)/100)))
			velocity 		= plane_dict[icao][14]
			xtd 			= crosstrack(distance, (180 + azimuth) % 360, track)
			
			plane_dict[icao][13] = xtd
			
			if (xtd <= xtd_tst and distance < warning_distance and warning == "" and direction != "RECEDING"):
				plane_dict[icao][12] = "WARNING"
				plane_dict[icao][13] = xtd
				# gong()

			if (xtd > xtd_tst and distance < warning_distance and warning == "WARNING" and direction != "RECEDING"):
				plane_dict[icao][12] = ""
				plane_dict[icao][13] = xtd
				# gong()

			if (plane_dict[icao][8] == ""):
				plane_dict[icao][8] = "LINKED!"
		
			#
			
			#
			# if ((elevation <= 8000) and distance <= 30):
				# gong()
			
			if (plane_dict[icao][5] <= alert_distance and plane_dict[icao][8] != "ENTERING"):
				plane_dict[icao][8] = "ENTERING"
				gong()

			#
			# if plane leaves detection zone, generate email and include history capture
			#
			if (plane_dict[icao][5] > alert_distance and plane_dict[icao][8] == "ENTERING"):
			    plane_dict[icao][8] = "LEAVING"


	aktualizuj_stellarium()
	clean_dict()
