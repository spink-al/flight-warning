# Meters above sea level
MY_ALT="90"

# timestamp diff
time_corr="1"
minutes_add="-60"

# timestamp diff mlat
time_corr_mlat="1"
minutes_add_mlat="-60"




# data output to file, for no output change "/tmp/out.txt" to "/dev/null"
gen_term="0" # 0 will disable data in terminal
out_path="/tmp/out.txt"

gen_html="1" # 0 will disable html and html play wav with countdown 3m,2m,1m,50s,40,30,20,10,9,8,7,6,5,4,3,2,1,0s
out_path_html="/tmp/out6.html"

gen_html_snd="1" # 0 will disable html play wav with countdown 3m,2m,1m,50s,40,30,20,10,9,8,7,6,5,4,3,2,1,0s
out_path_html_snd="/tmp/out7.html"



# need more tests:
metar_active="0" # 0/1
metar_path="/tmp/metar.txt"
# if metar not available (0) use this pressure:
pressure="1013"
ignore_pressure="1"
near_airport_code="EPPO" # EPPO EDDB etc not POZ SXF
near_airport_elevation="94"

display_limit="250" # ignore planes further than, in km
warning_distance="249"
# "check age of newest icao record, compare to newly-input value, and kill dictionary if too old (i.e. start fresh history)"
alert_duplicate_minutes="20" # minutes
# radius of "detection zone"; status "ENTERING" or "LEAVING"
alert_distance="35" # km
# comparison value for "xtd"/"cross-track error routine" calculated minimal distance at which plane will be near observator(?)
xtd_tst="40" # km

# maximum transit angle separation for sound alert 
transit_separation_sound_alert="1.5" # terminal beeps and/or html play wav with countdown 3m,2m,1m,50s,40,30,20,10,9,8,7,6,5,4,3,2,1,0s
# maximum transit angle separation for colouring in table 
transit_separation_REDALERT_FG="20"
transit_separation_GREENALERT_FG="10"  # terminal beeps and/or html play wav with countdown 3m,2m,1m,50s,40,30,20,10,9,8,7,6,5,4,3,2,1,0s
transit_separation_notignored="90"

minimum_alt_transits="5"   # terminal beeps and/or html play wav with countdown 3m,2m,1m,50s,40,30,20,10,9,8,7,6,5,4,3,2,1,0s

# write transit history to file, (with colours, tail -f /tmp/tr.txt or less -r /tmp/tr.txt):
transit_history_log="0" # 1/0
transit_history_log_path="/tmp/tr.txt"

# enable/disable sounds alerts:
# Sun transits:
sun_tr_sound="1" # 1/0   # terminal beeps and/or html play wav with countdown 3m,2m,1m,50s,40,30,20,10,9,8,7,6,5,4,3,2,1,0s
# Moon transits:
moon_tr_sound="1" # 1/0   # terminal beeps and/or html play wav with countdown 3m,2m,1m,50s,40,30,20,10,9,8,7,6,5,4,3,2,1,0s

# terminal beeps
terminal_beeps="0" #1/0 # master mute for terminal beeps
# Entering detection zone:
entering_sound="1" # 1/0 terminal beeps only
# New plane that will enter detection zone in near future:
detected_sound="1" # 1/0 terminal beeps only
# how often gong can be released in seconds (putty/terminal settings may use longer timeouts if bell is overused!)
min_t_sound="1.0" # float for test # seconds between terminal beeps, can be altered by putty/terminal conf

# write data for 3d heatmaps to file (lat,lon,alt,):
heatmap_latlon_log="0"
heatmap_latlon_log_path="/tmp/_heatmap_asi.dat"


# not working todo
time_corr_ephem="0"
minutes_add_ephem="0"
