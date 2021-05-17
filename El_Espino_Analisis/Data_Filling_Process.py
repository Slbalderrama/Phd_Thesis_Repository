# -*- coding: utf-8 -*-
"""
Created on Mon May 17 15:53:25 2021

@author: Dell
"""


import pandas as pd

data = pd.read_csv('Data_Espino_Thesis.csv', header=0,index_col=0)


Power_Data = pd.DataFrame()


Power_Data['PV Power']  = data['PV Power 1'] + data['PV Power 2'] + data['PV Power 3'] 
Power_Data['Bat Power'] = data['Bat Power 1'] + data['Bat Power 2'] + data['Bat Power 3'] 
Power_Data['GenSet Power'] = data['GenSet Power']
Power_Data['Bat SOC'] = data['Bat Soc 1'] + data['Bat Soc 2'] + data['Bat Soc 3']
Power_Data['Demand'] = Power_Data['PV Power'] + Power_Data['Bat Power'] + Power_Data['GenSet Power']
Power_Data['PV Temperature'] =  data['PV Temperature']
Power_Data['Ambient temperature'] =  data['Ambient temperature']
Power_Data['Solar Irradiation'] =  data['Solar Irradiation']

data_describe  = data.describe() 

index = pd.DatetimeIndex(start='2016-01-01 00:00:00', periods=166464, freq=('5min'))
data.index = index
#%%

# broken data

broken_demand = Power_Data.loc[Power_Data['Demand'] <=0]

percentage_1 = (len(broken_demand)/len(Power_Data))*100
percentage_1 = round(percentage_1, 2)

print('The percentage of points with demand equal or lower to 0 is ' + str(percentage_1) + ' %' )

broken_demand_describe  = broken_demand.describe() 
#%%

broken_PV_power_1 = Power_Data.loc[(Power_Data['PV Power'] == 0) & (Power_Data['Solar Irradiation'] > 0 ) ]

percentage_2 = (len(broken_PV_power_1)/len(Power_Data))*100
percentage_2 = round(percentage_2, 2)

print('The percentage of points were there is sun and not PV power is ' + str(percentage_2) + ' %' )

broken_PV_power_1_describe  = broken_PV_power_1.describe() 
#%%
broken_PV_power_2 = Power_Data.loc[(Power_Data['PV Power'] > 0) & (Power_Data['Solar Irradiation'] == 0 ) ]

percentage_3 = (len(broken_PV_power_2)/len(Power_Data))*100
percentage_3 = round(percentage_3, 2)

print('The percentage of points were there is not sun and there is PV power is ' + str(percentage_3) + ' %' )

broken_PV_power_2_describe  = broken_PV_power_2.describe() 
