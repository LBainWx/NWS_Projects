from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import matplotlib.image as mpimg
import sys


##################################################################
#Fcst_Ver.py is a crude program designed to retrieve
#20 min observational AWOS data to help compare and
#verify personal forecasts
#Author: Lamont Bain -WFO FWD
#EXPERIMENTAL
#################################################################

#Read in the comma seperated file (tho it's not 100% comma seperated
f = open('C:\Users\Lamont\Desktop\Python\Verification\Bowie_Obs.txt', "r")
data = f.readlines()

#Blank arrays for data...will be adding to this very soon
wrk1        = []
stn         = []
date        = []
time        = []
temp        = []
tempf       = []
date_count  = []
date_index  = []
tmax        = []
tmin        = []
date_pos    = []
time_tmax   = []
time_tmin   = []

for i in range(0, len(data)):
	wrk1.append((data[i]).split(","))
	
#Data from IEM has a 5-6 line header block at the top of the file
#Needed to split date and time since whitespace and not comma seperated >:(

for i in range(6, len(wrk1)):
	stn.append((wrk1[i][0]))
	date.append(((wrk1[i][1]))[  :10].translate(None, '-'))
        date_index.append(((wrk1[i][1]))[  :10].translate(None, '-'))
        time.append(((wrk1[i][1]))[10:  ])
        temp.append((wrk1[i][2]).translate(None, "\n :':]:] "))
        
for i in range(0, len(temp)):
    if temp[i] == 'M':
        temp[i] = -999.0              
                
for i in range(0, len(temp)):
    tempf.append(float(temp[i]))
    

#Sort observations by date
#This will return only unique dates
date_sort = sorted(set(date))


#Needed to count the number of observations per day
#Need to sort the observations into a day and then find max and min
for i in range(0, len(date_sort)):    
    date_count.append(date.count(date_sort[i]))
    date_pos.append(date.index(date_sort[i]))

#Creates array for TMax and Tmin
    tmax.append(max(tempf[date_pos[i]:(date_count[i]+date_pos[i])])) 
    tmin.append(min(tempf[date_pos[i]:(date_count[i]+date_pos[i])]))     
    
#Need to determine time of tmax and tmin    
    a1 = time[date_pos[i]:(date_count[i]+date_pos[i])]
    b1 = (tempf[date_pos[i]:(date_count[i]+date_pos[i])])
    time_tmax.append(a1[b1.index(max(b1))])
    time_tmin.append(a1[b1.index(min(b1))])

#Create array for the Number of 100 F/32 F Degree Days
OHDay  = []      #Represents 1 One Hundred Degree Day
OHDate = []	 #Represents the Hundred Degree Date
FZDay  = []	 #Represents 1 32 Degree Day
FZDate = []      #Represents the 32 Degree Date

for i in range(0, len(tmax)):
    if tmax[i] > 99.5 and tmax[i] != -999.0: 
        #print '100 Degree Day Here'
        OHDay.append(tmax[i])
    #else :
        #print 'Not a 100 Degree Day'

for i in range(0, len(OHDay)):
    OHDate.append(date_sort[tmax.index(OHDay[i])])                
                                                

#Create array for the Number of 32 F Degree Days
for i in range(0, len(tmin)):
    if tmin[i] <= 32.0 and tmin[i] != -999.0: 
        #print 'Min Temp below 32 F'
        FZDay.append(tmin[i])
    #else :
        #print 'Min Temp is above 32 F'        

for i in range(0, len(FZDay)):
    FZDate.append(date_sort[tmin.index(FZDay[i])])                

#Temporary Break
sys.exit() 
                                
                                                                                              
#Max Temperature Data (really for astethics, but does nothing in this iteration of program)
tmax_arr = [tmax]
tmax_arr = np.reshape((tmax),(len(tmax),1))
tmax_dat =  str(tmax_arr).translate(None,"[:]:':':,")

#Min Temperature Data (really for astethics, but does nothing in this iteration of program)
tmin_arr = [tmin]
tmin_arr = np.reshape((tmin),(len(tmin),1))
tmin_dat =  str(tmin_arr).translate(None,"[:]:':':,")

#zip function is useful for packaging data neatly
#Header works...but requires some manipulation to open in excel...still working on this
header   = ('ID','Date','TMAX','TimeofTMAX', 'TMIN', 'TimeofTMIN')
temp_dat = zip(stn,date_sort,tmax,time_tmax, tmin, time_tmin)


#Output file
filename = 'C:\Users\Lamont\Desktop\LB_NWS_Verification\AWOS\Bowie_Obs.txt'
import csv
from itertools import izip
with open(filename, 'wb') as csvfile:
    filewriter = csv.writer(csvfile,delimiter=',', quotechar=' ') #, quoting=csv.QUOTE_MINIMAL) 
    #filewriter.writerow(header)
    for i in range(0, len(date_sort)):
       filewriter.writerow(temp_dat[i])

#close program
sys.exit()
