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



sf = shapefile.Reader('C:\Users\Lamont\Desktop\NWS_GIS\w_03de14')
records = sf.records()
shapes=sf.shapes()


#Blank Arrays for CWA
CWA_att = []
CWAs    = []

#Enter the CWA desired here
CWA_name = 'EWX'

#records[i][0] == STATE
#records[i][1] == CWA
#records[i][2] = COUNTY


#Create lists of CWA's to determine the index of the desired CWA
for i in range(0, len(records)):
    CWAs.append(records[i][0])
    


#Sort through records to extract the attributes
for i in range(0, len(records)):
    if records[i][1] == CWA_name:
        att = [records[i][0], records[i][1], records[i][2], records[i][3]]
        CWA_att.append(att)


#Callup CWA and CWA points using indexed value
CWA_index  = (CWAs.index(CWA_att[0][0]))
CWA_points = (shapes[CWA_index].points)

lat = []
lon = []

for i in range(0, len(CWA_points)):
    lat.append(float(CWA_points[i][1]))
    lon.append(float(CWA_points[i][0]))




#Plot the CWA using the points

#This will just be a zoom for the entire CONUS
map = Basemap(llcrnrlon=-124.8,llcrnrlat=24.687,urcrnrlon=-67.6,urcrnrlat=49.978,projection='mill',resolution='i')  
map.drawcoastlines(linewidth=0.75)
map.drawstates(linewidth=1, color='black')
map.drawcountries(linewidth=0.75)
map.fillcontinents(color='grey')
map.drawmapboundary(fill_color='black')

#Map coordinate transformation 
x, y = map(lon, lat)
map.plot(x,y,  linestyle='solid', linewidth=1.0, color='black')
plt.show()
