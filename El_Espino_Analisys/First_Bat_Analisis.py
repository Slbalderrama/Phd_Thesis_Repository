# -*- coding: utf-8 -*-
"""
Created on Tue May 11 15:49:16 2021

@author: Dell
"""


import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

data = pd.read_csv('Data/Data_Espino_Thesis_2.csv', header=0,index_col=0)



test_bat = pd.DataFrame()

test_bat['Bat Power 1'] = data['Bat Power 1']
test_bat['Bat Power 2'] = data['Bat Power 2']
test_bat['Bat Power 3'] = data['Bat Power 3']
test_bat['Power 2 Bat 1'] = data['Power 2 Bat 1']
test_bat['Power 2 Bat 2'] = data['Power 2 Bat 2']
test_bat['Power 2 Bat 3'] = data['Power 2 Bat 3']


#%%

bat_info_1 = test_bat.info()
# it is important to remeber that bat power, takes in account power in and out of the battery
# The sum show problems in Power 2 bat 3
print(test_bat.sum())
# The mean values, shows that 'Power 2 bat 3' has higher numbers.
print(test_bat.mean())
# higer variation 
print(test_bat.std())

test_bat['dif 1'] = abs(test_bat['Bat Power 1']) - abs(test_bat['Power 2 Bat 1'])
test_bat['dif 2'] = abs(test_bat['Bat Power 2']) - abs(test_bat['Power 2 Bat 2'])
test_bat['dif 3'] = abs(test_bat['Bat Power 3']) - abs(test_bat['Power 2 Bat 3'])

# the inspection shows that Power '2 bat 3' Reachs values higher than 18, many times

# due to the mean, std the value -10 is choosen. There is high varation
# the values of Power 2 Bat 3 cannot be used 

#%%
test_bat_1 = test_bat.loc[test_bat['dif 3']<-10]

# too many "diferences" in Power 2 bat 3 to use it.
#%%

test_bat['Bat Power 1 sign'] = np.sign(test_bat[['Bat Power 1']])
test_bat['Bat Power 2 sign'] = np.sign(test_bat[['Bat Power 2']])
test_bat['Bat Power 3 sign'] = np.sign(test_bat[['Bat Power 3']])

# if a is equal to b and b is equal to c, then a and c are equal

test_bat['1 to 2'] = test_bat['Bat Power 1 sign'] == test_bat['Bat Power 2 sign'] 
test_bat['2 to 3'] = test_bat['Bat Power 2 sign'] == test_bat['Bat Power 3 sign'] 
test_bat['1 to 2 to 3'] = test_bat['1 to 2'] == test_bat['2 to 3']


test_bat_2 = test_bat.loc[test_bat['1 to 2 to 3'] == False]

(len(test_bat_2)/len(data))*100
#Around 99 % of the time the batteries have the same flow sign

#%%
test_bat_describe_2 = test_bat_2.describe()
test_bat_info_2 = test_bat_2.info()

test_bat_3 = data.loc[test_bat['1 to 2 to 3'] == False]

test_bat_3_1 = test_bat_3.loc[test_bat_3['Sunny Island State 3'] == '2: Warning']


test_bat_4 = data.loc[data['Sunny Island State 3'] == '2: Warning']

test_bat['1 to 2 dif'] = abs(abs(test_bat['Bat Power 1']) - abs(test_bat['Bat Power 2'])) 
test_bat['2 to 3 dif'] = abs(abs(test_bat['Bat Power 2']) - abs(test_bat['Bat Power 3']))
test_bat['1 to 3 dif'] = abs(abs(test_bat['Bat Power 1']) - abs(test_bat['Bat Power 3']))

test_bat_5_1 = test_bat.loc[test_bat['1 to 2 dif']>2] 
test_bat_5_2 = test_bat.loc[test_bat['2 to 3 dif']>2] 
test_bat_5_3 = test_bat.loc[test_bat['1 to 3 dif']>2] 

soc_test = pd.DataFrame()

soc_test['Bat Soc 1'] = data['Bat Soc 1']
soc_test['Bat Soc 2'] = data['Bat Soc 2']
soc_test['Bat Soc 3'] = data['Bat Soc 3']

soc_describe = soc_test.describe()
soc_describe.info()

soc_test_0_1 = soc_test.loc[soc_test['Bat Soc 1'] == 0]
soc_test_0_2 = soc_test.loc[soc_test['Bat Soc 2'] == 0]
soc_test_0_3 = soc_test.loc[soc_test['Bat Soc 3'] == 0]


