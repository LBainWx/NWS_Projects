from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import matplotlib.image as mpimg
import sys

f = open("C:\Users\Lamont\Desktop\Misc_WFO_FWD\FWD_torsV2.csv", 'r')
all_tor = f.readlines()


wrk1                 = []
#Date/Time Info
year                 = []
month 				 = []
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

#cumulative stats
year_tor_count       = []
year_count           = []

#indexing to sort
county_index         = []
event_index          = []

for i in range(1, len(all_tor)):
	wrk1.append(str(all_tor[i]).split(','))

for i in range(0, len(wrk1)):
	year.append(int(wrk1[i][1]))
	month.append(int(wrk1[i][2]))
	day.append(int(wrk1[i][3]))
	date.append((wrk1[i][4]).translate(None, '/'))
	event_index.append(str(wrk1[i][4])) #.translate(None, '/'))
	time.append((wrk1[i][5]).translate(None, ':'))
	rate.append(int(wrk1[i][10]))
	county.append(str(wrk1[i][28]).translate(None, '\n'))	
	county_index.append((wrk1[i][28]).translate(None, '\n'))

co_list = sorted(set(county))

#for i in range(0, len(co_list)):
	#print co_list[i]
#
#print county



#--------------------Date Specific Statistics---------------------------------#
#Sort by specific date (e.g., for Outbreaks)

#Event date needs to be in mmddyyyy format
#Don't use leading zero for months/days with single digits (e.g. use 5 instead of 05 for May)

event_date = '4/26/2011'
event_index = [k for k, event_index in enumerate(event_index) if event_index == event_date]
print event_index
#for i in range(0, len(event_index)):
#    print county[event_index[i]], rate[event_index[i]], time[event_index[i]]

#print len(event_index)
sys.exit() 



#---------------------County Based Statistics----------------------------------#	
#Return the Index for a given County for various statistics

#The County for stats to be computed. 
co_name = 'Dallas'
county_index = [k for k, county_index in enumerate(county_index) if county_index == co_name]


#Print Total Number of TORs by County.
	#print 'The tornado count for',co_list[i],'County is:', county.count(co_list[i])
	#print county.count(co_list[i])
	#continue


sys.exit()

TOR_count = str(county.count(co_name))
#Need individual arrays for ratings in a given county
EF0_Co = []
EF1_Co = []
EF2_Co = []
EF3_Co = []
EF4_Co = []
EF5_Co = []

#Sort the number of tornadoes by rating for a given county
for i in range(0, len(county_index)):
#Print entire list of whatever tornado stat wanted by county
#	print county[county_index[i]], "EF",(rate[county_index[i]])	
	if rate[county_index[i]] == 0:
		EF0_Co.append(rate.count(0))
	elif rate[county_index[i]] == 1:
		EF1_Co.append(rate.count(1))
	elif rate[county_index[i]] == 2:
		EF2_Co.append(rate.count(2))
	elif rate[county_index[i]] == 3:
		EF3_Co.append(rate.count(3))
	elif rate[county_index[i]] == 4:
		EF4_Co.append(rate.count(4))	
	elif rate[county_index[i]] == 5:
		EF5_Co.append(rate.count(5))	
	

	
#Needed to do this number of if/elif statements...may be an easier way to do this
#in the future, but right now this appears to work really well. 

#Actually have this code for months below
	
#Print out Tornado By Rating for Selected County
#print len(EF0_Co), len(EF1_Co), len(EF2_Co), len(EF3_Co), len(EF4_Co), len(EF5_Co)

	
#Print out total number of weak tornadoes
#print "The total number of weak (F/EF-0 to F/EF-1) tornadoes for", co_name, "County :", np.add(len(EF0_Co), len(EF1_Co))

#Print out total number of significant tornadoes
#print "The total number of significant (F/EF-2 to F/EF-3) tornadoes for", co_name, "County :", np.add(len(EF2_Co), len(EF3_Co))

#Print out total number of violent tornadoes
#print "The total number of violent (F/EF-4 or F/EF-5) tornadoes for", co_name, "County :", np.add(len(EF4_Co), len(EF5_Co))

#Print out total number of F/EF-5 Tornadoes
#print "The total number of F/EF-5 tornadoes for", co_name, "County :", (len(EF5_Co))	
	

#Sort the total number of tornadoes by month for a given county	

mon_co_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']	
total_month = []

for i in range(0, len(county_index)):
	for j in range(len(mon_co_name)):
		if month[county_index[i]]     == j+1:
				month[county_index[i]]    =  mon_co_name[j]
			
for i in range(len(mon_co_name)):
	total_month.append(int(month.count(mon_co_name[i])))
print total_month, sum(total_month)

#Terminate program here
sys.exit()

