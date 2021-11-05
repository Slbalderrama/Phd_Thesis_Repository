#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 15:21:25 2018

@author: Sergio Balderrama
ULg-UMSS
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.ticker as mtick
import matplotlib.pylab as pylab
import enlopy as el
import matplotlib as mpl
from datetime import datetime
import os
from matplotlib.dates import DateFormatter
#%%
############################# Load Method ###################################


Power_Data_4 = pd.read_csv('Data_Espino_Thesis.csv',index_col=0)
index = pd.DatetimeIndex(start='2016-01-01 00:00:00', periods=166464, 
                                   freq=('5min'))

Power_Data_4.index = index

start = '2016-03-21 00:00:00'
end = '2017-03-20 23:55:00'

index2 = pd.DatetimeIndex(start='2016-03-21 00:00:00', periods=365, 
                                   freq=('1D'))
#index3 = pd.DatetimeIndex(start='2016-01-01 00:05:00', periods=3456, 
#                                   freq=('5min'))

load = Power_Data_4['Demand'][start:end]*1000

Hour = []

for i in range(365):
    for j in range(288):
        Hour.append(j)

Month_Average = load.groupby([load.index.month,Hour]).mean()
#Month_Average_2 = Month_Average
#Month_Average_2.index = index3

mean = pd.Series()
n = 0
for i in range(365):
    m = index2[i].month
    for i in range(288):
        
        mean.loc[n] = Month_Average[(m,i)]
        n += 1    

mean.index = load.index

error = load - mean

log_error = np.log(load) - np.log(mean)
z = 0.3 # 0.3
log_error = np.maximum(-z,log_error)

for i in log_error.index:
    if log_error[i] > z:
        log_error.loc[i] = z
    
    
##Sample new loads from load duration curve
curve = log_error
N = len(curve)
LDC_curve = el.get_LDC(curve)

Scenarios = pd.DataFrame()

Scenarios['Base Scenario'] = load

scenarios = 20 # number of scenarios cretated

for i in range(1, scenarios+1): 
    curve_ldc = el.gen_load_from_LDC(LDC_curve, N=len(LDC_curve[0]))

    PSD = plt.psd(curve, Fs=1, NFFT=N, sides='twosided')
    Sxx = PSD[0]

    curve_psd = el.generate.gen_load_from_PSD(Sxx, curve_ldc, 1)
    
    load_psd = mean*np.exp(curve_psd)
    name= 'Scenario ' + str(i)

    Scenarios[name] = load_psd

#Scenarios.index = range(len(Scenarios))
#%%
size = [20,15]
fig=plt.figure(figsize=size)
ax=fig.add_subplot(111, label="1")
alpha= 0.1

start = 228*50
end = 228*60
ax.plot(Scenarios.index[start:end], Scenarios['Base Scenario'][start:end]/1000, c='k')

for i in range(1, scenarios+1): 
    
    name= 'Scenario ' + str(i)
    ax.plot(Scenarios.index[start:end], Scenarios[name][start:end]/1000, c='b', alpha=alpha)

date_form = DateFormatter("%H:%M")
ax.xaxis.set_major_formatter(date_form)

ax.set_xlabel("Time (hours)",size=30)
ax.set_ylabel("kW",size=30)
ax.set_xlim(Scenarios.index[start], Scenarios.index[end-1])
tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
ax.tick_params(axis='x', which='major', labelsize = tick_size )
ax.tick_params(axis='y', which='major', labelsize = tick_size )    

handle1 = mlines.Line2D([], [], color='b',
                                  label='Stochastic Scenarios')
handle2 = mlines.Line2D([], [], color='k',
                                  label='Base scenarios')


plt.legend(handles=[handle2, handle1], bbox_to_anchor=(0.85, -0.05), 
           fontsize = 30, frameon=False,  ncol=2)        
        
plt.savefig('Top_Down_Demand_Modeling.png')
plt.show()        


#%%

Scenarios['year'] = Scenarios.index.year
Scenarios['day']  = Scenarios.index.dayofyear
Scenarios['hour'] = Scenarios.index.hour


hourly_scenarios = Scenarios.groupby(['year','day', 'hour']).mean()
index_hourly = pd.DatetimeIndex(start='2016-03-21 01:00:00', periods=8760, 
                                   freq=('1H'))
hourly_scenarios.index = index_hourly
#%%
size = [20,15]
fig=plt.figure(figsize=size)
ax=fig.add_subplot(111, label="1")
alpha= 0.1

start = 24*50
end = 24*60
ax.plot(hourly_scenarios.index[start:end], 
        hourly_scenarios['Base Scenario'][start:end]/1000, 
        c='k')

for i in range(1, scenarios+1): 
    
    name= 'Scenario ' + str(i)
    ax.plot(hourly_scenarios.index[start:end], 
            hourly_scenarios[name][start:end]/1000, c='b', 
            alpha=alpha)

date_form = DateFormatter("%H:%M")
ax.xaxis.set_major_formatter(date_form)

ax.set_xlabel("Time (hours)",size=30)
ax.set_ylabel("kW",size=30)
ax.set_xlim(hourly_scenarios.index[start], hourly_scenarios.index[end-1])
tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
ax.tick_params(axis='x', which='major', labelsize = tick_size )
ax.tick_params(axis='y', which='major', labelsize = tick_size )    

handle1 = mlines.Line2D([], [], color='b',
                                  label='Stochastic Scenarios')
handle2 = mlines.Line2D([], [], color='k',
                                  label='Base scenarios')


plt.legend(handles=[handle2, handle1], bbox_to_anchor=(0.85, -0.05), 
           fontsize = 30, frameon=False,  ncol=2)        
        
#plt.savefig('Top_Down_Demand_Modeling.png')
plt.show()        


#%%







