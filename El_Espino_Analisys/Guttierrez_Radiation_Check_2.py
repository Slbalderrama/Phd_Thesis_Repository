#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 17:40:58 2017

@author: sergio
"""
from pvlib import location
from pvlib import irradiance
import pandas as pd
from matplotlib import pyplot as plt

# For this example, we will be using Golden, Colorado
tz = 'America/La_Paz'
lat, lon =-19.2, -63.3

# Create location object to store lat, lon, timezone
site = location.Location(lat, lon, tz=tz)


# Calculate clear-sky GHI and transpose to plane of array
# Define a function so that we can re-use the sequence of operations with
# different locations
def get_irradiance(site_location,tilt, surface_azimuth):
    # Creates one day's worth of 10 min intervals
    times = pd.date_range(start='2013-01-01 00:00:00', periods=8760, 
                                   freq=('1H'),  tz = site_location.tz)
    # Generate clearsky data using the Ineichen model, which is the default
    # The get_clearsky method returns a dataframe with values for GHI, DNI,
    # and DHI
    clearsky = site_location.get_clearsky(times)
    # Get solar azimuth and zenith to pass to the transposition function
    solar_position = site_location.get_solarposition(times=times)
    # Use the get_total_irradiance function to transpose the GHI to POA
    POA_irradiance = irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=surface_azimuth,
        dni=clearsky['dni'],
        ghi=clearsky['ghi'],
        dhi=clearsky['dhi'],
        solar_zenith=solar_position['apparent_zenith'],
        solar_azimuth=solar_position['azimuth'])
    # Return DataFrame with only GHI and POA
    
    Monthly_Data = POA_irradiance.copy()
    Monthly_Data['month'] = Monthly_Data.index.month
    Monthly_Data = Monthly_Data.groupby(['month']).mean()
    
    return  Monthly_Data['poa_global']


# Get irradiance data for summer and winter solstice, assuming 25 degree tilt
# and a south facing array
test = pd.DataFrame()
for i in [5,10,11,13 ,15,19.2, 20, 25, 30]:
    test[i] = get_irradiance(site, i, 0)

print(test.mean())

