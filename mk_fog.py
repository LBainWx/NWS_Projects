# -*- coding: utf-8 -*-
"""
This python program will cluster
obs that contain some sort of reduced visibility
"""


import pandas as pd
import numpy as np

from datetime import datetime
from datetime import timedelta

import math

import sys

import seaborn as sns

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors
import matplotlib.image as image

import warnings
warnings.filterwarnings("ignore") #since some of this stuff is deprecated

site = "DFW"

metar_df = pd.read_csv('C:/Users/Lamont/FWD/Aviation/climo/fog/input/'+str(site)+'_fog_events_v2.csv',delimiter=',', )
metar_df['datetime'] = pd.to_datetime(metar_df['datetime_v2'], format=('%m/%d/%Y %H:%M')) 
metar_df.sort_values(by=['datetime'],ascending=True, inplace=True)
metar_df.drop_duplicates(keep='first', inplace=True)

del metar_df['datetime_v2']



#This will group each xwind observations into events
fogobs = pd.DataFrame((metar_df.where(metar_df['vsby'] <= 5.)))
fogobs = fogobs[['ob', 'wspd', 'wgst', 'wdir', 'sky1', 'sky1_hgt', 'sky2', 'sky2_hgt',
       'sky3', 'sky3_hgt', 't_houlry', 'td_hourly', 'vsby', 'datetime' ]]

#Remove HZ and SN
fogobs = fogobs.iloc[np.where(fogobs['ob'].str.contains('HZ') != True)] 
fogobs = fogobs.iloc[np.where(fogobs['ob'].str.contains('DU') !=True)]    

fogobs = fogobs.iloc[np.where(fogobs['wspd'] <= 15.0)]
#fogobs = fogobs.dropna(subset=['vsby'])




#Tdiff is the amount of time allowed to elapse between successive observations before they are grouped into another event
tdiff = 7200.


obdiff = (fogobs['datetime'].diff(periods=1)).astype('timedelta64[s]')
fogobs = fogobs.assign(obdiff=obdiff.values).fillna(0)
fogobs.drop_duplicates(subset='datetime', inplace=True)


obdiff_lst = list(fogobs['obdiff'])
tmp = []
obdiffi = 0

#fogobs['obdiff'].iloc[0] = 0.0

for i in range(0, len(obdiff_lst)):
    if obdiff_lst[i] <= tdiff:
        tmp.append(int(obdiffi))
    if obdiff_lst[i] > tdiff:
        obdiffi = int(obdiffi+1)
        tmp.append(int(obdiffi))



fogobs['obtag'] = tmp

fog_list = list(set(fogobs['obtag']))


tmp_event  = []
start_list = []
end_list   = []
event_time = []



for i in range(0, len(fog_list)):
    start_list.append((fogobs['datetime'].where(fogobs['obtag'] == fog_list[i]).dropna(how='any')).iloc[0])
    end_list.append((fogobs['datetime'].where(fogobs['obtag'] == fog_list[i]).dropna(how='any')).iloc[-1])
    event_time.append((end_list[i]-start_list[i]).total_seconds()/60.)


tag_number = fogobs['obtag'].unique()


min_vsby = []
avg_vsby = []
avg_wspd = []
avg_wdir = []
percent_25 = []
percent_50 = []
percent_75 = []

w_percent_25 = []
w_percent_50 = []
w_percent_75 = []



'''
#lets set things up to compute mean winds
pi_rads = 2*(math.pi)

fogobs['wdir'] = fogobs['wdir'].replace('VRB', float(np.nan))
fogobs['wdir'] = fogobs['wdir'].replace('NOG', float(np.nan))
fogobs['wdir'] = fogobs['wdir'].convert_objects(convert_numeric=True)

u_comp = []
v_comp = []
for i in range(0, len(fogobs['wdir'])):
    if fogobs['wdir'].iloc[i] != np.nan:
        u_comp.append(-1*fogobs['wspd'].iloc[i]*math.sin(pi_rads*(fogobs['wdir'].iloc[i]/360.)))
        v_comp.append(-1*fogobs['wspd'].iloc[i]*math.cos(pi_rads*(fogobs['wdir'].iloc[i]/360.)))
    else:
        u_comp.append(np.nan)
        v_comp.append(np.nan)
        
fogobs['u'] = np.power(u_comp, 2)
fogobs['v'] = np.power(v_comp, 2)
'''



