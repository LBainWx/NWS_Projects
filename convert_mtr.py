import pandas as pd
import numpy as np

from datetime import datetime
from datetime import timedelta

import sys
import re
import glob

import warnings
warnings.filterwarnings("ignore")
#from run_all import fname
#print(fname)

site = "KDFW"
#filelist = (glob.glob('C:/Users/Lamont/FWD/Aviation/climo/metars/2004/dfwobs/*'))

tmp_mtr = []
#fname = 'C:/Users/Lamont/FWD/Aviation/climo/metars/2007/dfwobs/dfwobs.04'
with open(fname) as fp:
    contents = fp.read()
    for entry in contents.split(site):
        tmp_mtr.append(entry)
        


raw_mtr = []
a_mtr = pd.Series(tmp_mtr)
for i in range(0, len(a_mtr)):
    if (((a_mtr.iloc[i]).replace("\n", "").strip())) != 'SAUS70' and (((a_mtr.iloc[i]).replace("\n", "").strip())) != 'SPUS70':
        raw_mtr.append(((a_mtr.iloc[i]).replace("\n", "").strip()).replace("COR",""))


mtr = []
#qc_mtr = pd.Series(mtr, 'mtr_ob')  



for i in range(1, len(raw_mtr)):
    if raw_mtr[i].find("METAR") == -1 and raw_mtr[i].find("SPECI") == -1:
        mtr.append(' '.join(raw_mtr[i].split()))
        #qc_mtr['mtr_ob'].iloc[i] = (' '.join(raw_mtr[i].split()))


#qc_mtr.index.name='metar'   
qc_mtr = pd.Series(mtr, dtype=str)


metar_date = raw_mtr[0][(((raw_mtr[0]).find("/"))-2):(((raw_mtr[0]).find("/"))+8)]    
metar_date = (' '.join(metar_date.split()))


qc_mtr = qc_mtr.str.split(" ", n=1, expand=True) 
qc_mtr['date'] = metar_date
try:
    qc_mtr['filedate'] = pd.to_datetime(qc_mtr['date'], format= '%m/%d/%Y')
except:
     qc_mtr['filedate'] = pd.to_datetime(qc_mtr['date'], format= '%m/%d/%y')
   
qc_mtr['ob'] = qc_mtr[1]




#qc_mtr_tmp_date = qc_mtr['date'].str.split('/', n=3)

qc_mtr['tmp_time'] = qc_mtr[0].str.strip('Z') 
qc_mtr['mon'] = (qc_mtr['filedate'].dt.month)
qc_mtr['day'] = (qc_mtr['filedate'].dt.day)
qc_mtr['year'] = (qc_mtr['filedate'].dt.year)

qc_mtr['mtr_day'] =  (qc_mtr['tmp_time'].str.slice(start=0, stop=2))


#Need this to compare date in METAR and date in filename since 
#files are not based on the calendar day 

for i in range(0, len(qc_mtr)):
    #print(((qc_mtr['filedate'].dt.day).iloc[i]) - int(qc_mtr['mtr_day'].iloc[i]))
    #print(qc_mtr['filedate'].dt.day).iloc[i]
    #print(qc_mtr['mtr_day'].iloc[i])

    
    if (qc_mtr['filedate'].dt.day).iloc[i] != int(qc_mtr['mtr_day'].iloc[i]):
        qc_mtr['filedate'].iloc[i] = (qc_mtr['filedate'].iloc[i])+timedelta(days=1)

qc_mtr['time'] =  (qc_mtr['tmp_time'].str.slice(start=2))

#del qc_mtr['tmp_time']
del qc_mtr['mtr_day']
del qc_mtr['date']

qc_mtr['datetime'] = qc_mtr['filedate'].dt.strftime('%m/%d/%Y') + ' ' + qc_mtr['time']
qc_mtr['datetime_v2'] = pd.to_datetime(qc_mtr['datetime'], format=('%m/%d/%Y %H%M'))


del qc_mtr['datetime']

#qc_mtr['wdir'] = qc_mtr['ob'].str.slice(start=0, stop=3)
qc_mtr['wspd'] = (qc_mtr['ob'].where(qc_mtr['ob'].str.contains('(.*)KT'))).fillna(value=str('0'))
qc_mtr['wgst'] = (qc_mtr['ob'].where(qc_mtr['ob'].str.contains('G(.*)KT'))).fillna(value=str('0'))


qc_mtr= qc_mtr.replace(to_replace='None', value=np.nan).dropna()
tmp_slice = (qc_mtr['ob'].str.slice(start=0))

wind_slice = []
for i in range(0, len(tmp_slice)):
    if tmp_slice.iloc[i].find('KT') != -1: 
        #print(tmp_slice.iloc[i])
        wind_slice.append(tmp_slice.iloc[i][:tmp_slice.iloc[i].index('KT')+2])
    if tmp_slice.iloc[i].find('KT') == -1:
        wind_slice.append('NOG')


