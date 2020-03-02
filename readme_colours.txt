Colors used in table for various ranges.

 dist_col(distance): (distance in km)
        distance > 300  PURPLEDARK    (default/black bg)
 300 >= distance > 100  PURPLE        (default/black bg)
 100 >= distance > 50   CYAN          (default/black bg)
 50  >= distance > 30   YELLOW        (default/black bg)
 30  >= distance > 15   REDALERT      (black on red bg)
 15  >= distance > 0    GREENALERT    (black on green bg) (same as green?)

 alt_col(altitude): (alt in degrees)
 5  and <= altitude <  15  PURPLE     (default/black bg)
 15 and <= altitude <  25  CYAN       (default/black bg)
 25 and <= altitude <  30  YELLOW     (default/black bg)
 30 and <= altitude <  35  REDALERT   (white on red bg)
 35 and <= altitude <= 90  GREEN      (black on green bg) (same as greenalert?)
           altitude >  35  PURPLEDARK (default/black bg)

 elev_col(elevation): (elevation in meters)
         elevation  < 8000 RESET       (white on default/black bg)
 4000 <= elevation <= 8000 PURPLE      (default/black bg)
 2000 <= elevation  < 4000 GREEN       (black on green bg) (same as greenalert?)
 0    <  elevation  < 2000 YELLOW      (default/black bg)

Definitions:
#TERMINAL COLORS
REDALERT        = '\x1b[1;37;41m'
PURPLE          = '\x1b[1;35;40m'
PURPLEDARK      = '\x1b[0;35;40m'
RED             = '\x1b[0;31;40m'.
GREEN           = '\x1b[0;30;42m'.
GREENALERT      = '\x1b[0;30;42m'.
# GREENFG       = '\x1b[0;42;40m'.
GREENFG         = '\x1b[1;32;40m'.
BLUE            = '\x1b[1;34;40m'
YELLOW          = '\x1b[1;33;40m'
CYAN            = '\x1b[1;36;40m'
RESET           = '\x1b[0m'.
CLEARSCREEN     = '\033c'
# Used directly for sound:
GONG            = '\a'
