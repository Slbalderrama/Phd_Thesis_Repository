#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 17:40:58 2017

@author: sergio
"""
import pandas as pd
from pvlib import irradiance
import pandas as pd
import math as mt
import numpy as np
from pvlib import location
from pvlib import irradiance
import pandas as pd
from matplotlib import pyplot as plt

Radiation_12 = pd.read_excel('Data/GUTIERREZ RAD SOLAR  2013.xlsx')
Temperature_12 = pd.read_excel('Data/GUTIERREZ TEMP  2013.xlsx')

for i in range(len(Radiation_12)):
    if Radiation_12['Date'][i] != Temperature_12['Date'][i]:
        print(i)
        
for i in range(len(Radiation_12)):
    if Radiation_12['Time'][i] != Temperature_12['Time'][i]:
        print(i)        

Index_Dates = pd.date_range('2013-01-01 00:00:00', 
                            periods=len(Radiation_12), freq='15min')        

del Temperature_12['Time']
del Temperature_12['Date']
del Radiation_12['Time']
del Radiation_12['Date']


Data = pd.DataFrame()

Data['W/m2'] = Radiation_12['Radiacion']
Data['Temperature'] = Temperature_12['Temperatura']

Data.index = Index_Dates


tz = 	'America/La_Paz'
Hourly_Data = pd.DataFrame()


Data['Day'] = Data.index.dayofyear
 
Data['hour'] = Data.index.hour 

Hourly_Data = Data.groupby(['Day','hour']).mean()

index_hourly = pd.DatetimeIndex(start='2013-01-01 00:00:00', periods=8760, 
                                   freq=('1H'),  tz = tz )

Hourly_Data.index = index_hourly



lat, lon = -19.2, -63.3
surface_azimuth = 0
tilt = [5,10,11,13 ,15,19.2, 20, 25, 30]

test_data=pd.DataFrame()

for i in tilt:
    site_location = location.Location(lat, lon, tz=tz)
    
    times = index_hourly
    
    solar_position = site_location.get_solarposition(times=times)
        # Use the get_total_irradiance function to transpose the GHI to POA
    
    di = irradiance.erbs(Hourly_Data['W/m2'], solar_position['apparent_zenith'], times.dayofyear)
    
    POA_isotropic = irradiance.get_total_irradiance(
            surface_tilt=i,
            surface_azimuth=surface_azimuth,
            dni=di['dni'],
            ghi=Hourly_Data['W/m2'],
            dhi=di['dhi'],
            solar_zenith=solar_position['apparent_zenith'],
            solar_azimuth=solar_position['azimuth'],
            model='isotropic')
    
    Hourly_Data['Radiation tilt isotropic ' + str(i)] = POA_isotropic['poa_global']
    

    Monthly_Data = Hourly_Data.copy()
    Monthly_Data['month'] = Monthly_Data.index.month
    Monthly_Data = Monthly_Data.groupby(['month']).mean()
    test_data[i] = Monthly_Data['Radiation tilt isotropic ' + str(i)]
    
    
print(test_data.mean())    
    