climo_dur = (max(year)-min(year)+1)
climo_yr_co = np.arange(climo_dur)+min(year)
total_climo_yr = []
year_tor_count_co = []
#print climo_yr_co


for i in range(0,len(county_index)):
#	print year[county_index[i]]
	total_climo_yr.append(year[county_index[i]])		

for j in range(min(year), max(year)+1):
	year_tor_count_co.append(total_climo_yr.count(j))
	#yrly_co_county.append(int(j))
	

max_year = str(max(year))
min_year = str(min(year))

#print min_year, "-", max_year
	
#print year_tor_count_co, sum(year_tor_count_co)
#Plot # of TORs in a County By Year
#print len(year_tor_count_co), len(climo_yr_co)
#print climo_yr_co
#plt.bar(climo_yr_co, year_tor_count_co, color='red', align='center')
#pl.xlim(1949.5,2012.5)
#pl.ylim(0,75)
#plt.grid()
#plt.suptitle('1950-2011 Tornadoes in '+co_name+' County By Year')
#plt.xlabel('Years')
#plt.ylabel('Number of Tornadoes')
#plt.legend(('TOR',), loc='upper right')

#Plot # of TORS in a County By Month
pl.xlim(0.5,12.5)
mon_num = [1,2,3,4,5,6,7,8,9,10,11,12]
#img = ("NWS_log.png")
#print len(mon_num)


plt.xticks(mon_num, mon_co_name)
plt.bar(mon_num, total_month, align='center', label = "Tornadoes", color='red')
pl.ylim(0,max(total_month)+5)
#plt.grid()
plt.suptitle('Number of Tornadoes by Month between '+min_year+'-'+max_year+' in '+co_name+' County is: '+TOR_count+' \n NOAA\NWS Fort Worth, Texas')
plt.xlabel('Months')
plt.ylabel('Number of Tornadoes')
plt.legend(('Tornado',), loc='upper right')

#For loop to help plot the text assoc. w/total number of tornadoes
#by month
for i in range(len(mon_num)):
	plt.annotate(str(total_month[i]), xy=(mon_num[i]-0.1,total_month[i]+0.7))

#plt.imshow(img)
#plt.show()	
#plt.text(12, 20, 'EXPERIMENTAL', fontsize=50, color='gray', ha='right', va='bottom',
#alpha=0.5)
#plt.savefig('C:\Users\Lamont\Desktop\Misc_WFO_FWD\Plots\Month\ '+co_name+'.png')

#a = np.array(total_month)
#print a.transpose()
#myfile = file("Lamar_test.txt", "w")
#myfile = file("Lamar_test.txt", "a")
#f.write(total_month)			
#print >>myfile, total_month
#myfile.close()

#print max(year)
#print min(year)
#print total_mon_co


#Sort the total number of tornadoes by month for a given county	

 

#-----------------------CWA Wide Statistics--------------------------------------------# 

#county_index = [k for k, county_index in enumerate(county_index) if county_index == co_list]
#Print the Total Number of TORs by Year for the entire CWA. 
#for j in range(min(year), max(year)+1):
#	year_tor_count.append(year.count(j))
#	year_count.append(int(j))
	
#YTC = year_tor_count
#YC  = year_count  
#print len(YC), len(YTC)	
#print YC
 
 
#Print Total Number of TORs by rating across the entire CWA. 
#F0_CWA = rate.count(0)
#print 'The total number of F/EF-0 TORs:',F0
#F1_CWA = rate.count(1)
#print 'The total number of F/EF-1 TORs:',F1
#F2_CWA = rate.count(2)
#print 'The total number of F/EF-2 TORs:',F2
#F3_CWA = rate.count(3)
#print 'The total number of F/EF-3 TORs:',F3
#F4_CWA = rate.count(4)
#print 'The total number of F/EF-4 TORs:',F4
#F5_CWA = rate.count(5)
#print 'The total number of F/EF-5 TORs:',F5

#Sig_Tor_CWA = np.add(F2, F3)
#V_Tor_CWA   = np.add(F4, F5)

#print 'The total number of Significant Tornadoes across the FWD CWA:',Sig_Tor_CWD
#print 'The total number of Violent Tornadoes the FWD CWA:',V_Tor_CWD	

#Print the total number of tornadoes by month for the entire CWA
#for i in range(len(mon_co)):
#	total_mon_co.append(int(month.count(mon_co[i])))
	

	
#Plotting Statistical Information	
#plt.bar(YC, YTC, color='red', align='center')
#pl.xlim(1949.5,2012.5)
#pl.ylim(0,75)
#plt.grid()
#plt.suptitle('1950-2012 Tornadoes in FWD CWA By Year')
#plt.xlabel('Years')
#plt.ylabel('Number of Tornadoes')
#plt.legend(('TOR',), loc='upper right')
#plt.show()	
