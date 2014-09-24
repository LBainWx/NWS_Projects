from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import shapefile
import matplotlib.image as mpimg
import sys



#opens and reads CSV file that contains storm information
 #in this case, it's for tornado data
f = open("C:\Users\Lamont\Desktop\Misc_WFO_FWD\FWD_torsV3.csv", 'r')
all_tor = f.readlines()


wrk1                 = []
#Date/Time Info
year                 = []
month 	             = []
day                  = []
date                 = []
time                 = []

#Impact Info
rate                 = []
inj                  = []
fat                  = []
prop_loss            = []
crop_loss            = []

#Track Info
start_lat            = []
start_lon            = []
end_lat              = []
end_lon              = []
county               = []
county_index         = []
path_len             = []


#cumulative stats
year_tor_count       = []
year_count           = []

for i in range(1, len(all_tor)):
	wrk1.append(str(all_tor[i]).split(','))

for i in range(0, len(wrk1)):
	year.append(int(wrk1[i][1]))
	month.append(int(wrk1[i][2]))
	day.append(int(wrk1[i][3]))
	date.append((wrk1[i][4]))#.translate(None, '/'))
	time.append((wrk1[i][5]).translate(None, '\n'))
	county.append(str(wrk1[i][28]).translate(None, '\n'))	
	county_index.append((wrk1[i][28]).translate(None, '\n'))
	start_lat.append((wrk1[i][15]).translate(None, '\n'))
	start_lon.append((wrk1[i][16]).translate(None, '\n'))
	end_lat.append((wrk1[i][17]).translate(None, '\n'))
	end_lon.append((wrk1[i][18]).translate(None, '\n'))
	path_len.append((wrk1[i][19]).translate(None, '\n'))
	rate.append((wrk1[i][10]).translate(None, '\n'))

#To account for any whitespace in the starting or ending lat/lons as well as path lenghts
 #may need to add for other columns	
	if start_lat[i] == '':
		start_lat[i] = -9999.0
	if start_lon[i] == '':
		start_lon[i] = -9999.0
		#print start_lat[i]
	if path_len[i] == '':
		path_len[i] = -9999.0
#quit()
#co_list = sorted(set(county))
#print list(start_lat[0])
#print float(start_lat[0])
#The County for stats to be computed. 

co_name = 'Milam'
county_index = [k for k, county_index in enumerate(county_index) if county_index == co_name]

#start_coord = ([],[])
start_lat_float = []
start_lon_float = []
end_lat_float   = []
end_lon_float   = []
path_len_float  = []
sort_date       = [] 
sort_time       = []
slat = []
slon = []
elat = []
elon = []  
tor_rate = []

#Still a little buggy when it comes to missing path lenghts as well. 
for j in range(0,len(county_index)):
	if start_lat[county_index[j]] and start_lon[county_index[j]] != -9999.0: #or path_len[county_index[j]]# 
		slat.append(float(start_lat[county_index[j]]))
		elat.append(float(end_lat[county_index[j]]))
		slon.append(float(start_lon[county_index[j]]))
		elon.append(float(end_lon[county_index[j]]))
		path_len_float.append(float(path_len[county_index[j]]))
		sort_date.append(date[county_index[j]])
		sort_time.append(time[county_index[j]])
		tor_rate.append(rate[county_index[j]])

for j in range(0, len(slat)):		
	if elat[j] == 0:
		elat[j] = slat[j]
	if elon[j] == 0:
		elon[j] = slon[j]
	#print co_name, slat[j], slon[j], elat[j], elon[j], path_len_float[j], sort_date[j], sort_time[j]



#Pushes all data into arrays...true_dat is the finished product
header_dat   =str(['Date','Time','Start_Lat','Start_Lon', 'End_Lat', 'End_Lon', 'Path_Len_Miles', 'Rating']).translate(None, "[:]:,:'")
array_dat    = [sort_date,sort_time ,slat,slon,elat,elon, path_len_float, tor_rate]

all_dat      = np.array(array_dat)
true_dat     = str(all_dat.transpose()).translate(None,"[:]:':'")

numb_tor = str(len(tor_rate))


#print all_dat
#print true_dat
#sys.exit()

#Create Output Files
filename = 'C:\Users\Lamont\Desktop\TOR_txt\ '+co_name+'.txt'
#output_file = file(filename, "w")
#output_file = file(filename, "a")
#print >>output_file, true_dat
#output_file.close()

#import csv
#with open(filename, 'wb') as csvfile:
#       filewriter = csv.writer(csvfile, delimiter=',', quotechar=' ') #, quoting=csv.QUOTE_MINIMAL) 
#       filewriter.writerow([header_dat])
#       filewriter.writerow([true_dat])
#sys.exit()

#print >>output_file, true_dat
#print >>filename, true_dat
#filename.close()
#sys.exit()
#################################



#Exit to terminate program early
#print 'End of File'
#sys.exit()


#map = Basemap(llcrnrlon=-99.28,llcrnrlat=30.76,urcrnrlon=-94.76,urcrnrlat=34.15,projection='mill',resolution='i')
map = Basemap(llcrnrlon=-97.5,llcrnrlat=30.36,urcrnrlon=-95.45,urcrnrlat=31.80,projection='mill',resolution='i')
map.drawcoastlines(linewidth=0.75)
map.drawstates(linewidth=1, color='black')
map.drawcountries(linewidth=0.75)
map.fillcontinents(color='grey')
map.drawmapboundary(fill_color='black')
#map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
map.readshapefile('C:\Users\Lamont\Desktop\Python\c_05fe14', name='CWA', color='black', linewidth=0.5)
#y2 = end_lat_float

x1 = slon
y1 = slat
x2 = elon
y2 = elat

 
x1, x2 = map(slon, slat)
y1, y2 = map(elon, elat) 
 

props = dict(boxstyle='round', facecolor = 'wheat', alpha=1.0)
plt.plot([x1,y1],[x2,y2], marker='v',markersize=5,  linestyle='solid', linewidth=3.5, color='r')
map.plot(y1,y2, 'bv')

#xy=(10,-5)
#xycoords='axes pixels'
#ax.title("test title", x=0.5, y =0.6)
#plt.annotate('Dallas County Tornado Tracks', xy=(1,0), xytext=(.8,.8))
#plt.text(2,2,'Dallas County Tornado Tracks 1950-2014',bbox = props, fontsize=12)
#plt.suptitle(0,0,'Dallas County Tornado Tracks 1950-2014', fontsize=12)

fig = plt.gcf()
fig.set_size_inches(12,12)


plt.title(co_name+ ' County Tornado Tracks 1950-2014 Total # of TORs: '+numb_tor+'', bbox = props, fontsize=14, ha='center', va='center', loc = 'center')
#plt.subplot(1,1,1) 
#plt.title('test')
#plt.text(0,0,'Test')
plt.show()
#plt.savefig(co_name+'.png', format = 'png', dpi=900,bbox_inches='tight')

#plt.savefig('C:\Users\Lamont\Desktop\TOR_tracks\ '+co_name+'.png', format = 'png', dpi=1000,bbox_inches='tight')
plt.clf
