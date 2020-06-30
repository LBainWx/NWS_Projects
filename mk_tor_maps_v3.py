import geopandas as gpd
from geopandas import GeoSeries, GeoDataFrame
from shapely.geometry import Point, LineString, Polygon
import shapely.geometry as geom

import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import pandas as pd
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
import sys

#from scipy.misc import imread
import scipy
import matplotlib.image as image
from PIL import Image, ImageDraw, ImageFont

from PIL import Image
from pylab import *
from skimage import transform, io


import datetime
cur_date = datetime.datetime.now()
cur_day = cur_date.day
cur_mon = cur_date.month
cur_yr = cur_date.year
max_year = cur_yr

import warnings
warnings.filterwarnings("ignore")


from datetime import datetime
from datetime import timedelta
now_date = str(cur_mon)+'/'+str(cur_day)+'/'+(str(cur_yr))


#Run python script that createst all of the output files
#import new_tor_climo_v2.py


#Get shapefile information
county_fp = (r"C:\Users\Lamont\FWD\TorClimo\gis\input\shp\counties\uscounties.shp")
county_mp_df = gpd.read_file(county_fp)
cwa_name = 'FWD'
cwa_mp = (county_mp_df[county_mp_df['CWA'] == cwa_name])


#Get information from tornado rating table

rating_df = pd.read_csv('C:/Users/Lamont/FWD/TorClimo/txt/cwa/FWDRatingTable.csv')

rate_merged_df = cwa_mp.set_index('COUNTYNAME').join(rating_df.set_index('County'))
rate_merged_df['center'] = rate_merged_df['geometry'].centroid
rate_merged_df_points = rate_merged_df.copy()
rate_merged_df_points.set_geometry("center", inplace = True)

weak    = rate_merged_df['Weak']
strong  = rate_merged_df['Strong']
violent = rate_merged_df['Violent']
alltors = rate_merged_df['Weak'] + rate_merged_df['Strong'] + rate_merged_df['Violent']
rate_merged_df =pd.concat([rate_merged_df, alltors.rename('alltors')], axis=1)


ef0 = rate_merged_df['EF0']
ef1 = rate_merged_df['EF1']
ef2 = rate_merged_df['EF2']
ef3 = rate_merged_df['EF3']
ef4 = rate_merged_df['EF4']
ef5 = rate_merged_df['EF5']




monthly_df = pd.read_csv('C:/Users/Lamont/FWD/TorClimo/txt/cwa/FWDMonthlyTornadoTable.csv')
monthly_merged_df = cwa_mp.set_index('COUNTYNAME').join(monthly_df.set_index('County'))
monthly_merged_df['center'] = monthly_merged_df['geometry'].centroid
monthly_merged_df_points = monthly_merged_df.copy()
monthly_merged_df_points.set_geometry("center", inplace = True)

'''
print("Making October Tornado Heat Map")
mon_name = "October"
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(50,50))
val_texts =[]
cty_texts = []
monthly_merged_df.plot(column=monthly_merged_df['Oct'], cmap='Reds', linewidth=1, edgecolor='#1E1E1E', vmin=0, vmax=25, ax=ax)
for x, y, label in zip(monthly_merged_df_points.geometry.x, monthly_merged_df_points.geometry.y, monthly_merged_df[['Oct']].sum(axis=1)):
    val_texts.append(plt.text(x, y+.0025, label, fontsize=73, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
    
for x, y, label in zip(monthly_merged_df_points.geometry.x, monthly_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y-.095, label, fontsize=51, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
ax.axis('off')
ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n 1880-2019 '+mon_name+' Tornado Count by County\n Last Updated: ' +str(cur_yr)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/monthly/october.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)

import sys
sys.exit()
'''

