Colors used in table for various ranges.

 dist_col(distance): (distance in km)
        distance > 300  PURPLEDARK
 300 >= distance > 100  PURPLE
 100 >= distance > 50   CYAN
 50  >= distance > 30   YELLOW
 30  >= distance > 15   REDALERT
 15  >= distance > 0    GREENALERT

 alt_col(altitude): (alt in degrees)
 5  and <= altitude <  15  PURPLE
 15 and <= altitude <  25  CYAN
 25 and <= altitude <  30  YELLOW
 30 and <= altitude <  35  REDALERT
 35 and <= altitude <= 90  GREEN
           altitude >  35  PURPLEDARK

 elev_col(elevation): (elevation in meters)
         elevation  < 8000 RESET (white on black)
 4000 <= elevation <= 8000 PURPLE
 2000 <= elevation  < 4000 GREEN
 0    <  elevation  < 2000 YELLOW
