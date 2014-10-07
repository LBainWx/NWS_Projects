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






#Read in ShapeFile from NWS AWIPS GIS Page#
sf = shapefile.Reader('C:\Users\Lamont\Desktop\NWS_GIS\w_03de14')
records = sf.records()
shapes  = sf.shapes()


#Read in Shapefiles from SPC (which has all U.S. counties)#
sf1   = shapefile.Reader('C:\Users\Lamont\Desktop\Python\c_05fe14')
records1  = sf1.records()
shapes1   = sf1.shapes()



#Blank Arrays for CWA

append_arr  = []
CWA_county  = []
CWAs        = []
CWA_att     = []
#Enter the CWA desired here
CWA_name = 'FWD'


for i in range(0, len(records1)):
    append_arr.append(records1[i][1])



#Return the county names in a CWA
for i in range(0, len(records1)):
    if records1[i][1] == CWA_name:
        att = records1[i][2]
        CWA_county.append(att)

county =  [x for x, y in enumerate(append_arr) if y == CWA_name]

#Create lists of CWA's to determine the index of the desired CWA
for i in range(0, len(records)):
    CWAs.append(records[i][0])
    


#Sort through records to extract the attributes
for i in range(0, len(records)):
    if records[i][1] == CWA_name:
        att = [records[i][0], records[i][1], records[i][2], records[i][3]]
        CWA_att.append(att)




county_lat = []
county_lon = []

#Call Basemap for plotting
map = Basemap(llcrnrlon=-99.76,llcrnrlat=30.27,urcrnrlon=-94.27,urcrnrlat=34.32,projection='mill',resolution='i')
shapes1_pts = []
for i in range(0, len(county)):
    shapes1_pts.append(shapes1[county[i]].points)


for i in range(0, len(shapes1_pts)):
    for j in range(0, len(shapes1_pts[i])):
        county_lat.append(shapes1_pts[i][j][1])
        county_lon.append(shapes1_pts[i][j][0])
        x, y = map(county_lon, county_lat)
        map.plot(x,y,  linestyle='solid', linewidth=0.75, color='black')
    county_lat = []
    county_lon = []
    


#Callup CWA and CWA points using indexed value
CWA_index  = (CWAs.index(CWA_att[0][0]))
CWA_points = (shapes[CWA_index].points)

lat = []
lon = []

for i in range(0, len(CWA_points)):
    lat.append(float(CWA_points[i][1]))
    lon.append(float(CWA_points[i][0]))


#For use with the IEM Archived SBW Polygon Shapefiles#
sf = shapefile.Reader('C:\Users\Lamont\Desktop\Python\Warnings\wwa_201305150000_201305160600')
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
TOR_points = []
for i in range(0, len(TOR_event)):
    TOR_points.append(shapes[TOR_event[i]].points)

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



#Next we will plot the TOR Polygons
for i in range(0, len(TOR_points)):
    for j in range(0, len(TOR_points[i])):
        TOR_lat.append(float(TOR_points[i][j][1]))
        TOR_lon.append(float(TOR_points[i][j][0])) 
        x, y = map(TOR_lon, TOR_lat)
        map.plot(x,y,  linestyle='solid', linewidth=0.8, color='red')
    TOR_lat = []
    TOR_lon = []




#Next we will plot the SVR Polygons
for i in range(0, len(SVR_points)):
    for j in range(0, len(SVR_points[i])):
        SVR_lat.append(float(SVR_points[i][j][1]))
        SVR_lon.append(float(SVR_points[i][j][0])) 
        x, y = map(SVR_lon, SVR_lat)
        map.plot(x,y,  linestyle='solid', linewidth=0.8, color='yellow')
    SVR_lat = []
    SVR_lon = []

#Flash Flood Warning Plots
for i in range(0, len(FFW_points)):
    for j in range(0, len(FFW_points[i])):
        FFW_lat.append(float(FFW_points[i][j][1]))
        FFW_lon.append(float(FFW_points[i][j][0])) 
        x, y = map(FFW_lon, FFW_lat)
        map.plot(x,y,  linestyle='solid', linewidth=0.8, color='green')
    FFW_lat = []
    FFW_lon = []


#Areal Flood Advisory (I think)
for i in range(0, len(FAY_points)):
    for j in range(0, len(FAY_points[i])):
        FAY_lat.append(float(FAY_points[i][j][1]))
        FAY_lon.append(float(FAY_points[i][j][0])) 
        x, y = map(FAY_lon, FAY_lat)
        map.plot(x,y,  linestyle='solid', linewidth=0.8, color='teal')
    FAY_lat = []
    FAY_lon = []



#Plot the CWA using the points

#This will just be a zoom for the entire CONUS
#map = Basemap(llcrnrlon=-124.8,llcrnrlat=24.687,urcrnrlon=-67.6,urcrnrlat=49.978,projection='mill',resolution='i')  
#map.drawcoastlines(linewidth=0.75)
map.drawstates(linewidth=0.2, color='black')
map.drawcountries(linewidth=0.75)
map.fillcontinents(color='grey')
map.drawmapboundary(fill_color='black')

x, y = map(lon, lat)
map.plot(x,y,  linestyle='solid', linewidth=0.75, color='black')
plt.show()
