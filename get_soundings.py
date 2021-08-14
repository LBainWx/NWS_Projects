# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 17:19:44 2019
Modified M. Stalley's 100F RAOB codode
to retrieve sounding data for aviation studies 
@author: Lamont
"""

import numpy as np
from bs4 import BeautifulSoup
import urllib3
from urllib.request import urlopen
import datetime
import os
import csv
import pandas as pd

#date_str = []
#from get_dates_4_raobs import date_str, z_time

#date_str = date_df
date_str = '20040225'
z_time = '00'
year =  date_str[0:4]
mn = date_str[4:6]
dy = date_str[-2:]
#print(date_str)

#Fetch the sounding data
print('Fetching sounding data for FWD for '+str(date_str)+' at '+str(z_time)+'Z')
url12='http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR=' + year + '&MONTH=' + mn + '&FROM=' + dy + ''+str(z_time)+'&TO=' + dy + ''+str(z_time)+'&STNM=72249'
print(url12)
sndpg12 = urlopen(url12)
soup12 = BeautifulSoup(sndpg12, features='lxml')
txt12 = (soup12.findAll(text=True))
raob_txt = txt12[7] # hope it always number 75


if (len(raob_txt)) > 1500:

    txt_lines = []
    sounding_header = (raob_txt.splitlines()[2]).split()
    for line in raob_txt.splitlines()[6:]:
        txt_lines.append(line.split())
    
    
    #Will have to iterate over each individual element
    pres = []
    hgt  = []
    temp = []
    dewp   = []
    mixr = []
    drct = []
    sknt = []
    thet = []
    thea = []
    thev = []
    
    
    for i in range(0, len(txt_lines)):
        pres.append(txt_lines[i][0])
        hgt.append(txt_lines[i][1])
        if float(txt_lines[i][2]) == '':
            temp.append(np.nan)
        else:
            temp.append(txt_lines[i][2])
        
        if float(txt_lines[i][3]) == '':
            dewp.append(np.nan)
        else:
            dewp.append(txt_lines[i][3])
        
        #print(txt_lines[i][5])
        if float(txt_lines[i][5]) == ' ':
            mixr.append(np.nan)
        else:
            mixr.append(txt_lines[i][5])
        
        if float(txt_lines[i][6]) > 360:
            #print("Missing Data")
            drct.append(np.nan)
        else:
            drct.append(txt_lines[i][6])
        #print(txt_lines[i][7])
        if float(txt_lines[i][7]) > 500:
                sknt.append(np.nan)
        else:
            sknt.append(txt_lines[i][7])
        #thet.append(txt_lines[i][7])
        #thea.append(txt_lines[i][8])
        #thev.append(txt_lines[i][9])
        
        
        
    
    #raob = pd.Series(txt_lines)
    
    raob_df = pd.DataFrame(pres, columns=['pressure'])
    raob_df['height'] = hgt
    raob_df['temperature'] = temp
    raob_df['dewpoint'] = dewp
    raob_df['mixing_ratio'] = mixr
    raob_df['speed'] = sknt
    raob_df['direction'] = drct 
    
    #print('Creaing Sounding Output file for '+str(date_str)+str(z_time)+'Z')
    raob_df.to_csv('C:/Users/Lamont/FWD/Aviation/climo/fog/raob/txt/'+str(date_str)+str(z_time)+'Z.csv', index=None)
    print('Creating Sounding file for '+str(date_str)+str(z_time)+'Z')
    #print(url12)
    exec(open("C:/Users/Lamont/FWD/Aviation/climo/code/mk_raob.py").read())
    
else:
    print('Sounding Data may be missing for ' +str(date_str)+str(z_time)+'Z')    
    #Output the sounding data
    
    
    
    #raob_txt = ((soup12.find_all('pre')[0]).get_text())
    #file12 = open(dir + '\SND\\SND_' + date + '_12.txt','w')
    #file12.write(txt12)
    #file12.close()
    #print 'Sounding data acquired for', date, 'at 12z'
    #elif int(year) >= Ystart and int(year) <= Yend:
    #print 'Found sounding data for', date, 'at 12z'