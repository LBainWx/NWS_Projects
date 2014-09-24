from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import matplotlib.image as mpimg
import sys



f = open('C:\Users\Lamont\Desktop\Python\Verification\Bowie.txt', "r")
data = f.readlines()

#Blank arrays for data
wrk1        = []
stn         = []
date        = []
time        = []
tempf       = []
date_count  = []
date_index  = []
tmax        = []
tmin        = []
date_pos    = []


for i in range(0, len(data)):
	wrk1.append(str(data[i]).split(","))
	
#Data from IEM has a 5-6 line header block at the top of the file
#Needed to split date and time since whitespace and not comma seperated >:(

for i in range(6, len(wrk1)):
	stn.append((wrk1[i][0]))
	date.append(((wrk1[i][1]))[  :10].translate(None, '-'))
        date_index.append(((wrk1[i][1]))[  :10].translate(None, '-'))
        time.append(((wrk1[i][1]))[10:  ].translate(None, ':'))
        tempf.append((wrk1[i][2]).translate(None, "\n :':]:] "))
          

#Sort observations by date
#This will return only unique dates
date_sort = sorted(set(date))



#Needed to count the number of observations per day
for i in range(0, len(date_sort)):    
    date_count.append(date.count(date_sort[i]))
    date_pos.append(date.index(date_sort[i]))
    tmax.append(max(tempf[date_pos[i]:(date_count[i]+date_pos[i])])) 
    tmin.append(min(tempf[date_pos[i]:(date_count[i]+date_pos[i])])) 
    
#Max Temperature Data
tmax_arr = [tmax]
tmax_arr = np.reshape((tmax),(len(tmax),1))
tmax_dat =  str(tmax_arr).translate(None,"[:]:':':,")

#Min Temperature Data
tmin_arr = [tmin]
tmin_arr = np.reshape((tmin),(len(tmin),1))
tmin_dat =  str(tmin_arr).translate(None,"[:]:':':,")


#print tmin_dat
#print tmax_dat

#print tmax_dat, tmin_dat
#sys.exit()


clim_dat = [tmax_dat, tmin_dat]


#filename = 'C:\Users\Lamont\Desktop\TOR_txt\Bowie_AWOS.txt'

myfile = file("C:\Users\Lamont\Desktop\TOR_txt\Bowie_AWOS.txt", "w")
myfile = file("C:\Users\Lamont\Desktop\TOR_txt\Bowie_AWOS.txt", "a")
print >>myfile, tmax_dat
print >>myfile, tmin_dat
myfile.close()



#import csv
#with open(filename, 'wb') as csvfile:
#       filewriter = csv.writer(csvfile, delimiter=',', quotechar=',') #, quoting=csv.QUOTE_MINIMAL) 
#       filewriter.writerow(clim_dat)
#sys.exit()


sys.exit()

    #print max(tempf[date_pos[i]:date_count[i]])
    #print tempf[date_count[i]]
    #break

#print date_count

#for i in range(0, len(date_sort)):
#    c.append(date.index(date_sort[i]))


