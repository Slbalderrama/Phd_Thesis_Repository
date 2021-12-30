# -*- coding: utf-8 -*-
"""
Created on Tue May 11 15:49:16 2021

@author: Dell
"""


import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

data = pd.read_csv('Data_Espino_Thesis_2.csv', header=0,index_col=0)


pv_test = pd.DataFrame()
pv_test['PV Power 1'] = round(data['PV Power 1'],4)
pv_test['PV Power 2'] = round(data['PV Power 2'],4)
pv_test['PV Power 3'] = round(data['PV Power 3'],4)
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
pv_test['dif 1 to 2'] = abs(pv_test['PV Power 1']  - pv_test['PV Power 2']) 
pv_test['dif 2 to 3'] = abs(pv_test['PV Power 2']  - pv_test['PV Power 3']) 
pv_test['dif 1 to 3'] = abs(pv_test['PV Power 1']  - pv_test['PV Power 3']) 

pv_describe_1  = pv_test.describe()

pv_test_1_1 = pv_test.loc[pv_test['dif 1 to 2']!= 0]
pv_test_1_2 = pv_test.loc[pv_test['dif 1 to 2']!= 0]
pv_test_1_3 = pv_test.loc[pv_test['dif 1 to 2']!= 0]

pv_test_1_001_1 = pv_test.loc[pv_test['dif 1 to 2']>0.01]
pv_test_1_001_2 = pv_test.loc[pv_test['dif 2 to 3']>0.01]
pv_test_1_001_3 = pv_test.loc[pv_test['dif 1 to 3']>0.01]


pv_test_1_005_1 = pv_test.loc[pv_test['dif 1 to 2']>0.05]
pv_test_1_005_2 = pv_test.loc[pv_test['dif 2 to 3']>0.05]
pv_test_1_005_3 = pv_test.loc[pv_test['dif 1 to 3']>0.05]

pv_test_1_01_1 = pv_test.loc[pv_test['dif 1 to 2']>0.1]
pv_test_1_01_2 = pv_test.loc[pv_test['dif 2 to 3']>0.1]
pv_test_1_01_3 = pv_test.loc[pv_test['dif 1 to 3']>0.1]



pv_test_1_05_1 = pv_test.loc[pv_test['dif 1 to 2']>0.5]
pv_test_1_05_2 = pv_test.loc[pv_test['dif 2 to 3']>0.5]
pv_test_1_05_3 = pv_test.loc[pv_test['dif 1 to 3']>0.5]



pv_test_1_1_1 = pv_test.loc[pv_test['dif 1 to 2']>1]
pv_test_1_1_2 = pv_test.loc[pv_test['dif 2 to 3']>1] 
pv_test_1_1_3 = pv_test.loc[pv_test['dif 1 to 3']>1]

pv_test_1_2_1 = pv_test.loc[pv_test['dif 1 to 2']>2]
pv_test_1_2_2 = pv_test.loc[pv_test['dif 2 to 3']>2]
pv_test_1_2_3 = pv_test.loc[pv_test['dif 1 to 3']>2]


a = len(pv_test_1_2_1)/len(pv_test_1_1)
b = len(pv_test_1_2_2)/len(pv_test_1_2)
c = len(pv_test_1_2_3)/len(pv_test_1_3) 
print(((a+b+c)/3)*100)


# only 0.25 % of measurments have a difference of more than 2 kW
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



ax3.plot(pv_hourly.index, pv_hourly['PV Power 1'])
ax3.plot(pv_hourly.index, pv_hourly['PV Power 2'])
ax3.plot(pv_hourly.index, pv_hourly['PV Power 3'])

ax4.plot(pv_hourly.index,  pv_hourly['Bat Soc 1'])
ax4.plot(pv_hourly.index,  pv_hourly['Bat Soc 2'])
ax4.plot(pv_hourly.index, pv_hourly['Bat Soc 3'])

ax4.yaxis.tick_right()
ax4.yaxis.set_label_position('right') 
# limits
# ax.set_xlim([0,1650])
# ax.set_ylim([0,1000])


# ax2.set_xlim([0,1650])
# ax2.set_ylim([0,100])


# labels
ax3.set_xlabel('Hour',size=label_size) 
ax3.set_ylabel('PV Power (kW)',size=label_size) 
ax4.set_ylabel('Irradiation (W)',size=label_size) 
plt.show()

































