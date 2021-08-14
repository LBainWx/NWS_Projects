# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 12:17:55 2019

@author: Lamont
"""

# Copyright (c) 2016,2017 MetPy Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
"""
===========================
Upper Air Sounding Tutorial
===========================

Upper air analysis is a staple of many synoptic and mesoscale analysis
problems. In this tutorial we will gather weather balloon data, plot it,
perform a series of thermodynamic calculations, and summarize the results.
To learn more about the Skew-T diagram and its use in weather analysis and
forecasting, checkout `this <https://homes.comet.ucar.edu/~alanbol/aws-tr-79-006.pdf>`_
air weather service guide.
"""


import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.gridspec as gridspec
from metpy.calc import resample_nn_1d
import numpy as np
import pandas as pd
import xarray as xr
import sys


import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import Hodograph, SkewT
from metpy.units import units


#from get_dates_4_raobs import date_str, z_time
from get_soundings import date_str, z_time


#########################################################################
# Getting Data
# ------------
#
# Upper air data can be obtained using the siphon package, but for this tutorial we will use
# some of MetPy's sample data. This event is the Veterans Day tornado outbreak in 2002.


col_names = ['pressure', 'height', 'temperature', 'dewpoint', 'direction', 'speed']



#df = pd.read_fwf(get_test_data('nov11_sounding.txt', as_file_obj=False),
#                 skiprows=5, usecols=[0, 1, 2, 3, 6, 7], names=col_names)
filename = 'C:/Users/Lamont/FWD/Aviation/climo/fog/raob/txt/'+str(date_str)+str(z_time)+'Z.csv'
df = pd.read_csv(filename, delimiter=',')

df.replace(-9999.00,float(np.NaN), inplace=True)
#df.dropna(how='any')
#df['temperature'].replace(-9999.00, np.nan, inplace=True)

df['u_wind'], df['v_wind'] = mpcalc.wind_components(df['speed'],
                                                    np.deg2rad(df['direction']))



# Drop any rows with all NaN values for T, Td, winds
df = df.dropna(subset=('temperature', 'dewpoint', 'direction', 'speed',
                       'u_wind', 'v_wind'), how='all').reset_index(drop=True)


##########################################################################

# We will pull the data out of the example dataset into individual variables and
# assign units.

p = df['pressure'].values * units.hPa
T = df['temperature'].values * units.degC
Td = df['dewpoint'].values * units.degC
wind_speed = df['speed'].values * units.knots
wind_dir = df['direction'].values * units.degrees
u, v = mpcalc.wind_components(wind_speed, wind_dir)

##########################################################################
# Thermodynamic Calculations
# --------------------------
#
# Often times we will want to calculate some thermodynamic parameters of a
# sounding. The MetPy calc module has many such calculations already implemented!
#
# * **Lifting Condensation Level (LCL)** - The level at which an air parcel's
#   relative humidity becomes 100% when lifted along a dry adiabatic path.
# * **Parcel Path** - Path followed by a hypothetical parcel of air, beginning
#   at the surface temperature/pressure and rising dry adiabatically until
#   reaching the LCL, then rising moist adiabatially.

# Calculate the LCL
lcl_pressure, lcl_temperature = mpcalc.lcl(p[0], T[0], Td[0])

#print(lcl_pressure, lcl_temperature)

# Calculate the parcel profile.
parcel_prof = mpcalc.parcel_profile(p, T[0], Td[0]).to('degC')


##########################################################################
# Adding a Hodograph
# ------------------
#
# A hodograph is a polar representation of the wind profile measured by the rawinsonde.
# Winds at different levels are plotted as vectors with their tails at the origin, the angle
# from the vertical axes representing the direction, and the length representing the speed.
# The line plotted on the hodograph is a line connecting the tips of these vectors,
# which are not drawn.

# Create a new figure. The dimensions here give a good aspect ratio
fig = plt.figure(figsize=(9, 9))
#skew = SkewT(fig, rotation=30)
gs = gridspec.GridSpec(3, 3)

skew = SkewT(fig, rotation=30, subplot=gs[:, :3])

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew.plot(p, T, 'r', linewidth=4)
skew.plot(p, Td, 'g', linewidth=4)
my_interval = np.arange(100, 1000, 50) * units('mbar')
ix = resample_nn_1d(p, my_interval)
skew.plot_barbs(p[ix], u[ix], v[ix])
#skew.plot_barbs(p, u, v, xloc=1.0, x_clip_radius=0.1, y_clip_radius=0.08)
skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-50, 45)
plt.ylabel(' ')
plt.xlabel(' ')
plt.xticks(size=15)
plt.yticks(size=15)
plt.title("FWD RAOB for "+str((date_str))+str(z_time)+"", size=25)





# Plot LCL as black dot
#skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')

# Plot the parcel profile as a black line
#skew.plot(p, parcel_prof, 'k', linewidth=2)

# Shade areas of CAPE and CIN
#skew.shade_cin(p, T, parcel_prof)
#skew.shade_cape(p, T, parcel_prof)

# Plot a zero degree isotherm
skew.ax.axvline(color='c', linestyle='--', linewidth=3)

skew.ax.axvline(0, color='c', linestyle='--', linewidth=3)


# Add the relevant special lines
skew.plot_dry_adiabats(linewidth=2)
skew.plot_moist_adiabats()
skew.plot_mixing_lines()


# Create a hodograph
# Create an inset axes object that is 40% width and height of the
# figure and put it in the upper right hand corner.
#h = Hodograph(ax_hod, component_range=80.)
#h.add_grid(increment=20)
#h.plot_colormapped(u, v, wind_speed)  # Plot a line colored by wind speed

ax = fig.add_subplot(gs[0, -1])
h = Hodograph(ax, component_range=60.)
h.add_grid(increment=20)
h.plot(u, v)

# Show the plot
#print("Saving RAOB plot for FWD for", str((filename[40:52])))
print(filename)
plt.savefig('C:/Users/Lamont/FWD/Aviation/climo/fog/raob/plot/'+str(z_time)+'UTC/'+str((date_str))+str(z_time)+'.png', bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=1.25)
plt.close()


