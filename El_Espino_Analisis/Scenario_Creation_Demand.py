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

#%%
############################# Load Method ###################################


Power_Data_4 = pd.read_csv('Data/Data_Espino_Thesis_Fill_2.csv',index_col=0)
index = pd.DatetimeIndex(start='2016-01-01 00:00:00', periods=166464, 
                                   freq=('5min'))

Power_Data_4.index = index

start = '2016-03-21 00:05:00'
end = '2017-03-21 00:00:00'

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
z = 0.3 # 3
log_error = np.maximum(-z,log_error)

for i in log_error.index:
    if log_error[i] > z:
        log_error.loc[i] = z
    
    
##Sample new loads from load duration curve
curve = log_error
N = len(curve)
LDC_curve = el.get_LDC(curve)

Scenarios = pd.DataFrame()
LDC_Scenarios = pd.DataFrame()
Scenarios['Base Scenario'] = load

foo = load
foo = foo.sort_values(ascending=False)

index_LDC = []
for i in range(len(foo)):
    index_LDC.append((i+1)/float(len(foo))*100)

foo.index = index_LDC

LDC_Scenarios['Base Scenario'] = foo

scenarios = 10 # number of scenarios cretated

for i in range(1, scenarios+1): 
    curve_ldc = el.gen_load_from_LDC(LDC_curve, N=len(LDC_curve[0]))

    PSD = plt.psd(curve, Fs=1, NFFT=N, sides='twosided')
    Sxx = PSD[0]

    curve_psd = el.generate.gen_load_from_PSD(Sxx, curve_ldc, 1)
    
    load_psd = mean*np.exp(curve_psd)
    name= 'Scenario ' + str(i)

    Scenarios[name] = load_psd
    foo = load_psd
    foo = foo.sort_values(ascending=False)
    foo.index = index_LDC
    LDC_Scenarios[name] = foo


ax = LDC_Scenarios.plot()

ax.legend(bbox_to_anchor=(1.42, 1.05))    
ax.set_ylabel('Power (kW)')
ax.set_xlabel('hours')
#%%
############################### Transfor scenarios to hourly data ############
Hourly_Data = pd.DataFrame()


Scenarios['Day'] = 0

foo = 0
iterations = int(len(Scenarios)/288)

a = len(Scenarios.columns)-1

for i in range(iterations):
    for j in range(288):
        index = Scenarios.index[foo]
        Scenarios.loc[index,'Day'] = i
        foo += 1
 
Scenarios['hour'] = 0

foo = 0

for i in range(iterations):
    for j in range(int(288/12)):
        for s in range(12):
            index = Scenarios.index[foo]
            Scenarios.loc[index,'hour'] = j
            foo += 1

Hourly_Data = Scenarios.groupby(['Day','hour']).mean()

index_hourly = pd.DatetimeIndex(start='2016-03-21 01:00:00', periods=8760, 
                                   freq=('1H'))
Demand_Hourly = pd.DataFrame()
Demand_Hourly['Base Scenario'] = Hourly_Data['Base Scenario']

Demand_Hourly.index = range(1,8761)

Base_Sce = pd.DataFrame()
Base_Sce['Base Scenario'] = Hourly_Data['Base Scenario']

Hourly_Data.index = index_hourly 
Demand_Hourly.index = index_hourly

Hourly_Data = Hourly_Data.drop('Base Scenario', axis=1)

Power_Factors = []

Iter = len(Hourly_Data.columns)

Value = 0.8
step = 0.1
 
for i in range(Iter):
    if i == 0:
        Power_Factors.append(Value)

    else:
        Power_Factors.append(Value)
    Value += step
    
        
    

Hourly_Data_2 = pd.DataFrame()
for i in range(Iter):
    name = Hourly_Data.columns[i]
    Hourly_Data_2[i+1] = Hourly_Data[name]*Power_Factors[i]

Hourly_Data_2.index = range(1,8761)

