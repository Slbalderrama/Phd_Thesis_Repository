# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 14:55:33 2021

Energy distribution and Sankey plot

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
from plotly.offline import plot
#%%

# load data

data = pd.read_csv('Data/Data_Espino_Thesis_Fill_2.csv', header=0,index_col=0)
data2 = pd.read_csv('Data/Data_Espino_Thesis_2.csv', header=0,index_col=0)
pv_curtailment = pd.read_csv('Results/Renewable_Energy_Optimal_Espino.csv', header=0,index_col=0)

index = pd.DatetimeIndex(start='2016-01-01 00:00:00', periods=166464, freq=('5min'))
data.index = index
data2.index = index
pv_curtailment.index = index

#%%

# take out the added values in the filling process

fill = data2.loc[data2['Bat Soc 1']==0]

data = data.drop(fill.index)
pv_curtailment = pv_curtailment.drop(fill.index)


#%%

data['Bat Power'] = data['Bat Power out'] - data['Bat Power in']  
data['Curtail Energy'] = pv_curtailment['Optimal PV Power'] - data['PV Power']

test_pv = pd.DataFrame()

test_pv['Optimal PV Power'] = pv_curtailment['Optimal PV Power']
test_pv['PV Power'] = data['PV Power']
test_pv['Curtail Power'] = pv_curtailment['Optimal PV Power'] - data['PV Power']

negative_curtail = test_pv.loc[test_pv['Curtail Power']<0]

# ther is a big difference, the only good comparision is in absolute numbers

#%%

Label_Distribution = ['From PV to Bat','From Gen to Bat','From PV to Grid', 
                      'From Gen to Grid', 'From Bat to Grid']

Energy_Distribution = pd.DataFrame(index=data.index, columns=Label_Distribution)
Rate_PV_Gen = pd.DataFrame(index = data.index, columns=['Rate','Rate PV','Rate Gen']) 



Rate_PV_Gen['Rate'] = (data['PV Power']/ data['GenSet Power'])
Rate_PV_Gen['Rate PV'] = (data['PV Power']/(data['PV Power']+ data['GenSet Power']))
Rate_PV_Gen['Rate Gen'] = (1 - Rate_PV_Gen['Rate PV'])
        
        
       
for i in data.index:
    print(i)
    if data['Bat Power'][i] > 0:
        
        Energy_Distribution['From Bat to Grid'][i] = data['Bat Power'][i]/12
        Energy_Distribution['From PV to Grid'][i] = data['PV Power'][i]/12
        Energy_Distribution['From Gen to Grid'][i] = data['GenSet Power'][i]/12
        Energy_Distribution['From PV to Bat'][i] =  0
        Energy_Distribution['From Gen to Bat'][i] =  0

    elif  data['Bat Power'][i] < 0:
        
        if data['PV Power'][i] > 0 and data['GenSet Power'][i]>0:
            
            Energy_Distribution['From Gen to Bat'][i] = -(Rate_PV_Gen['Rate Gen'][i]*data['Bat Power'][i])/12                               
            Energy_Distribution['From PV to Bat'][i] = -(Rate_PV_Gen['Rate PV'][i]*data['Bat Power'][i])/12                                  
            Energy_Distribution['From PV to Grid'][i] = (Rate_PV_Gen['Rate PV'][i]*data['Demand'][i])/12
            Energy_Distribution['From Gen to Grid'][i] = (Rate_PV_Gen['Rate Gen'][i]*data['Demand'][i])/12
            Energy_Distribution['From Bat to Grid'][i] = 0   
        
        elif data['PV Power'][i] > 0 and data['GenSet Power'][i]==0:
        
                Energy_Distribution['From PV to Bat'][i] = -data['Bat Power'][i]/12                                 
                Energy_Distribution['From Gen to Bat'][i] = 0
                Energy_Distribution['From PV to Grid'][i] =  data['Demand'][i]/12 
                Energy_Distribution['From Gen to Grid'][i] = 0  
                Energy_Distribution['From Bat to Grid'][i] = 0
        
        elif data['PV Power'][i] == 0 and data['GenSet Power'][i]>0:
                
                Energy_Distribution['From PV to Bat'][i] = 0                                  
                Energy_Distribution['From Gen to Bat'][i] = -data['Bat Power'][i]/12  
                Energy_Distribution['From PV to Grid'][i] =  0
                Energy_Distribution['From Gen to Grid'][i] = data['Demand'][i]/12 
                Energy_Distribution['From Bat to Grid'][i] = 0
                
    elif data['Bat Power'][i] == 0:
        
                Energy_Distribution['From PV to Bat'][i] = 0                                  
                Energy_Distribution['From Gen to Bat'][i] = 0  
                Energy_Distribution['From PV to Grid'][i] =  Rate_PV_Gen['Rate PV'][i]*data['Demand'][i]/12  
                Energy_Distribution['From Gen to Grid'][i] = Rate_PV_Gen['Rate Gen'][i]*data['Demand'][i]/12
                Energy_Distribution['From Bat to Grid'][i] = 0   
                
