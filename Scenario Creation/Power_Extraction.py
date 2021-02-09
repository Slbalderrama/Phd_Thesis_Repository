#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 08:56:50 2017

@author: Sergio Balderrama
ULg-UMSS
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.ticker as mtick
import matplotlib.pylab as pylab
import matplotlib as mpl



Power_Data = pd.read_csv('Power Data.csv',index_col=0)

index_date = pd.DatetimeIndex(start='2016-01-01 00:00:00', periods=166464, 
                                   freq=('5min'))

index_date_2 = pd.DatetimeIndex(start='2017-01-01 00:00:00', periods=17280, 
                                   freq=('15min'))

Power_Data.index = index_date

index_values = []
for i in range(len(Power_Data['GenSet Power'])):
        index_values.append((i+1)/float(len(Power_Data['GenSet Power']))*100)

Columns = ['Bat Power','PV Power','GenSet Power','Demand Cre']
Power_Data_2 = pd.DataFrame(index=Power_Data.index,columns=Columns)

Power_Data_2['Bat Power'] =  (Power_Data['Bat Power 1'] + Power_Data['Bat Power 2']  
                            + Power_Data['Bat Power 3'])
Power_Data_2['PV Power'] = (Power_Data['PV Power 1'] + Power_Data['PV Power 2'] 
                            + Power_Data['PV Power 3'])
Power_Data_2['GenSet Power'] = Power_Data['GenSet Power']

Power_Data_2['SOC'] = (Power_Data['Bat Soc 1'] + Power_Data['Bat Soc 2'] 
                            + Power_Data['Bat Soc 3'])/3
#%%
# Cleaning values lower than zero

for i in range(len(Power_Data_2)):
    if Power_Data_2['GenSet Power'][i] < 0:
       Power_Data_2['GenSet Power'][i]=0 

# there is 2 pointes where the bat is charging and there is not electrical energy production
# This points are in the mornning and the ouput is lower thatn 40 
# They are PV power 
Power_Data_2['PV Power'][66352] =  -Power_Data_2['Bat Power'][66352]
Power_Data_2['PV Power'][66353] =  -Power_Data_2['Bat Power'][66353]



Power_Data_2['Demand Cre'] = (Power_Data_2['Bat Power'] + Power_Data_2['PV Power']  
                            + Power_Data_2['GenSet Power'])

# Dividing Bat power in two: entering and leaving the battery

Power_Data_2['Bat Power in'] = -Power_Data_2['Bat Power'].where(
                                                    Power_Data_2['Bat Power']<0,0)
    
Power_Data_2['Bat Power out'] = Power_Data_2['Bat Power'].where(
                                                    Power_Data_2['Bat Power']>0,0)
# This moments have negative demand, small values, minor to 1 kW
Power_Data_2['Demand Cre']['2016-03-08 09:45:00'] = 0
Power_Data_2['Demand Cre']['2016-04-18 10:10:00'] = 0
Power_Data_2['Demand Cre']['2017-03-18 12:20:00'] = 0
Power_Data_2['Demand Cre']['2016-03-30 12:40:00'] = 0 



Power_Data_2.to_csv('Power_Data_2.csv')