print("Making Winter Tornado Heat Map")
mon_name = "December January February (3 Month Total)"
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(50,50))
val_texts =[]
cty_texts = []
monthly_merged_df.plot(column=monthly_merged_df[['Dec', 'Jan', 'Feb']].sum(axis=1), cmap='Reds', linewidth=1, edgecolor='#1E1E1E', vmin=0, vmax=25, ax=ax)
for x, y, label in zip(monthly_merged_df_points.geometry.x, monthly_merged_df_points.geometry.y, monthly_merged_df[['Dec', 'Jan', 'Feb']].sum(axis=1)):
    val_texts.append(plt.text(x, y+.0025, label, fontsize=73, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
    
for x, y, label in zip(monthly_merged_df_points.geometry.x, monthly_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y-.095, label, fontsize=51, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
ax.axis('off')


cb = plt.cm.ScalarMappable(cmap = 'Reds', norm=plt.Normalize(vmin=0, vmax=int((25))))
cb._A = []
cbar = fig.colorbar(cb, fraction=0.04, pad=-0.025, orientation='vertical')
cbar.ax.tick_params(labelsize=65, which='major')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=50, yo=10, zorder=1)

ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n 1880-'+str(cur_yr)+' '+mon_name+' Tornado Count by County\n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
print("Saved "+mon_name+" Tornado Table Map")
#plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/monthly/'+mon_name+'tornadoes.png', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=1.25)
#plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/monthly/wintertornadoes2.gif', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=1.25, quality=30)
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/monthly/wintertornadoes.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
#img = Image.open('C:/Users/Lamont/FWD/TorClimo/output/monthly/wintertornadoes3.jpg')
#img.save('C:/Users/Lamont/FWD/TorClimo/output/monthly/wintertornadoes3.gif', 'gif', optimize=True)
plt.close()



print("Making Spring Tornado Heat Map")
mon_name = "March April May (3 Month Total)"
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(50, 50))
val_texts =[]
cty_texts = []
monthly_merged_df.plot(column=monthly_merged_df[['Mar', 'Apr', 'May']].sum(axis=1), cmap='Reds', linewidth=1, edgecolor='#1E1E1E', vmin=0, vmax=70, ax=ax)
for x, y, label in zip(monthly_merged_df_points.geometry.x, monthly_merged_df_points.geometry.y, monthly_merged_df[['Mar', 'Apr', 'May']].sum(axis=1)):
    val_texts.append(plt.text(x, y+.0025, label, fontsize=73, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
    
for x, y, label in zip(monthly_merged_df_points.geometry.x, monthly_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y-.095, label, fontsize=51, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
ax.axis('off')

cb = plt.cm.ScalarMappable(cmap = 'Reds', norm=plt.Normalize(vmin=0, vmax=int((70))))
cb._A = []
cbar = fig.colorbar(cb, fraction=0.04, pad=-0.025, orientation='vertical')
cbar.ax.tick_params(labelsize=65, which='major')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=50, yo=10, zorder=1)

ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n 1880-'+str(cur_yr)+' '+mon_name+' Tornado Count by County\n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
print("Saved "+mon_name+" Tornado Table Map")
#plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/monthly/'+mon_name+'tornadoes.png', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=1.25)
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/monthly/springtornadoes.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
plt.close()



print("Making Summer Tornado Heat Map")
mon_name = "June July August (3 Month Total)"
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(50, 50))
val_texts =[]
cty_texts = []
monthly_merged_df.plot(column=monthly_merged_df[['Jun', 'Jul', 'Aug']].sum(axis=1), cmap='Reds', linewidth=1, edgecolor='#1E1E1E', vmin=0, vmax=25, ax=ax)
for x, y, label in zip(monthly_merged_df_points.geometry.x, monthly_merged_df_points.geometry.y, monthly_merged_df[['Jun', 'Jul', 'Aug']].sum(axis=1)):
    val_texts.append(plt.text(x, y+.0025, label, fontsize=73, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
    
for x, y, label in zip(monthly_merged_df_points.geometry.x, monthly_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y-.095, label, fontsize=51, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
ax.axis('off')

cb = plt.cm.ScalarMappable(cmap = 'Reds', norm=plt.Normalize(vmin=0, vmax=int((25))))
cb._A = []
cbar = fig.colorbar(cb, fraction=0.04, pad=-0.025, orientation='vertical')
cbar.ax.tick_params(labelsize=65, which='major')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=50, yo=10, zorder=1)

ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n 1880-' +str(cur_yr)+' '+mon_name+' Tornado Count by County\n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
print("Saved "+mon_name+" Tornado Table Map")
#plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/monthly/'+mon_name+'tornadoes.png', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=1.25)
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/monthly/summertornadoes.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
plt.close()


print("Making Fall Tornado Heat Map")
mon_name = "September October November (3 Month Total)"
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(50, 50))
val_texts =[]
cty_texts = []
monthly_merged_df.plot(column=monthly_merged_df[['Sep', 'Oct', 'Nov']].sum(axis=1), cmap='Reds', linewidth=1, edgecolor='#1E1E1E', vmin=0, vmax=25, ax=ax)
for x, y, label in zip(monthly_merged_df_points.geometry.x, monthly_merged_df_points.geometry.y, monthly_merged_df[['Sep', 'Oct', 'Nov']].sum(axis=1)):
    val_texts.append(plt.text(x, y+.0025, label, fontsize=73, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
    
for x, y, label in zip(monthly_merged_df_points.geometry.x, monthly_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y-.095, label, fontsize=51, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
ax.axis('off')

cb = plt.cm.ScalarMappable(cmap = 'Reds', norm=plt.Normalize(vmin=0, vmax=int((25))))
cb._A = []
cbar = fig.colorbar(cb, fraction=0.04, pad=-0.025, orientation='vertical')
cbar.ax.tick_params(labelsize=65, which='major')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=50, yo=10, zorder=1)

ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n 1880-2019 '+mon_name+' Tornado Count by County\n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
print("Saved "+mon_name+" Tornado Table Map")
#plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/monthly/'+mon_name+'tornadoes.png', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=1.25)
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/monthly/falltornadoes.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
plt.close()



#Get information from large tornado table
tornadotable_df = pd.read_csv('C:/Users/Lamont/FWD/TorClimo/txt/cwa/FWDTornadoTable.csv')
table_merged_df = cwa_mp.set_index('COUNTYNAME').join(tornadotable_df.set_index('County'))
table_merged_df['center'] = table_merged_df['geometry'].centroid
table_merged_df_points = table_merged_df.copy()
table_merged_df_points.set_geometry("center", inplace = True)


#Plotting Yearly Heat Map


print("Making Yearly Heat Map")
#for i in range(0, len(tornadotable_df.columns[1:-1])):
#    year = tornadotable_df.columns[1:][i]


year = str(2020)
#To create multiple years,indent code starting here
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(50, 50))
val_texts =[]
cty_texts = []
rate_merged_df.plot(column=table_merged_df[year], cmap='Reds', linewidth=1, edgecolor='#1E1E1E', vmin=0, vmax=10, ax=ax)
for x, y, label in zip(table_merged_df_points.geometry.x, table_merged_df_points.geometry.y, table_merged_df[year]):
    val_texts.append(plt.text(x, y+.0025, label, fontsize=73, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
    
for x, y, label in zip(table_merged_df_points.geometry.x, table_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y-.095, label, fontsize=51, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
ax.axis('off')


cb = plt.cm.ScalarMappable(cmap = 'Reds', norm=plt.Normalize(vmin=0, vmax=int((10))))
cb._A = []
cbar = fig.colorbar(cb, fraction=0.04, pad=-0.025, orientation='vertical')
cbar.ax.tick_params(labelsize=65, which='major')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=20, yo=20, zorder=1)

ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n '+year+' Tornado Count by County\n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
print("Saved "+year+" Tornado Table Map")
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/'+year+'.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
plt.close()
    #stop indent here if using multiple years



#por = map(int, (sorted(set(tornado_df['Year']))))
#year = str(por[0])+'-'+str(por[-1])+' Tornadoes'
year = "1880-2020 Tornadoes"
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(50, 50))
val_texts =[]
cty_texts = []
rate_merged_df.plot(column=table_merged_df[year], cmap='Reds', linewidth=1, edgecolor='#1E1E1E', vmin=0, ax=ax)
for x, y, label in zip(table_merged_df_points.geometry.x, table_merged_df_points.geometry.y, table_merged_df[year]):
    val_texts.append(plt.text(x, y+.0025, label, fontsize=73, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
    
for x, y, label in zip(table_merged_df_points.geometry.x, table_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y-.095, label, fontsize=51, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
ax.axis('off')
cb = plt.cm.ScalarMappable(cmap = 'Reds', norm=plt.Normalize(vmin=0, vmax=int((110))))
cb._A = []

cbar = fig.colorbar(cb, fraction=0.04, pad=-0.025, orientation='vertical')
#bound_labels = (min(table_merged_df[year]), max(table_merged_df[year]))
#cbar.set_ticklabels(bound_labels)
cbar.ax.tick_params(labelsize=65, which='major')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=20, yo=20, zorder=1)


label_year = "1880-"+str(cur_yr)+""
ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n '+str(label_year)+' Tornado Count By County \n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
print("Saved "+year+" Table Map")

plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/all_tor_count.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
#plt.savefig(r'C:\\Users\\Lamont\\FWD\\TorClimo\\img\\all_tor_count.png')
plt.close()



#Let's make a tornado track map
print("Reading CSV File to make track maps")
#tornado_df = pd.read_csv('C:/Users/Lamont/FWD/TorClimo/txt/master/FWD_tors_1950_2019_v3.csv')
tornado_df = pd.read_csv('C:/Users/Lamont/FWD/TorClimo/txt/master/FWD_tors_masterv3.csv')


#rename a column or two
tornado_df.rename(columns={'Time (CST?)':'Time_CST', 'F/EF Rating':'Rating'}, inplace=True)

#track_yr = str(2019)



#track_yr = "Pre88DEra"
tornado_df = (tornado_df.iloc[np.where(tornado_df['Year'] >= 1950)])
#tornado_df = (tornado_df.iloc[np.where(np.logical_and(tornado_df['Year'] < 1988, tornado_df['Year'] > 1950))])

start_tor_long = tornado_df['Start Long']
start_tor_lat = tornado_df['Start Lat']

end_tor_long = tornado_df['End Long']
end_tor_lat = tornado_df['End Lat']



start_tor = list(zip(start_tor_long, start_tor_lat))
end_tor   = list(zip(end_tor_long, end_tor_lat))


#tor_rating = map(float, (tornado_df['Rating']).tolist())


pnts = []
badpnts = []
for i in range(0, len((start_tor))):
    if start_tor[i] != end_tor[i]:
        pnts.append(LineString([start_tor[i], end_tor[i]]))
    if start_tor[i] == end_tor[i]: #need this for tornadoes that have the same start and end
        pnts.append(Point(start_tor[i]))



#Plot the tornado tracks
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(60, 100))
tracks = GeoDataFrame(tornado_df, geometry=pnts)

rate_merged_df.plot(ax=ax, color='#E3DAC9', edgecolor='black', linewidth=4)

(tracks.iloc[np.where(tornado_df['Rating'] == 0.)]).plot(ax=ax, color='#000000', linewidth = 8)
(tracks.iloc[np.where(tornado_df['Rating'] == 1.)]).plot(ax=ax, color='#2D658B', linewidth = 8)
(tracks.iloc[np.where(tornado_df['Rating'] == 2.)]).plot(ax=ax, color='#0C8B20', linewidth = 8)
(tracks.iloc[np.where(tornado_df['Rating'] == 3.)]).plot(ax=ax, color='#FF8000', linewidth = 8)
(tracks.iloc[np.where(tornado_df['Rating'] == 4.)]).plot(ax=ax, color='#FF001B', linewidth = 8)
(tracks.iloc[np.where(tornado_df['Rating'] == 5.)]).plot(ax=ax, color='#FF4FA7', linewidth = 8)



cty_texts = []
for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y, label, fontsize=61, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))


ax.axis('off')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=20, yo=70, zorder=1)

plt.legend((['F/EF-0','_nolegend_', 'F/EF-1','_nolegend_', 'F/EF-2', '_nolegend_', 'F/EF-3','_nolegend_', 'F/EF-4', 'F/EF-5']), edgecolor='black', fontsize='large', fancybox='true',ncol=6, loc='lower center',  prop = {'size':62})


#ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n Tornado Tracks '+str(track_yr)+' \n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n 1950-'+str(cur_yr)+' Tornado Tracks \n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
#plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/'+str(track_yr)+'tracks.png', bbox_inches='tight',facecolor=fig.get_facecolor(), pad_inches=0.5)
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/all_tors_tracks.jpg', bbox_inches='tight',facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
#print("Saved "+str(track_yr)+" Tornado Track Map")
plt.close()


#Export Track Map as a shapefile
tracks.to_file('C:/Users/Lamont/FWD/TorClimo/output/tracks.shp', driver='ESRI Shapefile')

sys.exit()

#Plot Heat Maps for #F0, #EF1, EF2, EF3, EF4, EF5
print("Making F/EF0 Tornado Heat Map")
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(50, 50))
val_texts =[]
cty_texts = []
rate_merged_df.plot(column=ef0, cmap='OrRd', linewidth=1, edgecolor='#1E1E1E', vmin=0, ax=ax)

for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, rate_merged_df['EF0']):
    val_texts.append(plt.text(x, y+.0025, label, fontsize=73, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
    
for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y-.095, label, fontsize=51, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
ax.axis('off')
cb = plt.cm.ScalarMappable(cmap = 'OrRd', norm=plt.Normalize(vmin=0, vmax=int((max(ef0)))))
cb._A = []

cbar = fig.colorbar(cb, fraction=0.04, pad=-0.025, orientation='vertical')
cbar.ax.tick_params(labelsize=65, which='major')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=50, yo=10, zorder=1)
label_year = "1880-"+str(cur_yr)+""
ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n Number of F/EF-0 Tornadoes by County '+label_year+' \n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
print("Saved Heat Map for F/EF-0 Tornadoes")
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/ef0.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
plt.close()

print("Making F/EF1 Tornado Heat Map")
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(50, 50))
val_texts =[]
cty_texts = []
rate_merged_df.plot(column=ef1, cmap='OrRd', linewidth=1, edgecolor='#1E1E1E', vmin=0, ax=ax)

for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, rate_merged_df['EF1']):
    val_texts.append(plt.text(x, y+.0025, label, fontsize=73, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
    
for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y-.095, label, fontsize=51, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
ax.axis('off')
cb = plt.cm.ScalarMappable(cmap = 'OrRd', norm=plt.Normalize(vmin=0, vmax=int((max(ef1)))))
cb._A = []

cbar = fig.colorbar(cb, fraction=0.04, pad=-0.025, orientation='vertical')
cbar.ax.tick_params(labelsize=65, which='major')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=50, yo=10, zorder=1)

ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n Number of F/EF-1 Tornadoes by County '+label_year+' \n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
print("Saved Heat Map for F/EF-1 Tornadoes")
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/ef1.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
plt.close()


print("Making F/EF2 Tornado Heat Map")
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(50, 50))
val_texts =[]
cty_texts = []
rate_merged_df.plot(column=ef2, cmap='OrRd', linewidth=1, edgecolor='#1E1E1E', vmin=0, ax=ax)

