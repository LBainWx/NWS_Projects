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

import scipy
import imread
import matplotlib.image as image
from PIL import Image, ImageDraw, ImageFont

from pylab import *
from skimage import transform, io

import datetime
cur_date = datetime.datetime.now()
cur_day = cur_date.day
cur_mon = cur_date.month
cur_yr = cur_date.year
max_year = cur_yr

from datetime import datetime
from datetime import timedelta
now_date = str(cur_mon)+'/'+str(cur_day)+'/'+(str(cur_yr))


#Get shapefile information
county_fp = (r'C:\Users\Lamont\FWD\TorClimo\gis\input\shp\counties\uscounties.shp')
county_mp_df = gpd.read_file(county_fp)
cwa_name = 'FWD'
county_name = 'Mills'
print("Creating", county_name, "County tornado bar plots, map and text files")

cwa_mp = (county_mp_df[county_mp_df['CWA'] == cwa_name])
county_mp = (cwa_mp[cwa_mp['COUNTYNAME'] == county_name])

#Read in CSV file...I made this one by hand, but I'm sure one could leverage AWIPS cities/WarnGen LOC shapefiles
city_label = pd.read_csv('C:/Users/Lamont/FWD/TorClimo/txt/cwa/FWD_Cities.csv')
city_label = city_label.dropna(how='any')

city = city_label.iloc[np.where(city_label['County'] == str(county_name))]

#Read in created tornado rating by county table
rating_df = pd.read_csv('C:/Users/Lamont/FWD/TorClimo/txt/cwa/FWDRatingTable.csv')
rate_merged_df = cwa_mp.set_index('COUNTYNAME').join(rating_df.set_index('County'))
rate_merged_df['center'] = rate_merged_df['geometry'].centroid
rate_merged_df_points = rate_merged_df.copy()
rate_merged_df_points.set_geometry("center", inplace = True)


tornado_df = pd.read_csv('C:/Users/Lamont/FWD/TorClimo/txt/master/FWD_tors_masterv3.csv')
tornado_df.rename(columns={'Time (CST?)':'Time_CST', 'F/EF Rating':'Rating'}, inplace=True)

#Try to sort tornadoes by Year, Month and Date. Think this will play nicely with excel
tornado_df = tornado_df.sort_values(by=['Year', 'Month', 'Day'])

#find the max and min years in the whole tornado climatology
min_year = tornado_df['Year'].min()
max_year = tornado_df['Year'].max()


#Reads through master tornado database excel file and parses out tornado information for given county
county_df = tornado_df.iloc[np.where(tornado_df['County'] == str(county_name))] 

#NUMBER OF TORNADOES BY FUJITA/ENHANCED FUJITA RATING
print("Begin tornadoes sorted by Fujita/Enhanced Fujita rating plot for "+county_name+" County")
plt.clf()
fig = plt.gcf()
fig.set_size_inches(70,35)

ax = plt.axes()
ax.yaxis.grid(lw=2.0, c='grey', ls='-')
for axis in ['top','bottom','left','right']:
   ax.spines[axis].set_linewidth(5)
   ax.spines[axis].set_color('black')

ax.yaxis.grid(lw=2, c='black', ls=':', dashes=(20, 20))
ax.xaxis.grid(lw=2, c='black', ls=':', dashes=(20, 20))


ef0 = (county_df.iloc[np.where(county_df['Rating'] == 0)])
ef1 = (county_df.iloc[np.where(county_df['Rating'] == 1)])
ef2 = (county_df.iloc[np.where(county_df['Rating'] == 2)])
ef3 = (county_df.iloc[np.where(county_df['Rating'] == 3)])
ef4 = (county_df.iloc[np.where(county_df['Rating'] == 4)])
ef5 = (county_df.iloc[np.where(county_df['Rating'] == 5)])


cat = [0,1,2, 3, 4, 5]
cat_name = ['(F/EF0)','(F/EF1)','(F/EF2)','(F/EF3)','(F/EF4)','(F/EF5)']
num_rate_cat = [len(ef0), len(ef1), len(ef2), len(ef3), len(ef4), len(ef5)]
plt.xticks(cat, cat_name, size='65',  fontweight='bold', zorder=(100))
plt.bar(cat, num_rate_cat, align='center', color='red', zorder=(3),  edgecolor='black', lw=10)

