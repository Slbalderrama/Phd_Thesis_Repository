# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 14:55:33 2021

@author: Dell
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
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

#%%

# load data

data = pd.read_csv('Data/Data_Espino_Thesis_Fill_2.csv', header=0,index_col=0)
index = pd.DatetimeIndex(start='2016-01-01 00:00:00', periods=166464, freq=('5min'))
data.index = index

pv_curtailment = pd.read_csv('Results/Renewable_Energy_Optimal_Espino.csv', header=0,index_col=0)
pv_curtailment.index = index
data['Curtail Energy'] = pv_curtailment['Optimal PV Power'] - data['PV Power']


#%%

data['hour'] = data.index.hour
data['day'] = data.index.dayofyear
data['day of the month'] = data.index.day
data['year'] = data.index.year
data['month'] = data.index.month

data_hourly = data.groupby(['year','day', 'hour']).mean()
index_hourly = pd.DatetimeIndex(start='2016-01-01 00:00:00', periods=13872, 
                                   freq=('1H'))

data_hourly.index = index_hourly
data_hourly['Bat Power'] = data_hourly['Bat Power out'] - data_hourly['Bat Power in']  
#%%

Label_Distribution = ['From PV to Bat','From Gen to Bat','From PV to Grid', 
                      'From Gen to Grid', 'From Bat to Grid']

Energy_Distribution = pd.DataFrame(index=index_hourly, columns=Label_Distribution)
Rate_PV_Gen = pd.DataFrame(index = index_hourly, columns=['Rate','Rate PV','Rate Gen']) 


for i in Rate_PV_Gen.index:
#        print(i)
        Rate_PV_Gen.loc[i,'Rate'] = (data_hourly.loc[i,'PV Power']/ data_hourly.loc[i,'GenSet Power'])
        Rate_PV_Gen.loc[i,'Rate PV'] = (data_hourly.loc[i,'PV Power']/
                                    (data_hourly.loc[i,'PV Power']+ data_hourly.loc[i,'GenSet Power']))
        Rate_PV_Gen.loc[i,'Rate Gen'] = (1 - Rate_PV_Gen.loc[i,'Rate PV'])
        
        
       
for i in data_hourly.index:
#    print(i)
    if data_hourly['Bat Power'][i] > 0:
        
        Energy_Distribution['From Bat to Grid'][i] = data_hourly['Bat Power'][i]
        Energy_Distribution['From PV to Grid'][i] = data_hourly['PV Power'][i]
        Energy_Distribution['From Gen to Grid'][i] = data_hourly['GenSet Power'][i]
        Energy_Distribution['From PV to Bat'][i] =  0
        Energy_Distribution['From Gen to Bat'][i] =  0

    elif  data_hourly['Bat Power'][i] < 0:
        
        if data_hourly['PV Power'][i] > 0 and data_hourly['GenSet Power'][i]>0:
            
            Energy_Distribution['From Gen to Bat'][i] = -(Rate_PV_Gen['Rate Gen'][i]*data_hourly['Bat Power'][i])                               
            Energy_Distribution['From PV to Bat'][i] = -(Rate_PV_Gen['Rate PV'][i]*data_hourly['Bat Power'][i])                                  
            Energy_Distribution['From PV to Grid'][i] = (Rate_PV_Gen['Rate PV'][i]*data_hourly['Demand'][i])
            Energy_Distribution['From Gen to Grid'][i] = (Rate_PV_Gen['Rate Gen'][i]*data_hourly['Demand'][i])
            Energy_Distribution['From Bat to Grid'][i] = 0   
        
        elif data_hourly['PV Power'][i] > 0 and data_hourly['GenSet Power'][i]==0:
        
                Energy_Distribution['From PV to Bat'][i] = -data_hourly['Bat Power'][i]                                 
                Energy_Distribution['From Gen to Bat'][i] = 0
                Energy_Distribution['From PV to Grid'][i] =  data_hourly['Demand'][i] 
                Energy_Distribution['From Gen to Grid'][i] = 0  
                Energy_Distribution['From Bat to Grid'][i] = 0
        
        elif data_hourly['PV Power'][i] == 0 and data_hourly['GenSet Power'][i]>0:
                
                Energy_Distribution['From PV to Bat'][i] = 0                                  
                Energy_Distribution['From Gen to Bat'][i] = -data_hourly['Bat Power'][i]  
                Energy_Distribution['From PV to Grid'][i] =  0
                Energy_Distribution['From Gen to Grid'][i] = data_hourly['Demand'][i] 
                Energy_Distribution['From Bat to Grid'][i] = 0
                
    elif data_hourly['Bat Power'][i] == 0:
        
                Energy_Distribution['From PV to Bat'][i] = 0                                  
                Energy_Distribution['From Gen to Bat'][i] = 0  
                Energy_Distribution['From PV to Grid'][i] =  Rate_PV_Gen['Rate PV'][i]*data_hourly['Demand'][i]  
                Energy_Distribution['From Gen to Grid'][i] = Rate_PV_Gen['Rate Gen'][i]*data_hourly['Demand'][i]
                Energy_Distribution['From Bat to Grid'][i] = 0   
                