for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, rate_merged_df['EF2']):
    val_texts.append(plt.text(x, y+.0025, label, fontsize=73, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
    
for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y-.095, label, fontsize=51, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
ax.axis('off')
cb = plt.cm.ScalarMappable(cmap = 'OrRd', norm=plt.Normalize(vmin=0, vmax=int((max(ef2)))))
cb._A = []

cbar = fig.colorbar(cb, fraction=0.04, pad=-0.025, orientation='vertical')
cbar.ax.tick_params(labelsize=65, which='major')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=50, yo=10, zorder=1)

ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n Number of F/EF-2 Tornadoes by County '+label_year+' \n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
print("Saved Heat Map for F/EF-2 Tornadoes")
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/ef2.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
plt.close()


print("Making F/EF3 Tornado Heat Map")
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(50, 50))
val_texts =[]
cty_texts = []
rate_merged_df.plot(column=ef3, cmap='OrRd', linewidth=1, edgecolor='#1E1E1E', vmin=0, ax=ax)

for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, rate_merged_df['EF3']):
    val_texts.append(plt.text(x, y+.0025, label, fontsize=73, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
    
for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y-.095, label, fontsize=51, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
ax.axis('off')
cb = plt.cm.ScalarMappable(cmap = 'OrRd', norm=plt.Normalize(vmin=0, vmax=int((max(ef3)))))
cb._A = []

cbar = fig.colorbar(cb, fraction=0.04, pad=-0.025, orientation='vertical')
cbar.ax.tick_params(labelsize=65, which='major')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=50, yo=10, zorder=1)

ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n Number of F/EF-3 Tornadoes by County '+label_year+' \n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
print("Saved Heat Map for F/EF-3 Tornadoes")
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/ef3.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
plt.close()


print("Making F/EF4 Tornado Heat Map")
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(50, 50))
val_texts =[]
cty_texts = []
rate_merged_df.plot(column=ef4, cmap='OrRd', linewidth=1, edgecolor='#1E1E1E', vmin=0, vmax=8, ax=ax)