Energy_Distribution['To Grid'] =  (Energy_Distribution['From PV to Grid'] +
                                   Energy_Distribution['From Gen to Grid'] +
                                   Energy_Distribution['From Bat to Grid']) 


Energy_Distribution['To Bat'] = (Energy_Distribution['From PV to Bat'] +
                                 Energy_Distribution['From Gen to Bat']) 


Energy_Distribution_Describe = Energy_Distribution.describe()


#
#Energy_Distribution.to_csv('Energy Distribution.csv')

                
Total_Energy_Distribution  = Energy_Distribution.sum()


test = pd.DataFrame()
test['To Grid'] = Energy_Distribution['To Grid']
test['Demand'] = data['Demand']/12
test['dif'] = abs(test['To Grid'] - test['Demand'])
print('Summation of the values of the demand')
print(test.sum())
print('Nan values')
print(test.isna().sum())

test1 = pd.DataFrame()
test1['To Bat'] = Energy_Distribution['To Bat']
test1['Bat Power in'] = data['Bat Power in']/12
test1['dif'] = abs(test1['To Bat'] - test1['Bat Power in'])
print('Summation of the values of the Battery')
print(test1.sum())
print('Nan values')
print(test1.isna().sum())

#%%

Energy_Production = pd.DataFrame()

Total_Energy_Production = (data['PV Power'].sum()+data['GenSet Power'].sum())/12

Energy_Production.loc['PV Share', 'Share']  = (data['PV Power'].sum()/12)/Total_Energy_Production
Energy_Production.loc['PV Share', 'Share']  = round(Energy_Production.loc['PV Share', 'Share']*100,0)

Energy_Production.loc['GenSet Share', 'Share']  = (data['GenSet Power'].sum()/12)/Total_Energy_Production
Energy_Production.loc['GenSet Share', 'Share' ]  = round(Energy_Production.loc['GenSet Share' , 'Share']*100,0)


To_Battery = pd.DataFrame()

Total_Energy_Battery = (Energy_Distribution['From PV to Bat'].sum() + Energy_Distribution['From Gen to Bat'].sum())

To_Battery.loc['From PV', 'Share'] = Energy_Distribution['From PV to Bat'].sum()/Total_Energy_Battery

To_Battery.loc['From PV', 'Share'] = round(To_Battery.loc['From PV', 'Share']*100, 0)

To_Battery.loc['From GenSet', 'Share'] = Energy_Distribution['From Gen to Bat'].sum()/Total_Energy_Battery
To_Battery.loc['From GenSet', 'Share'] = round(To_Battery.loc['From GenSet', 'Share']*100, 0)

From_GenSet = pd.DataFrame()

Total_Energy_GenSet = (Energy_Distribution ['From Gen to Bat'].sum() + Energy_Distribution['From Gen to Grid'].sum())/12
From_GenSet.loc['To Bat', 'Share'] = Energy_Distribution['From Gen to Bat'].sum()/Total_Energy_GenSet
From_GenSet.loc['To Bat', 'Share'] = round(From_GenSet.loc['To Bat', 'Share']*100, 0)

From_GenSet.loc['To GenSet', 'Share'] = Energy_Distribution ['From Gen to Grid'].sum()/Total_Energy_GenSet          
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
                    + (data['Curtail Energy'].sum()/12))


test2 = pd.DataFrame()
test2['PV 1'] = (Energy_Distribution['From PV to Bat']
                    + Energy_Distribution['From PV to Grid'] 
                    + data['Curtail Energy']/12)
test2['PV'] = pv_curtailment ['Optimal PV Power']/12
test2['dif'] = abs(test2['PV 1'] - test2['PV'])
print('Summation of the values of the PV')
print(test2.sum())
print('Nan values')
print(test2.isna().sum())




