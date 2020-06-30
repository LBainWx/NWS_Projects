import pandas as pd
import numpy as np

from datetime import datetime
from datetime import timedelta
import datetime


import matplotlib.pyplot as plt

import sys
import glob

#import geopandas as gpd

tornado_df = pd.read_csv('C:/Users/Lamont/FWD/TorClimo/txt/master/FWD_tors_masterv3.csv')

#delete these unnecessary columns
#del tornado_df['Tor Number']
#del tornado_df['Time Zone']
#del tornado_df['State']
#del tornado_df['State FIPS']
#del tornado_df['State Tor Number']
#del tornado_df['$ Property Loss (in millions)']
#del tornado_df['$ Crop Loss (in millions)']
#del tornado_df['Unnamed: 21']
#del tornado_df['Unnamed: 22']
#del tornado_df['Unnamed: 23']

#rename messy columns
tornado_df.rename(columns={'Time (CST?)':'Time_CST', 'F/EF Rating':'Rating', 'Length (miles)':'Length', 'Width (yards)':'Width'}, inplace=True)
#tornado_df['Date'] = pd.to_datetime(tornado_df['Date'])


#find the period of record
#por = map(int, (sorted(set(tornado_df['Year']))))
por = (list(set(sorted(tornado_df['Year']))))
#create just a list of counties
fwdcounties = sorted((tornado_df['County'].unique()).tolist())
county_lst = sorted((tornado_df['County'].unique()).tolist())
counties_mon = sorted((tornado_df['County'].unique()).tolist())
counties = fwdcounties
tmp_list = []
for i in range(0, len(counties)):
            tmp_list = []
            #sys.exit()
            #print fwdcounties[i]
            for j in range(0, len(por)):
                tmp_list.append(len(tornado_df.where(np.logical_and(tornado_df['Year'] == por[j], tornado_df['County'] == str(counties[i]))).dropna(how='any')))
            fwdcounties[i] = tmp_list



#Create Monthly Tornado Count by County
tmp_list_v2 = []
tornado_df['Mon'] = pd.DataFrame((pd.DatetimeIndex((pd.to_datetime(tornado_df['Date']))).month_name()))
for i in range(0, len(counties)):
    tmp_list_v2 = []
    for j in range(1,13):
        #tmp_list_v2.append(len((tornado_df.where(np.logical_and(tornado_df['Month'] == int(j), tornado_df['County'] == str(counties[i]))).dropna(how='any'))))
        tmp_list_v2.append((len((tornado_df.where(np.logical_and(tornado_df['Month'] == int(j), tornado_df['County'] == str(county_lst[i]))).dropna(how='any')))))
        #print tmp)list_v2
    counties_mon[i] = tmp_list_v2

#sys.exit()
#mon.rename(columns={0:'Month'}, inplace=True)


                        
#create yearly tornado table
tor_table = pd.DataFrame(fwdcounties, columns = por)
all_tors = pd.DataFrame(tor_table.sum(axis=1))
all_tors.rename(columns={0:str(por[0])+'-'+str(por[-1])+' Tornadoes'}, inplace=True)