for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, rate_merged_df['EF4']):
    val_texts.append(plt.text(x, y+.0025, label, fontsize=73, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
    
for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y-.095, label, fontsize=51, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
ax.axis('off')
cb = plt.cm.ScalarMappable(cmap = 'OrRd', norm=plt.Normalize(vmin=0, vmax=int(((8)))))
cb._A = []

cbar = fig.colorbar(cb, fraction=0.04, pad=-0.025, orientation='vertical')
cbar.ax.tick_params(labelsize=65, which='major')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=50, yo=10, zorder=1)

ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n Number of F/EF-4 Tornadoes by County '+label_year+' \n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
print("Saved Heat Map for F/EF-4 Tornadoes")
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/ef4.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
plt.close()


print("Making F/EF5 Tornado Heat Map")
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(50, 50))
val_texts =[]
cty_texts = []
rate_merged_df.plot(column=ef5, cmap='OrRd', linewidth=1, edgecolor='#1E1E1E', vmin=0, vmax=5, ax=ax)

for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, rate_merged_df['EF5']):
    val_texts.append(plt.text(x, y+.0025, label, fontsize=73, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
    
for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y-.095, label, fontsize=51, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
ax.axis('off')
cb = plt.cm.ScalarMappable(cmap = 'OrRd', norm=plt.Normalize(vmin=0, vmax=int(((5)))))
cb._A = []

cbar = fig.colorbar(cb, fraction=0.04, pad=-0.025, orientation='vertical')
cbar.ax.tick_params(labelsize=65, which='major')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=50, yo=10, zorder=1)

ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n Number of F/EF-5 Tornadoes by County '+label_year+' \n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
print("Saved Heat Map for F/EF-5 Tornadoes")
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/ef5.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
plt.close()




#PLOT Weak Tornadoes
print("Making Maps for F/EF-0 and F/EF-1 Tornadoes")
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(50, 50))
val_texts =[]
cty_texts = []
rate_merged_df.plot(column=weak, cmap='OrRd', linewidth=1, edgecolor='#1E1E1E', vmin=0, ax=ax)

