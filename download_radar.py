#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 19:37:51 2020

@author: Lamont

Created to quickly download level II data from amazon
"""

from xml.dom import minidom
from sys import stdin
import urllib3
from urllib.request import urlopen
from subprocess import call
import sys

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


date = "2020/04/12"  #YYYY/MM/DD 
hour = "10"          #Time in UTC
site = "KFWS"
bucketURL = "http://noaa-nexrad-level2.s3.amazonaws.com"
dirListURL = bucketURL+ "/?prefix=" + date + "/" + site

xmldoc = minidom.parse(urlopen(dirListURL))
itemlist = xmldoc.getElementsByTagName('Key')
new_date = date[5:7]+date[8:]+date[0:4]

#this is a hack since I use anaconda/spyder
from six.moves import urllib

for i in range(0, len(itemlist)):
    file = getText(itemlist[i].childNodes)
    if file[29:31] == hour:
        fn = (bucketURL+str('/')+file)
        print("Now Downloading: ", fn)
        #urllib.request.urlretrieve(fn, 'C:/Users/Lamont/FWD/Radar/05162020/'+str(site)+'/'+str(file[16:]).replace("/", ""))
        urllib.request.urlretrieve(fn, 'E:/Radar-Archive/Level2/20200412/'+str(site)+'/'+str(file[16:]).replace("/", ""))
        #E:\Radar-Archive\Level2\20200505\FWS