soc_test_40_1 = soc_test.loc[soc_test['Bat Soc 1'] < 40]
soc_test_40_2 = soc_test.loc[soc_test['Bat Soc 2'] < 40]
soc_test_40_3 = soc_test.loc[soc_test['Bat Soc 3'] < 40]

soc_test_48_1 = soc_test.loc[soc_test['Bat Soc 1'] < 48]
soc_test_48_2 = soc_test.loc[soc_test['Bat Soc 2'] < 48]
soc_test_48_3 = soc_test.loc[soc_test['Bat Soc 3'] < 48]


soc_test_50_1 = soc_test.loc[soc_test['Bat Soc 1'] < 50]
soc_test_50_2 = soc_test.loc[soc_test['Bat Soc 2'] < 50]
soc_test_50_3 = soc_test.loc[soc_test['Bat Soc 3'] < 50]

(len(soc_test_50_3)/len(data))*100
(len(soc_test_50_2)/len(data))*100
(len(soc_test_50_1)/len(data))*100

# more than 98 % of the values are above 50 % 

#%%
soc_test.index = pd.to_datetime(soc_test.index)
soc_test['hour'] = soc_test.index.hour

soc_hourly = soc_test.groupby(['hour']).mean()

size = [20,15]
label_size = 25
tick_size = 25 
mpl.rcParams['xtick.labelsize'] = tick_size 
mpl.rcParams['ytick.labelsize'] = tick_size 


fig=plt.figure(figsize=size)
ax=fig.add_subplot(111, label="1")
#ax2=fig.add_subplot(111, label="2", frame_on=False)



ax.plot(soc_hourly.index, soc_hourly['Bat Soc 1'])
ax.plot(soc_hourly.index, soc_hourly['Bat Soc 2'])
ax.plot(soc_hourly.index, soc_hourly['Bat Soc 3'])

#ax2.plot(soc_hourly.index, soc_hourlyy['Solar Irradiation'])
#ax2.plot(index_LDC, data_1['Curtailment Percentage'], c='m')


# ax2.yaxis.tick_right()
# ax2.yaxis.set_label_position('right') 

ax.set_xlabel('Hour',size=label_size) 
ax.set_ylabel('SOC (%)',size=label_size) 

plt.show()

# The state of charge of the battery is relatively uniform during the day

soc_test['1 to 2'] = abs(soc_test['Bat Soc 1'] - soc_test['Bat Soc 2'])
soc_test['2 to 3'] = abs(soc_test['Bat Soc 2'] - soc_test['Bat Soc 3'])
soc_test['1 to 3'] = abs(soc_test['Bat Soc 1'] - soc_test['Bat Soc 3'])

bat_info = test_bat.describe()

soc_test_dif_1_1 = soc_test.loc[soc_test['1 to 2'] < 1]
soc_test_dif_1_2 = soc_test.loc[soc_test['2 to 3'] < 1]
soc_test_dif_1_3 = soc_test.loc[soc_test['1 to 3'] < 1]

soc_test_dif_2_1 = soc_test.loc[soc_test['1 to 2'] < 2]
soc_test_dif_2_2 = soc_test.loc[soc_test['2 to 3'] < 2]
soc_test_dif_2_3 = soc_test.loc[soc_test['1 to 3'] < 2]

soc_test_dif_5_1 = soc_test.loc[soc_test['1 to 2'] < 5]
soc_test_dif_5_2 = soc_test.loc[soc_test['2 to 3'] < 5]
soc_test_dif_5_3 = soc_test.loc[soc_test['1 to 3'] < 5]

soc_test_dif_10_1 = soc_test.loc[soc_test['1 to 2'] < 10]
soc_test_dif_10_2 = soc_test.loc[soc_test['2 to 3'] < 10]
soc_test_dif_10_3 = soc_test.loc[soc_test['1 to 3'] < 10]

soc_test_dif_10_1_mayor = soc_test.loc[soc_test['1 to 2'] > 10]
soc_test_dif_10_2_mayor = soc_test.loc[soc_test['2 to 3'] > 10]
soc_test_dif_10_3_mayor = soc_test.loc[soc_test['1 to 3'] > 10]

soc_test_dif_5_1_mayor = soc_test.loc[soc_test['1 to 2'] > 5]
soc_test_dif_5_2_mayor = soc_test.loc[soc_test['2 to 3'] > 5]
soc_test_dif_5_3_mayor = soc_test.loc[soc_test['1 to 3'] > 5]

# the state of charge is relatively uniform between batteries


