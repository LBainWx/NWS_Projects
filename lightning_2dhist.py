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

#Event date  mmddyyyy
event_date = '04222020'

#where do you want to center this data
county_name = 'Lamar'

#map center coords
m_lat = 33.408680
m_lon = -95.85897


#m_lat = 33.408680   #Centered near Roxton on 04222020
#m_lon = -95.85897  #Centered near Roxton

#Read in and sort filtered lightning data created from slice_lightning.py
print("Reading in filtered total lightning data for "+str(event_date)+"")
raw_ltg_df = pd.read_csv('C:/Users/Lamont/FWD/Research/lightning/txt/'+str(event_date)+'/filter_ltg.csv')


print("Reading in time bin data")
time_bin = pd.read_csv('C:/Users/Lamont/FWD/Research/lightning/txt/'+str(event_date)+'/time_binv2.csv')

#convert raw_ltg_df.date and time_bin.date_time to python datetime
raw_ltg_df.date = pd.to_datetime(raw_ltg_df.date, format="%Y-%m-%d %H:%M:%S.%f")
raw_ltg_df.date = raw_ltg_df.date.astype('datetime64[s]')

time_bin.date_time = pd.to_datetime(time_bin.date_time, format="%Y-%m-%d %H:%M:%S.%f")
time_bin.date_time = time_bin.date_time.astype('datetime64[s]')




########PLOT THE LIGHTNING DATA ON A MAP########
#GIS Data for plotting
print("Reading in GIS Shapefile Data")
county_fp = (r'C:\Users\Lamont\FWD\TorClimo\gis\input\shp\counties\uscounties.shp')
county_mp_df = gpd.read_file(county_fp)

cwa_name = 'FWD'
cwa_mp = (county_mp_df[county_mp_df['CWA'] == cwa_name])
county_mp = (cwa_mp[cwa_mp['COUNTYNAME'] == county_name])
t_zone  = (county_mp_df[county_mp_df['TIME_ZONE'] == 'C'])


#print("Combine Lightning Data")
#ltg_coords = (list(zip(raw_ltg_df.lon, raw_ltg_df.lat)))


#only interested in lightning data within a certain time frame
for i in range(0, len(time_bin)):
#for i in range(0, 2):
    ltg_start = time_bin.iloc[i][0].to_pydatetime()
    ltg_end   = ltg_start+pd.Timedelta(minutes=2)
    raw_ltg_df2 = (raw_ltg_df.where(np.logical_and(raw_ltg_df.date >= ltg_start, 
    raw_ltg_df.date < ltg_end))).dropna(how='all')
    
    
    print("Creating 2D Histogram for time bin "+str(ltg_start.strftime('%H%M'))+"Z to "+str(ltg_end.strftime('%H%M'))+"Z")
    ltg_coords = (list(zip(raw_ltg_df2.lon, raw_ltg_df2.lat)))

    pnts = []
    for i in range(0, len(ltg_coords)):
        pnts.append(Point(ltg_coords[i]))
    strikes = GeoDataFrame(raw_ltg_df2, geometry=pnts)

    strikes.crs = {'init' :'epsg:4326'} #Define a projection
    cwa_mp.crs = {'init' :'epsg:4326'}
    t_zone.crs = {'init' :'epsg:4326'}


    proj4_txt = '+proj=aeqd +lat_0='+str(m_lat)+' +lon_0='+str(m_lon)+' +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=km +no_defs'      
    cwa_mp2       = cwa_mp.geometry.to_crs(proj4_txt) 
    t_zone2       = t_zone.geometry.to_crs(proj4_txt) 
    strikes2      = strikes.geometry.to_crs(proj4_txt)

    plt.clf()
    fig, ax, = plt.subplots(facecolor='white', figsize=(40,40), edgecolor='black',  constrained_layout=True)
    t_zone2.plot(ax=ax, color='white', linewidth=5, edgecolor='#1E1E1E')
     
    x1 = []
    y1 = []

    for pp in strikes2.geometry: #if you only want to show points inside the range ring of the storm
        x1.append(pp.x)
        y1.append(pp.y)

    x = (np.array(x1))
    y = (np.array(y1))



    #Set up a grid and determine the size
    g_param = 5 #kilometers
    grid_size =  g_param
    h = g_param      


    scale=100

    minx =-(scale)
    maxx = scale

    miny = -(scale)
    maxy = scale


    #This will create the grid
    x_grid = np.arange(minx-h, maxx+h, grid_size)
    y_grid = np.arange(miny-h, maxy+h, grid_size)
    xx, yy = np.meshgrid(x_grid, y_grid)


    plt.plot(xx, yy, marker='.', color='black', markersize= 5, linestyle='none', alpha=0.2)
    plt.hist2d(x, y, bins=(xx[0]), cmap='plasma', cmin=1, vmin=5, vmax=85., alpha=0.5)
    strikes2.plot(ax=ax, marker='o', color='red', markersize=9)

    cb = plt.colorbar(orientation="vertical", pad=0.03, shrink=.6)
    cb.set_label('Gridded Total Lightning Data (Flashes / $\mathregular{km^2}$)  \n \n', rotation=270, labelpad=75, size='65')
    cb.ax.tick_params(labelsize=65, which='major')
    cb.ax.yaxis.set_ticks_position('left')
    ax.axis('off')

    plt.suptitle('\n \n Gridded Total Lightning Data for '+str(ltg_start.strftime('%m/%d/%Y'))+' | Time : '+str(ltg_start.strftime('%H:%M'))+'Z to '+str(ltg_end.strftime('%H:%M'))+'Z \n Total Lightning Flash: '+(str(len(raw_ltg_df2)))+'', size='65', fontweight='bold', y=1.05)

    plt.savefig('C:/Users/Lamont/FWD/Research/lightning/plots/'+str(event_date)+'/maps/histogram/'+str(ltg_start.strftime('%m%d%Y'))+'_'+str(ltg_start.strftime('%H%M'))+'Z.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=.05)
    ltg_start = []
    ltg_end = []
    raw_ltg_df2 = []

    plt.close()

print("End of Program")