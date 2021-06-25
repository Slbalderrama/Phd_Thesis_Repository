# -*- coding: utf-8 -*-
"""
Created on Mon May 17 15:53:25 2021

@author: Dell
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv('Data/Data_Espino_Thesis_2.csv', header=0,index_col=0)


Power_Data = pd.DataFrame()


Power_Data['PV Power']  = data['PV Power 1'] + data['PV Power 2'] + data['PV Power 3'] 
Power_Data['Bat Power'] = data['Bat Power 1'] + data['Bat Power 2'] + data['Bat Power 3'] 
Power_Data['GenSet_Power'] = data['GenSet Power']
Power_Data['GenSet Power 2'] = Power_Data.GenSet_Power.where(Power_Data.GenSet_Power > 0, 
                                                             other= 0)

Power_Data['SOC'] = (data['Bat Soc 1'] + data['Bat Soc 2'] + data['Bat Soc 3'])/3
Power_Data['Demand'] = (Power_Data['PV Power'] + Power_Data['Bat Power'] 
                        + Power_Data['GenSet Power 2'])
Power_Data['PV Temperature'] =  data['PV Temperature']
Power_Data['Ambient temperature'] =  data['Ambient temperature']
Power_Data['Solar Irradiation'] =  data['Solar Irradiation']

Power_Data_Describe_1  = Power_Data.describe() 

index = pd.DatetimeIndex(start='2016-01-01 00:00:00', periods=166464, freq=('5min'))
Power_Data.index = index
#%%

# broken data

broken_demand = Power_Data.loc[Power_Data['Demand'] <=0]

percentage_1 = (len(broken_demand)/len(Power_Data))*100
percentage_1 = round(percentage_1, 4)

print('The percentage of points with demand equal or lower to 0 is ' + str(percentage_1) + ' %' )

broken_demand_describe  = broken_demand.describe() 
#%%

broken_PV_power_1 = Power_Data.loc[(Power_Data['PV Power'] == 0) & (Power_Data['Solar Irradiation'] > 0 ) ]

percentage_2 = (len(broken_PV_power_1)/len(Power_Data))*100
percentage_2 = round(percentage_2, 4)

print('The percentage of points were there is sun and not PV power is ' + str(percentage_2) + ' %' )

broken_PV_power_1_describe  = broken_PV_power_1.describe() 
#%%
broken_PV_power_2 = Power_Data.loc[(Power_Data['PV Power'] > 0) & (Power_Data['Solar Irradiation'] == 0 ) ]

percentage_3 = (len(broken_PV_power_2)/len(Power_Data))*100
percentage_3 = round(percentage_3, 4)

print('The percentage of points were there is not sun and there is PV power is ' + str(percentage_3) + ' %' )

broken_PV_power_2_describe  = broken_PV_power_2.describe() 



#%%


for i in Power_Data.index[0:2016]:
    if Power_Data['Demand'][i] <= 0:
        Power_Data.loc[i,'Demand 2'] = Power_Data.loc[i+288,'Demand']
        
#        print(i)
        if Power_Data['Solar Irradiation'][i] == 0:
            Power_Data.loc[i,'Solar Irradiation 2'] = Power_Data.loc[i+288,'Solar Irradiation']
        else:
            Power_Data.loc[i, 'Solar Irradiation'] = Power_Data.loc[i, 'Solar Irradiation']
        if Power_Data['PV Temperature'][i] == 0:
            Power_Data.loc[i, 'PV Temperature 2'] = Power_Data.loc[i+288,'PV Temperature']
        else:
            Power_Data.loc[i,'PV Temperature 2'] = Power_Data.loc[i,'PV Temperature']
            
    else:
        Power_Data.loc[i,'Demand 2'] = Power_Data.loc[i,'Demand']
        Power_Data.loc[i,'Solar Irradiation 2'] = Power_Data.loc[i, 'Solar Irradiation']
        Power_Data.loc[i,'PV Temperature 2'] = Power_Data.loc[i,'PV Temperature']
    
for i in Power_Data.index[2016:164448]:
#    print(i)
    if Power_Data['Demand'][i] <= 0:
        Power_Data.loc[i,'Demand 2'] = Power_Data.loc[i-2016,'Demand']
        if Power_Data['Solar Irradiation'][i] == 0:
            Power_Data.loc[i, 'Solar Irradiation 2'] = Power_Data.loc[i-2016, 'Solar Irradiation']
        else:
            Power_Data.loc[i, 'Solar Irradiation 2'] = Power_Data.loc[i, 'Solar Irradiation']
        if Power_Data['PV Temperature'][i] == 0:
            Power_Data.loc[i,'PV Temperature 2'] = Power_Data.loc[i-2016,'PV Temperature']
        else:
            Power_Data.loc[i,'PV Temperature 2'] = Power_Data.loc[i,'PV Temperature']

    else:
        Power_Data.loc[i,'Demand 2'] = Power_Data.loc[i,'Demand']
        Power_Data.loc[i, 'Solar Irradiation 2'] = Power_Data.loc[i, 'Solar Irradiation']
        Power_Data.loc[i,'PV Temperature 2'] = Power_Data.loc[i,'PV Temperature']        

for i in Power_Data.index[164448:]:
#    print(i)
    if Power_Data['Demand'][i] <= 0:
        Power_Data.loc[i, 'Demand 2'] = Power_Data.loc[i-288, 'Demand']
        if Power_Data['Solar Irradiation'][i] == 0:
            Power_Data.loc[i, 'Solar Irradiation 2'] = Power_Data.loc[i-288, 'Solar Irradiation']
        else:
            Power_Data.loc[i, 'Solar Irradiation 2'] = Power_Data.loc[i, 'Solar Irradiation']
        if Power_Data['PV Temperature'][i] == 0:
            Power_Data.loc[i,'PV Temperature 2'] = Power_Data.loc[i-288, 'PV Temperature']
        else:
            Power_Data.loc[i,'PV Temperature 2'] = Power_Data.loc[i, 'PV Temperature']

    else:
        Power_Data.loc[i,'Demand 2'] = Power_Data.loc[i,'Demand']
        Power_Data.loc[i, 'Solar Irradiation 2'] = Power_Data.loc[i,'Solar Irradiation']
        Power_Data.loc[i,'PV Temperature 2'] = Power_Data.loc[i,'PV Temperature']


#%%
# broken data

broken_demand_1 = Power_Data.loc[Power_Data['Demand 2'] <=0]

percentage_4 = (len(broken_demand_1)/len(Power_Data))*100
percentage_4 = round(percentage_4, 4)

print('The percentage of points with demand equal or lower to 0 is ' + str(percentage_4) + ' %' )

broken_demand_describe_1  = broken_demand_1.describe() 
#%%

# broken_PV_power_3 = Power_Data.loc[(Power_Data['PV Power 2'] == 0) & (Power_Data['Solar Irradiation 2'] > 0 ) ]

# percentage_5 = (len(broken_PV_power_3)/len(Power_Data))*100
# percentage_5 = round(percentage_5, 2)

# print('The percentage of points were there is sun and not PV power is ' + str(percentage_5) + ' %' )

# broken_PV_power_1_describe_3  = broken_PV_power_3.describe() 
# #%%
# broken_PV_power_4 = Power_Data.loc[(Power_Data['PV Power 2'] > 0) & (Power_Data['Solar Irradiation 2'] == 0 ) ]

# percentage_6 = (len(broken_PV_power_4)/len(Power_Data))*100
# percentage_6 = round(percentage_6, 2)

# print('The percentage of points were there is not sun and there is PV power is ' + str(percentage_6) + ' %' )

# broken_PV_power_2_describe_4  = broken_PV_power_4.describe() 

#%%


a = broken_demand_1.index
b = a+1
c = a-1

Power_Data.loc[a,'Demand 2'] = (Power_Data['Demand 2'][b] + Power_Data['Demand 2'][c])/2

#%%

Power_Data['Bat Power in'] = -Power_Data['Bat Power'].where(
                                                    Power_Data['Bat Power']<0,0)
    
Power_Data['Bat Power out'] = Power_Data['Bat Power'].where(
                                                    Power_Data['Bat Power']>0,0)



#%%
# broken data

broken_demand_2 = Power_Data.loc[Power_Data['Demand 2'] <=0]

percentage_7 = (len(broken_demand_2)/len(Power_Data))*100
percentage_7 = round(percentage_7, 4)

print('The percentage of points with demand equal or lower to 0 is ' + str(percentage_7) + ' %' )

#%%

Power_Data_2 = Power_Data.drop(['Demand', 'Solar Irradiation' , 
                                'PV Temperature', 'Bat Power', 
                                'GenSet_Power'], axis =1)

Power_Data_2.columns = ['PV Power', 'GenSet Power', 'SOC', 'Ambient temperature', 'Demand',
       'Solar Irradiation', 'PV Temperature 2', 'Bat Power in',  'Bat Power out']


for i in Power_Data_2.index:
    a = i.hour
    if a==4:
        if Power_Data_2.loc[i,'Solar Irradiation']>0:
             Power_Data_2.loc[i,'Solar Irradiation']=0

Power_Data_2.to_csv('Data/Data_Espino_Thesis_Fill_2.csv')


#%%


Power_Data_Describe_2  = Power_Data_2.describe() 

Power_Data_old  = pd.read_csv('Data/Data_Espino_Thesis_Fill.csv', header=0,
                               index_col=0)
Power_Data_old.index = index
Power_Data_old_Describe  = Power_Data_old.describe() 
#%%

data_slice_new =  Power_Data_2['2017-01-05 00:00:00':'2017-01-05 23:55:00']
    
data_slice_old =  Power_Data_old['2017-01-05 00:00:00':'2017-01-05 23:55:00']    
    
data_slice_new_describe = data_slice_new.describe()    
data_slice_old_describe = data_slice_old.describe()


data_slice_new['Demand'].plot(c='b')
data_slice_old['Demand'].plot(c='y')
plt.show()

#%%

data_slice_new_2 =  Power_Data_2['2017-01-01 00:00:00':'2017-01-31 23:55:00']
    
data_slice_old_2 =  Power_Data_old['2017-01-01 00:00:00':'2017-01-31 23:55:00']    
    
data_slice_new_describe_2 = data_slice_new.describe()    
data_slice_old_describe_2 = data_slice_old.describe()


demand_2 = pd.DataFrame()

demand_2['Demand new'] = data_slice_new_2['Demand']
demand_2['Demand old'] = data_slice_old_2['Demand'] 
demand_2['hour'] = demand_2.index.hour
demand_2_Daily = demand_2.groupby(['hour']).mean()   

demand_2_Daily['Demand new'].plot(c='b')
demand_2_Daily['Demand old'].plot(c='y')
plt.show()

demand_2_Daily['diff'] = demand_2_Daily['Demand new'] - demand_2_Daily['Demand old']

demand_2_Daily['Percentage'] = ((demand_2_Daily['Demand new'] - demand_2_Daily['Demand old'])/demand_2_Daily['Demand new'])*100

#%%
New_LDR = data_slice_new_2.sort_values('Demand', ascending=False)
Old_LDR = data_slice_old_2.sort_values('Demand', ascending=False)


index_LDR = []
for i in range(len(Old_LDR )):
        index_LDR.append((i+1)/float(len(Old_LDR ))*100)
        
Old_LDR.index = index_LDR
New_LDR.index = index_LDR

New_LDR['Demand'].plot(c='b')
Old_LDR['Demand'].plot(c='y')


plt.show()