tor_mon_table = pd.DataFrame(counties_mon, columns = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
tor_mon_table['County'] = county_lst

tor_mon_table = tor_mon_table[['County', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]


counties = pd.DataFrame((sorted((tornado_df['County'].unique()).tolist())))
counties.rename(columns={0:'County'}, inplace=True)
#mon = pd.DataFrame((pd.DatetimeIndex((pd.to_datetime(tornado_df['Date']))).month_name()).tolist())
tor_table = pd.concat([counties, tor_table, all_tors], axis=1)
#tmp_mon = pd.DatetimeIndex((pd.to_datetime(tornado_df['Date']))).month_name()

#tornado_df['Date'] = pd.to_datetime(tornado_df['Date'])
public_table = pd.concat([tornado_df['County'], tornado_df['Year'], tornado_df['Date'], tornado_df['Time_CST'], tornado_df['Rating'], tornado_df['Length'], tornado_df['Width'], tornado_df['Start Lat'], tornado_df['Start Long'], tornado_df['End Lat'], tornado_df['End Long']], axis=1)
public_table = public_table.sort_values('Year')


#output tornado table for the entire CWA
print("Making FWD Tornado Table")
tor_table.to_csv('C:/Users/Lamont/FWD/TorClimo/txt/cwa/FWDTornadoTable.csv', index=None)

print("Making FWD Tornadoes By Year")
tor_table.to_csv('C:/Users/Lamont/FWD/TorClimo/output/FWD_YearlyTornadoTable.csv', index=None)
public_table.to_csv('C:/Users/Lamont/FWD/TorClimo/output/FWD_PublicTornadoTable.csv', index=None)

print("Making FWD Tornadoes By Month")
tor_mon_table.to_csv('C:/Users/Lamont/FWD/TorClimo/output/FWD_MonthlyTornadoTable.csv', index=None)
tor_mon_table.to_csv('C:/Users/Lamont/FWD/TorClimo/txt/cwa/FWDMonthlyTornadoTable.csv', index=None)



tmp_counties = sorted((tornado_df['County'].unique()).tolist())

'''
#output tornado table 
for i in range(0, len(counties)):
    print("Making Tornado Table for", tmp_counties[i])
    counties
sys.exit()
'''

weak_tors = []
strong_tors = []
violent_tors = []
ef_0 = []
ef_1 = []
ef_2 = []
ef_3 = []
ef_4 = []
ef_5 = []



for i in range(0, len(tmp_counties)):
    weak_tors.append(len(tornado_df.where(np.logical_and(tornado_df['Rating'] <=1,  tornado_df['County'] == tmp_counties[i])).dropna(how='any')))
    strong_tors.append(len(tornado_df.where(np.logical_and(tornado_df['Rating'] == 2,  tornado_df['County'] == tmp_counties[i])).dropna(how='any')) + len(tornado_df.where(np.logical_and(tornado_df['Rating'] ==3,  tornado_df['County'] == tmp_counties[i])).dropna(how='any')))
    violent_tors.append(len(tornado_df.where(np.logical_and(tornado_df['Rating'] >=4,  tornado_df['County'] == tmp_counties[i])).dropna(how='any')))
    ef_0.append(len(tornado_df.where(np.logical_and(tornado_df['Rating'] == 0, tornado_df['County'] == tmp_counties[i])).dropna(how='any')))
    ef_1.append(len(tornado_df.where(np.logical_and(tornado_df['Rating'] == 1, tornado_df['County'] == tmp_counties[i])).dropna(how='any')))
    ef_2.append(len(tornado_df.where(np.logical_and(tornado_df['Rating'] == 2, tornado_df['County'] == tmp_counties[i])).dropna(how='any')))
    ef_3.append(len(tornado_df.where(np.logical_and(tornado_df['Rating'] == 3, tornado_df['County'] == tmp_counties[i])).dropna(how='any')))
    ef_4.append(len(tornado_df.where(np.logical_and(tornado_df['Rating'] == 4, tornado_df['County'] == tmp_counties[i])).dropna(how='any')))
    ef_5.append(len(tornado_df.where(np.logical_and(tornado_df['Rating'] == 5, tornado_df['County'] == tmp_counties[i])).dropna(how='any')))


        

weak_tors   = pd.DataFrame(weak_tors)
weak_tors.rename(columns={0:'Weak'}, inplace=True)
strong_tors = pd.DataFrame(strong_tors)
strong_tors.rename(columns={0:'Strong'}, inplace=True)
violent_tors = pd.DataFrame(violent_tors)
violent_tors.rename(columns={0:'Violent'}, inplace=True)

ef_0 = pd.DataFrame(ef_0)
ef_0.rename(columns={0:'EF0'}, inplace=True)

ef_1 = pd.DataFrame(ef_1)
ef_1.rename(columns={0:'EF1'}, inplace=True)

ef_2 = pd.DataFrame(ef_2)
ef_2.rename(columns={0:'EF2'}, inplace=True)

ef_3 = pd.DataFrame(ef_3)
ef_3.rename(columns={0:'EF3'}, inplace=True)

ef_4 = pd.DataFrame(ef_4)
ef_4.rename(columns={0:'EF4'}, inplace=True)

ef_5 = pd.DataFrame(ef_5)
ef_5.rename(columns={0:'EF5'}, inplace=True)

rate_table = pd.concat([counties, weak_tors, strong_tors, violent_tors, ef_0, ef_1, ef_2, ef_3, ef_4, ef_5], axis=1)
print("Making FWD Tornado Rating Table")
rate_table.to_csv('C:/Users/Lamont/FWD/TorClimo/txt/cwa/FWDRatingTable.csv', index=None)

tmp_mon = pd.DatetimeIndex((pd.to_datetime(tornado_df['Date']))).month_name()

#Make CWA Plots
#import Storm_Dat_CWA_v3

#Make County Specific Plots. 
#See run_torcounty_climo file to determine which counties
#import run_torcounty_climo



