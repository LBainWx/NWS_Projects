# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 23:18:59 2019

@author: Lamont
"""
import pandas as pd
import numpy as np

from datetime import datetime
from datetime import timedelta
import re
import sys

#Read in the downloaded METARs from IAState Repository
site = "DFW"
#fields = ['station', 'valid',  'sknt', 'drct', 'gust', 'mslp', 'wxcodes', 'peak_wind_gust', 'peak_wind_gust_mph', 'peak_wind_drct', 'peak_wind_time']
metar_df = pd.read_csv('C:/Users/Lamont/FWD/Aviation/climo/metars/merged_metars/kdfw/merged_dfw_metars_v2.csv',delimiter=',', )

metar_df['rmk_index'] = metar_df['ob'].str.find("RMK")

rmk= []
for i in range(0, len(metar_df['ob'])):
    rmk.append(metar_df['ob'].iloc[i][metar_df['rmk_index'].iloc[i]:])

metar_df['rmk'] = pd.Series(rmk)

#for i in range(0, len(metar_df)):
#    metar_df['rmk'] = (metar_df['ob'].iloc[i][metar_df['rmk_index'].iloc[i]:])
    #metar_df['RMK'] = metar_df['ob'].iloc[i][(metar_df['ob'].str.find("RMK")):]
    #metar_df['rmk'] = (metar_df['ob'].iloc[i][metar_df['ob'].iloc[i].find("RMK"):])

    
#Retrieve Observations for Hourly Temperature and Dewpoint    
t_group = re.compile("(T0).*|(T1).*")
hourly_temp = []
hourly_dpt = []
for i in range(0, len(metar_df['rmk'])):
    if len([m.group(0) for l in metar_df['rmk'].iloc[i].split(" ") for m in [t_group.search(l)] if m]) == 1:
        if int(([m.group(0) for l in metar_df['rmk'].iloc[i].split(" ") for m in [t_group.search(l)] if m][0][1])) == 0: #Temperatures above 0 Celsius
                hourly_temp.append(float([m.group(0) for l in metar_df['rmk'].iloc[i].split(" ") for m in [t_group.search(l)] if m][0][2:5])/10.)
        if int(([m.group(0) for l in metar_df['rmk'].iloc[i].split(" ") for m in [t_group.search(l)] if m][0][1])) == 1:  #Temperatures below 0 Celsius
                hourly_temp.append(-1.*float([m.group(0) for l in metar_df['rmk'].iloc[i].split(" ") for m in [t_group.search(l)] if m][0][2:5])/10.)
    else:
        hourly_temp.append(np.nan) #temperature and dewpoint data is missing
            

for i in range(0, len(metar_df['rmk'])):
    if len(([m.group(0) for l in metar_df['rmk'].iloc[i].split(" ") for m in [t_group.search(l)] if m])) == 1 and (len([m.group(0) for l in metar_df['rmk'].iloc[i].split(" ") for m in [t_group.search(l)] if m][0][0:9])) >=9: 
        #print((([m.group(0) for l in metar_df['rmk'].iloc[i].split(" ") for m in [t_group.search(l)] if m])))     
        #print(metar_df['rmk'].iloc[i])      
        if int(([m.group(0) for l in metar_df['rmk'].iloc[i].split(" ") for m in [t_group.search(l)] if m][0][5])) == 0: #Dewpoint above 0 Celsius
            hourly_dpt.append(float([m.group(0) for l in metar_df['rmk'].iloc[i].split(" ") for m in [t_group.search(l)] if m][0][6:9])/10.)
            #print(([m.group(0) for l in metar_df['rmk'].iloc[i].split(" ") for m in [t_group.search(l)] if m][0][0:9]))
            #print(((float([m.group(0) for l in metar_df['rmk'].iloc[i].split(" ") for m in [t_group.search(l)] if m][0][6:9])/10.)))
        if int(([m.group(0) for l in metar_df['rmk'].iloc[i].split(" ") for m in [t_group.search(l)] if m][0][5])) == 1: #Dewpoint below Celsius
            hourly_dpt.append(-1*float([m.group(0) for l in metar_df['rmk'].iloc[i].split(" ") for m in [t_group.search(l)] if m][0][6:9])/10.)
            #print(([m.group(0) for l in metar_df['rmk'].iloc[i].split(" ") for m in [t_group.search(l)] if m][0][5]))
            #print((-1*float([m.group(0) for l in metar_df['rmk'].iloc[i].split(" ") for m in [t_group.search(l)] if m][0][6:9])/10.))
    else:
        hourly_dpt.append(np.nan)



metar_df['t_houlry'] = pd.Series(hourly_temp)
metar_df['td_hourly'] = pd.Series(hourly_dpt)

del metar_df['rmk_index']
del metar_df['rmk']

#Need to prase out visibility
vis_group = re.compile(".*10SM.*|.*9SM.*|.*8SM.*|.*7SM.*|.*6SM.*|.*5SM*|.*4SM.*|.*3SM.*|.*2 1/2SM.*|.*2SM.*|.*3/4SM.*|.*1 1/2SM.*|.*1 1/4SM.*|.*1SM.*|.*1 3/4SM.*|.*1/2SM.*|.*1/4SM.*|.*M1/4SM.*|.*1/8SM.*|.*0SM.*|.*1/16SM.*")


vsby = []
for i in range(0, len(metar_df)):
    if metar_df['ob'].iloc[i].find("SM") != -1:
        
        if '2 1/2SM' in metar_df['ob'].iloc[i]:
            vsby.append(2.5)
        elif '1 3/4SM' in metar_df['ob'].iloc[i]:
            vsby.append(1.75)
        elif '1 1/2SM' in metar_df['ob'].iloc[i]:
            vsby.append(1.5)
        elif '1 1/4SM' in metar_df['ob'].iloc[i]:
            vsby.append(1.25)
        elif '3/4SM' in metar_df['ob'].iloc[i]:
            vsby.append(0.75)
        elif '1/2SM' in metar_df['ob'].iloc[i]:
            vsby.append(0.50)
        elif '1/4SM' in metar_df['ob'].iloc[i]:
            vsby.append(0.25)
        elif 'M1/4SM' in metar_df['ob'].iloc[i]:
            vsby.append(0.25)
        elif '1/8SM' in metar_df['ob'].iloc[i]:
            vsby.append(0.125)
        elif '1/16SM' in metar_df['ob'].iloc[i]:
            vsby.append(0.625)
        else:        
            vsby.append(float((([m.group(0) for l in metar_df['ob'].iloc[i].split(" ") for m in [vis_group.search(l)] if m][0])).rstrip("SM")))
    else:
        vsby.append(np.nan)


        
metar_df['vsby'] = vsby

metar_df.to_csv('C:/Users/Lamont/FWD/Aviation/climo/metars/misc/obs4dan_v2.csv', index=None)

wx = re.compile("|.*TSRA.*|.*RA.*|.*SN.*")
metar_df = metar_df.iloc[np.where(metar_df['ob'].str.contains('TS') != True)]
metar_df = metar_df.iloc[np.where(metar_df['ob'].str.contains('RA') != True)]
metar_df = metar_df.iloc[np.where(metar_df['ob'].str.contains('SN') != True)]

metar_df = metar_df.iloc[np.where(metar_df['vsby'] <= 3.0)]
metar_df.to_csv('C:/Users/Lamont/FWD/Aviation/climo/fog/dfw_fog_events_v2.csv', index=None)
#metar_df = metar_df.iloc[np.where(metar_df['ob'].str.contains('RA') != True)]

