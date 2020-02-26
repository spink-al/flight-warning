#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageStat, ImageFont, ImageDraw,ImageColor
#from PIL.ExifTags import TAGS
#import PIL.ExifTags
import sys
import time
from time import gmtime, strftime
import datetime
import ephem
import math
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np
import os.path,errno
import shutil 
#import cv2
#import ASR_Conf

tleFileName = './iss.tle'

gatech = ephem.Observer()
gatech.lat = '52.4451'
gatech.lon = '16.9535'
gatech.elevation = 90
deg = u'\xb0'
uus = u'\xb5s'
jups = u"\u2643"
mars = u"\u2642"
vens = u"\u2640"
sats = u"\u2644"
sols = u"\u2609"
luns = u"\u263d"
issline=[]

tlefile=open(tleFileName, 'r')
tledata=tlefile.readlines()
tlefile.close()

for i, line in enumerate(tledata):
    if "ISS" in line: 
        for l in tledata[i:i+3]: issline.append(l.strip('\r\n').rstrip()),

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

#def symlink_force(target, link_name):
#    try:
#        os.symlink(target, link_name)
#    except OSError, e:
#        if e.errno == errno.EEXIST:
#            os.remove(link_name)
#            os.symlink(target, link_name)
#        else:
#            raise e

def get_field (exif,field) :
  for (k,v) in exif.iteritems():
     if TAGS.get(k) == field:
        return v