qc_mtr['wind_slice'] = wind_slice
qc_mtr['wdir'] = qc_mtr['wind_slice'].str.slice(start=0, stop=3) #extract wind direction



#Retrieve the sustained wind speeds
for i in range(0, len(qc_mtr['wdir'])):
    if (qc_mtr['wind_slice'].iloc[i]).find('G') == -1:
        qc_mtr['wspd'].iloc[i] = (qc_mtr['wind_slice'].iloc[i][qc_mtr['wind_slice'].iloc[i].index('KT')-2:-2])
        #print(qc_mtr['wspd'].iloc[i])
    if (qc_mtr['wind_slice'].iloc[i]).find('G') != -1:
        #print("There is a gust here")
        qc_mtr['wspd'].iloc[i] = (qc_mtr['wind_slice'].iloc[i][3:qc_mtr['wind_slice'].iloc[i].index('G')])
        #print(qc_mtr['wspd'].iloc[i])
        
    #else:
        #qc_mtr['wspd'].iloc[i] = (re.search('(.*)G', qc_mtr['wind_slice'].iloc[i]).group(1))
        


#Retrieve the wind gusts
for i in range(0, len(qc_mtr['wgst'])):
    if qc_mtr['wgst'].iloc[i] != '0':
        #print(qc_mtr['ob'].iloc[i])
        qc_mtr['wgst'].iloc[i] = ((re.search('G(.*)KT', str(qc_mtr['wgst'].iloc[i]))).group(1))
    else:
        qc_mtr['wgst'].iloc[i] == 0

del qc_mtr['mon']
del qc_mtr['day']
del qc_mtr['year']
del qc_mtr['time']
del qc_mtr['tmp_time']
del qc_mtr['wind_slice']

#Retrive the sky group
#Look for the following items 
sky = re.compile(".*(CLR).*|.*(FEW).*|.*(SCT).*|.*(BKN).*|.*(OVC).*|.*(VV).*")

sky1 = []
sky2 = []
sky3 = []

for i in range(0, len(qc_mtr['ob'])):
    tmp_sky = [m.group(0) for l in qc_mtr['ob'].iloc[i].split(" ") for m in [sky.search(l)] if m]
    if len(tmp_sky) >=1 and 'CLR' not in tmp_sky:
        sky1.append(tmp_sky[0])
        #qc_mtr['sky1'] = (tmp_sky[0])
    else:
        #qc_mtr['sky1'] = np.nan
        sky1.append(str(np.nan))
        
    if len(tmp_sky) ==2:
        #qc_mtr['sky2'] = tmp_sky[1]
        sky2.append(tmp_sky[1])
    else:
        #qc_mtr['sky2'] = np.nan
        sky2.append(str(np.nan))
        
    if len(tmp_sky) == 3:
        #qc_mtr['sky3'] = tmp_sky[2]
        sky3.append(tmp_sky[2])
    else:
        #qc_mtr['sky3'] = np.nan
        sky3.append(str(np.nan))
    
qc_mtr['sky1'] = (sky1)
qc_mtr['sky1_hgt'] = (qc_mtr['sky1'].str.extract('(\d+)').astype(float))

qc_mtr['sky2'] = (sky2)
qc_mtr['sky2_hgt'] = (qc_mtr['sky2'].str.extract('(\d+)').astype(float))


qc_mtr['sky3'] = (sky3)
qc_mtr['sky3_hgt'] = (qc_mtr['sky3'].str.extract('(\d+)').astype(float))


#print(qc_mtr['sky1'].str.extract('(\d+)').astype(float))

#tmp_sky_grp = (qc_mtr['ob'].str.extract(sky))



#qc_mtr['tmp_sky_grp'] = pd.Series(tmp_sky_grp)

metar_stamp = (sorted(qc_mtr['filedate'])[0]).strftime('%m%d%Y')
del qc_mtr['filedate']
del qc_mtr[0]
del qc_mtr[1]



qc_mtr.drop_duplicates(subset = 'datetime_v2', keep = 'first', inplace=True)

col_order = ['datetime_v2', 'ob', 'wspd', 'wgst', 'wdir', 'sky1', 'sky1_hgt','sky2', 'sky2_hgt', 'sky3', 'sky3_hgt' ]
qc_mtr = qc_mtr.reindex(columns=col_order)
qc_mtr.to_csv('C:/Users/Lamont/FWD/Aviation/climo/metars/2019/qc_dfwobs/'+str(site)+str(metar_stamp)+'obs.csv', index=None)
print("Created decoded METARs for "+str(site)+" on "+str(metar_stamp)+"")

