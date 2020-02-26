#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
=======================================================================
Original idea: https://github.com/darethehair/flight-warning
=======================================================================
flight_warning.py
version 2.20200226

=======================================================================
Changes:
=======================================================================
v2.20200226
- mlat from merged feed via VRS and FA
- metar inactive
- writing data for matplotlib allsky
- python3-ready (most diff changes will be indent tabs vs spaces

v0.2
- try/except for plane lat/lon in MSG 3

v0.1
- Color console realtime display Az/Alt
- Sun/Moon transits prediction

<aleksander5416@gmail.com>

=======================================================================
=======================================================================

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

#
# import required libraries
#
import os
import sys
import datetime
import time
import math
import ephem
import re
from math import atan2, sin, cos, acos, radians, degrees, atan, asin, sqrt, isnan
if os.name == 'nt':
    print(os.name)
    os.system('color')
    os.system('mode con: cols=160 lines=13')
    metar_path = 'Y:\AS\current\metar.txt'
    out_path = 'D:\rpi\chess\tst3.txt'
else:
    print(os.name)
    metar_path = '/home/pi/work/arch/AS/current/metar.txt'
    out_path = '/tmp/tst2a.txt'

print( "Starting...")
started = datetime.datetime.now()


deg = u'\xb0'
earth_R = 6371

#TERMINAL COLORS
REDALERT        = '\x1b[1;37;41m'
PURPLE          = '\x1b[1;35;40m'
PURPLEDARK      = '\x1b[0;35;40m'
RED             = '\x1b[0;31;40m' 
GREEN           = '\x1b[0;30;42m' 
GREENALERT      = '\x1b[0;30;42m' 
# GREENFG       = '\x1b[0;42;40m' 
GREENFG         = '\x1b[1;32;40m' 
BLUE            = '\x1b[1;34;40m'
YELLOW          = '\x1b[1;33;40m'
CYAN            = '\x1b[1;36;40m'
RESET           = '\x1b[0m' 

#
# initialize empty dictionaries
#
plane_dict = {}


# 
# set desired units
#
metric_units = True # inactive

aktual_t = datetime.datetime.now()
last_t = datetime.datetime.now() - datetime.timedelta(seconds=10) 
metar_t = datetime.datetime.now() - datetime.timedelta(minutes=20) 
gong_t = datetime.datetime.now()
#
# set desired distance and time limits
#
warning_distance                    = 249 
alert_duplicate_minutes             = 20
alert_distance                      = 15
xtd_tst                             = 20

transit_separation_sound_alert         = 2.2
transit_separation_REDALERT_FG         = 5
transit_separation_GREENALERT_FG       = 3
transit_separation_notignored          = 90

#
# set geographic location and elevation
#
my_lat = 50.1234 #yourlatitude # (positive = north, negative = south)
my_lon = 15.1234 #yourlongitude # (positive = east, negative = west)
my_elevation_const = 90 #yourantennaelevation
my_elevation = 90 #yourantennaelevation
near_airport_elevation = 94

pressure = 1013


gatech = ephem.Observer()

gatech.lat, gatech.lon = str(my_lat), str(my_lon)
gatech.elevation = my_elevation_const

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
    d = float(radius * c)

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


#
# przeciecie azymutu slonca/ksiezyca z torem lotu
# credit: http://www.movable-type.co.uk/scripts/latlong.html
#
def transit_pred(obs2moon, plane_pos, track, velocity, elevation, moon_alt, moon_az):

    if moon_alt < 0.1:
        return 0
    lat1, lon1 = obs2moon
    lat2, lon2 = plane_pos
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    theta_13 = radians(float(moon_az))
    theta_23 = radians(float(track))
    Dlat = lat1-lat2
    Dlon = lon1-lon2
    delta_12 =  2*asin( sqrt( sin(Dlat/2)*sin(Dlat/2) + \
    cos(lat1)*cos(lat2)*sin(Dlon/2)*sin(Dlon/2) ) )
    if (float(delta_12 == 0)):
        return 0 
    theta_a = acos( ( sin(lat2) - sin(lat1)*cos(delta_12) ) / ( sin(delta_12)*cos(lat1) ) )
    if (isnan(theta_a)):
        theta_a = 0
    theta_b = acos( ( sin(lat1) - sin(lat2)*cos(delta_12) ) / ( sin(delta_12)*cos(lat2) ) )
    if sin(lon2-lon1) > 0:
        theta_12 = theta_a
        theta_21 = 2*math.pi - theta_b
    else:
        theta_12 = 2*math.pi - theta_a
        theta_21 = theta_b
    
    alfa_1 = theta_13 - theta_12
    alfa_2 = theta_21 - theta_23

    if (sin(alfa_1) == 0) and (sin(alfa_2) == 0):
        return 0 #null
    if ((sin(alfa_1))*(sin(alfa_2)) < 0):
        return 0 #null
    
    alfa_3 = acos( -cos(alfa_1)*cos(alfa_2) + sin(alfa_1)*sin(alfa_2)*cos(delta_12) )
    delta_13 = atan2( sin(delta_12)*sin(alfa_1)*sin(alfa_2), cos(alfa_2)+cos(alfa_1)*cos(alfa_3) )
    lat3 = asin( sin(lat1)*cos(delta_13) + cos(lat1)*sin(delta_13)*cos(theta_13) )
    Dlon_13 = atan2( sin(theta_13)*sin(delta_13)*cos(lat1), cos(delta_13)-sin(lat1)*sin(lat3) )
    lon3 = lon1 + Dlon_13;

    lat3 = degrees(lat3)
    lon3 = (degrees(lon3)+540)%360-180
    ## the distance from the observer's position to the calculated position of the aircraft when it crosses the azimuth of the moon
    dst_h2x = round(haversine((my_lat, my_lon), (lat3, lon3)),1)    
    if dst_h2x > 500:
        return 0
    if dst_h2x == 0:
        dst_h2x = 0.001
    ## tu test wysokosci na metrach nie ft    
    # if elevation < 2166:
        # my_elevation = 0 ## taka sama wysokość punktu obserwacji n.p.m jak pas na EPPO
    # else:
        # my_elevation = my_elevation_const
    if not is_int_try(elevation):
        return 0        
    altitude1 = degrees(atan(int(elevation - my_elevation)/(dst_h2x*1000)))
    azimuth1 = atan2(sin(radians(lon3-my_lon)) * cos(radians(lat3)),  cos(radians(my_lat)) * sin(radians(lat3)) - sin(radians(my_lat))*cos(radians(lat3))*cos(radians(lon3-my_lon)))    
    azimuth1 = round(((degrees(azimuth1) + 360) % 360),1)
    
    ## the distance from the CURRENT position of the airplane to the calculated position of the aircraft when it CROSSES the azimuth of the moon
    dst_p2x = round(haversine((plane_pos[0], plane_pos[1]), (lat3, lon3)),1) 
    if not velocity == '':
        velocity = int(velocity)
    else:
        velocity = 900 # only used for transit countdown
    delta_time = (dst_p2x / velocity)*3600

    
    moon_alt_B = 90.00 - moon_alt
    ideal_dist = (sin(radians(moon_alt_B))*elevation) / sin(radians(moon_alt)) / 1000
    ideal_lat = asin((sin(radians(my_lat)) * cos(ideal_dist/earth_R)) + (cos(radians(my_lat)) * sin(ideal_dist/earth_R) * cos(radians(moon_az))))
    ideal_lon = radians(my_lon) + atan2((sin(radians(moon_az))*sin(ideal_dist/earth_R)*cos(radians(my_lat))), (cos(ideal_dist/earth_R)-((sin(radians(my_lat))) * sin(ideal_lat))))

    ideal_lat = degrees(ideal_lat)
    ideal_lon = degrees(ideal_lon)
    ideal_lon = (ideal_lon+540)%360-180

    return  lat3, lon3, azimuth1, altitude1, dst_h2x, dst_p2x, delta_time, 0, moon_az, moon_alt
    ##        0        1        2        3            4        5        6           7    8        9
    
def dist_col(distance):
    if (distance <= 300 and distance > 100):
        return PURPLE
    elif (distance <= 100 and distance > 50):
        return CYAN
    elif (distance <= 50 and distance > 30):
        return YELLOW
    elif (distance <= 30 and distance > 15):
        return REDALERT
    elif (distance <= 15 and distance >0):
        return GREENALERT
    else:
        return PURPLEDARK

def alt_col(altitude):
    if (altitude >= 5 and altitude < 15):
        return PURPLE
    elif (altitude >= 15 and altitude < 25):
        return CYAN
    elif (altitude >= 25 and altitude < 30):
        return YELLOW
    elif (altitude >= 30 and altitude < 35):
        return REDALERT
    elif (altitude >=35 and altitude <= 90):
        return GREEN
    else:
        return PURPLEDARK

def elev_col(elevation):
    if (elevation >= 4000 and elevation <= 8000):
        return PURPLE
    elif (elevation >= 2000 and elevation < 4000):
        return GREEN
    elif (elevation > 0 and elevation < 2000):
        return YELLOW
    else:
        return RESET    
    
def wind_deg_to_str1(deg):
        if   deg >=  11.25 and deg <  33.75: return 'NNE'
        elif deg >=  33.75 and deg <  56.25: return 'NE'
        elif deg >=  56.25 and deg <  78.75: return 'ENE'
        elif deg >=  78.75 and deg < 101.25: return 'E'
        elif deg >= 101.25 and deg < 123.75: return 'ESE'
        elif deg >= 123.75 and deg < 146.25: return 'SE'
        elif deg >= 146.25 and deg < 168.75: return 'SSE'
        elif deg >= 168.75 and deg < 191.25: return 'S'
        elif deg >= 191.25 and deg < 213.75: return 'SSW'
        elif deg >= 213.75 and deg < 236.25: return 'SW'
        elif deg >= 236.25 and deg < 258.75: return 'WSW'
        elif deg >= 258.75 and deg < 281.25: return 'W'
        elif deg >= 281.25 and deg < 303.75: return 'WNW'
        elif deg >= 303.75 and deg < 326.25: return 'NW'
        elif deg >= 326.25 and deg < 348.75: return 'NNW'
        else: return 'N'

def gong():
    global gong_t
    aktual_gong_t = datetime.datetime.now()
    diff_gong_t = (aktual_gong_t - gong_t).total_seconds() 
    if (diff_gong_t > 2):
        gong_t = aktual_gong_t
        print( '\a') ## TERMINAL GONG!

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
    '''
    global metar_t
    global pressure
    global metar_path 
    aktual_metar_t = datetime.datetime.now()
    diff_metar_t = (aktual_metar_t - metar_t).total_seconds() 
    if (diff_metar_t > 900):
        metar_t = aktual_metar_t    
        # metar_path = 'Y:\AS\current\metar.txt'
        metar_file=open(metar_path, 'r')
        metar_data=metar_file.readlines()
        metar_file.close()
        metar_line=[]
        pressure = ''
        
        PRESS_RE = re.compile(r"Q[0-1][0-9][0-9][0-9]")                       
        # metar_data=['METAR EPPO 021730Z 25007KT 6000 OVC023 04/03 Q0998 =' ]
        
        for i, line in enumerate(metar_data):
            if "EPPO" in line: 
                metar_line.append(line.strip('\r\n').rstrip().strip())
            else:
                return 1012
        
        for f, fields in enumerate(metar_line): 
            metar_fields = fields.split(" ")

        # print( metart_fields        

        for ff, field in enumerate(metar_fields): 
            if PRESS_RE.search(field): 
                pressure = int(field[1:5])
        #
        
        if ( 800 < pressure < 1100):
            return pressure
        else:
            return 1013
    else:
    
        return pressure
    '''
    # alt pressure correction from metar inactive until tested
    # returns 1013 from global var
    return pressure
    
def clean_dict():
    for pentry in plane_dict:
        then2 = plane_dict[pentry][0]
        now2 = datetime.datetime.now()
        diff_minutes2 = (now2 - then2).total_seconds() / 60.
        
        if (diff_minutes2 > 1):
            del plane_dict[pentry]
            break

def tabela():
    global last_t
    
    
    gatech.date = ephem.now()
    # vm for right table slot, vs for left table slot 
    vs = ephem.Moon(gatech)
    vm = ephem.Sun(gatech)
    
    # can be used via star name like this: 
    # vs = ephem.star('Polaris')
    
    # or via planet name like this:
    # vs = ephem.Mars(gatech)
    # vm = ephem.Jupiter(gatech)
    
    
    vm.compute(gatech)
    vs.compute(gatech)
    moon_alt, moon_az= round(math.degrees(vm.alt), 1), round(math.degrees(vm.az), 1)
    sun_alt, sun_az= round(math.degrees(vs.alt), 1), round(math.degrees(vs.az), 1)
    
    diff_t = (aktual_t - last_t).total_seconds()
    ## Update freq 1=1s, 0=realtime 
    if (diff_t > 1):
        last_t = aktual_t

        """
        print( 'Age of last received message (s): -------------------------------------------------------'
        print( 'Time to cross azimuth of '+'{:15}'.format(str(v.name))+'------------------------------------------      |'
        print( 'Distance from observer pos to predicted cross: ---------------------------       |      |'
        print( 'Distance from plane pos to crossing: -------------------------------     |       |      |'
        print( 'Predicted angle between crossing and obj: -------------------      |     |       |      |'
        print( 'Closest distance to observer: ------------------------      |      |     |       |      |'
        print( 'Airplane visible at deg above horizon: ---------     |      |      |     |       |      |'
        print( 'Airplane visible at azimuth: ------------      |     |      |      |     |       |      |'
        print( '                                        |      |     |      |      |     |       |      |'
        ##     flight     elev   dist  trck   news azmth    alt  warn    Sep    p2x   h2x   time2X   age
        """
        print( "\033c"+" Flight info -----------|-------|Pred. closest   |- Current Az/Alt ---|--- Transits:", vs.name, sun_az, sun_alt ,'  &  ', vm.name, moon_az, moon_alt)
        print( '{:9} {:>6} {:>6} {} {:>5} {} {:>6} {:>7} {} {:>5} {:>6} {:>5} {} {:>7} {:>7} {:>7} {:>8} {} {:>7} {:>7} {:>7} {:>7} {} {:>5}'.format(\
        ' icao or', ' (m)', '(d)', '|', '(km)', '|', '(km)', '(d)', '|', '(d)', '(d)', '(l)', '|', '(d)', '(km)', '(km)', '   (s)', '|', '(d)', '(km)', '(km)', '   (s)', ' |', '(s)'))
        print( '{:9} {:>6} {:>6} {} {:>5} {} {:>6} {:>7} {} {:>5} {:>6} {:>5} {} {:>7} {:>7} {:>7} {:>8} {} {:>7} {:>7} {:>7} {:>7} {} {:>5}'.format(\
        ' flight', 'elev', 'trck', '|', 'dist', '|', '[warn]', '[Alt]', '|', 'Alt', 'Azim', 'Azim', '|', 'Sep', 'p2x', 'h2x', 'time2X', '|', 'Sep', 'p2x', 'h2x', 'time2X', ' |', 'age'))
        print( "------------------------|-------|----------------|--------------------|----------------------------------|----------------------------------|-------")

        ## Subloop through all entries
        with open(out_path,'w') as tsttxt:
            tsttxt.write('')
        for pentry in plane_dict:
            with open(out_path,'a') as tsttxt:
                if not (plane_dict[pentry][5] == '') and (plane_dict[pentry][5] <= 250):
                        if plane_dict[pentry][17] != "":
                            then = plane_dict[pentry][17]
                            now = datetime.datetime.now()
                            diff_seconds = (now - then).total_seconds()
                        else:
                            diff_seconds = 999
                            
                        then1 = plane_dict[pentry][0]
                        now1 = datetime.datetime.now()
                        diff_minutes = (now1 - then1).total_seconds() / 60.

                        wiersz = ''
                        if plane_dict[pentry][1] != "":
                            wiersz += '{} {:7} {}'.format(YELLOW, str(plane_dict[pentry][1]), RESET)                                                 ##flight
                        else:
                            wiersz += '{} {:7} {}'.format(RESET, str(pentry), RESET)                            ##flight
                        if is_float_try(plane_dict[pentry][4]):
                            elevation=int(plane_dict[pentry][4])    
                        else:
                            elevation=9999
                        wiersz += '{} {:>6} {}'.format(elev_col(elevation), str(elevation),RESET)     ##elev
                        wiersz += '{:>5}'.format(str(plane_dict[pentry][11]))                                                ## trck
                        wiersz += '  |'
                        wiersz += '{} {:>5} {}'.format(dist_col(plane_dict[pentry][5]), str(plane_dict[pentry][5]),RESET)    ## dist
                        wiersz += '|'

                        if (plane_dict[pentry][12] == 'WARNING' and plane_dict[pentry][9] != "RECEDING"):
                            wiersz += '{}{}{:>5}{}{}'.format(str('['),REDALERT, str( plane_dict[pentry][13]),RESET, str(']'))                    ## warn
                        elif (plane_dict[pentry][12] == 'WARNING' and plane_dict[pentry][9] == "RECEDING"):
                            wiersz += '{}{}{:>5}{}{}'.format(str('['),RED, str( plane_dict[pentry][13]),RESET, str(']'))                            ## warn
                        elif (plane_dict[pentry][12] != 'WARNING' and plane_dict[pentry][9] == "RECEDING"):
                            wiersz += '{}{}{:>5}{}{}'.format(str('['),PURPLEDARK, str( plane_dict[pentry][13]),RESET, str(']'))                    ## warn
                        else:
                            wiersz += '{}{}{:>5}{}{}'.format(str('['),PURPLE, str(plane_dict[pentry][13]),RESET, str(']'))                        ## warn
                        
                        

                        if is_float_try(plane_dict[pentry][13]):
                            if plane_dict[pentry][13] == 0:
                                altitudeX = round(degrees(atan((elevation - my_elevation)/(float(0.01)*1000))) ,1)
                            else:
                                altitudeX = round(degrees(atan((elevation - my_elevation)/(float(plane_dict[pentry][13])*1000))) ,1)
                        else:
                            altitudeX = '0'
                        wiersz += '{}{}{:>5}{}{}'.format(str(' ['), str(alt_col(float(altitudeX))), str(altitudeX),RESET, str(']'))    
                        wiersz += ' |'
                        wiersz += '{} {:>5} {}'.format(alt_col(plane_dict[pentry][7]), str(plane_dict[pentry][7]),RESET)    ## Alt
                        if diff_seconds >= 999:
                            wiersz += '{}'.format(RED+str("x") +RESET)    
                        elif diff_seconds > 30:
                            wiersz += '{}'.format(RED+str("!") +RESET)    
                        elif diff_seconds > 15:
                            wiersz += '{}'.format(YELLOW+ str("!")+ RESET)    
                        elif diff_seconds > 10:
                            wiersz += '{}'.format(GREENFG+ str("!")+ RESET)    
                        else:
                            wiersz += '{}'.format(GREENFG+str("o") +RESET)    
                        wiersz += '{:>6}'.format(str(plane_dict[pentry][6]))                                                ## Az    
                        wiersz += '{:>6}'.format(str(wind_deg_to_str1(plane_dict[pentry][6])))                                ## news

                        

                        wiersz += ' |'

            
                        thenx = plane_dict[pentry][0]
                        nowx = datetime.datetime.now()
                        diff_secx = (nowx - thenx).total_seconds()
                        
                        
                        if is_float_try(plane_dict[pentry][19]) and is_float_try(plane_dict[pentry][18]):
                            separation_deg2 = round(float(plane_dict[pentry][19]-plane_dict[pentry][18]),1)
                        else:
                            separation_deg2 = 90.0
                        
                        if (-transit_separation_GREENALERT_FG < separation_deg2 < transit_separation_GREENALERT_FG):
                            wiersz += '{} {:>6} {}'.format(GREENALERT, str(round((plane_dict[pentry][19]-plane_dict[pentry][18]),1)),RESET) ## SEPARACJA
                            wiersz += '{:>8}'.format(str(plane_dict[pentry][21]))  ## DISTANCE: AIRPLANE POS TO AIRPLANE PATH CROSS  
                            wiersz += '{:>7}'.format(str(round(plane_dict[pentry][20],1))) ## DISTANCE MY_POS TO CROSS POINT
                            wiersz += '{:>10}'.format(str(plane_dict[pentry][22]))            ## delta_tim    ## TIME UNTIL PLANE ARRIVE AT CROS
                            
                        elif (-transit_separation_REDALERT_FG < separation_deg2 < transit_separation_REDALERT_FG):
                            wiersz += '{} {:>6} {}'.format(REDALERT, str(round((plane_dict[pentry][19]-plane_dict[pentry][18]),1)),RESET) ## SEPARACJA
                            wiersz += '{:>8}'.format(str(plane_dict[pentry][21]))  ## DISTANCE: AIRPLANE POS TO AIRPLANE PATH CROSS  
                            wiersz += '{:>7}'.format(str(round(plane_dict[pentry][20],1))) ## DISTANCE MY_POS TO CROSS POINT
                            wiersz += '{:>10}'.format(str(plane_dict[pentry][22]))            ## delta_tim    ## TIME UNTIL PLANE ARRIVE AT CROSS POINT
                        
                        elif (-transit_separation_notignored < separation_deg2 < transit_separation_notignored):
                            wiersz += '{} {:>6} {}'.format(RED, str(round((plane_dict[pentry][19]-plane_dict[pentry][18]),1)),RESET) ## SEPARACJA
                            wiersz += '{:>8}'.format(str(plane_dict[pentry][21]))  ## DISTANCE: AIRPLANE POS TO AIRPLANE PATH CROSS  
                            wiersz += '{:>7}'.format(str(round(plane_dict[pentry][20],1))) ## DISTANCE MY_POS TO CROSS POINT
                            wiersz += '{:>10}'.format(str(plane_dict[pentry][22]))            ## delta_tim    ## TIME UNTIL PLANE ARRIVE AT CROSS POINT    
                        
                        else:
                            wiersz += '{:>8}'.format(str("---"))  ## SEPARACJA
                            wiersz += '{:>8}'.format(str("---"))  ## DISTANCE: AIRPLANE POS TO AIRPLANE PATH CROSS   
                            wiersz += '{:>7}'.format(str("---")) ## DISTANCE MY_POS TO CROSS POINT
                            wiersz += '{:>10}'.format(str("---"))            ## delta_tim    ## TIME UNTIL PLANE ARRIVE AT CROSS POINT                        
                        ###tu koniec
            
                        wiersz += ' |'
                        if is_float_try(plane_dict[pentry][24]) and is_float_try(plane_dict[pentry][23]):
                            separation_deg = round(float(plane_dict[pentry][24]-plane_dict[pentry][23]),1)
                        else:
                            separation_deg = 90.0
                        if (-transit_separation_GREENALERT_FG < separation_deg < transit_separation_GREENALERT_FG):
                            wiersz += '{} {:>6} {}'.format(GREENALERT, str(round((plane_dict[pentry][24]-plane_dict[pentry][23]),1)),RESET) ## SEPARACJA
                            wiersz += '{:>8}'.format(str(plane_dict[pentry][27]))  ## DISTANCE: AIRPLANE POS TO AIRPLANE PATH CROSS  
                            wiersz += '{:>7}'.format(str(round(plane_dict[pentry][25],1))) ## DISTANCE MY_POS TO CROSS POINT
                            wiersz += '{:>10}'.format(str(plane_dict[pentry][26]))            ## delta_tim    ## TIME UNTIL PLANE ARRIVE AT CROS
                            
                            
                        elif (-transit_separation_REDALERT_FG < separation_deg < transit_separation_REDALERT_FG):
                            wiersz += '{} {:>6} {}'.format(REDALERT, str(round((plane_dict[pentry][24]-plane_dict[pentry][23]),1)),RESET) ## SEPARACJA
                            wiersz += '{:>8}'.format(str(plane_dict[pentry][27]))  ## DISTANCE: AIRPLANE POS TO AIRPLANE PATH CROSS  
                            wiersz += '{:>7}'.format(str(round(plane_dict[pentry][25],1))) ## DISTANCE MY_POS TO CROSS POINT
                            wiersz += '{:>10}'.format(str(plane_dict[pentry][26]))            ## delta_tim    ## TIME UNTIL PLANE ARRIVE AT CROSS POINT
                        
                        elif (-transit_separation_notignored < separation_deg < transit_separation_notignored):
                            wiersz += '{} {:>6} {}'.format(RED, str(round((plane_dict[pentry][24]-plane_dict[pentry][23]),1)),RESET) ## SEPARACJA
                            wiersz += '{:>8}'.format(str(plane_dict[pentry][27]))  ## DISTANCE: AIRPLANE POS TO AIRPLANE PATH CROSS  
                            wiersz += '{:>7}'.format(str(round(plane_dict[pentry][25],1))) ## DISTANCE MY_POS TO CROSS POINT
                            wiersz += '{:>10}'.format(str(plane_dict[pentry][26]))            ## delta_tim    ## TIME UNTIL PLANE ARRIVE AT CROSS POINT    
                        
                        else:
                            wiersz += '{:>8}'.format(str("---"))  ## SEPARACJA
                            wiersz += '{:>8}'.format(str("---"))  ## DISTANCE: AIRPLANE POS TO AIRPLANE PATH CROSS   
                            wiersz += '{:>7}'.format(str("---")) ## DISTANCE MY_POS TO CROSS POINT
                            wiersz += '{:>10}'.format(str("---"))            ## delta_tim    ## TIME UNTIL PLANE ARRIVE AT CROSS POINT
                        ##tu koniec2    
                        wiersz += ' |'
                        wiersz += '{:>6}'.format(str(round(diff_secx, 1)))

                        print( wiersz)
                        
                        # next 4 lines data for txt transit history
                        #if (-transit_separation_REDALERT_FG < separation_deg2 < transit_separation_REDALERT_FG) or (-transit_separation_REDALERT_FG < separation_deg < transit_separation_REDALERT_FG):
                        #    with open('/tmp/tr.txt','a') as tra_txt:
                        #        trans_wiersz = str(plane_dict[pentry][0])+wiersz+'\n'
                        #        tra_txt.write(str(trans_wiersz))
                        

                        zapis=str(pentry)+','+str(plane_dict[pentry][1])+','+str(plane_dict[pentry][2])+','+\
                        str(plane_dict[pentry][3])+','+str(plane_dict[pentry][4])+','+str(plane_dict[pentry][5])+','+\
                        str(plane_dict[pentry][6])+','+str(plane_dict[pentry][7])+','+str(plane_dict[pentry][8])+','+\
                        str(plane_dict[pentry][9])+','+str(plane_dict[pentry][10])+','+str(plane_dict[pentry][11])+','+\
                        str(plane_dict[pentry][12])+','+str(plane_dict[pentry][13])+','+str(plane_dict[pentry][14])+','
                        for ii,e in enumerate(plane_dict[pentry][15]):
                            zapis += str(plane_dict[pentry][15][ii])+';'
                        zapis += ','
                        for ii,e in enumerate(plane_dict[pentry][16]):
                            zapis += str(plane_dict[pentry][16][ii])+';'
                        zapis += ','
                        zapis += str(plane_dict[pentry][17])+','+str(datetime.datetime.now().strftime('%H:%M:%S'))+','
                        zapis += str(plane_dict[pentry][27])+','+str(separation_deg)+','+str(moon_az)+','+str(plane_dict[pentry][24])+','
                        zapis += str(plane_dict[pentry][21])+','+str(separation_deg2)+','+str(sun_az)+','+str(plane_dict[pentry][19])+','
                        zapis += str(vm.name)+','+str(vs.name)+','+str(diff_seconds)+',\n'
                        tsttxt.write(str(zapis))
                        
                else:
                    if plane_dict[pentry][17] != "":
                        then = plane_dict[pentry][17]
                        now = datetime.datetime.now()
                        diff_seconds = (now - then).total_seconds()
                    else:
                        diff_seconds = 999
                    if plane_dict[pentry][1] != "":
                        wiersz = ''
                        wiersz += '{} {:7} {}'.format(YELLOW, str(plane_dict[pentry][1]), RESET)   ##flight
                    else:
                        wiersz = ''
                        wiersz += '{} {:7} {}'.format(RESET, str(pentry),RESET)                    ##icao
                        
                    if plane_dict[pentry][4] != "":
                        if is_float_try(plane_dict[pentry][4]):
                            elevation=int(plane_dict[pentry][4])    
                        else:
                            elevation=9999
                        wiersz += '{} {:>6} {}'.format(elev_col(elevation), str(elevation),RESET)     ##elev
                        
                    else:
                        wiersz += '{} {:>6} {}'.format(RESET,str('---'),RESET)                         ##elev
                    if plane_dict[pentry][11] != "":
                        wiersz += '{:>5}'.format(str(plane_dict[pentry][11]))                          ##track
                    else:
                        wiersz += '{:>5}'.format(str('---'))
                        
                    wiersz += '  |'
                    if plane_dict[pentry][5] != "":
                        wiersz = ''
                        wiersz += '{} {:>5} {}'.format(RESET, str(plane_dict[pentry][5]), RESET)       ##flight
                    else:    
                        wiersz += '{} {:>5} {}'.format(RESET, str('---'),RESET)    
                    wiersz += '|'                

                    
                    wiersz += '{} {:>5} {}'.format(RESET, str('---'),RESET)                     ## warn

                    wiersz += '{} {:>5} {}'.format(RESET, str('---'),RESET) ## alt    
                    wiersz += '  |'                

                    wiersz += '{} {:>5} {}'.format(RESET, str('---'),RESET) ## alt    
                    if diff_seconds > 5:
                        wiersz += '{}'.format(str("!"))    
                    else:
                        wiersz += '{}'.format(str(" "))
                    wiersz += '{:>7}'.format(str('---'))                     ## az1 news

                    wiersz += '{:>5}'.format(str('---'))                     ## az2
                    wiersz += ' |'
                    wiersz += '{} {:>7} {}'.format(RESET, str('---'),RESET)                ## Sep
                    wiersz += '{:>7}'.format(str('---')) 
                    wiersz += '{:>7}'.format(str('---')) 
                    wiersz += '{:>10}'.format(str('---')) 
                    wiersz += ' |'
                    wiersz += '{} {:>7} {}'.format(RESET, str('---'),RESET)                ## Sep
                    wiersz += '{:>7}'.format(str('---')) 
                    wiersz += '{:>7}'.format(str('---')) 
                    wiersz += '{:>10}'.format(str('---')) 
                    wiersz += ' |'
                    thenx = plane_dict[pentry][0]
                    nowx = datetime.datetime.now()
                    diff_secx = (nowx - thenx).total_seconds()
                    wiersz += '{:>6}'.format(str(round(diff_secx, 1)))

                    print( wiersz)

        lastline=str(datetime.datetime.time(datetime.datetime.now()))
        lastline+= " --- "
        lastline+= str(len (plane_dict))
        lastline+= " --- "
        lastline+= str(int(diff_t))
        lastline+= " --- "+ str(pressure)+"hPa"
        lastline+= " Started: "+str(started)#+" Ago: "+str(aktual_txx)
        print( lastline)

    return moon_alt, moon_az, sun_alt, sun_az 

moon_alt, moon_az, sun_alt, sun_az = tabela()
#
# loop through all records from dump1090 port 10003 input stream on stdin
#
while True:
    line=sys.stdin.readline()
    aktual_t = datetime.datetime.now()

    if line in ['\n', '\r\n']:
        plane_dict.clear()     # remove all entries in dict
        print( ''    )    
        with open(out_path,'w') as tsttxt:
            tsttxt.write('')
    else:
        #
        # divide input line into parts and extract desired values
        #
        parts = line.split(",")
        ## MLAT,3,1,1,484B31,1,2020/02/06,21:47:08.674,2020/02/06,21:47:08.674,,38993,441,93,52.4934,16.8546,45,,,,,,,,
        type = parts[1].strip()
        typemlat = parts[0].strip()
        icao = parts[4].strip()
        date = parts[6].strip()
        time = parts[7].strip()
        if (typemlat == "MLAT"):
            date_time_local = datetime.datetime.strptime(date + " " + time, '%Y/%m/%d %H:%M:%S.%f') #+ datetime.timedelta(minutes=60)
        else:
            date_time_local = datetime.datetime.strptime(date + " " + time, '%Y/%m/%d %H:%M:%S.%f')- datetime.timedelta(minutes=60)
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
                if elevation > 6500:
                    pressure = int(get_metar_press())
                    elevation = elevation + ((1013 - pressure)*30)
                    my_elevation = my_elevation_const
                else:
                    my_elevation = 90# -90 ## taka sama wysokość punktu obserwacji n.p.m jak pas na EPPO
                ## powyzsze tu nic nie robi
                if (metric_units):
                    elevation = float((elevation * 0.3048)) # convert elevation feet to meters
                else:
                    elevation = ""
            if (icao not in plane_dict): 
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
                    distance = float(round(haversine((my_lat, my_lon), (plane_lat, plane_lon)),1))
                    azimuth = atan2(sin(radians(plane_lon-my_lon))*cos(radians(plane_lat)), cos(radians(my_lat))*sin(radians(plane_lat))-sin(radians(my_lat))*cos(radians(plane_lat))*cos(radians(plane_lon-my_lon)))
                    azimuth = round(((degrees(azimuth) + 360) % 360),1)
                    if distance == 0:
                        distance = 0.01    
                    altitude = degrees(atan((elevation - my_elevation)/(distance*1000))) # distance converted from kilometers to meters to match elevation
                    altitude = round(altitude,1)
                    if (icao not in plane_dict):
                        if (typemlat == "MLAT"):
                            track = parts[13].strip()
                            plane_dict[icao] = [date_time_local, "", plane_lat, plane_lon, elevation, float(distance), azimuth, altitude, "", "", float(distance), track, "", "", "", [], [], "", "", "", "", "", "", "", "", "", "", "", ""]
                        else:
                            plane_dict[icao] = [date_time_local, "", plane_lat, plane_lon, elevation, float(distance), azimuth, altitude, "", "", float(distance), "", "", "", "", [], [], "", "", "", "", "", "", "", "", "", "", "", ""]
                        plane_dict[icao][15] = []
                        plane_dict[icao][16] = []    
                        plane_dict[icao][15].append(azimuth)
                        plane_dict[icao][16].append(altitude)                
                    else:
                        #
                        # figure out if plane is approaching/holding/receding
                        #
                        if not (plane_dict[icao][5] == '' or plane_dict[icao][10] == ''):
                            distance = plane_dict[icao][5]
                            min_distance = plane_dict[icao][10]
                            if (distance < min_distance):
                                plane_dict[icao][9] = "APPROACHING"
                                plane_dict[icao][10] = distance
                            elif (distance > min_distance):
                                plane_dict[icao][9] = "RECEDING"
                            else:
                                plane_dict[icao][9] = "HOLDING"

                        if (typemlat == "MLAT"):
                            track = parts[13].strip()
                            plane_dict[icao][11] = track
                        
                        plane_dict[icao][0] = date_time_local
                        plane_dict[icao][2] = plane_lat
                        plane_dict[icao][3] = plane_lon
                        plane_dict[icao][4] = elevation 
                        plane_dict[icao][5] = distance 
                        plane_dict[icao][6] = azimuth 
                        plane_dict[icao][7] = altitude 
                        
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
                        
                        # Next 3 lines - data for heatmaps
                        #log_line = str(plane_lat)+","+str(plane_lon)+","+str(elevation)
                        #with open("/tmp/_heatmap_asi.dat", 'a') as tsttxt:
                        #        tsttxt.write(log_line+",\n")            
                #        
                # if matched record between type 1/3  occurs, log stats to stdout and also email if entering/leaving detection zone
                #
                # if ((type == "1" or type == "3" or type == "4") and (icao in plane_dict and plane_dict[icao][1] != "" and plane_dict[icao][2] != "" and plane_dict[icao][11] != "")):
        if ((type == "1" or type == "3" or type == "4") and (icao in plane_dict and plane_dict[icao][2] != "" and plane_dict[icao][11] != "")):

            flight             = plane_dict[icao][1]
            plane_lat         = plane_dict[icao][2]
            plane_lon         = plane_dict[icao][3]
            elevation         = plane_dict[icao][4]
            distance         = plane_dict[icao][5]
            azimuth         = plane_dict[icao][6]
            altitude         = plane_dict[icao][7]
            track             = plane_dict[icao][11]
            warning         = plane_dict[icao][12]
            direction         = plane_dict[icao][9]
            # elevation_feet     = int(round(int(round(elevation / 0.3048)/100)))
            velocity         = plane_dict[icao][14]
            xtd             = crosstrack(distance, (180 + azimuth) % 360, track)
            
            plane_dict[icao][13] = xtd
            
            if (xtd <= xtd_tst and distance < warning_distance and warning == "" and direction != "RECEDING"):
                plane_dict[icao][12] = "WARNING"
                plane_dict[icao][13] = xtd
                gong()

            if (xtd > xtd_tst and distance < warning_distance and warning == "WARNING" and direction != "RECEDING"):
                plane_dict[icao][12] = ""
                plane_dict[icao][13] = xtd
                gong()

            if (plane_dict[icao][8] == ""):
                plane_dict[icao][8] = "LINKED!"
        
            #
            # if plane enters detection zone, send email and begin history capture
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


            ## Transit check
            tst_int1 = transit_pred((my_lat, my_lon), (plane_lat, plane_lon), track, velocity, elevation, moon_alt, moon_az)
            tst_int2 = transit_pred((my_lat, my_lon), (plane_lat, plane_lon), track, velocity, elevation, sun_alt, sun_az)
            
            if tst_int1 == 0:
                #if (plane_dict[icao][23] == ''):
                alt_a = 90.0 # moon_alt
                dst_p2x = 996
                delta_time = 0
                dst_h2x = 998
                plane_dict[icao][23] = 999.0         ## MOON ALT
                plane_dict[icao][24] = alt_a
                plane_dict[icao][25] = dst_h2x        ## dst_h2x        ## DISTANCE MY_POS TO CROSS POINT
                plane_dict[icao][26] = delta_time 
                plane_dict[icao][27] = dst_p2x         ## dst_p2x        ## DISTANCE PLANE TO MOON AZIMUTH (CROSS)    
            else:
                alt_a     = round(tst_int1[3],2)          ##    altitude1    ## ALT OF CROSS POINT
                dst_h2x = round(tst_int1[4],2)      ## dst_h2x        ## DISTANCE MY_POS TO CROSS POINT
                dst_p2x = round(tst_int1[5],2)          ## dst_p2x        ## DISTANCE PLANE TO MOON AZIMUTH (CROSS)
                delta_time = int(tst_int1[6])         ## delta_tim    ## TIME UNTIL PLANE ARRIVE AT CROSS POINT
                plane_dict[icao][25] = dst_h2x        ## dst_h2x        ## DISTANCE MY_POS TO CROSS POINT
                plane_dict[icao][23] = moon_alt
                plane_dict[icao][24] = alt_a 
                plane_dict[icao][26] = delta_time 
                plane_dict[icao][27] = dst_p2x         ## dst_p2x        ## DISTANCE PLANE TO MOON AZIMUTH (CROSS)    
                
                if is_float_try(plane_dict[icao][24]) and is_float_try(plane_dict[icao][23]):
                    separation_deg = round(float(plane_dict[icao][24]-plane_dict[icao][23]),1)
                else:
                    separation_deg = 90.0
                if (-transit_separation_sound_alert < separation_deg < transit_separation_sound_alert):
                    # sun
                    #gong() # SUN!!!
                    pass
                
            if tst_int2 == 0:
                #if (plane_dict[icao][23] == ''):
                alt_a = 90.0 # moon_alt
                dst_p2x = 996
                delta_time = 0
                dst_h2x = 998
                plane_dict[icao][18] = 999.0        ## SUN ALT
                plane_dict[icao][19] = alt_a 
                plane_dict[icao][20] = dst_h2x        ## dst_h2x        ## DISTANCE MY_POS TO CROSS POINT
                plane_dict[icao][22] = delta_time 
                plane_dict[icao][21] = dst_p2x         ## dst_p2x        ## DISTANCE PLANE TO SUN AZIMUTH (CROSS)    

            else:
                alt_a     = round(tst_int2[3],2)         ##    altitude1    ## ALT OF CROSS POINT
                dst_h2x = round(tst_int2[4],2)      ## dst_h2x        ## DISTANCE MY_POS TO CROSS POINT
                dst_p2x = round(tst_int2[5],2)          ## dst_p2x        ## DISTANCE PLANE TO SUN AZIMUTH (CROSS)
                delta_time = int(tst_int2[6])         ## delta_tim    ## TIME UNTIL PLANE ARRIVE AT CROSS POINT
                plane_dict[icao][20] = dst_h2x        ## dst_h2x        ## DISTANCE MY_POS TO CROSS POINT
                plane_dict[icao][18] = sun_alt
                plane_dict[icao][19] = alt_a 
                plane_dict[icao][22] = delta_time 
                plane_dict[icao][21] = dst_p2x         ## dst_p2x        ## DISTANCE PLANE TO SUN AZIMUTH (CROSS)    
            
                if is_float_try(plane_dict[icao][19]) and is_float_try(plane_dict[icao][18]):
                    separation_deg2 = round(float(plane_dict[icao][19]-plane_dict[icao][18]),1)
                else:
                    separation_deg2 = 90.0
                if (-transit_separation_sound_alert < separation_deg2 < transit_separation_sound_alert):
                    # moon
                    gong()
                        #pass

    moon_alt, moon_az, sun_alt, sun_az = tabela()
    clean_dict()