for i in range(0, len(tag_number)):
    #avg_xwind.append((np.mean((xwindobs['xwindsus'].where(xwindobs['obtag'] == tag_number[i])).dropna(how='any'))))
    avg_vsby.append((np.mean((fogobs['vsby'].where(fogobs['obtag'] == tag_number[i])).dropna(how='any'))))
    min_vsby.append(min((fogobs['vsby'].where(fogobs['obtag'] == tag_number[i])).dropna(how='any')))
    avg_wspd.append((np.mean((fogobs['wspd'].where(fogobs['obtag'] == tag_number[i])).dropna(how='any'))))
    
    
    tmp_arr25 = (math.ceil(len(fogobs.where(fogobs['obtag'] == tag_number[i]).dropna(how='any').sort_values(by='vsby'))*.25))-1
    percent_25.append((fogobs.where(fogobs['obtag'] == tag_number[i]).dropna(how='any').sort_values(by='vsby').iloc[int(tmp_arr25)]['vsby']))
    tmp_arr25 = []
    
    tmp_arr50 = (math.ceil(len(fogobs.where(fogobs['obtag'] == tag_number[i]).dropna(how='any').sort_values(by='vsby'))*.50))-1
    percent_50.append((fogobs.where(fogobs['obtag'] == tag_number[i]).dropna(how='any').sort_values(by='vsby').iloc[int(tmp_arr50)]['vsby']))
    tmp_arr50 = []
    
    tmp_arr75 = (math.ceil(len(fogobs.where(fogobs['obtag'] == tag_number[i]).dropna(how='any').sort_values(by='vsby'))*.75))-1
    percent_75.append((fogobs.where(fogobs['obtag'] == tag_number[i]).dropna(how='any').sort_values(by='vsby').iloc[int(tmp_arr75)]['vsby']))
    tmp_arr75 = []
    
    
    wtmp_arr25 = (math.ceil(len(fogobs.where(fogobs['obtag'] == tag_number[i]).dropna(how='any').sort_values(by='wspd'))*.25))-1
    w_percent_25.append((fogobs.where(fogobs['obtag'] == tag_number[i]).dropna(how='any').sort_values(by='wspd').iloc[int(wtmp_arr25)]['wspd']))
    wtmp_arr25 = []
    
    wtmp_arr50 = (math.ceil(len(fogobs.where(fogobs['obtag'] == tag_number[i]).dropna(how='any').sort_values(by='wspd'))*.50))-1
    w_percent_50.append((fogobs.where(fogobs['obtag'] == tag_number[i]).dropna(how='any').sort_values(by='wspd').iloc[int(wtmp_arr50)]['wspd']))
    wtmp_arr50 = []
    
    wtmp_arr75 = (math.ceil(len(fogobs.where(fogobs['obtag'] == tag_number[i]).dropna(how='any').sort_values(by='wspd'))*.75))-1
    w_percent_75.append((fogobs.where(fogobs['obtag'] == tag_number[i]).dropna(how='any').sort_values(by='wspd').iloc[int(wtmp_arr75)]['wspd']))
    wtmp_arr75 = []
    
    
    
    
    #percent_pos.append(math.ceil(len(fogobs.where(fogobs['obtag'] == tag_number[i]).dropna(how='any').sort_values(by='vsby'))*.25))
    #quarter_per.append((math.ceil(len(fogobs.where(fogobs['obtag'] == tag_number[i]).dropna(how='any').sort_values(by='vsby'))*.25)))
 
    #avg_wspd.append((fogobs['u'].where(fogobs['obtag'] == tag_number[i]).dropna(how='any'), 
    #                + fogobs['v'].where(fogobs['obtag'] == tag_number[i]).dropna(how='any')))
    
    #                +fogobs['v'].where(fogobs['obtag'] == tag_number[i])).dropna(how='any')))), 0.5)])
    #if ((fogobs['wdir'].where(fogobs['obtag'] == tag_number[i])).dropna(how='any')) != 'VRB':
    #avg_wdir.append((np.mean((fogobs['wdir'].where(fogobs['obtag'] == tag_number[i])).dropna(how='any'))))
        