plt.xticks(cat, cat_name, size='65',  fontweight='bold', zorder=100)
plt.xticks(size='65', fontweight='bold')
plt.yticks(size='65', fontweight='bold')
plt.xlim(-0.5,5.5)
plt.ylim(0,max(num_rate_cat)+5)

plt.yticks(np.arange(0., max(num_rate_cat)+12., 5), size='65', fontweight='bold')
plt.xlabel('Fujita/Enhanced Fujita Scale', size='65',  fontweight='bold')
plt.ylabel('Number of Tornadoes \n', size='65', fontweight='bold')
plt.legend(('Number of Tornadoes',), loc='upper right', prop={'size':65})
plt.suptitle('Number of Tornadoes by Rating for '+str(county_name)+' County \n Data: '+str(min_year)+'-'+str(max_year)+' || Tornado Total: '+str(sum(num_rate_cat))+'\n NWS Fort Worth, TX || Last Updated: ' +str(now_date)+'', size='65', fontweight='bold', y=0.99) 

#Plot the tornado count above the bar plot
for i in range(len(num_rate_cat)):
   if (num_rate_cat[i]) > 0:
       plt.annotate(str(num_rate_cat[i]), xy=(cat[i],num_rate_cat[i]+0.3), size='70',  ha='center', fontweight='bold')
       
       