From_PV.loc['To Battery' ,'Share'] = Energy_Distribution['From PV to Bat'].sum()/Total_PV_Energy
From_PV.loc['To Battery' ,'Share'] = round(From_PV.loc['To Battery' ,'Share']*100, 0)

From_PV.loc['To Grid' ,'Share'] =  Energy_Distribution['From PV to Grid'].sum()/Total_PV_Energy
From_PV.loc['To Grid' ,'Share'] = round(From_PV.loc['To Grid' ,'Share']*100, 0)

From_PV.loc['Curtailment' ,'Share'] = (data['Curtail Energy'].sum()/12)/Total_PV_Energy
From_PV.loc['Curtailment' ,'Share'] = round(From_PV.loc['Curtailment' ,'Share']*100, 0)


print('The percentage of energy going to the Battery from the PV is ' + str(From_PV.loc['To Battery' ,'Share']) + ' %')
print('The percentage of energy going to the grid from the PV is ' + str(From_PV.loc['To Grid' ,'Share']) + ' %')
print('The percentage of energy curtail from the PV is ' + str(From_PV.loc['Curtailment' ,'Share']) + ' %')

To_Grid = pd.DataFrame()

Total_Energy_Grid = (Energy_Distribution['From PV to Grid'].sum() 
                     + Energy_Distribution['From Gen to Grid'].sum() 
                     +  Energy_Distribution['From Bat to Grid'].sum())

To_Grid.loc['From PV','Share'] = Energy_Distribution['From PV to Grid'].sum()/Total_Energy_Grid
To_Grid.loc['From PV','Share'] = round(To_Grid.loc['From PV','Share']*100, 0)

To_Grid.loc['From GenSet','Share'] = Energy_Distribution['From Gen to Grid'].sum()/Total_Energy_Grid
To_Grid.loc['From GenSet','Share'] = round(To_Grid.loc['From GenSet','Share']*100, 0)

To_Grid.loc['From Battery','Share'] = Energy_Distribution['From Bat to Grid'].sum()/Total_Energy_Grid
To_Grid.loc['From Battery','Share'] = round(To_Grid.loc['From Battery','Share']*100, 0)

print('The percentage of energy going to the grid from the PV is ' + str(To_Grid.loc['From PV','Share']) + ' %')
print('The percentage of energy going to the grid from the genset is ' + str(To_Grid.loc['From GenSet','Share']) + ' %')
print('The percentage of energy going to the grid from the battery ' + str(To_Grid.loc['From Battery','Share']) + ' %')


#%%

# Diesel compsuption load data

Diesel_Comsuption = pd.read_excel('Data/Diesel_Comsuption.xls',index_col=0)
Diesel_Comsuption = Diesel_Comsuption.fillna(0)
Diesel_Comsuption = Diesel_Comsuption[:-1]
Diesel_Comsuption.index =  pd.to_datetime(Diesel_Comsuption.index)
LHV = 9.9


#%%
Start = '2017-01-01 00:05:00'
end = '2017-06-30 23:55:00'

Sankey_Data = pd.Series()
Sankey_Data['Solar energy'] = data['Solar Irradiation'][Start:end].sum()
Sankey_Data['Solar energy'] = round(Sankey_Data['Solar energy'], 0)/1000000

Sankey_Data['PV energy'] =  data['PV Power'][Start:end].sum()
Sankey_Data['PV energy'] = round(Sankey_Data['PV energy'],0)/(1000*12)

Sankey_Data['PV losses'] = Sankey_Data['Solar energy'] - Sankey_Data['PV energy']

Sankey_Data['From PV to Bat'] = Energy_Distribution['From PV to Bat'][Start:end].sum()
Sankey_Data['From PV to Bat'] = round(Sankey_Data['From PV to Bat'],1)/(1000)

Sankey_Data['From PV to Grid'] = Energy_Distribution['From PV to Grid'][Start:end].sum()
Sankey_Data['From PV to Grid'] = round(Sankey_Data['From PV to Grid'],1)/1000

Sankey_Data['Curtailment'] = (data['Curtail Energy'][Start:end].sum())/(1000*12)

Sankey_Data['From Gen to Bat'] = Energy_Distribution['From Gen to Bat'][Start:end].sum()
Sankey_Data['From Gen to Bat'] = round(Sankey_Data['From Gen to Bat'],1)/1000

