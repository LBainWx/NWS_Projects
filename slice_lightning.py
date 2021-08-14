'''
This program will capture lightning 
within 'x' distance of a storm 
(tracked manually). It will
then merge the lightning data and bin for calculations.

In addition, it will create output files
used to make histograms and KDE plots used in the
batch_capture_lightning_v2.py file and lightning_2dhist.py file
data by taking the position of a storm 
'''


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

import warnings
warnings.filterwarnings("ignore") #since some of this stuff is deprecated



#Event date  mmddyyyy
event_date = '08102014'

#where do you want to center this data
county_name = 'Denton'

#storm location file used for storm tracking
storm_loc_file = pd.read_csv('C:/Users/Lamont/FWD/Research/lightning/input/'+str(event_date)+'/input.csv')

#combines the date and time assigned to each radar volume in the storm location file
tmp = pd.concat([storm_loc_file.date, storm_loc_file.time], axis=1)
tmp_2f = tmp.date +' '+tmp.time

storm_loc_file = storm_loc_file.assign(start_date = tmp_2f)

#datetime conversions
t_start = (pd.to_datetime(storm_loc_file.start_date, format='%m/%d/%Y %H:%M'))

#stripping 
time_start =   t_start.iloc[0:-1]
time_end   =   t_start.iloc[1:]

#Sort lightning data from ENTLN archive file using Pandas
print("Reading and sorting total lightning data for "+str(event_date)+"")

#col_names = ['ftype', 'date', 'lat', 'lon', 'current']   #only need to do this if column names are not defined
raw_ltg_df = pd.read_csv('C:/Users/Lamont/FWD/Research/lightning/input/'+str(event_date)+'/lightning.csv')


#rename columns in the file
raw_ltg_df.rename(columns={'type':'ftype', 'latitude':'lat', 'longitude':'lon', 'peakcurrent':'current', 'timestamp':'date'}, inplace=True)

#had to change time to timesamp since ENI keeps changing their headers >:(
    #type is what is used as of 8/13
    #timestamp is what is used as of 8/13



#sensitivity studies if the number of sensors column is available
#raw_ltg_df =  raw_ltg_df[raw_ltg_df.numbersensors >=6] #not all files will have this

#del raw_ltg_df['icheight']
#del raw_ltg_df['numbersensors']
#del raw_ltg_df['multiplicity']

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
cwa_mp = (county_mp_df[county_mp_df['CWA'] == cwa_name])
county_mp = (cwa_mp[cwa_mp['COUNTYNAME'] == county_name])
t_zone  = (county_mp_df[county_mp_df['TIME_ZONE'] == 'C'])

m_lon = float(county_mp.LON)
m_lat = float(county_mp.LAT)

#Plot lightning data
print("Combine Lightning Data")
ltg_coords = (list(zip(raw_ltg_df.lon, raw_ltg_df.lat)))


            
pnts = []
for i in range(0, len(ltg_coords)):
    pnts.append(Point(ltg_coords[i]))
strikes = GeoDataFrame(raw_ltg_df, geometry=pnts)

strikes.crs = {'init' :'epsg:4326'} #Define a projection
cwa_mp.crs = {'init' :'epsg:4326'}
t_zone.crs = {'init' :'epsg:4326'}

storm_loc = pd.concat([storm_loc_file.lon, storm_loc_file.lat, storm_loc_file.rad_m], join ='outer', axis=1)

storm_loc_pt = gpd.GeoDataFrame(storm_loc, geometry=gpd.points_from_xy(storm_loc.lon, storm_loc.lat))
storm_loc_pt.crs = {'init' :'epsg:4326'}


#coorinate transformations
proj4_txt = '+proj=aeqd +lat_0='+str(m_lat)+' +lon_0='+str(m_lon)+' +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=km +no_defs'      
cwa_mp2       = cwa_mp.geometry.to_crs(proj4_txt) 
t_zone2       = t_zone.geometry.to_crs(proj4_txt) 
strikes2      = strikes.geometry.to_crs(proj4_txt)
storm_loc_pt2 = storm_loc_pt.geometry.to_crs(proj4_txt) 



print("Filtering Lightning Data")
storm_ring = gpd.GeoDataFrame(geometry=storm_loc_pt2.buffer(storm_loc_pt.rad_m/1000.))
strikes3 = gpd.GeoDataFrame(strikes, geometry=strikes2) 



#lightning inside the polygon/circle
pointsinside = gpd.sjoin(strikes3, storm_ring, how="inner")



