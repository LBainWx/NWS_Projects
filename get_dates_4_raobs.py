# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 22:24:48 2019
This is a batch program that will create RAOBs for specific events
E.g., crosswind events, winter weather, etc
@author: Lamont
"""

import pandas as pd
import numpy as np

from datetime import datetime
from datetime import timedelta

import sys

date_df = pd.read_csv('C:/Users/Lamont/FWD/Aviation/climo/fog/dfwfogdates.csv', infer_datetime_format=True)

#date_df['time'] =  (((pd.to_datetime(date_df['time'], format=('%m/%d/%Y')))+pd.Timedelta(days=1))).dt.strftime('%Y%m%d')

#tmp_date =  sorted(set(date_df['time']))
#tmp_date = (tmp_date.replace("-","", regex=True)).values.tolist()
tmp_date = date_df.drop_duplicates()
#new_date = (tmp_date.replace("-","", regex=True)).values.tolist()
#date_df = (date_df.replace("-","", regex=True)).values.tolist()
new_date = tmp_date.values.tolist()

for i in range(0, 10):
    #if new_date[i][0] != '20060219':
    date_str = (str(new_date[i][0]))
    print(str(new_date[i][0]), i)
    z_time = '12'
        
    exec(open("C:/Users/Lamont/FWD/Aviation/climo/code/get_soundings.py").read())
    
    #("C:/Users/Lamont/FWD/Aviation/AWW/get_soundings.py").close()
 