now = str(datetime.now())    
path = 'Scenarios/Demand_' + now[:10] + '-' + now[11:13] + '-' + now[14:16] 
os.makedirs(path)
# non multiply scenarios
Hourly_Data.to_excel( path + '/Normal_Scenarios.xls')
# multiply scenarios
Hourly_Data_2.to_excel( path + '/Mulitply_Scenarios.xls')
# Base scenario, which means that the  load generation method was not applied here
Demand_Hourly.to_excel(path + '/Base_Scenarios.xls')

Expected_Probability =  {1:0.05,
	                      2:0.08,                      
	                      3:0.18,
	                      4:0.20,
	                      5:0.14,
	                      6:0.103,
	                      7:0.097,
	                      8:0.086,
	                      9:0.042,	
                         10:0.022}


Expected_Demand = pd.DataFrame()

for i in Hourly_Data_2.index:
    
    demand = 0
    
    for j in Hourly_Data_2.columns:
        demand += Hourly_Data_2[j][i]*Expected_Probability[j]
    
    Expected_Demand.loc[i,1] = demand     

Expected_Demand.to_excel(path + '/Expected_Demand.xls')


#%%
################### plots Demand profile

plot_1 = Hourly_Data[624:696]/1000
ax = plot_1.plot(lw=0.5)
ax.legend(bbox_to_anchor=(1.42, 1.05))    
ax.set_ylabel('Power (kW)')
ax.set_xlabel('hours')

#%%
################### plots LDC profile

index_LDC_2 = []
for i in range(len(Hourly_Data)):
    index_LDC_2.append((i+1)/float(len(Hourly_Data))*100)

LDC_Daily_1 = pd.DataFrame()
for i in Hourly_Data.columns:
    foo = Hourly_Data[i]
    LDC_Daily_1[i] = list(foo.sort_values(ascending=False))
    LDC_Daily_1[i] = LDC_Daily_1[i]/1000
    
LDC_Daily_1.index = index_LDC_2
    
ax1 = LDC_Daily_1.plot()
ax1.legend(bbox_to_anchor=(1.42, 1.05))    
fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
xticks = mtick.FormatStrFormatter(fmt)
ax1.xaxis.set_major_formatter(xticks)
ax1.set_ylabel('Power (kW)')
ax1.set_xlabel('Percentage (%)')


#%%
################## plots LDC multiply profiles

LDC_Daily_2 = pd.DataFrame()
for i in Hourly_Data_2.columns:
    foo = Hourly_Data_2[i]
    LDC_Daily_2[i] = list(foo.sort_values(ascending=False))
    LDC_Daily_2[i] = LDC_Daily_2[i]/1000 

LDC_Daily_2.index = index_LDC_2    
ax2 = LDC_Daily_2.plot()
ax2.legend(bbox_to_anchor=(1.42, 1.05))    
fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
xticks = mtick.FormatStrFormatter(fmt)
ax2.xaxis.set_major_formatter(xticks)
ax2.set_ylabel('Power (kW)')
ax2.set_xlabel('Percentage (%)')

#%%
####################### LDC base scenario

Demand = pd.DataFrame()

Start = '2016-03-21 01:00:00'
End =   '2017-03-21 00:00:00'


Demand["Demand"]=Demand_Hourly['Base Scenario'][Start:End]/1000

Demand_LDR = Demand.sort_values('Demand', ascending=False)


index_LDR = []
for i in range(len(Demand_LDR)):
        index_LDR.append((i+1)/float(len(Demand_LDR))*100)
Demand_LDR.index = index_LDR
ax1 = Demand_LDR.plot(style='b-',linewidth=2)

fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
xticks = mtick.FormatStrFormatter(fmt)
ax1.xaxis.set_major_formatter(xticks)
ax1.set_ylabel('Power (kW)')
ax1.set_xlabel('Percentage (%)')
pylab.ylim([0,26])

