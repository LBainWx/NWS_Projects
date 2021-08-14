import pandas as pd
import numpy as np

from datetime import datetime
from datetime import timedelta

import sys

#Read in the downloaded METARs from IAState Repository
site = "DFW"
#fields = ['station', 'valid',  'sknt', 'drct', 'gust', 'mslp', 'wxcodes', 'peak_wind_gust', 'peak_wind_gust_mph', 'peak_wind_drct', 'peak_wind_time']
xwind_df = pd.read_csv('C:/Users/Lamont/FWD/Aviation/climo/metars/merged_metars/kdfw/merged_dfw_metars_v2.csv',delimiter=',', )





#Convert things to datetime, make sure items are in order and remove any duplicate observations
xwind_df['datetime'] = pd.to_datetime(xwind_df['datetime_v2'], format=('%m/%d/%Y %H:%M'))
xwind_df.sort_values(by=['datetime'],ascending=True, inplace=True)
xwind_df.drop_duplicates(keep='first', inplace=True)

del xwind_df['datetime_v2']







#Remove data that has any TS in the wxcode
xwind_df = xwind_df.iloc[np.where(xwind_df['ob'].str.contains('TS') != True)]
xwind_df = xwind_df.iloc[np.where(xwind_df['wdir'].str.contains('VRB') != True)]
xwind_df = xwind_df.iloc[np.where(xwind_df['wdir'].str.contains('NOG') != True)]

#xwind_df['wspd'].astype('float').dtypes
#xwind_df['wdir'].astype('int').dtypes
xwind_df['wspd'] = pd.to_numeric(xwind_df['wspd'])
xwind_df['wdir'] = pd.to_numeric(xwind_df['wdir'])


#Need to remove any non-integer wind speeds 
xwind_df['wspd'].dropna(how='any')
xwind_df['wdir'].dropna(how='any')




#Need to compute crosswind component and add a column to dataframe
rwy_hdg = 360.

#xwindsus is the sustained crosswind speed in knots xwindgst is the crosswind gust
xwind_df['xwindsus'] = round(xwind_df['wspd']*abs(np.sin(np.pi/180.*((xwind_df['wdir'])-rwy_hdg))),0)
xwind_df['xwindgst'] = round(xwind_df['wgst']*abs(np.sin(np.pi/180.*((xwind_df['wdir'])-rwy_hdg))),0)


#We only are interested in events where the crosswind sustained wind speed or gust is 25 knots or greater
xwindobs = pd.DataFrame((xwind_df.where(np.logical_or(xwind_df['xwindsus'] >= 25.0, xwind_df['xwindgst'] >=25.0))))
xwindobs = xwindobs[['datetime','ob', 'wspd', 'wdir', 'xwindsus', 'wgst', 'xwindgst']]

#Look at either the crosswind sustained wind speed or the crosswind gust
xwindobs = xwindobs.dropna(subset=['xwindsus', 'xwindgst'], thresh=2)

#Tdiff is the amount of time allowed to elapse between successive observations before they are grouped into another event
tdiff = 7200.

#This will group each xwind observations into events
obdiff = (xwindobs['datetime'].diff(periods=1)).astype('timedelta64[s]')
xwindobs = xwindobs.assign(obdiff=obdiff.values).fillna(0)

obdiff_lst = list(xwindobs['obdiff'])
tmp = []
obdiffi = 0

for i in range(0, len(obdiff_lst)):
    if obdiff_lst[i] <= tdiff:
        tmp.append(int(obdiffi))
    if obdiff_lst[i] > tdiff:
        obdiffi = int(obdiffi+1)
        tmp.append(int(obdiffi))

sys.exit()
xwindobs['obtag'] = tmp

xwind_list = list(set(xwindobs['obtag']))
tmp_event  = []
start_list = []
end_list   = []
event_time = []

for i in range(0, len(xwind_list)):
    start_list.append((xwindobs['datetime'].where(xwindobs['obtag'] == xwind_list[i]).dropna(how='any')).iloc[0])
    end_list.append((xwindobs['datetime'].where(xwindobs['obtag'] == xwind_list[i]).dropna(how='any')).iloc[-1])
    event_time.append((end_list[i]-start_list[i]).total_seconds()/60.)


avg_xwind = []
avg_xwind_gust = []

avg_wind_obs = []
avg_gust_obs = []

tag_number = xwindobs['obtag'].unique()

for i in range(0, len(tag_number)):
    avg_xwind.append((np.mean((xwindobs['xwindsus'].where(xwindobs['obtag'] == tag_number[i])).dropna(how='any'))))
    avg_wind_obs.append(((len((xwindobs['xwindsus'].where(xwindobs['obtag'] == tag_number[i])).dropna(how='any')))))
    avg_xwind_gust.append((np.mean((xwindobs['xwindgst'].where(xwindobs['obtag'] == tag_number[i])).dropna(how='any'))))
    avg_gust_obs.append(((len((xwindobs['xwindgst'].where(xwindobs['obtag'] == tag_number[i])).dropna(how='any')))))




xwindevents = pd.DataFrame()
xwindevents['id'] = tag_number
xwindevents['Start'] = start_list
xwindevents['End'] = end_list
xwindevents['Duration_min'] = (event_time)
xwindevents['Average_xwind'] = (avg_xwind)
xwindevents['Number_of_xwind_obs'] = avg_wind_obs
xwindevents['Average_xwind_gust'] = avg_xwind_gust
xwindevents['Number_of_xwind_gust_obs'] = avg_gust_obs

xwindevents['Average_xwind'] = xwindevents['Average_xwind'].round(1)
xwindevents['Average_xwind_gust'] = xwindevents['Average_xwind_gust'].round(1)




#Essentially remove all xwind events that are shorter than 30 minutes
xwindevents = xwindevents.where(xwindevents['Duration_min'] > 30.).dropna(how='any')

#Sort xwindevents by month
xwindmon = xwindevents['Start'].dt.month
xwindmon = xwindmon.value_counts(sort=True).sort_index()

#Sort xwindevents by time of day
xwindhour_start = xwindevents['Start'].dt.hour
xwindhour_start = xwindhour_start.value_counts(sort=True).sort_index()

xwindhour_end = xwindevents['End'].dt.hour
xwindhour_end = xwindhour_end.value_counts(sort=True).sort_index()



#Create Output Files
print("Creating Output files for xwind events at "+str(site))
xwindevents.to_csv('C:/Users/Lamont/FWD/Aviation/climo/xwinds/'+str(site)+'_'+str(int(rwy_hdg))+'xwindevents_v2.csv', index=None)
xwindobs.to_csv('C:/Users/Lamont/FWD/Aviation/climo/xwinds/'+str(site)+'_'+str(int(rwy_hdg))+'xwindobsv_v2.csv', index=None)
xwindmon.to_csv('C:/Users/Lamont/FWD/Aviation/climo/xwinds/'+str(site)+'_'+str(int(rwy_hdg))+'xwindmon_v2.csv', index=True)
