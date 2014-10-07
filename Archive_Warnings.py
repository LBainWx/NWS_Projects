from mpl_toolkits.basemap import Basemap
import shapefile
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import urllib
import os
import zipfile
import glob
import sys
import numpy as np
import pylab as pl



#For use with the IEM Archived SBW Polygon Shapefiles#
sf = shapefile.Reader('C:\Users\Lamont\Desktop\Python\Warnings\wwa_201410060000_201410070000')
records = sf.records()
shapes=sf.shapes()

SVR       = []
TOR       = []
FFW       = []
FAY       = []
FLW       = []

Warn_Type = []

for i in range(0, len(records)):
    Warn_Type.append(records[i][5])

for i in range(0, len(records)):
    if records[i][5] == 'SV':        #Severe Thunderstorm Warnings
        warn_att = records[i][5]
        SVR.append(warn_att)
    elif records[i][5] == 'TO':      #Tornado Warnings
        warn_att = records[i][5]
        TOR.append(warn_att)
    elif records[i][5] == 'FF':       #Flash Flood Warnings
        warn_att = records[i][5]
        FFW.append(warn_att)
    elif records[i][5] == 'FA':       #Areal Flood Advisory
        warn_att = records[i][5]
        FAY.append(warn_att)
    elif records[i][5] == 'FL':       #Flood Advisory
        warn_att = records[i][5]
        FLW.append(warn_att)


#Find the index of each event#
SVR_event = [x for x, y in enumerate(Warn_Type) if y == 'SV']
TOR_event = [x for x, y in enumerate(Warn_Type) if y == 'TO']
FFW_event = [x for x, y in enumerate(Warn_Type) if y == 'FF']
FAY_event = [x for x, y in enumerate(Warn_Type) if y == 'FA']
FLW_event = [x for x, y in enumerate(Warn_Type) if y == 'FL']




#Need to loop over and return the lon, lat for the various events
SVR_points = []
for i in range(0, len(SVR_event)):
    SVR_points.append(shapes[SVR_event[i]].points)

FFW_points = []
for i in range(0, len(FFW_event)):
    FFW_points.append(shapes[FFW_event[i]].points)
    
FAY_points = []
for i in range(0, len(FAY_event)):
    FAY_points.append(shapes[FAY_event[i]].points)

#Dummy Arrays for Lat Lons of various Warning products
SVR_lat = []
SVR_lon = []

TOR_lat = []
TOR_lon = []

FFW_lat = []
FFW_lon = []

FAY_lat = []
FAY_lon = []

FLW_lat = []
FLW_lon = []



#Need the map here in order to use map function below
map = Basemap(llcrnrlon=-124.8,llcrnrlat=24.687,urcrnrlon=-67.6,urcrnrlat=49.978,projection='mill',resolution='i') 

#Next we will plot the SVR Polygons
for i in range(0, len(SVR_points)):
    for j in range(0, len(SVR_points[i])):
        SVR_lat.append(float(SVR_points[i][j][1]))
        SVR_lon.append(float(SVR_points[i][j][0])) 
        x, y = map(SVR_lon, SVR_lat)
        map.plot(x,y,  linestyle='solid', linewidth=2.5, color='yellow')
    SVR_lat = []
    SVR_lon = []

#Flash Flood Warning Plots
for i in range(0, len(FFW_points)):
    for j in range(0, len(FFW_points[i])):
        FFW_lat.append(float(FFW_points[i][j][1]))
        FFW_lon.append(float(FFW_points[i][j][0])) 
        x, y = map(FFW_lon, FFW_lat)
        map.plot(x,y,  linestyle='solid', linewidth=2.5, color='brown')
    FFW_lat = []
    FFW_lon = []


#Areal Flood Advisory (I think)
for i in range(0, len(FAY_points)):
    for j in range(0, len(FAY_points[i])):
        FAY_lat.append(float(FAY_points[i][j][1]))
        FAY_lon.append(float(FAY_points[i][j][0])) 
        x, y = map(FAY_lon, FAY_lat)
        map.plot(x,y,  linestyle='solid', linewidth=2.5, color='teal')
    FAY_lat = []
    FAY_lon = []

map = Basemap(llcrnrlon=-124.8,llcrnrlat=24.687,urcrnrlon=-67.6,urcrnrlat=49.978,projection='mill',resolution='i') 
map.drawcoastlines(linewidth=0.75)
map.drawstates(linewidth=1, color='black')
map.drawcountries(linewidth=0.75)
map.fillcontinents(color='grey')
map.drawmapboundary(fill_color='black')

plt.show()
sys.exit()