for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, rate_merged_df['Weak']):
    val_texts.append(plt.text(x, y+.0025, label, fontsize=73, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
    
for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y-.095, label, fontsize=51, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
ax.axis('off')
cb = plt.cm.ScalarMappable(cmap = 'OrRd', norm=plt.Normalize(vmin=0, vmax=int((max(weak)))))
cb._A = []

cbar = fig.colorbar(cb, fraction=0.04, pad=-0.025, orientation='vertical')
cbar.ax.tick_params(labelsize=65, which='major')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=50, yo=10, zorder=1)

ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n Number of F/EF-0 and F/EF-1 Tornadoes by County '+label_year+' \n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
print("Saved Heat Map for F/EF-0 and F/EF-1 Tornadoes")
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/weak.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
plt.close()

print("Making Weak Tornado Track Maps")
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(60, 100))
tracks = GeoDataFrame(tornado_df, geometry=pnts)

rate_merged_df.plot(ax=ax, color='#E3DAC9', edgecolor='black', linewidth=4)
(tracks.iloc[np.where(tornado_df['Rating'] == 0.)]).plot(ax=ax, color='#000000', linewidth = 8)
(tracks.iloc[np.where(tornado_df['Rating'] == 1.)]).plot(ax=ax, color='#2D658B', linewidth = 8)