while True:
    #line=sys.stdin.readline()
    dataczas = str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    start = time.time()    

    gatech.date = ephem.now()  #- ephem.hour#'2018/2/27 02:57:00'
    
    vs = ephem.Sun(gatech)
    vm = ephem.Moon(gatech)
    print (gatech.date)
    vju = ephem.Jupiter(gatech)
    vsa = ephem.Saturn(gatech)
    vma = ephem.Mars(gatech)
    vve = ephem.Venus(gatech)
    str_vs  = "Sol:  "+str('{:> 6.1f}'.format((  round(math.degrees(vs.alt	), 1))))+deg+" "+str('{:> 6.1f}'.format((  round(math.degrees(vs.az ), 1))))+deg
    str_vm  = "Lun:  "+str('{:> 6.1f}'.format((  round(math.degrees(vm.alt	), 1))))+deg+" "+str('{:> 6.1f}'.format((  round(math.degrees(vm.az ), 1))))+deg
    str_vju = "Jup:  "+str('{:> 6.1f}'.format((  round(math.degrees(vju.alt), 1))))+deg+" "+str('{:> 6.1f}'.format((  round(math.degrees(vju.az), 1))))+deg
    str_vsa = "Sat:  "+str('{:> 6.1f}'.format((  round(math.degrees(vsa.alt), 1))))+deg+" "+str('{:> 6.1f}'.format((  round(math.degrees(vsa.az), 1))))+deg
    str_vma = "Mar:  "+str('{:> 6.1f}'.format((  round(math.degrees(vma.alt), 1))))+deg+" "+str('{:> 6.1f}'.format((  round(math.degrees(vma.az), 1))))+deg
    str_vve = "Ven:  "+str('{:> 6.1f}'.format((  round(math.degrees(vve.alt), 1))))+deg+" "+str('{:> 6.1f}'.format((  round(math.degrees(vve.az), 1))))+deg

    if os.path.isfile('/tmp/out.txt'):
        DataFileName='/tmp/out.txt'
        datafile=open(DataFileName, 'r')
        dataz=datafile.readlines()
        datafile.close()
    else:
        dataz=''

    if not dataz:
        last_time_fw = 'N/A'

    
    in_center = ''

    overlay = "1" #parts[3] 
    in_center = "1" #parts[2]

    stars_ovrl = "0" #parts[12]

    
    # crop faza 1
    #imagCrop = imagBIG.crop((85, 25, 2449, 2389))
    #imagCrop = imagBIG.crop((64, 32, 2304, 2272))
    imagCrop = Image.new('RGB', (1080, 1080), color = 'black')
    #imagCrop = Image.new('RGB', (2240, 2240), color = '#262626')
    #imagCrop = Image.new('RGB', (1080, 1080), color = '#262626')
    #imagCrop = Image.new('RGB', (1080, 1080), color = '#9fa69b')
    
    draw = ImageDraw.Draw(imagCrop)
    
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", 15)
    #draw.text((30,5  ),metar.strip(' ')							,(125,125,125),font=font)
    draw.text((20,5 ),"AllSkyRadar a0.1 - dummy"						,(100,100,100),font=font)
    #draw.text((30,75 ),"rPi0.0C+rPiCam_v2.1_noir_mod1.1"				,(100,100,100),font=font)
    '''
    draw.text((30,110),"Exp: "+exp+"s = "+exp_ms+uus				,(125,125,125),font=font)
    #draw.text((30,145),"ISO: N/A"						,(125,125,125),font=font)
    draw.text((30,180),"ag: "+ag+" dg: "+dg					,(125,125,125),font=font)
    draw.text((30,215),"wb_r: N/A "+"wb_b: N/A"					,(125,125,125),font=font)
    draw.text((30,250),"Tam: "+ambtemp+"C"+deg						,(125,125,125),font=font)
    draw.text((30,285),"Tco: "+coretemp+"C"+deg						,(125,125,125),font=font)
    draw.text((30,320),"ff: "+dirname						,(125,125,125),font=font)
    #draw.text((30,355),"Tof: "+file_tttt_exif[1]				,(255,255,0),font=font)
    '''
    draw.text((20,25),"tt: "+dataczas				,(255,255,0),font=font)
    '''
    draw.text((30,355),"Tof: "+file_tttt_exif[1]				,(255,255,0),font=font)
    draw.text((30,390),"jpg: "+ff						,(125,125,125),font=font)
    draw.text((30,425),"1: "+str(br_1Ai2Ai3A)					,(125,125,125),font=font)
    draw.text((30,460),"2: "+str(br_1Bi2Bi3B)					,(125,125,125),font=font)
    draw.text((30,495),"3: "+str(br_4Ai5A)					,(125,125,125),font=font)
    draw.text((30,530),"4: "+str(br_4Bi5B)					,(125,125,125),font=font)
    draw.text((30,565),"5: "+str(int(stat6A.rms[0]))				,(125,125,125),font=font)
    draw.text((30,600),"6: "+str(int(stat6B.rms[0]))				,(125,125,125),font=font)
    draw.text((30,635),"S: "+str(brightness_sum)				,(125,125,125),font=font)	
    '''
    draw.text((20,980 ),str_vs  					,(125,125,125),font=font)
    draw.text((20,995 ),str_vm  					,(125,125,125),font=font)
    #draw.text((20,940 ),str_vju 					,(125,125,125),font=font)
    #draw.text((20,965 ),str_vsa 					,(125,125,125),font=font)
    #draw.text((20,990 ),str_vma 					,(125,125,125),font=font)
    #draw.text((20,1015),str_vve  					,(125,125,125),font=font)
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 17)
    
                        
    draw.text((60,980 ),sols  	,(125,125,125),font=font)
    draw.text((60,995 ),luns  	,(125,125,125),font=font)
    #draw.text((60,940 ),jups  	,(125,125,125),font=font)
    #draw.text((60,965 ),sats  	,(125,125,125),font=font)
    #draw.text((60,990 ),mars  	,(125,125,125),font=font)
    #draw.text((60,1015),vens  	,(125,125,125),font=font)
    
    #opencvImage = cv2.cvtColor(np.array(imagCrop), cv2.COLOR_RGB2BGR)
    
    
    imagCropHD = imagCrop #.resize((1080, 1080),Image.LANCZOS)  
    

    if (overlay == "1"):
        #in_center = sys.argv[1]
        #plt.ioff()
        ##########
        
        plt = Figure(figsize=(10.80, 10.80))
        plt.patch.set_alpha(0)
        canvas = FigureCanvasAgg(plt)
        ax = plt.add_subplot(111, projection='polar')#, facecolor='#ff0000')  # create figure & 1 axis
        ax.patch.set_alpha(0)
        
    
        # Always get the latest ISS TLE data from:
        # http://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html
            
        #        issline1, issline2, issline3 = """\
        #ISS (ZARYA)
        #1 25544U 98067A   18287.70571382  .00002129  00000-0  39808-4 0  9995
        #2 25544  51.6416 143.1173 0003445 287.0504 150.6208 15.53823327137100
        #""".splitlines()
        
        iss=ephem.readtle(issline[0], issline[1], issline[2])
        iss.compute(gatech)
        
        #print math.degrees(iss.alt),math.degrees(iss.az)
        #info = gatech.next_pass(iss)
        #print("Rise time: %s azimuth: %s" % (info[0], info[1]))
        
        if iss.eclipsed:
            fontX = {'color':  "darkgray", 'size': 12, 'weight': 'bold', 'family': 'monospace', }
            vert_alX=str('bottom') ; hori_alX=str('left')
        else:
            fontX = {'color':  "white", 'size': 12, 'weight': 'bold', 'family': 'monospace', }
            vert_alX=str('bottom') ; hori_alX=str('left')
        
        ax.plot(iss.az,90-(round(math.degrees(iss.alt),1)),'o',markersize=15, markerfacecolor='none', markeredgecolor=fontX['color'], alpha=1) 
        #ax.text(iss.az,90-(round(math.degrees(iss.alt),1)), ' ISS', verticalalignment=vert_alX, horizontalalignment=hori_alX, fontdict=fontX, alpha=1)
        ax.text(iss.az,90-(round(math.degrees(iss.alt),1)), ' \n ISS \n '+str(int(iss.range)/1000)+'km', verticalalignment=vert_alX, horizontalalignment=hori_alX, fontdict=fontX, alpha=0.5)
        iss_azis=[]
        iss_elevis=[]
    
        ISS_PREDICT=[-180,-150,-120,-90,-60,-30,30,60,90,120,150,180,210,240,270,300,330,360,390,420,450,480,510,540,570,600]
        for i in ISS_PREDICT:
            d_t1 = datetime.datetime.utcnow() + datetime.timedelta(seconds=i)#+ datetime.timedelta(minutes=35)
            gatech.date = ephem.Date(d_t1)
            iss.compute(gatech)
            iss_azis.append(iss.az)
            iss_elevis.append(90-(round(math.degrees(iss.alt),1)))
            #print iss.az,round(math.degrees(iss.alt),1)
        ax.plot(iss_azis,iss_elevis,'--',markersize=2, color='white', lw=1, alpha=0.6) 
        #print iss_elevis
    
        fontX = {'color':  "white", 'size': 8, 'weight': 'normal', 'family': 'monospace', }
        vert_alX=str('top') ; hori_alX=str('left')
    
        gatech.date = ephem.now() #- ephem.hour #RESET!
        if (stars_ovrl == "1"):
            #lista_s=['Phecda','Dubhe','Castor','Pollux','Mizar','Betelgeuse','Altair','Vega','Rigel','Diphda','Sirius','Deneb','Arcturus','Capella','Hamal','Alcyone','Aldebaran','Alphecca','Menkalinan','Menkar','Polaris','Procyon','Sadr']
            lista_s=['Acamar', 'Achernar', 'Acrux', 'Adara', 'Agena', 'Albereo', 'Alcaid', 'Alcor', 'Alcyone', 'Aldebaran', 'Alderamin', 'Alfirk', 'Algenib', 'Algieba', 'Algol', 'Alhena', 'Alioth', 'Almach', 'Alnair', 'Alnilam', 'Alnitak', 'Alphard', 'Alphecca', 'Alpheratz', 'Alshain', 'Altair', 'Ankaa', 'Antares', 'Arcturus', 'Arkab Posterior', 'Arkab Prior', 'Arneb', 'Atlas', 'Atria', 'Avior', 'Bellatrix', 'Betelgeuse', 'Canopus', 'Capella', 'Caph', 'Castor', 'Cebalrai', 'Deneb', 'Denebola', 'Diphda', 'Dubhe', 'Electra', 'Elnath', 'Eltanin', 'Enif', 'Etamin', 'Fomalhaut', 'Formalhaut', 'Gacrux', 'Gienah', 'Hadar', 'Hamal', 'Izar', 'Kaus Australis', 'Kochab', 'Maia', 'Markab', 'Megrez', 'Menkalinan', 'Menkar', 'Menkent', 'Merak', 'Merope', 'Miaplacidus', 'Mimosa', 'Minkar', 'Mintaka', 'Mirach', 'Mirfak', 'Mirzam', 'Mizar', 'Naos', 'Nihal', 'Nunki', 'Peacock', 'Phecda', 'Polaris', 'Pollux', 'Procyon', 'Rasalgethi', 'Rasalhague', 'Regulus', 'Rigel', 'Rigil Kentaurus', 'Rukbat', 'Sabik', 'Sadalmelik', 'Sadr', 'Saiph', 'Scheat', 'Schedar', 'Shaula', 'Sheliak', 'Sirius', 'Sirrah', 'Spica', 'Suhail', 'Sulafat', 'Tarazed', 'Taygeta', 'Thuban', 'Unukalhai', 'Vega', 'Vindemiatrix', 'Wezen', 'Zaurak', 'Zubenelgenubi']
    
            ############
            for star in lista_s:
                v = ephem.star(star)
                v.compute(gatech)
                ax.plot(np.radians(float(round(math.degrees(v.az), 1))),90-(round(math.degrees(v.alt),1)),'.',markersize=3, markerfacecolor='none', markeredgecolor='#ffffff', alpha=1.0) 
                ax.text(np.radians(float(round(math.degrees(v.az), 1))),90-(round(math.degrees(v.alt),1)), ' \n'+str(star)+' \n ', verticalalignment=vert_alX, horizontalalignment=hori_alX, fontdict=fontX, alpha=0.3)
    
        fontb = {'color':  "white", 'size': 16, 'weight': 'bold', 'family': 'monospace', }
        font_c = {'color':  "white", 'size': 16, 'weight': 'bold', 'family': 'monospace', }
        
        ax.plot(vs.az,90-(round(math.degrees(vs.alt),1)),'o',markersize=15, markerfacecolor='none', markeredgecolor='#ffffff', alpha=1) 
        ax.text(vs.az,90-(round(math.degrees(vs.alt),1)), ' '+sols, verticalalignment='bottom', horizontalalignment='left', fontdict=font_c, alpha=1.0)
        
        ax.plot(vm.az,90-(round(math.degrees(vm.alt),1)),'o',markersize=15, markerfacecolor='none', markeredgecolor='#ffffff', alpha=0.3) 
        ax.text(vm.az,90-(round(math.degrees(vm.alt),1)), ' '+luns, verticalalignment='bottom', horizontalalignment='left', fontdict=font_c, alpha=1.0)
        
        ax.plot(vju.az,90-(round(math.degrees(vju.alt),1)),'o',markersize=15, markerfacecolor='none', markeredgecolor='#ffffff', alpha=0.3) 
        ax.text(vju.az,90-(round(math.degrees(vju.alt),1)), ' '+jups, verticalalignment='bottom', horizontalalignment='left', fontdict=fontb, alpha=1.0)
        
        ax.plot(vsa.az,90-(round(math.degrees(vsa.alt),1)),'o',markersize=15, markerfacecolor='none', markeredgecolor='#ffffff', alpha=0.3) 
        ax.text(vsa.az,90-(round(math.degrees(vsa.alt),1)), ' '+sats, verticalalignment='bottom', horizontalalignment='left', fontdict=fontb, alpha=1.0)
        
        ax.plot(vma.az,90-(round(math.degrees(vma.alt),1)),'o',markersize=15, markerfacecolor='none', markeredgecolor='red', alpha=0.3) 
        ax.text(vma.az,90-(round(math.degrees(vma.alt),1)), ' '+mars, verticalalignment='bottom', horizontalalignment='left', fontdict=fontb, alpha=1.0)
        
        ax.plot(vve.az,90-(round(math.degrees(vve.alt),1)),'o',markersize=15, markerfacecolor='none', markeredgecolor='#ffffff', alpha=0.3) 
        ax.text(vve.az,90-(round(math.degrees(vve.alt),1)), ' '+vens, verticalalignment='bottom', horizontalalignment='left', fontdict=fontb, alpha=1.0)
        
        
        for i,line in enumerate(dataz):
            #print(i)
            plane_dict = line.split(',')
            flight=str(plane_dict[1].strip())
            if flight == '':
        	    flight = str(plane_dict[0].strip())
            if is_int_try(str(plane_dict[4].strip())):
        	    meters=int(str(plane_dict[4].strip()))
            elif is_float_try(str(plane_dict[4].strip())):
        	    meters=int(float(str(plane_dict[4].strip())))
            else:
        	    ## TODO
        	    meters=10000
        	
            distance=float(plane_dict[5].strip())
            
            if is_int_try(str(plane_dict[11].strip())):
                track=float(360-(270-int(str(plane_dict[11].strip()))))
            else:
        	    track = 0
            azi=np.radians(float(plane_dict[6].strip()))
            aaz=float(plane_dict[6].strip())
            elev=90-float(plane_dict[7].strip())
            elunc=90-float(plane_dict[7].strip())
            #kolorek=str(plane_dict[pentry][8])
            kolorek='#ff0000'
            dziewiec=str(plane_dict[9].strip())
            dwana=str(plane_dict[12].strip())
            pos_age = int(float(str(plane_dict[29].strip())))
            if pos_age > 30:
        	    alpha_age = 0.1
            elif pos_age > 20:
        	    alpha_age = 0.2
            elif pos_age > 15:
        	    alpha_age = 0.3
            elif pos_age > 10:
        	    alpha_age = 0.4
            else:
        	    alpha_age = 0.6
        	
            ##################### to bylo aktywne
            loSep = -20
            hiSep = 20
            #if not plane_dict[22].strip() == '':
            if is_float_try(str(plane_dict[20].strip())):
        	    dist2mo1 = str(plane_dict[19].strip())
        	    deg_missed1 = float(str(plane_dict[20].strip()))
        	    if (loSep < float(deg_missed1) < hiSep):
        	        moon_s='' #sun
        	        #moon_s=dist2mo1+'km '+sols+' '+str(deg_missed1)+deg+' \n '
        	    else:
        	        #moon_s='X n/a \n'
        	        moon_s=''
        	    #dist2mo+' o '+str(deg_missed)+deg+' \n '
            else:
        	    deg_missed1 = ''
        	    #moon_s= 'X -- \n'
        	    moon_s= ''
        		
            if is_float_try(str(plane_dict[24].strip())):	
                #if not plane_dict[26].strip() == '':
        	    dist2mo2 = str(plane_dict[23].strip())
        	    deg_missed2 = float(str(plane_dict[24].strip()))
        	    if (loSep < float(deg_missed2) < hiSep):
        	        #if 
        	        # sun_s='' ##moon
        	        sun_s=dist2mo2+'km '+luns+' '+str(deg_missed2)+deg+' \n '
        	    else:
        	    	#moon_s='X n/a \n'
        	    	sun_s=''
        	    	#dist2mo+' o '+str(deg_missed)+deg+' \n '
            else:
        	    deg_missed2 = ''
        	    #sun_s= 'X -- \n'
        	    sun_s= ''
        
            if aaz >= 0 and aaz < 90:
        	    vert_al=str('top') ; hori_al=str('left')
            elif aaz >= 90 and aaz < 180:
        	    vert_al=str('bottom') ; hori_al=str('left')
            elif aaz >= 180 and aaz < 270:
        	    vert_al=str('bottom') ; hori_al=str('right')
            elif aaz >= 270:
        	    vert_al=str('top') ; hori_al=str('right')
        
            fonta = {'color':  "white", 'size': 12, 'weight': 'normal', 'family': 'monospace', }
            fontb = {'color':  "white", 'size': 12, 'weight': 'bold', 'family': 'monospace', }
            #fonta['color'] = 'kupa'
            #print fonta    
        
            if meters < 5000:
        	    #fonta['color'] = '#ff9900' ; fonta['size'] = '12' 
        	    fonta['color'] = 'white' ; fonta['size'] = '12' 
        	    fontb['color'] = '#ff9900' ; fonta['size'] = '12'
            elif (dwana == 'WARNING' and dziewiec != "RECEDING") and (meters >= 5000):
        	    #fonta['color'] = '#ff0000' 
        	    fonta['color'] ='white' 
        	    fontb['color'] = '#ff0000'
            elif (dwana == 'WARNING' and dziewiec == "RECEDING") and (meters >= 5000):
        	    #fonta['color'] = '#660000' 
        	    fonta['color'] ='white' 
        	    fontb['color'] = '#660000'
            elif (dwana != 'WARNING' and dziewiec == "RECEDING") and (meters >= 5000):
        	    #fonta['color'] = '#8000ff' 
        	    fonta['color'] ='white' 
        	    fontb['color'] = '#8000ff'
            else: 
        	    #fonta['color'] = '#ff00ff' 
        	    fonta['color'] ='white' 
        	    fontb['color'] = '#ff00ff' 
            
            #moon_s='aaa'
            if meters < 5000:
        	    fonta['size'] = '12' 
        	    fonta['size'] = '12'
        	    ax.plot(azi,elunc,'o',markersize=15, markerfacecolor='none', markeredgecolor=fontb['color'], alpha=1.0) 
        	    ax.text(azi,elunc, '    ---', verticalalignment='center', horizontalalignment='center',rotation=track,fontdict=fontb, alpha=1.0)
        	    ax.text(azi,elunc, ' \n '+str(flight)+' \n '+str(meters)+'m'+' \n '+str(distance)+'km \n '+moon_s+sun_s, verticalalignment=vert_al, horizontalalignment=hori_al, fontdict=fonta, alpha=alpha_age)
            elif (distance > 60) and (meters >= 5000):
        	    fonta['size'] = '10' 
        	    fonta['size'] = '10'
        	    ax.plot(azi,elunc,'o',markersize=15, markerfacecolor='none', markeredgecolor=fontb['color'], alpha=1.0) 
        	    ax.text(azi,elunc, '    ---', verticalalignment='center', horizontalalignment='center', rotation=track,fontdict=fontb, alpha=1.0)
        	    ax.text(azi,elunc, '  \n '+str(flight)+' \n '+str(distance)+'km \n '+moon_s+sun_s, verticalalignment=vert_al, horizontalalignment=hori_al, fontdict=fonta, alpha=alpha_age)
            elif (distance <= 60) and distance > 40 and (meters >= 5000):
        	    fonta['size'] = '10' 
        	    fonta['size'] = '10'
        	    ax.plot(azi,elunc,'o',markersize=15, markerfacecolor='none', markeredgecolor=fontb['color'], alpha=1.0) 
        	    ax.text(azi,elunc, '    ---', verticalalignment='center', horizontalalignment='center', rotation=track,fontdict=fontb, alpha=1.0)
        	    ax.text(azi,elunc, '  \n '+str(flight)+' \n '+str(distance)+'km \n '+moon_s+sun_s, verticalalignment=vert_al, horizontalalignment=hori_al, fontdict=fonta, alpha=alpha_age)
            elif (distance <= 40) and distance > 20 and (meters >= 5000):
        	    fonta['size'] = '11' 
        	    fonta['size'] = '11'
        	    ax.plot(azi,elunc,'o',markersize=15, markerfacecolor='none', markeredgecolor=fontb['color'], alpha=1.0) 
        	    ax.text(azi,elunc, '    ---', verticalalignment='center', horizontalalignment='center', rotation=track,fontdict=fontb, alpha=1.0)
        	    ax.text(azi,elunc, '  \n '+str(flight)+' \n '+str(meters)+'m'+' \n '+str(distance)+'km \n '+moon_s+sun_s, verticalalignment=vert_al, horizontalalignment=hori_al, fontdict=fonta, alpha=alpha_age)
            elif (distance <= 20) and (meters >= 5000):
        	    fonta['size'] = '11' 
        	    fonta['size'] = '11'
        	    ax.plot(azi,elunc,'o',markersize=15, markerfacecolor='none', markeredgecolor=fontb['color'], alpha=1.0) 
        	    ax.text(azi,elunc, '    ---', verticalalignment='center', horizontalalignment='center', rotation=track,fontdict=fontb, alpha=1.0)
        	    ax.text(azi,elunc, '  \n '+str(flight)+' \n '+str(meters)+'m'+' \n '+str(distance)+'km \n '+moon_s+sun_s, verticalalignment=vert_al, horizontalalignment=hori_al, fontdict=fonta, alpha=alpha_age)
            else:
                fonta['size'] = '12' 
                fonta['size'] = '12'
                ax.plot(azi,elunc,'o',markersize=15, markerfacecolor='none', markeredgecolor=fontb['color'], alpha=1.0) 
                ax.text(azi,elunc, '    ---', verticalalignment='center', horizontalalignment='center', rotation=track,fontdict=fontb, alpha=1.0)
                ax.text(azi,elunc, '  \n '+str(flight)+' \n '+str(meters)+'m'+' \n  '+str(distance)+'km \n '+moon_s+sun_s, verticalalignment=vert_al, horizontalalignment=hori_al, fontdict=fonta, alpha=alpha_age)
        
            azis	= []
            elevis	= []
            alphis      = []
            #azis.append(azi)
            #elevis.append(elev)
            ############################## tranzyty
            if is_float_try(str(deg_missed1)):
                if (loSep < float(deg_missed1) < hiSep):
                    fut_alt = str(plane_dict[22].strip())
                    fut_az  =float( str(plane_dict[21].strip()))
        	    #print fut_az, fut_alt
                    if not fut_az == 0:
            	        object1 = str(plane_dict[27].strip())
            	        if not object1  == '':
                            if object1 == 'Moon':
                                v1 = ephem.Moon(gatech)
                            elif object1 == 'Sun':
                                v1 = ephem.Sun(gatech)
                            elif object1 == 'Mars':
                                v1 = ephem.Mars(gatech)
                            elif object1 == 'Jupiter':
                                v1 = ephem.Jupiter(gatech)
                            elif object1 == 'Saturn':
                                v1 = ephem.Saturn(gatech)
                            else:
                                v1 = ephem.star(object1)
                                v1.compute(gatech)
                    	    
                            tst_x=[v1.az, math.radians(float(fut_az)), azi]
                            tst_y=[90-(round(math.degrees(v1.alt),1)), 90-float(fut_alt), elunc]
            	    #ax.plot(tst_x,tst_y,'--',markersize=10, color='white', lw=1,alpha=0.1) #sun

            if is_float_try(str(deg_missed2)):
                if (loSep < float(deg_missed2) < hiSep):
                    fut_alt = str(plane_dict[26].strip())
                    fut_az  =float( str(plane_dict[25].strip()))
        	    #print fut_az, fut_alt
                    if not fut_az == 0:
                        object2 = str(plane_dict[28].strip())
                        if not object2  == '':
                            if object2 == 'Moon':
                                v2 = ephem.Moon(gatech)
                            elif object2 == 'Sun':
                                v2 = ephem.Sun(gatech)
                            elif object2 == 'Mars':
                                v2 = ephem.Mars(gatech)
                            elif object2 == 'Jupiter':
                                v2 = ephem.Jupiter(gatech)
                            elif object2 == 'Saturn':
                                v2 = ephem.Saturn(gatech)
                            else:
                                v2 = ephem.star(object2)
                                v2.compute(gatech)
                        tst_x=[v2.az, math.radians(float(fut_az)), azi]
                        tst_y=[90-(round(math.degrees(v2.alt),1)), 90-float(fut_alt), elunc]
                        ax.plot(tst_x,tst_y,'--',markersize=10, color='white', lw=1,alpha=0.6)
            	    
            
            tmp_i = 0
            
            if not plane_dict[15].strip() == '':
                words1 = plane_dict[15]
                words2 = plane_dict[16]
                plane_pos1 = words1.split(';')
                plane_pos2 = words2.split(';')
                plane_pos_len = len(plane_pos1)	
                for a,word in enumerate(plane_pos1):
        	        if not plane_pos1[a].strip() == '':
        	            aaz1a=np.radians(float(plane_pos1[a].strip()))
        	            ele1a=90-float(plane_pos2[a].strip())
        	            azis.append(aaz1a)
        	            elevis.append(ele1a)		
        		
        	            if ((plane_pos_len-1) > a > 0):
        	                #    #alpha_hist = 0.6
        	                #else:
        	                #alpha_hist = round(float(1.0/float(i/5.0)),2)
        	                alpha_hist = round(1/float(plane_pos_len/float(a)),2)
        	                # za duży koszt czasu
        	                #ax.plot((azis[a-1],azis[a]),(elevis[a-1], elevis[a]),'-',markersize=10, color=fontb['color'], lw=1, alpha=(alpha_hist))
        		
        	            else:
        	                alpha_hist = 1
        	            alphis.append(alpha_hist)
        	            tmp_i = a
                ax.plot((azis[0:tmp_i+1]),(elevis[0:tmp_i+1]),'-',markersize=10, color=fontb['color'], lw=1, alpha=0.6)
            
        ax.set_theta_zero_location('N', offset=0.0)
        #ax.set_theta_direction(-1)
        
        #ax.set_theta_zero_location('N', offset=-354.0)
        #ax.set_theta_zero_location('N', offset=176.8)
        
        ax.set_rlim(0,90)	
        #ax.set_rticks([0, 15, 30, 45, 60, 75, 90])
        #ax.set_yticklabels(ax.get_yticks()[::-1])
        #ax.spines['polar'].set_visible(False) #wyłącza zewn krawedz
        ax.spines['polar'].set_color('red')
        ax.spines['polar'].set_visible(True) #wyłącza zewn krawedz
        #ax.axes.set_frame_on(True)
        ax.tick_params(axis='x', which='both', labelsize=10, labelcolor='white',color='none', direction='out')
        ax.set_yticklabels([])
        #ax.grid(True)
        ax.grid(False)
        
        
        plt.subplots_adjust(left=0.03, bottom=0.03, right=0.97, top=0.97)
        
        
        s, (width, height) = canvas.print_to_buffer()
        foreground = Image.frombytes("RGBA", (width, height), s)#,alpha=1)
        imagCropHD.paste(foreground, (0, 0), foreground)        
        #opencvImageHD = cv2.cvtColor(np.array(imagCropHD), cv2.COLOR_RGB2BGR)
        imagCropHD.save('/tmp/dummy_tmp.jpg')
        #cv2.imwrite('/home/pi/dummy/'+dataczas+'.jpg', opencvImageHD, [int(cv2.IMWRITE_JPEG_QUALITY), 90]) 
        #cv2.imwrite('/tmp/dummy_tmp.jpg', opencvImageHD, [int(cv2.IMWRITE_JPEG_QUALITY), 90]) 
        
        #src = '/home/pi/dummy/'+dataczas+'.jpg'
        src = '/tmp/dummy_tmp.jpg'
        #dst = '/var/www/html/tmp/last_asr.jpg'
        dst = '/tmp/last_asr.jpg'
        #dst_tmp = '/tmp/last_asr_tmp.jpg'
        shutil.copy(src, dst)
        #symlink_force(dst_tmp, dst)
    else:
    	print("else ?")
    end = time.time()
    tookt=end - start
    print (dataczas, str(tookt)+'s' ,datetime.datetime.now())

    #with open(dirdata+'/_ASR_DUMMY.A0','a') as tsttxt:
    #	tsttxt.write('/home/pi/work/arch/AS/_Dummy/'+dataczas+'.jpg\n')
    time.sleep(5)
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    