#avg_vsby2 = round(avg_vsby, 2)

    
fogevents = pd.DataFrame()
fogevents['id'] = tag_number
fogevents['Start'] = start_list
fogevents['End'] = end_list
fogevents['Duration_min'] = event_time
fogevents['avg_vsby'] = avg_vsby
fogevents['min_vsby'] = min_vsby
fogevents['avg_wind'] = avg_wspd
fogevents['per_25'] = percent_25
fogevents['per_50'] = percent_50
fogevents['per_75'] = percent_75

fogevents['w_per_25'] = w_percent_25
fogevents['w_per_50'] = w_percent_50
fogevents['w_per_75'] = w_percent_75



#fogevents.Avg_vsby.round(1)
#fogevents.Min_vsby.round(1)
#fogevents.Avg_wind.round(1)


fogevents['avg_vsby'] = fogevents['avg_vsby'] #.round(decimals=2)
fogevents['min_vsby'] = fogevents['min_vsby'] #.round(decimals=2)
fogevents['avg_wind'] = fogevents['avg_wind'] #.round(decimals=2)


#fogevents['Avg_wdir'] = avg_wdir

#sys.exit()
fogeventsmon = fogevents['Start'].dt.month
fogeventsmon = fogeventsmon.value_counts(sort=True).sort_index()

fogeventsyear = fogevents['Start'].dt.year
fogeventsyear = fogeventsyear.value_counts(sort=True).sort_index()


fogevents = fogevents.where(fogevents['Duration_min'] >= 120.).dropna(how='any')
fogdates = fogevents['Start'].dt.strftime('%Y%m%d')
fogdates.drop_duplicates()

fogobs.to_csv('C:/Users/Lamont/FWD/Aviation/climo/fog/dfwfogobs.csv')
fogevents.to_csv('C:/Users/Lamont/FWD/Aviation/climo/fog/dfwfogevents.csv')
fogeventsmon.to_csv('C:/Users/Lamont/FWD/Aviation/climo/fog/dfwfogeventsmonth.csv')
fogdates.to_csv('C:/Users/Lamont/FWD/Aviation/climo/fog/dfwfogdates.csv', index=False)


#Make seaborn violin plots
#ax = sns.violinplot(x="wind speed", y = "visibility", data=




#I love making 2d histograms

g_param = 2 
grid_size =  g_param
h = g_param      


#scale=  #this is probably in km as well, but think of it as a zoom level
#minx =-(scale)
#maxx = scale
#miny = -(scale)
#maxy = scale

#This will create the grid
#x_grid = np.arange(minx, maxx+h, grid_size)
#y_grid = np.arange(miny, maxy+h, grid_size)
#xx, yy = np.meshgrid(x_grid, y_grid)


#df = pd.concat([fogevents['Avg_wind'], fogevents['Avg_vsby']], axis=1)
#df.hist(bins=[0, 5, 10, 15, 20, 25])
#ax = sns.scatterplot(x=fogevents['Avg_wind'], y=fogevents['Avg_vsby'])
#dbins=[0., 0.25, 0.5, 0.75, 1., 1.25, 1.5, 1.75, 2., 2.5, 3., 15.]
dbins=[0., 0.25, 0.50, 0.75, 1., 1.25, 1.5, 2.0, 2.5, 3.0]