Energy_Distribution['To Grid'] =  (Energy_Distribution['From PV to Grid'] +
                                   Energy_Distribution['From Gen to Grid'] +
                                   Energy_Distribution['From Bat to Grid']) 


Energy_Distribution['To Bat'] = (Energy_Distribution['From PV to Bat'] +
                                 Energy_Distribution['From Gen to Bat']) 


#Energy_Distribution.to_csv('Energy Distribution.csv')

                
#Total_Energy_Distribution  = Energy_Distribution.sum()

#%%

Energy_Production = pd.DataFrame()


Energy_Production.loc['PV Share', 'Share']  = data_hourly['PV Power'].sum()/(data_hourly['PV Power'].sum()
                                                                +data_hourly['GenSet Power'].sum())
Energy_Production.loc['PV Share', 'Share']  = round(Energy_Production.loc['PV Share', 'Share']*100,0)

Energy_Production.loc['GenSet Share', 'Share']  = data_hourly['GenSet Power'].sum()/(data_hourly['PV Power'].sum()
                                                                +data_hourly['GenSet Power'].sum())
Energy_Production.loc['GenSet Share', 'Share' ]  = round(Energy_Production.loc['GenSet Share' , 'Share']*100,0)


To_Battery = pd.DataFrame()


To_Battery.loc['From PV', 'Share'] = Energy_Distribution['From PV to Bat'].sum()/(Energy_Distribution['From PV to Bat'].sum() +
                                                          Energy_Distribution['From Gen to Bat'].sum())

To_Battery.loc['From PV', 'Share'] = round(To_Battery.loc['From PV', 'Share']*100, 0)

To_Battery.loc['From GenSet', 'Share'] = Energy_Distribution['From Gen to Bat'].sum()/(Energy_Distribution['From PV to Bat'].sum() +
                                                          Energy_Distribution['From Gen to Bat'].sum())
To_Battery.loc['From GenSet', 'Share'] = round(To_Battery.loc['From GenSet', 'Share']*100, 0)

From_GenSet = pd.DataFrame()


From_GenSet.loc['To Bat', 'Share'] = Energy_Distribution['From Gen to Bat'].sum()/(Energy_Distribution ['From Gen to Bat'].sum() + 
                                                             Energy_Distribution['From Gen to Grid'].sum())
From_GenSet.loc['To Bat', 'Share'] = round(From_GenSet.loc['To Bat', 'Share']*100, 0)

From_GenSet.loc['To GenSet', 'Share'] = Energy_Distribution ['From Gen to Grid'].sum()/(Energy_Distribution ['From Gen to Bat'].sum() + 
                                                             Energy_Distribution['From Gen to Grid'].sum())           
From_GenSet.loc['To GenSet', 'Share'] = round(From_GenSet.loc['To GenSet', 'Share']*100, 0)



#%%
fig = plt.figure(figsize=(40,30))
label_size = 25
tick_size = 25 
fontsize = '40'

ax1 = fig.add_subplot(131)
wedges1, texts1, autotexts1 = ax1.pie(Energy_Production['Share'], autopct='%1.1f%%')
plt.setp(autotexts1, size=45)

plt.legend(labels=['PV Share', 'GenSet Share'], fontsize=fontsize, bbox_to_anchor=(0.9, 0))

ax2 = fig.add_subplot(132)
wedges2, texts2, autotexts2 = ax2.pie(To_Battery['Share'], autopct='%1.1f%%' )
plt.setp(autotexts2, size=45)
plt.legend(labels=['From PV', 'From GenSet'], fontsize=fontsize, bbox_to_anchor=(0.9, 0))

ax3 = fig.add_subplot(133)
wedges3, texts3, autotexts3 = ax3.pie(From_GenSet['Share'], autopct='%1.1f%%')
plt.setp(autotexts3, size=45)
plt.legend(labels=['To Bat', 'To Grid'], fontsize=fontsize, bbox_to_anchor=(0.9, 0))

plt.show()

#%%


From_PV = pd.DataFrame()


Total_PV_Energy = (Energy_Distribution['From PV to Bat'].sum() 
                    + Energy_Distribution['From PV to Grid'].sum() 
                    + data_hourly['Curtail Energy'].sum())

From_PV.loc['To Battery' ,'Share'] = Energy_Distribution['From PV to Bat'].sum()/Total_PV_Energy
From_PV.loc['To Grid' ,'Share'] = Energy_Distribution['From PV to Bat'].sum()/Total_PV_Energy
From_PV.loc['Curtailment' ,'Share'] = data_hourly['Curtail Energy'].sum()/Total_PV_Energy



To_Grid = pd.DataFrame()

Total_Energy_Grid = (Energy_Distribution['From PV to Grid'].sum() 
                     + Energy_Distribution['From Gen to Grid'].sum() 
                     +  Energy_Distribution['From Bat to Grid'].sum())

To_Grid['From PV'] = Energy_Distribution['From PV to Grid'].sum()/Total_Energy_Grid
To_Grid['From GenSet'] = Energy_Distribution['From Gen to Grid'].sum()/Total_Energy_Grid
To_Grid['From Battery'] = Energy_Distribution['From PV to Grid'].sum()/Total_Energy_Grid




