cty_texts = []
for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y, label, fontsize=61, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))


ax.axis('off')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=20, yo=70, zorder=1)

ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n 1950-'+str(cur_yr)+' F/EF-0 and F/EF-1 Tornado Tracks \n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
plt.legend((['F/EF-0','_nolegend_', 'F/EF-1','_nolegend_', 'F/EF-2', '_nolegend_', 'F/EF-3','_nolegend_', 'F/EF-4', 'F/EF-5']), edgecolor='black', fontsize='large', fancybox='true',ncol=6, loc='lower center',  prop = {'size':62})
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/weaktracks.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
plt.close()

print("Saved Track Map for F/EF-0 and F/EF-1 Tornadoes")


#Plotting Strong Tornado Heat Map
print("Making Maps for F/EF-2 and F/EF-3 Tornadoes")
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(50, 50))
val_texts =[]
cty_texts = []
rate_merged_df.plot(column=strong, cmap='OrRd', linewidth=1, edgecolor='#1E1E1E', vmin=0, ax=ax)
for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, rate_merged_df['Strong']):
    val_texts.append(plt.text(x, y+.0025, label, fontsize=73, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
    
for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y-.095, label, fontsize=51, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
ax.axis('off')
cb = plt.cm.ScalarMappable(cmap = 'OrRd', norm=plt.Normalize(vmin=0, vmax=int((max(strong)))))
cb._A = []

cbar = fig.colorbar(cb, fraction=0.04, pad=-0.025, orientation='vertical')
cbar.ax.tick_params(labelsize=65, which='major')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=50, yo=10, zorder=1)

ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n Number of F/EF-2 and F/EF-3 Tornadoes by County '+label_year+'\n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
print("Saved Heat Map for F/EF-2 and F/EF-3 Tornadoes")
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/strong.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
plt.close()



print("Making Strong Tornado Track Maps")
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(60, 100))
tracks = GeoDataFrame(tornado_df, geometry=pnts)