fig = plt.gcf()   
plt.clf()
fig.set_size_inches(20.5, 10.5)
ax = plt.axes()
ax.grid()

plt.hist2d(fogevents.per_25, fogevents.avg_wind, vmin=0, cmap='plasma')
ax = sns.scatterplot(x=fogevents.per_25, y=fogevents.w_per_25, color='black')
cb = plt.colorbar(orientation="vertical", pad=0.03, shrink=1.0)
plt.tick_params(axis='both', which='major', labelsize=10)

plt.xlabel('25th Percentile Visibility', size='25', fontweight='bold')
plt.ylabel('Average Wind Speed', size='25', fontweight='bold')

plt.xlim(-0.01,3.01)
ax = plt.axes()
ax.yaxis.grid(lw=0.5, c='black', ls=':', dashes=(20, 20))
ax.xaxis.grid(lw=0.5, c='black', ls=':', dashes=(20, 20))
for axis in ['bottom','left','right']:
  ax.spines[axis].set_linewidth(3)
  ax.spines[axis].set_color('grey')
plt.savefig(('C:/Users/Lamont/FWD/Aviation/climo/fog/hist25.png'), format = 'png', dpi=400, bbox_inches='tight')    
plt.close()

fig = plt.gcf()   
plt.clf()
fig.set_size_inches(20.5, 10.5)
ax = plt.axes()
ax.grid()

plt.hist2d(fogevents.per_50, fogevents.avg_wind, vmin=0, cmap='plasma')
ax = sns.scatterplot(x=fogevents.per_50, y=fogevents.w_per_50, color='black')
cb = plt.colorbar(orientation="vertical", pad=0.03, shrink=1.0)
plt.tick_params(axis='both', which='major', labelsize=10)

plt.xlabel('50th Percentile Visibility', size='25', fontweight='bold')
plt.ylabel('Average Wind Speed', size='25', fontweight='bold')

plt.xlim(-0.01,3.01)
ax = plt.axes()
ax.yaxis.grid(lw=0.5, c='black', ls=':', dashes=(20, 20))
ax.xaxis.grid(lw=0.5, c='black', ls=':', dashes=(20, 20))
for axis in ['bottom','left','right']:
  ax.spines[axis].set_linewidth(3)
  ax.spines[axis].set_color('grey')
plt.savefig(('C:/Users/Lamont/FWD/Aviation/climo/fog/hist50.png'), format = 'png', dpi=400, bbox_inches='tight')   
 
plt.close()

fig = plt.gcf()   
plt.clf()
fig.set_size_inches(20.5, 10.5)
ax = plt.axes()
ax.grid()

plt.hist2d(fogevents.per_75, fogevents.avg_wind, vmin=0, cmap='plasma')
ax = sns.scatterplot(x=fogevents.per_75, y=fogevents.avg_wind, color='black')
cb = plt.colorbar(orientation="vertical", pad=0.03, shrink=1.0)
plt.tick_params(axis='both', which='major', labelsize=10)

plt.xlabel('75th Percentile Visibility', size='25', fontweight='bold')
plt.ylabel('Average Wind Speed', size='25', fontweight='bold')

plt.xlim(-0.01,3.01)
ax = plt.axes()
ax.yaxis.grid(lw=0.5, c='black', ls=':', dashes=(20, 20))
ax.xaxis.grid(lw=0.5, c='black', ls=':', dashes=(20, 20))
for axis in ['bottom','left','right']:
  ax.spines[axis].set_linewidth(3)
  ax.spines[axis].set_color('grey')
plt.savefig(('C:/Users/Lamont/FWD/Aviation/climo/fog/hist75.png'), format = 'png', dpi=400, bbox_inches='tight')    
plt.close()
