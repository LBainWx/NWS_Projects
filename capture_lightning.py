# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 11:17:53 2020
Modified on Tue Jun 30 and renamed to capture_lightning.py
Will make histogram and KDE plots of lightning data
The goal is to create something similar to lightning density plots in AWIPS
for research purposes
@author: Lamont
"""
import sys
import geopandas as gpd


from geopandas import GeoSeries, GeoDataFrame
from shapely.geometry import Point, LineString, Polygon
import shapely.geometry as geom
from mpl_toolkits.axes_grid1 import make_axes_locatable


import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors
import matplotlib.image as image
from matplotlib.colors import LogNorm #this is just a test
from numpy.random import multivariate_normal #this is just a test


from PIL import Image, ImageDraw, ImageFont
from PIL import Image

import scipy
from scipy.stats import kde

from datetime import datetime
from datetime import timedelta
import datetime

matplotlib.colors.PowerNorm
matplotlib.axes.Axes.hist2d
matplotlib.pyplot.hist2d

import warnings
warnings.filterwarnings("ignore") #since some of this stuff is deprecated


#Event date  mmddyyyy
event_date = '04222020'

#Sort lightning data from ENTLN archive file using Pandas
print("Reading and sorting total lightning data for "+str(event_date)+"")

#col_names = ['ftype', 'date', 'lat', 'lon', 'current']   #only need to do this if column names are not defined
raw_ltg_df = pd.read_csv('C:/Users/Lamont/FWD/Research/lightning/input/'+str(event_date)+'/lightning.csv')


#rename columns in the file
raw_ltg_df.rename(columns={'flashType':'ftype', 'latitude':'lat', 'longitude':'lon', 'peakcurrent':'current', 'time':'date'}, inplace=True)

#sensitivity studies if the number of sensors column is available
raw_ltg_df =  raw_ltg_df[raw_ltg_df.numbersensors >=6]

#Split things into IC Flash and CG Flash
print("Splitting Lightning Data into CG and IC Flashes")
cgstrokes = raw_ltg_df[raw_ltg_df.ftype != 1]
icstrokes = raw_ltg_df[raw_ltg_df.ftype == 1]


#get rid of any messy white space in the date
raw_ltg_df.date = (raw_ltg_df.date.str.lstrip()).str.replace(" ","")
cgstrokes.date = (cgstrokes.date.str.lstrip()).str.replace(" ","")
icstrokes.date = (icstrokes.date.str.lstrip()).str.replace(" ","")


#Convert data to datetime
print("Converting to Python Date time")

raw_ltg_df.date = pd.to_datetime(raw_ltg_df.date, format="%Y-%m-%dT%H:%M:%S.%f")
raw_ltg_df.date = raw_ltg_df.date.astype('datetime64[s]')

cgstrokes.date = pd.to_datetime(cgstrokes.date, format="%Y-%m-%dT%H:%M:%S.%f")
cgstrokes.date = cgstrokes.date.astype('datetime64[s]')

icstrokes.date = pd.to_datetime(icstrokes.date, format="%Y-%m-%dT%H:%M:%S.%f")
icstrokes.date = icstrokes.date.astype('datetime64[s]')


#Makes it a series that can be resampled
raw_ltg_df_v2 = pd.Series(range(len(raw_ltg_df.date)), index=raw_ltg_df.date)
cgstrokes_v2 = pd.Series(range(len(cgstrokes.date)), index=cgstrokes.date)
icstrokes_v2 = pd.Series(range(len(icstrokes.date)), index=icstrokes.date)





########PLOT THE LIGHTNING DATA ON A MAP########
#GIS Data for plotting
print("Reading in GIS Shapefile Data")
county_fp = (r'C:\Users\Lamont\FWD\TorClimo\gis\input\shp\counties\uscounties.shp')
county_mp_df = gpd.read_file(county_fp)

cwa_name = 'FWD'
county_name = 'Lamar'
cwa_mp = (county_mp_df[county_mp_df['CWA'] == cwa_name])
county_mp = (cwa_mp[cwa_mp['COUNTYNAME'] == county_name])


#If I wanted to plot cities/other GIS data
#city_label = pd.read_csv('C:/Users/Lamont/FWD/TorClimo/txt/cwa/FWD_Cities.csv')
#city_label = city_label.dropna(how='any')
#city = city_label.iloc[np.where(city_label['County'] == str(county_name))]


#Plot lightning data
ltg_coords = (list(zip(raw_ltg_df.lon, raw_ltg_df.lat)))
            
pnts = []
for i in range(0, len(ltg_coords)):
    pnts.append(Point(ltg_coords[i]))
strikes = GeoDataFrame(raw_ltg_df, geometry=pnts)
strikes.crs = {'init' :'epsg:4326'} #Need to define a projection so I can convert it later
cwa_mp.crs = {'init' :'epsg:4326'}


#For storm tracking...this is manual and subjective

loc = pd.read_csv('C:/Users/Lamont/FWD/Research/lightning/input/'+str(event_date)+'/lamar_tor.csv')
storm_loc = pd.DataFrame(data=loc)
storm_loc_pt = gpd.GeoDataFrame(storm_loc, geometry=gpd.points_from_xy(storm_loc.lon, storm_loc.lat))
storm_loc_pt.crs = {'init' :'epsg:4326'}


#lat =32.77    #Centered on Dallas for October 2019 event
#lon =-96.78   #Centered on Dallas for October 2019 event

lat = 33.615326   #Centered on Bells for 04222020 event
lon = -96.415596  #Centered on Bells for 04222020 event

proj4_txt = '+proj=aeqd +lat_0='+str(lat)+' +lon_0='+str(lon)+' +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs'      
cwa_mp2       = cwa_mp.geometry.to_crs(proj4_txt) 
strikes2      = strikes.geometry.to_crs(proj4_txt)
storm_loc_pt2 = storm_loc_pt.geometry.to_crs(proj4_txt) 

plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(40,40), edgecolor='black')


storm_ring = gpd.GeoDataFrame(geometry=storm_loc_pt2.buffer(storm_loc_pt.rad_m))
strikes3 = gpd.GeoDataFrame(strikes, geometry=strikes2)                  
cwa_mp2.plot(ax=ax, color='#A9A9A9', linewidth=5, edgecolor='#1E1E1E')
#strikes2.plot(ax =ax, color='red', alpha=0.3, markersize=4)
storm_loc_pt2.plot(ax=ax, facecolors='none', markersize=10) 


#lightning inside the polygon/circle
pointsinside = gpd.sjoin(strikes3, storm_ring, how="inner")
#filter_ltg = pointsinside[pointsinside.date.dt.hour < 4] #testing to see data within a time window
filter_ltg = pointsinside
filter_ltg.plot(ax=ax, marker='o', color='green', markersize=10)
      

county_mp2 = county_mp.geometry.to_crs(proj4_txt) 
minx, miny, maxx, maxy = county_mp2.total_bounds
scale_factor = 90000
ax.set_xlim(minx-scale_factor, maxx+scale_factor)
ax.set_ylim(miny-scale_factor, maxy+scale_factor)

#Experimenting with some map scaling...need to figure this out
#ax.set_xlim(minx-1.50, maxx+1.50)
#ax.set_ylim(miny-1.50, maxy+1.50)

print("Creating Total Lightning Plot")
ax.text(.5,.9, 'Total Lightning Flashes'  
,fontweight='bold', fontsize='55', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round')
,horizontalalignment='center', transform=ax.transAxes)
#ax.axis('off')
plt.xticks(fontsize='25', fontweight='bold')
plt.yticks(fontsize='25', fontweight='bold')

plt.savefig('C:/Users/Lamont/FWD/Research/lightning/plots/'+str(event_date)+'/maps/without_rings.png', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=1.25)
storm_ring.plot(ax=ax, facecolor='none', linewidth=5, edgecolor='black', )   
plt.savefig('C:/Users/Lamont/FWD/Research/lightning/plots/'+str(event_date)+'/maps/with_rings.png', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=1.25)

plt.close()


x1 = []
y1 = []

for pp in strikes2:
    x1.append(pp.x)
    y1.append(pp.y)

x = (np.array(x1))
y = (np.array(y1))


#This will just create a 2-D Histogram of the lightning data (all lightning data)
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(40,40), edgecolor='black')
cwa_mp2.plot(ax=ax, color='#A9A9A9', linewidth=5, edgecolor='#1E1E1E', alpha=0.25)
plt.hist2d(x, y, bins=(100,50), cmap=plt.cm.jet, alpha=0.5) #norm=mcolors.PowerNorm(0.3) for power law
strikes2.plot(ax =ax, color='black', markersize=0.15)
county_mp2 = county_mp.geometry.to_crs(proj4_txt) 
minx, miny, maxx, maxy = (strikes2.total_bounds)
scale_factor = 10000
ax.set_xlim(minx-scale_factor, maxx+scale_factor)
ax.set_ylim(miny-scale_factor, maxy+scale_factor)
ax.axis('off')

cb = plt.colorbar(orientation="horizontal", pad=0.15)
cb.ax.tick_params(labelsize=65, which='major')

print("Creating 2-D Histogram Plot")
plt.savefig('C:/Users/Lamont/FWD/Research/lightning/plots/'+str(event_date)+'/maps/histogram.png', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=1.25)
plt.close()

#This will create KDE plots 
nbins = 50
k = kde.gaussian_kde([x,y])
xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
zi = k(np.vstack([xi.flatten(), yi.flatten()]))


plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(40,40), edgecolor='black')

cwa_mp2.plot(ax=ax, color='#A9A9A9', linewidth=5, edgecolor='#1E1E1E', alpha=0.75)
plt.pcolormesh(xi, yi, zi.reshape(xi.shape), cmap=plt.cm.jet, alpha=0.5)
cb = plt.colorbar(orientation="horizontal", pad=0.15)
cb.ax.tick_params(labelsize=65, which='major')

#Map things/bounds
county_mp2 = county_mp.geometry.to_crs(proj4_txt) 
minx, miny, maxx, maxy = (strikes2.total_bounds)
scale_factor = 10000
ax.set_xlim(minx-scale_factor, maxx+scale_factor)
ax.set_ylim(miny-scale_factor, maxy+scale_factor)
ax.axis('off')

#cbar = plt.colorbar()
#cbar.ax.set_ylabel('Counts')

print("Creating KDE Plot")
plt.savefig('C:/Users/Lamont/FWD/Research/lightning/plots/'+str(event_date)+'/maps/kde.png', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=1.25)
plt.close()



#Let's only count the lightning data that is within the range rings 
#based off of storm positions...we will refer to this as filter_data

filter_cgstrokes = filter_ltg[filter_ltg.ftype != 1]
filter_icstrokes = filter_ltg[filter_ltg.ftype == 1]


filter_ltg_v2 = pd.Series(range(len(filter_ltg.date)), index=filter_ltg.date)
filter_cgstrokes_v2 = pd.Series(range(len(filter_cgstrokes.date)), index=filter_cgstrokes.date)
filter_icstrokes_v2 = pd.Series(range(len(filter_icstrokes.date)), index=filter_icstrokes.date)



#This actually bins the data
delta_t = '1min'
print("Binning the data into "+str(delta_t)+" increments")
tltg_bin = filter_ltg_v2.resample(str(delta_t)).count()
cg_bin   = filter_cgstrokes_v2.resample(str(delta_t)).count()
ic_bin   = filter_icstrokes_v2.resample(str(delta_t)).count()


#Calculate some moving means from the binned data
tltg_df = pd.DataFrame(tltg_bin.values, columns=['Count'])


tltg_df_mm = tltg_df.rolling(11).mean() #look at previous 10 minutes in (number+1)
tltg_df_mm = tltg_df_mm['Count'].fillna(0)
tltg_df_mm = tltg_df_mm.round(2)


#Plot time rate of change of the moving mean
t_roc_tltg = tltg_df_mm.diff().fillna(0)

#PLOT THE LIGHTNING DATA ON A CHART

#Convert time that is a series into a string
str_time = np.datetime_as_string(tltg_bin.index.values, unit='m')

#Because I cannot find a function that simply returns the time from the datetime string
str_time_hhmm = []
for i in range(0, len(str_time)):
    str_time_hhmm.append(str_time[i][str_time[i].find("T")+1:])


#Will plot the data on a chart and give the apperance of a histogram

fig = plt.gcf()   
plt.clf()
fig.set_size_inches(20.5, 10.5)
ax = plt.axes()
ax.grid()


#ax2 = ax1.twinx() #trying to plot on dual axis
ax.bar(range(len(tltg_bin.values)), tltg_bin.values, color='maroon', label = 'Total Lightning Flash Counts')
ax.bar(range(len(ic_bin.values)), ic_bin.values, color='red', label = 'IC Lightning Flash Counts' )

#ax2 = ax.twinx()
ax.bar(range(len(cg_bin.values)), cg_bin.values, color='salmon', label = 'CG Lightning Flash Counts')

ax.plot(range(len(tltg_df_mm.values)),tltg_df_mm.values, lw = 3.0, color='black', label='Total Lightning Flash 10 min moving mean')  
ax.plot(range(len(t_roc_tltg.values)),t_roc_tltg.values, lw = 3.0, color='blue', label='Rate of Change of 10 min TLF moving mean') 


ax.legend(loc='upper center', ncol=3, prop = {'size': 18})

plt.xticks(range(len(str_time_hhmm)), (str_time_hhmm), rotation='90', size='7', fontweight='bold')
#plt.ylim(0, tltg_bin.values.max()+75.0)
plt.ylim(t_roc_tltg.values.min()-15.0, tltg_bin.values.max()+100.0)
plt.autoscale(enable=True, axis='x', tight='yes')


plt.xlabel('Time (UTC)', size='20', fontweight='bold')
plt.ylabel(''+str(delta_t)+' binned lightning flash counts', size='20',  fontweight='bold')


plt.savefig(('C:/Users/Lamont/FWD/Research/lightning/plots/'+str(event_date)+'/charts/'+str(delta_t)+'.jpg'), format = 'jpg', dpi=400, bbox_inches='tight')    
plt.close()
print("Created and Saved time series of lightning data")


#Reset the index and rename the columns

tltg_bin_df = pd.DataFrame(tltg_bin)
tltg_bin_df = tltg_bin_df.reset_index()
mm_df = pd.DataFrame(tltg_df_mm)

#add in the moving mean
tltg_bin_df = pd.concat([tltg_bin_df, mm_df], axis=1)

tltg_bin_df.rename(columns={'date':'Date', 0:'# of Total Lightning Flashes [Bin]', 'Count':'Moving Mean'}, inplace=True) 


cg_bin_df = pd.DataFrame(cg_bin)
cg_bin_df = cg_bin_df.reset_index()
cg_bin_df.rename(columns={'date':'Date', 0:'# of CG Lightning Flashes [Bin]'}, inplace=True)

ic_bin_df = pd.DataFrame(ic_bin)
ic_bin_df = ic_bin_df.reset_index()
ic_bin_df.rename(columns={'date':'Date', 0:'# of IC Lightning Flashes [Bin]'}, inplace=True)

#Export the tabular data into an csv file
print("Exporting "+str(delta_t)+" Binned Total Lightning Data to a CSV")
tltg_bin_df.to_csv('C:/Users/Lamont/FWD/Research/lightning/txt/'+str(event_date)+'/'+str(delta_t)+'_total_lightning.csv', index=False)

print("Exporting "+str(delta_t)+" Binned Cloud-to-Ground Lightning Data to a CSV")
cg_bin_df.to_csv('C:/Users/Lamont/FWD/Research/lightning/txt/'+str(event_date)+'/'+str(delta_t)+'_cg_lightning.csv', index=False)

print("Exporting "+str(delta_t)+" Binned Incloud Lightning Data to a CSV")
ic_bin_df.to_csv('C:/Users/Lamont/FWD/Research/lightning/txt/'+str(event_date)+'/'+str(delta_t)+'_ic_lightning.csv', index=False)