rate_merged_df.plot(ax=ax, color='#E3DAC9', edgecolor='black', linewidth=4)
(tracks.iloc[np.where(tornado_df['Rating'] == 2.)]).plot(ax=ax, color='#0C8B20', linewidth = 8)
(tracks.iloc[np.where(tornado_df['Rating'] == 3.)]).plot(ax=ax, color='#FF8000', linewidth = 8)

cty_texts = []
for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y, label, fontsize=61, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))


ax.axis('off')
logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=20, yo=70, zorder=1)



#logo4 = image.imread('C:/Users/Lamont/FWD/TorClimo/img/legend.png')
#leg = scipy.misc.imresize( logo4, 0.25)
#fig.figimage(leg, xo=4000, yo=10, zorder=1)
ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n 1950-'+str(cur_yr)+' F/EF-2 and F/EF-3 Tornado Tracks \n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
plt.legend((['F/EF-2', '_nolegend_', 'F/EF-3','_nolegend_']), edgecolor='black', fontsize='large', fancybox='true',ncol=6, loc='lower center',  prop = {'size':62})
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/strongtracks.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
print("Saved Track Map for F/EF-2 and F/EF-3 Tornadoes")
plt.close()



#Make Heat map for Violent Tornadoes
print("Making Maps for F/EF-4 and F/EF-5 Tornadoes")
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(50, 50))
val_texts =[]
cty_texts = []
rate_merged_df.plot(column=violent, cmap='OrRd', linewidth=1, edgecolor='#1E1E1E', vmin=0, vmax=8, ax=ax)
for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, rate_merged_df['Violent']):
    val_texts.append(plt.text(x, y+.0025, label, fontsize=73, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
    
for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y-.095, label, fontsize=51, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))
ax.axis('off')
cb = plt.cm.ScalarMappable(cmap = 'OrRd', norm=plt.Normalize(vmin=0, vmax=int((8))))
cb._A = []

cbar = fig.colorbar(cb, fraction=0.04, pad=-0.025, orientation='vertical')
cbar.ax.tick_params(labelsize=65, which='major')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=50, yo=10, zorder=1)

ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n Number of F/EF-4 and F/EF-5 Tornadoes by County '+label_year+' \n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
print("Saved Heat Map for F/EF-4 and F/EF-5 Tornado")
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/violent.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.5, dpi=18)
plt.close()

print("Making Violent Tornado Track Maps")
plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(60, 100))
tracks = GeoDataFrame(tornado_df, geometry=pnts)

rate_merged_df.plot(ax=ax, color='#E3DAC9', edgecolor='black', linewidth=4)
(tracks.iloc[np.where(tornado_df['Rating'] == 4.)]).plot(ax=ax, color='#FF001B', linewidth = 8)
(tracks.iloc[np.where(tornado_df['Rating'] == 5.)]).plot(ax=ax, color='#FF4FA7', linewidth = 8)

cty_texts = []
for x, y, label in zip(rate_merged_df_points.geometry.x, rate_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y, label, fontsize=61, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=18, foreground="white")]))


ax.axis('off')

logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (75,200))
fig.figimage(logo, xo=20, yo=70, zorder=1)



#logo4 = image.imread('C:/Users/Lamont/FWD/TorClimo/img/legend.png')
#leg = scipy.misc.imresize( logo4, 0.25)
#fig.figimage(leg, xo=4000, yo=10, zorder=1)
ax.set_title('National Weather Service Fort Worth/Dallas Tornado Climatology \n 1950-'+str(cur_yr)+' F/EF-4 and F/EF-5 Tornado Tracks \n Last Updated: ' +str(now_date)+'',size='85', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
plt.legend((['F/EF-4', 'F/EF-5']), edgecolor='black', fontsize='large', fancybox='true',ncol=6, loc='lower center',  prop = {'size':62})
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/violenttracks.jpg', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.50, dpi=18)
plt.close()
print("Saved Track Map for F/EF-4 and F/EF-5 Tornadoes")
print("End of Program")

