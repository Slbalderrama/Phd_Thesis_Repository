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



Hourly_Data = pd.DataFrame()


Data['Day'] = Data.index.dayofyear
 
Data['hour'] = Data.index.hour 

Hourly_Data = Data.groupby(['Day','hour']).mean()

index_hourly = pd.DatetimeIndex(start='2013-01-01 01:00:00', periods=8760, 
                                   freq=('1H'))

Hourly_Data.index = index_hourly

Noct = 44.8

for i in Hourly_Data.index:
    
    a = (Noct-20)/800
    b = a*Hourly_Data.loc[i,'W/m2']
    c = Hourly_Data.loc[i,'Temperature'] + b
    Hourly_Data.loc[i,'Cell Temperature'] = c 
 


#irradiance.disc(ghi=Hourly_Data['W/m2'], )


Hourly_Data['Time'] = Hourly_Data.index
   
Latitude = mt.radians(-19.2)
G_sc = 1367 # solar constant is 1367 W/m^2, 433 Btu/(ft^2*hr), 4.92 MJ/(m^2*hr) 
Albeldo = 0.25
tilt = [mt.radians(5),mt.radians(10),mt.radians(11), mt.radians(13),
        mt.radians(15), mt.radians(19.2), mt.radians(20), mt.radians(25), 
        mt.radians(30)]
Global_radiation = pd.DataFrame()
Global_radiation['W/m2'] = Hourly_Data['W/m2']
Global_radiation['Time'] = Hourly_Data.index
Months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
First_Day = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334] 

test = pd.DataFrame()
for Slope_S in tilt:
    First_Day_Month = dict(zip(Months, First_Day))
    
    Day_of_Year = []
    for i in range(0,len(Global_radiation)):
        Day_of_Year.append(Global_radiation['Time'][i].day + First_Day_Month[Global_radiation['Time'][i].month])
    
    Hour_Angle = []
    
    for i in range(0,len(Global_radiation)):
        Hour_Angle.append(mt.radians(-180 + 15*Global_radiation['Time'][i].hour))
        
    
    Declination =  []
    
    Angle_1 = []
    
    for i in range(0,len(Global_radiation)):
        Angle_1.append(mt.radians(360.0*((284.0 + Day_of_Year[i])/365)))
        
    
    for i in range(0,len(Global_radiation)):
        Declination.append(mt.radians(23.45 * mt.sin(Angle_1[i])))
    
    
    rb_numerator = []
    
    for i in range(0,len(Global_radiation)):
        rb_numerator.append(mt.cos(Latitude+Slope_S)*mt.cos(Declination[i])*mt.cos(Hour_Angle[i])+ mt.sin(Latitude+Slope_S)*mt.sin(Declination[i]))
        
    rb_Denominator = []
    for i in range(0,len(Global_radiation)):
        rb_Denominator.append(mt.cos(Latitude)*mt.cos(Declination[i])*mt.cos(Hour_Angle[i]) + mt.sin(Latitude)*mt.sin(Declination[i]))
    
    rb = [] 
    
    for i in range(0,len(Global_radiation)):
        rb.append(rb_numerator[i]/rb_Denominator[i])
        
    I_o = [] # Solar radiation incident in a horizontal plane outside the atmosphera
    
    for i in range(0,len(Global_radiation)):
    #    a = G_sc*(1 + 0.033 * mt.cos(mt.radians((360*Day_of_Year[i])/365)))*(mt.cos(Latitude)*mt.cos(Declination[i])*mt.cos(Hour_Angle[i]) + mt.sin(Latitude)*mt.sin(Declination[i]))    
    #    if a >= 0:
    #        I_o.append(G_sc*(1 + 0.033 * mt.cos(mt.radians((360*Day_of_Year[i])/365.0)))*(mt.cos(Latitude)*mt.cos(Declination[i])*mt.cos(Hour_Angle[i]) + mt.sin(Latitude)*mt.sin(Declination[i])))
    #    else:
    #        I_o.append(0)
        a= G_sc*(1 + 0.033 * mt.cos(mt.radians((360*Day_of_Year[i])/365)))*(mt.cos(Latitude)*mt.cos(Declination[i])*mt.cos(Hour_Angle[i]+mt.radians(-7.5)) + mt.sin(Latitude)*mt.sin(Declination[i]))
        if a >= 0:
            I_o.append(G_sc*(1 + 0.033 * mt.cos(mt.radians((360*Day_of_Year[i])/365)))*(mt.cos(Latitude)*mt.cos(Declination[i])*mt.cos(Hour_Angle[i]+mt.radians(-7.5)) + mt.sin(Latitude)*mt.sin(Declination[i])))
        else:
            I_o.append(0)
            
    
            
    K_t = []
    for i in range(0,len(Global_radiation)):
        if 0 < np.float64(Global_radiation['W/m2'][i])/I_o[i] < 200000000000000000000000000000000000:
            K_t.append(Global_radiation['W/m2'][i]/I_o[i])
        else:
            K_t.append(0)
    
    I_dif_hor =[] # Difussal radiation horizontal to the surface
    
    for i in range(0,len(Global_radiation)):
        if K_t[i] <= 0:
            I_dif_hor.append(0)
        elif 0 < K_t[i] <= 0.22:
            I_dif_hor.append((1.0-0.09*K_t[i])*Global_radiation['W/m2'][i])
        elif 0.22 < K_t[i] <= 0.8:
            I_dif_hor.append((0.9511-0.1604*K_t[i]+4.388*(K_t[i]**2)-16.638*(K_t[i]**3)+12.336*(K_t[i]**4) )*Global_radiation['W/m2'][i])
        else:
            I_dif_hor.append(0.165*Global_radiation['W/m2'][i])
            
    I_dir_hor = []
    
    for i in range(0,len(Global_radiation)):
        I_dir_hor.append(Global_radiation['W/m2'][i] -  I_dif_hor[i])    
    
    I_dir_Slope = []
    for i in range(0,len(Global_radiation)):
        a = I_dir_hor[i]*rb[i]
        if a >= 0:
            I_dir_Slope.append(a)
        else:
            I_dir_Slope.append(0)
        
    I_dif_Slope = []
    
    for i in range(0,len(Global_radiation)):
        I_dif_Slope.append((1+mt.cos(Slope_S))*0.5*I_dif_hor[i])
        
    I_Ground_reflected_Slope = []
    
    for i in range(0,len(Global_radiation)):
        I_Ground_reflected_Slope.append((1-mt.cos(Slope_S))*0.5*Global_radiation['W/m2'][i]*Albeldo)
        
    I_total_Slope = []
    
    for i in range(0,len(Global_radiation)):
        I_total_Slope.append(I_dir_Slope[i] + I_dif_Slope[i] + I_Ground_reflected_Slope[i])
    
    Rad = pd.DataFrame(I_total_Slope, index=range(1,8761))
    test.loc[mt.degrees(Slope_S),'Radiation']=Rad[0].mean()


print(test)