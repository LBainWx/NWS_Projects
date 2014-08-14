from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl


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
county_index         = []
#cumulative stats
year_tor_count       = []
year_count           = []

for i in range(1, len(all_tor)):
	wrk1.append(str(all_tor[i]).split(','))

for i in range(0, len(wrk1)-1):
	year.append(int(wrk1[i][0]))
	month.append(int(wrk1[i][1]))
	day.append(int(wrk1[i][2]))
	date.append((wrk1[i][3]). translate(None, '/'))
	time.append((wrk1[i][4]).translate(None, ':'))
	rate.append(int(wrk1[i][9]))
	county.append(str(wrk1[i][27]).translate(None, '\n'))	
	county_index.append((wrk1[i][27]).translate(None, '\n'))



#---------------------County Based Statistics----------------------------------#	
#Return the Index for a given County for various statistics
#The County for stats to be computed. 
co_name = 'Dallas'
county_index = [k for k, county_index in enumerate(county_index) if county_index == co_name]

#Print Total Number of TORs by County.
print 'The tornado count for',co_name,'County is:', county.count(co_name)

#Need individual arrays for ratings in a given county
EF0_Co = []
EF1_Co = []
EF2_Co = []
EF3_Co = []
EF4_Co = []
EF5_Co = []

#Sort the number of tornadoes by rating for a given county
#for i in range(0, len(county_index)):
    #Print entire list of whatever tornado stat wanted by county
#	print county[county_index[i]], "EF",(rate[county_index[i]])	
#	if rate[county_index[i]] == 0:
#		EF0_Co.append(rate.count(0))
#	elif rate[county_index[i]] == 1:
#		EF1_Co.append(rate.count(1))
#	elif rate[county_index[i]] == 2:
#		EF2_Co.append(rate.count(2))
#	elif rate[county_index[i]] == 3:
#		EF3_Co.append(rate.count(3))
#	elif rate[county_index[i]] == 4:
#		EF4_Co.append(rate.count(4))	
#	elif rate[county_index[i]] == 5:
#		EF5_Co.append(rate.count(5))	
	
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
#print "The total number of F/EF-5 tornadoes for", co_name, "County :", (len(EF4_Co))	
	

#Sort the total number of tornadoes by month for a given county	

mon_co_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']	
total_month = []

for i in range(0, len(county_index)):
	for j in range(len(mon_co_name)):
		if month[county_index[i]]     == j+1:
			month[county_index[i]]    =  mon_co_name[j]
			
for i in range(len(mon_co_name)):
	total_month.append(int(month.count(mon_co_name[i])))
#print total_month, sum(total_month)

#climo_dur = (max(year)-min(year))
climo_yr_co = np.arange(62)+1950
total_climo_yr = []
year_tor_count_co = []

#print len(climo_yr_co)
#print climo_yr_co

for i in range(0,len(county_index)):
	#print year[county_index[i]]
	total_climo_yr.append(year[county_index[i]])
	#for j in range(len(climo_yr_co)):
	#	if year[county_index[i]]  == j+1: 
	#		year[county_index[i]] =  climo_yr_co[j]	
			
#print total_climo_yr

for j in range(min(year), max(year)+1):
	year_tor_count_co.append(total_climo_yr.count(j))
	#yrly_co_county.append(int(j)
	
print year_tor_count_co, sum(year_tor_count_co)



			
#print max(year)
#print min(year)
#print total_mon_co

#Sort the total number of tornadoes by month for a given county	

 

#-----------------------CWA Wide Statistics--------------------------------------------# 

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
