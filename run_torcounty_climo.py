# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 22:51:09 2019
Allows you to run FWD_TorClimo_County_maps_text
as a batch type file

@author: Lamont
"""

#Essentially a batch python file that will create images for the counties
# in the county list. A little buggy...not sure why it keeps executing after the last county. 
#Will have to look into this a little later. 

#Update associated txt files
#This will execute Python Script that will create new text files
exec(open("C:/Users/Lamont/FWD/TorClimo/py/new_torclimo_v2.py").read())


#Create CWA Maps
exec(open("C:/Users/Lamont/FWD/TorClimo/py/mk_tor_maps_v3.py").read())



#List of FWD Counties to update tornado climo for all counties
'''county_list = ['Anderson', 'Bell', 'Bosque', 'Collin', 'Comanche', 'Cooke', 'Coryell', 'Dallas', 'Delta', 'Denton', 'Eastland', 
               'Ellis', 'Erath', 'Falls', 'Fannin', 'Freestone', 'Grayson', 'Hamilton', 'Henderson', 'Hill', 'Hood', 
               'Hopkins', 'Hunt', 'Jack', 'Johnson', 'Kaufman', 'Lamar', 'Lampasas', 'Leon', 'Limestone', 'McLennan', 'Milam', 'Mills', 
               'Montague', 'Navarro', 'Palo Pinto', 'Parker', 'Rains', 'Robertson', 'Rockwall', 'Somervell', 'Stephens', 'Tarrant', 
               'Van Zandt', 'Wise', 'Young']

'''

#Specific Counties
county_list = ['Montague']




for i in range(0,len(county_list)):
    county_name = county_list[i]
    exec(open("C:/Users/Lamont/FWD/TorClimo/py/FWD_TorClimo_County_maps_textv2.py").read())
    #exec(open("C:/Users/Lamont/FWD/TorClimo/py/mk_county_barplots_v1.py").read())




