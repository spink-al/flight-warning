# Do not use spaces between var name and "=" or after it,
# *conf.py files are used also by bash scripts, and this will creep them out!

# Lat/Lon
MY_LAT="51.1234"
MY_LON="15.1234"
# Meters above sea level
MY_ALT="90"


# timestamp diff
time_corr="1"
minutes_add="-60"

# timestamp diff mlat
time_corr_mlat="1"
minutes_add_mlat="-60"


# data output to file, for no output change "/tmp/out.txt" to "/dev/null"
out_path="/tmp/out.txt"

# need more tests:
metar_active="0" # 0/1
metar_path="/tmp/metar.txt"
# if metar not available (0) use this pressure:
pressure="1013"
ignore_pressure="1"
near_airport_code="EPPO" # EPPO EDDB etc not POZ SXF
near_airport_elevation="94"

display_limit="250" # ignore planes further than, in km
warning_distance="249" # do not generate warnings for planes further than, in km
alert_duplicate_minutes="20" # minutes # "check age of newest icao record, compare to newly-input value, and kill dictionary if too old (i.e. start fresh history)"
alert_distance="15" # km # radius of "detection zone"; status "ENTERING" or "LEAVING"
xtd_tst="20" # km # comparison value for "xtd"/"cross-track error routine" calculated minimal distance at which plane will be near observator(?)

transit_separation_sound_alert="2.2" #deg # maximum transit angle separation for sound alert
transit_separation_REDALERT_FG="5" # maximum transit angle separation for red colouring in table 
transit_separation_GREENALERT_FG="3" # maximum transit angle separation for green colouring in table 
transit_separation_notignored="90" # don't touch
xtd_tst="20" # km

minimum_alt_transits="5"

# write transit history to file, (with colours, tail -f /tmp/tr.txt or less -r /tmp/tr.txt):
transit_history_log="0" # 1/0
transit_history_log_path="/tmp/tr.txt"

# enable/disable sounds alerts:
# Sun transits:
sun_tr_sound="1" # 1/0
# Moon transits:
moon_tr_sound="1" # 1/0
# Entering detection zone:
entering_sound="1" # 1/0
# New plane that will enter detection zone in near future:
detected_sound="1" # 1/0
# how often gong can be released in seconds (putty/terminal settings may use longer timeouts if bell is overused!)
min_t_sound="2.0" # float for test

# write data for 3d heatmaps to file (lat,lon,alt,):
heatmap_latlon_log="0"
heatmap_latlon_log_path="/tmp/_heatmap_asi.dat"

# not working todo
time_corr_ephem="0"
minutes_add_ephem="0"
