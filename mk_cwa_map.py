import geopandas as gpd
from geopandas import GeoSeries, GeoDataFrame
from shapely.geometry import Point, LineString, Polygon
import shapely.geometry as geom

import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import pandas as pd
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
import sys


import scipy
import matplotlib.image as image
from PIL import Image, ImageDraw, ImageFont

from PIL import Image
from pylab import *



#import warnings
#warnings.filterwarnings("ignore")




#Get shapefile information
county_fp = (r"C:\Users\Lamont\FWD\TorClimo\gis\input\shp\counties\uscounties.shp")
county_mp_df = gpd.read_file(county_fp)
cwa_name = 'AMA'
cwa_mp = (county_mp_df[county_mp_df['CWA'] == cwa_name])
cwa_mp_merged_df = cwa_mp['geometry'].centroid
cwa_mp_merged_df_points = cwa_mp_merged_df.copy()



plt.clf()
fig, ax = plt.subplots(figsize=(90, 70))
ax = cwa_mp.plot(axes=ax, facecolor='grey', linewidth=5.5, edgecolor='black')
ax.axis('off')

cty_texts = []
for x, y, label in zip(cwa_mp_merged_df_points.geometry.x, cwa_mp_merged_df_points.geometry.y, cwa_mp['COUNTYNAME']):
    cty_texts.append(plt.text(x, y, label, fontsize=55, horizontalalignment='center', fontweight='bold', color='black', path_effects=[path_effects.withStroke(linewidth=15, foreground="white")]))


ax.set_title('National Weather Service '+cwa_name+' Warning Area',size='75', fontweight='bold', horizontalalignment='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round') )
plt.savefig('C:/Users/Lamont/FWD/TorClimo/output/'+str(cwa_name)+'map.jpg', optimize=True, dpi=30)
