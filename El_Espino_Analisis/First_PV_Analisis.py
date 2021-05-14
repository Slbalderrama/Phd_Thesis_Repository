# -*- coding: utf-8 -*-
"""
Created on Tue May 11 15:49:16 2021

@author: Dell
"""


import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

data = pd.read_csv('Data_Espino_Thesis.csv', header=0,index_col=0)


pv_test = pd.DataFrame()
pv_test['PV Power 1'] = round(data['PV Power 1']/1000,4)
pv_test['PV Power 2'] = round(data['PV Power 2']/1000,4)
pv_test['PV Power 3'] = round(data['PV Power 3']/1000,4)
pv_test['Solar Irradiation'] = data['Solar Irradiation']
pv_test['Bat Soc 1'] = data['Bat Soc 1']
pv_test['Bat Soc 2'] = data['Bat Soc 2']
pv_test['Bat Soc 3'] = data['Bat Soc 3']

#%%
pv_describe  = pv_test.describe()
pv_test.info()

# PV power is quite uniform between arrays

#%%

# estoy aca!
pv_test['dif 1 to 2'] = pv_test['PV Power 1']  - pv_test['PV Power 2'] 
pv_test['dif 1 to 2'] = pv_test['PV Power 1']  - pv_test['PV Power 2'] 
pv_test['dif 1 to 2'] = pv_test['PV Power 1']  - pv_test['PV Power 2'] 

#%%

pv_test.index = pd.to_datetime(pv_test.index)
pv_test['hour'] = pv_test.index.hour
#pv_test['day'] = pv_test.index.day

pv_hourly = pv_test.groupby(['hour']).mean()
#%%
size = [20,15]
label_size = 25
tick_size = 25 
mpl.rcParams['xtick.labelsize'] = tick_size 
mpl.rcParams['ytick.labelsize'] = tick_size 


fig=plt.figure(figsize=size)
ax=fig.add_subplot(111, label="1")
ax2=fig.add_subplot(111, label="2", frame_on=False)



ax.plot(pv_hourly.index, pv_hourly['PV Power 1'])
ax.plot(pv_hourly.index, pv_hourly['PV Power 2'])
ax.plot(pv_hourly.index, pv_hourly['PV Power 3'])

ax2.plot(pv_hourly.index, pv_hourly['Solar Irradiation'])
#ax2.plot(index_LDC, data_1['Curtailment Percentage'], c='m')


ax2.yaxis.tick_right()
ax2.yaxis.set_label_position('right') 
# limits
# ax.set_xlim([0,1650])
# ax.set_ylim([0,1000])


# ax2.set_xlim([0,1650])
# ax2.set_ylim([0,100])


# labels
ax.set_xlabel('Hour',size=label_size) 
ax.set_ylabel('PV Power (kW)',size=label_size) 
ax2.set_ylabel('Irradiation (W)',size=label_size) 
plt.show()

# diference between power peak and irradiation peak

#%%
fig2=plt.figure(figsize=size)
ax3=fig2.add_subplot(111, label="1")
ax4=fig2.add_subplot(111, label="2", frame_on=False)



ax.plot(pv_hourly.index, pv_hourly['PV Power 1'])
ax.plot(pv_hourly.index, pv_hourly['PV Power 2'])
ax.plot(pv_hourly.index, pv_hourly['PV Power 3'])

ax2.plot(pv_hourly.index, pv_hourly['Solar Irradiation'])
#ax2.plot(index_LDC, data_1['Curtailment Percentage'], c='m')


ax2.yaxis.tick_right()
ax2.yaxis.set_label_position('right') 
# limits
# ax.set_xlim([0,1650])
# ax.set_ylim([0,1000])


# ax2.set_xlim([0,1650])
# ax2.set_ylim([0,100])


# labels
ax.set_xlabel('Hour',size=label_size) 
ax.set_ylabel('PV Power (kW)',size=label_size) 
ax2.set_ylabel('Irradiation (W)',size=label_size) 
plt.show()

