logo2 = io.imread(r'C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (100,250))
fig.figimage(logo, xo =725 , yo = 350, zorder=1)       

plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/'+str(county_name).lower().replace(" ","")+'/'+str(county_name).replace(" ","")+'_TOR_Rating.jpg', bbox_inches='tight', dpi=18)
print("Tornado Fujita Rating Plot for "+county_name+" County created")



#NUMBER OF TORNADOES BY INTENSITY (WEAK...STRONG...VIOLENT)
print("Begin tornadoes sorted by Intensity (Weak, Strong, Violent) plot for "+county_name+" County")
Weak_TOR    = (county_df.iloc[np.where(np.logical_or(county_df['Rating'] == 0, county_df['Rating'] == 1))])
Strong_TOR  = (county_df.iloc[np.where(np.logical_or(county_df['Rating'] == 2, county_df['Rating'] == 3))])
Violent_TOR = (county_df.iloc[np.where(np.logical_or(county_df['Rating'] == 4, county_df['Rating'] == 5))])



plt.clf()
fig = plt.gcf()
fig.set_size_inches(70,35)
ax = plt.axes()
ax.yaxis.grid(lw=2.0, c='grey', ls='-')
for axis in ['top','bottom','left','right']:
   ax.spines[axis].set_linewidth(5)
   ax.spines[axis].set_color('black')
plt.xlim(-0.5,2.5)
ax.yaxis.grid(lw=2, c='black', ls=':', dashes=(20, 20))
ax.xaxis.grid(lw=2, c='black', ls=':', dashes=(20, 20))
cat = [0,1,2]
cat_name = ['Weak \n (F/EF0-F/EF1)', 'Strong \n (F/EF2-F/EF3) \n', 'Violent \n (F/EF4-F/EF5)']
num_rate_cat = [len(Weak_TOR), len(Strong_TOR), len(Violent_TOR)]
plt.xticks(cat, cat_name, size='65',  fontweight='bold')
plt.yticks(np.arange(0., max(num_rate_cat)+12., 5), size='65', fontweight='bold')
plt.bar(cat, num_rate_cat, align='center', color='red', zorder=3, edgecolor='black', lw=10)
plt.ylim(0,max(num_rate_cat)+10)

plt.ylabel('Number of Tornadoes \n', size='65',  fontweight='bold')
plt.legend(('Number of Tornadoes',), loc='upper right', prop={'size':65})
plt.xlabel('Tornado Intensity', size='65',  fontweight='bold')
plt.suptitle('Number of Tornadoes by Intensity for '+str(county_name)+' County \n Data: '+str(min_year)+'-'+str(max_year)+' || Tornado Total: '+str(sum(num_rate_cat))+'\n NWS Fort Worth, TX || Last Updated: ' +str(now_date)+'', size='65', fontweight='bold', y=0.99)


for i in range(len(num_rate_cat)):
   if num_rate_cat[i] > 0:
       plt.annotate(str(num_rate_cat[i]), xy=(cat[i] ,num_rate_cat[i]+0.5), size='70',  ha='center', fontweight='bold')


logo2 = io.imread(r'C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (100,250))
fig.figimage(logo, xo = 725 , yo = 350, zorder=1) 

plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/'+str(county_name).lower().replace(" ","")+'/'+str(county_name).replace(" ","")+'_TOR_Intensity.jpg', bbox_inches='tight', dpi=18)
plt.close()
print("Tornadoes sorted by intensity plot for "+county_name+" County created")



#NUMBER OF TORNADOES TIME OF DAY
print("Begin tornadoes sorted by time of day plot for "+county_name+" County")
#combine date and time strings to format into Python datetime
newdate = county_df.Date +' '+ county_df.Time_CST  

#combined date time will be the actual date time that Python uses
combine_dt = pd.to_datetime(newdate, format= "%m/%d/%Y %H:%M")

#creates a header name for new combined datetime column
combine_dt = combine_dt.to_frame('newdatetime')


#Include combine_dt back into county_df series
county_df = pd.concat([county_df, combine_dt], axis=1)


#create a list of times (using 24 hour clock)
#note that times are in CST
time_arr = np.arange(24)
tor_times = []
tmp = county_df.newdatetime.dt.hour.values
for i in range(0, 24):
   tor_times.append(county_df[county_df.newdatetime.dt.hour == i].shape[0])


plt.clf()
fig = plt.gcf()
fig.set_size_inches(70,35)


ax = plt.axes()
for axis in ['top','bottom','left','right']:
   ax.spines[axis].set_linewidth(5)
   ax.spines[axis].set_color('black')
plt.xticks(time_arr, rotation=45, size=65, fontweight='bold', color='black')
ax.yaxis.grid(lw=2, c='black', ls=':', dashes=(20, 20))
ax.xaxis.grid(lw=2, c='black', ls=':', dashes=(20, 20))
plt.bar(time_arr, tor_times, align='center', label = "Tornadoes", color='red', edgecolor='black', lw=10, zorder=3)
plt.xlabel(' Time (Local Standard Time)', size='65', fontweight='bold', color='black')
plt.ylabel('Number of Tornadoes \n', size='65', fontweight='bold', color='black')
plt.yticks(np.arange(0., max(tor_times)+12., 5), size='65', fontweight='bold')
plt.xlim(-0.5, 23.5)
plt.legend(('Number of Tornadoes',), loc='upper right', prop={'size':65})
plt.suptitle('Number of Tornadoes by Time of Day for '+str(county_name)+' County \n Data: '+str(min_year)+'-'+str(max_year)+' || Tornado Total: '+str(sum(tor_times))+'\n NWS Fort Worth, TX || Last Updated: ' +str(now_date)+'', size='65', fontweight='bold', y=0.99)

for i in range(len(time_arr)):
   if tor_times[i] > 0:
    plt.annotate(str(tor_times[i]), xy=(int(time_arr[i]),(tor_times[i])+.3), size='70',  ha='center', fontweight='bold')
       
logo2 = io.imread(r'C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (100,250))
fig.figimage(logo, xo = 75, yo = 400, zorder=1)

plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/'+str(county_name).lower().replace(" ","")+'/'+str(county_name).replace(" ","")+'_TOR_TOD.jpg', bbox_inches='tight', dpi=18)
print("Tornado time of day plot for "+county_name+" County created")




#NUMBER OF TORNADOES MONTH
print("Begin tornadoes sorted by month plot for "+county_name+" County")


mon_array = np.arange(1,13)
tor_mon = []
for i in range(1, 13):
    tor_mon.append(county_df[county_df.newdatetime.dt.month == i].shape[0])
    

plt.clf()
fig = plt.gcf()
fig.set_size_inches(70,35)

mon_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

ax = plt.axes()
for axis in ['top','bottom','left','right']:
   ax.spines[axis].set_linewidth(5)
   ax.spines[axis].set_color('black')
plt.xticks(mon_array, mon_name, size=65, fontweight='bold', color='black')
ax.yaxis.grid(lw=2, c='black', ls=':', dashes=(20, 20))
ax.xaxis.grid(lw=2, c='black', ls=':', dashes=(20, 20))    
plt.xticks(mon_array)
plt.bar(mon_array, tor_mon, align='center', label = "Tornadoes", color='red', zorder=3,  edgecolor='black', lw=10)
plt.ylim(0,(int(max(tor_mon))+5))      
plt.xlim(0.5, 12.5)           
plt.xlabel('Month', size='65',  fontweight='bold')
plt.ylabel('Number of Tornadoes \n', size='65',  fontweight='bold')
plt.xticks(size='65',  fontweight='bold')  

plt.yticks(np.arange(0., max(tor_mon)+12., 5), size='65', fontweight='bold')
plt.legend(('Number of Tornadoes',), loc='upper right',prop={'size':65})
plt.suptitle('Number of Tornadoes by Month for '+str(county_name)+' County \n Data: '+str(min_year)+'-'+str(max_year)+' || Tornado Total: '+str(sum(tor_mon))+'\n NWS Fort Worth, TX || Last Updated: ' +str(now_date)+'', size='65', fontweight='bold', y=0.99)

for i in range(len(tor_mon)):
   if tor_mon[i] > 0:
       plt.annotate(str(tor_mon[i]), xy=(mon_array[i],tor_mon[i]+0.2), size='60',  ha='center', fontweight='bold')
       
logo2 = io.imread(r'C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (100,250))
fig.figimage(logo, xo = 75, yo = 400, zorder=1)
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/'+str(county_name).lower().replace(" ","")+'/'+str(county_name).replace(" ","")+'_Monthly_Count.jpg', bbox_inches='tight', dpi=18)
print("Tornado by month plot for "+county_name+" County created")



#NUMBER OF TORNADOES BY YEAR


print("Begin tornadoes sorted by year plot for "+county_name+" County")
year_array = np.arange(min_year, max_year+1) #stupid indexing by computers >:/
tor_year = []
for i in range(0, len(year_array)):
    tor_year.append(county_df[county_df.newdatetime.dt.year== year_array[i]].shape[0])


print("Tornado by year plot for "+county_name+" County created")


sys.exit()


#For map plotting purposes, only plot data from 1950 to present (pre-1950 data does not have lat/lon information
tornado_df = (tornado_df.iloc[np.where(tornado_df['Year'] >= 1950)])


print("Making Tornado Track Map for "+str(county_name)+" County")

start_tor_long = tornado_df['Start Long']
start_tor_lat  = tornado_df['Start Lat']
end_tor_long = tornado_df['End Long']
end_tor_lat  = tornado_df['End Lat']
start_tor = list(zip(start_tor_long, start_tor_lat))
end_tor   = list(zip(end_tor_long, end_tor_lat) )
tor_rating = tornado_df['Rating']

pnts = []

for i in range(0, len(start_tor)):
    if start_tor[i] != end_tor[i]:
        pnts.append(LineString([start_tor[i], end_tor[i]]))
    if start_tor[i] == end_tor[i]: #need this for tornadoes that have the same start and end
        pnts.append(Point(start_tor[i]))


plt.clf()
fig, ax, = plt.subplots(facecolor='#A9A9A9', figsize=(40,40), edgecolor='black')
tracks = GeoDataFrame(tornado_df, geometry=pnts)


cwa_mp.plot(ax=ax, color='#A9A9A9', linewidth=5, edgecolor='#1E1E1E')
county_mp.plot(ax=ax, color='#EDEDED', edgecolor='#000034', linewidth=8)

minx, miny, maxx, maxy = county_mp.total_bounds
ax.set_xlim(minx-0.18, maxx+0.18)
ax.set_ylim(miny-0.18, maxy+0.18)


#plot the cities in the county
city_texts = []
for x, y, label in zip(city['Lon'], city['Lat'], (city['City']).str.title()):
    city_texts.append(plt.text(x, y, label, fontsize=40, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=9, foreground="white")]))



#rate_merged_df.plot(ax=ax, color='#E3DAC9', edgecolor='black', linewidth=4)
(tracks.iloc[np.where(tornado_df['Rating'] == 0.)]).plot(ax=ax, color='#000000', linewidth = 13)
(tracks.iloc[np.where(tornado_df['Rating'] == 1.)]).plot(ax=ax, color='#2D658B', linewidth = 13)
(tracks.iloc[np.where(tornado_df['Rating'] == 2.)]).plot(ax=ax, color='#0C8B20', linewidth = 13)
(tracks.iloc[np.where(tornado_df['Rating'] == 3.)]).plot(ax=ax, color='#FF8000', linewidth = 13)
(tracks.iloc[np.where(tornado_df['Rating'] == 4.)]).plot(ax=ax, color='#FF001B', linewidth = 13)
(tracks.iloc[np.where(tornado_df['Rating'] == 5.)]).plot(ax=ax, color='#FF4FA7', linewidth = 13)


plt.legend((['F/EF-0','_nolegend_', 'F/EF-1','_nolegend_', 'F/EF-2', '_nolegend_', 'F/EF-3','_nolegend_', 'F/EF-4', 'F/EF-5']), edgecolor='black', fontsize='large', fancybox='true',ncol=6, loc='lower center',  prop = {'size':50})

ax.text(.5,.9, 'National Weather Service Fort Worth/Dallas Tornado Climatology \n '+str(county_name)+' County Tornado Tracks (1950-'+str(cur_yr)+') | Last Updated: '+str(now_date)+''  
,fontweight='bold', fontsize='55', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round')
,horizontalalignment='center', transform=ax.transAxes)
ax.axis('off')
logo2 = io.imread('C:/Users/Lamont/FWD/TorClimo/img/logo3.png')
logo = transform.resize(logo2, (100,250))
fig.figimage(logo, xo=30, yo=80, zorder=1)

plt.savefig(('C:/Users/Lamont/FWD/TorClimo/output/'+str(county_name)+'/'+str(county_name)+'.jpg').replace(" ", ""), facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=30)
print("Program ended at county plot")

del county_df['1st FIPS']
del county_df['2nd FIPS']
del county_df['3rd FIPS']
del county_df['4th FIPS']

del county_df['Local Tor#']
del county_df['Month']
del county_df['Day']
del county_df['Year']
del county_df['newdatetime']

county_df['Date'] = pd.to_datetime(county_df['Date'], format='%m/%d/%Y')
county_df['Date'] = county_df['Date'].dt.strftime('%m/%d/%Y')

#Return most active dates
most_tors_date = pd.DataFrame(county_df['Date'].value_counts())
most_tors_date['Number of Tornadoes'] = most_tors_date['Date']
most_tors_date['Date'] = most_tors_date.index

#Return strong and violent tornadoes
sigtors = county_df.iloc[np.where(county_df['Rating'] >=2)]
sigtors = sigtors.sort_values('Rating', ascending=False)


print("Creating Complete Tornado Table for "+str(county_name)+" County")
county_df.to_csv('C:/Users/Lamont/FWD/TorClimo/output/'+"".join(str(county_name).split())+'/'+"".join(str(county_name).split())+'_TornadoTable.csv', index=None)


print("Creating Tornado Frequency by Date for "+str(county_name)+" County")
most_tors_date.to_csv('C:/Users/Lamont/FWD/TorClimo/output/'+''.join(str(county_name).split())+'/'+"".join(str(county_name).split())+'_TornadoFrequency.csv', index=None)

print("Creating Tornado Table for Significant Tornadoes for "+str(county_name)+" County")
sigtors.to_csv('C:/Users/Lamont/FWD/TorClimo/output/'+''.join(str(county_name).split())+'/'+"".join(str(county_name).split())+'_SigTors.csv', index=None)