Sankey_Data['From Gen to Grid'] = Energy_Distribution['From Gen to Grid'][Start:end].sum()
Sankey_Data['From Gen to Grid'] = round(Sankey_Data['From Gen to Grid'],1)/1000

Sankey_Data['Gen generation'] = (Sankey_Data['From Gen to Grid'] 
                                + Sankey_Data['From Gen to Bat'])

Sankey_Data['Diesel'] = Diesel_Comsuption['Diesel'].sum()*LHV
Sankey_Data['Diesel'] = round(Sankey_Data['Diesel']/1000,1)

Sankey_Data['Gen Losses'] = Sankey_Data['Diesel'] - Sankey_Data['Gen generation']

Sankey_Data['Battery In'] =  Sankey_Data['From Gen to Bat'] + Sankey_Data['From PV to Bat']

Sankey_Data['From Bat to Grid'] = Energy_Distribution['From Bat to Grid'][Start:end].sum()
Sankey_Data['From Bat to Grid'] = round(Sankey_Data['From Bat to Grid'],1)/1000

Sankey_Data['Battery Losses'] = Sankey_Data['Battery In'] - Sankey_Data['From Bat to Grid']  

TITLE =  'Energy Flow'
############################# Sankey Draw #####################################


#%%
Sankey_Data_2 = pd.DataFrame()

Sankey_Data_2['Labels'] = ['PV', # 0 
                           'Diesel', # 1 
                           'Battery', # 2 
                           'GenSet', # 3
                           'Grid', # 4
                           'Losses in the battery', # 5 
                           'Losses by combustion', # 6
                           'Curtailment'] # 7

Sankey_Data_2['Color'] = ['rgba(31, 119, 180, 0.8)',
                          'rgba(255, 127, 14, 0.8)',
                    'rgba(44, 160, 44, 0.8)','rgba(214, 39, 40, 0.8)',
                    'rgba(148, 103, 189, 0.8)','rgba(140, 86, 75, 0.8)',
                    'rgba(227, 119, 194, 0.8)','rgba(200, 119, 194, 0.8)']

Sankey_Data_3 = pd.DataFrame()

Sankey_Data_3['Source'] = [0,0,
                           1,
                           3,3,3,2,2,0]

Sankey_Data_3['Target'] = [2,4,
                           3,
                           2,6,4,4,5,7]

Sankey_Data_3['Values']=[Sankey_Data['From PV to Bat'], # 0 2
                         Sankey_Data['From PV to Grid'], # 0 4
                         Sankey_Data['Diesel'], # 1 3 
                         Sankey_Data['From Gen to Bat'], # 3 2
                         Sankey_Data['Gen Losses'] , # 3 6
                         Sankey_Data['From Gen to Grid'], # 3 4
                         Sankey_Data['From Bat to Grid'], # 2 4
                         Sankey_Data['Battery Losses'], # 2 5
                         Sankey_Data['Curtailment']] # 0 7


Sankey_Data_3['Label'] = ['40',
                          '',
                          '',
                          '',
                          '',
                          '',
                          '',
                          '',
                          '']

Sankey_Data_3['Color'] = ['rgba(44, 160, 44, 0.8)',
                          'rgba(148, 103, 189, 0.8)',
                          'rgba(214, 39, 40, 0.8)',
                          'rgba(44, 160, 44, 0.8)',
                          'rgba(227, 119, 194, 0.8)',
                          'rgba(148, 103, 189, 0.8)',
                          'rgba(148, 103, 189, 0.8)',
                          'rgba(140, 86, 75, 0.8)',
                          'rgba(200, 119, 194, 0.8)']

data_trace = dict(
    type='sankey',
    domain = dict(
      x =  [0,1],
      y =  [0,1]
    ),
    orientation = "h",
    valueformat = ".0f",
    size = 100,
    valuesuffix = "MWh",
    node = dict(
      pad = 100,
      thickness = 10,
      line = dict(
        color = "White",
        width = 0.5
      ),
      label =  Sankey_Data_2['Labels'],
      color =  Sankey_Data_2['Color']
    ),
    link = dict(
      source =  Sankey_Data_3['Source'],
      target =  Sankey_Data_3['Target'],
      value =  Sankey_Data_3['Values'],
      label =  Sankey_Data_3['Label'],
      color =  Sankey_Data_3['Color']
  ))


fig = dict(data=[data_trace])
plot(fig, validate = False)