print('Power mean ' + str(round(Demand_LDR['Demand'].mean(),1)) + ' w')
print('Power Standar Deviation ' + 
      str(round(Demand_LDR['Demand'].std(),1)) + ' w')
print('Max Power '  + str(round(Demand_LDR['Demand'].max(),1)) + ' w')
print(Start +' to ' + End) 

#%%
################################# Daily average curve

Demand = pd.DataFrame()

Start = '2016-03-21 01:00:00'
End =   '2017-03-21 00:00:00'
Demand["Demand"] = Demand_Hourly['Base Scenario'][Start:End]/1000

foo = 0
iterations = int(len(Demand)/24)

for i in range(iterations):
    for j in range(1,25):
        date = Demand.index[foo]
        Demand.loc[date,'hour'] = j
        foo += 1                     


Daily_Curve = Demand.groupby(['hour']).mean()

size = [20,15]
fig=plt.figure(figsize=size)
tick_size = 25    
mpl.rcParams['xtick.labelsize'] = tick_size 
mpl.rcParams['ytick.labelsize'] = tick_size 


ax=fig.add_subplot(111, label="1")
ax2=fig.add_subplot(111, label="2", frame_on=False)

label_size = 25
ax.plot(Demand_LDR.index,Demand_LDR['Demand'])
ax.set_xlim([0,100])
ax.set_xlabel("Percentage (%)",size=label_size)
ax.set_ylabel("Power (kW)",size=label_size)
ax.tick_params(axis='y', which='major', labelsize = tick_size )
ax.tick_params(axis='x', which='major', labelsize = tick_size )

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax2.plot( Daily_Curve.index,Daily_Curve['Demand'],c = 'k',
          linestyle='dashed')

col_labels=['Value']
row_labels=['Average Power (kW)','Standard Deviation (kW)'
            ,'Max Power demand (kW)']
table_vals=[[10],[3.5],[22.6]]

the_table = plt.table(cellText=table_vals,
                  colWidths = [0.1]*3,  
                  rowLabels=row_labels,
                  colLabels=col_labels,
                  loc='upper center')
the_table.set_fontsize(25)
the_table.scale(1, 4)

ax2.set_xlim([1,24])
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.set_xlabel('hours',size=label_size) 
ax2.set_ylabel('Power (kW)',size=label_size) 
ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right') 

demand = mlines.Line2D([], [], color='k',
                                  label='Demand', 
                                  linestyle='--')
ldr = mlines.Line2D([], [], color='b',
                                  label='LDC', 
                                  linestyle='-')

plt.legend(handles=[ demand, ldr],
           bbox_to_anchor=(0.67,-0.05),
    frameon=False, ncol=2,fontsize = 30)


#%%
################################### Log plot error #####################################

index_LDC_error = []
for i in range(len(log_error)):
    index_LDC_error.append((i+1)/float(len(log_error))*100)


log_error_sort = list(log_error.sort_values(ascending=False))

size = [20,15]
fig=plt.figure(figsize=size)
ax=fig.add_subplot(111, label="1")
ax2=fig.add_subplot(111, label="2", frame_on=False)

ax.plot(range(1,105121),list(log_error))
ax.set_xlabel("Time Step",size=30)

tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
ax.tick_params(axis='x', which='major', labelsize = tick_size )
ax.tick_params(axis='y', which='major', labelsize = tick_size )

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.set_xlim([0,105121])

ax2.plot(index_LDC_error,log_error_sort,c = 'r',
          linestyle='dashed', linewidth=4)
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right') 
ax2.xaxis.set_major_locator(plt.NullLocator())
ax2.yaxis.set_major_locator(plt.NullLocator())

demand = mlines.Line2D([], [], color='r',
                                  label='Load duration curve', 
                                  linestyle='--')
ldr = mlines.Line2D([], [], color='b',
                                  label='Logarithmic noise values', 
                                  linestyle='-')

plt.legend(handles=[ demand, ldr],
           bbox_to_anchor=(0.9,-0.05),
    frameon=False, ncol=2,fontsize = 30)