filter_ltg = (pointsinside.where(np.logical_and(pointsinside.date >= time_start.iloc[0].to_pydatetime(), 
    pointsinside.date < time_end.iloc[-1].to_pydatetime()))).dropna(how='all')


'''
plt.clf()
fig, ax, = plt.subplots(facecolor='white', figsize=(40,40), edgecolor='black',  constrained_layout=True)
scale=100

minx =-(scale)
maxx = scale

miny = -(scale)
maxy = scale

ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)


t_zone2.plot(ax=ax, color='white', linewidth=5, edgecolor='#1E1E1E')
filter_ltg.plot(ax=ax, marker='o', color='green', markersize=10)

plt.savefig('C:/Users/Lamont/FWD/Research/lightning/plots/'+str(event_date)+'/maps/with_ringsv2.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=1.25)
'''

#Let's only count the lightning data that is within the range rings 
#based off of storm positions...we will refer to this as filter_data



filter_ltg.drop_duplicates(subset=['ftype', 'date', 'lat', 'lon', 'current'], keep='last', inplace=True)
filter_ltg.sort_values(by='date', inplace=True)




filter_cgstrokes = filter_ltg[filter_ltg.ftype != 1]
filter_icstrokes = filter_ltg[filter_ltg.ftype == 1]


filter_ltg_v2 = pd.Series(range(len(filter_ltg.date)), index=filter_ltg.date)
filter_cgstrokes_v2 = pd.Series(range(len(filter_cgstrokes.date)), index=filter_cgstrokes.date)
filter_icstrokes_v2 = pd.Series(range(len(filter_icstrokes.date)), index=filter_icstrokes.date)



#This actually bins the data
delta_t = '2min'
print("Binning the data into "+str(delta_t)+" increments")
tltg_bin = filter_ltg_v2.resample(str(delta_t)).count()
cg_bin   = filter_cgstrokes_v2.resample(str(delta_t)).count()
ic_bin   = filter_icstrokes_v2.resample(str(delta_t)).count()


#Calculate some moving means from the binned data
tltg_df = pd.DataFrame(tltg_bin.values, columns=['Count'])

mm_num = int(delta_t.strip('min'))
tltg_df_mm = tltg_df.rolling(int(str(mm_num-1))).mean() #look at previous XX minutes in (number+1)
#tltg_df_mm = tltg_df.rolling(5).mean() 
tltg_df_mm = tltg_df_mm['Count'].fillna(0)
tltg_df_mm = tltg_df_mm.round(2)


#Return the time bins to use for plotting of histogram/KDE
time_bin = pd.DataFrame(np.datetime_as_string(tltg_bin.index.values, unit='s'))
time_bin.rename(columns={0:'date_time'}, inplace=True)

time_binv2 = pd.to_datetime(time_bin.date_time, format="%Y-%m-%dT%H:%M:%S.%f")

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

ax.plot(range(len(tltg_df_mm.values)),tltg_df_mm.values, lw = 3.0, color='black', label='Total Lightning Flash '+str((int(delta_t.strip('min'))))+' min moving mean')  
ax.plot(range(len(t_roc_tltg.values)),t_roc_tltg.values, lw = 3.0, color='blue', label='Rate of Change of '+str((int(delta_t.strip('min'))))+' min Total Lightning Flash moving mean') 


ax.legend(loc='upper center', ncol=3, prop = {'size': 12})

plt.xticks(range(len(str_time_hhmm)), (str_time_hhmm), rotation='90', size='7', fontweight='bold')
#plt.ylim(0, tltg_bin.values.max()+75.0)
plt.ylim(t_roc_tltg.values.min()-5.0, tltg_bin.values.max()+10.0)
plt.autoscale(enable=True, axis='x', tight='yes')


plt.xlabel('Time (UTC)', size='20', fontweight='bold')
plt.ylabel(''+str(delta_t)+' binned lightning flash counts', size='20',  fontweight='bold')

plt.title(str(event_date)+' Lightning Trends', loc='center', fontsize=50)
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

print("Exporting "+str(delta_t)+" Bin Times CSV")
time_binv2.to_csv('C:/Users/Lamont/FWD/Research/lightning/txt/'+str(event_date)+'/timebin2min.csv', index=False)


print("Exporting Filtered Lightning Data CSV")
filter_ltg.to_csv('C:/Users/Lamont/FWD/Research/lightning/txt/'+str(event_date)+'/filter_ltg.csv', index=False)