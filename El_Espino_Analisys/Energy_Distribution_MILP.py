# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 14:55:33 2021

Energy distribution and Sankey plot

@author: Dell
"""


import pandas as pd
import matplotlib.lines as mlines
from plotly.offline import plot
#%%

# load data

data_raw =  pd.read_excel('optimizations_results/MILP_Renewable_18/Results/Results.xls',sheet_name= 'Time Series'
                                  ,index_col=0,Header=None)
j= 3

re = 'Renewable Energy '+str(j) + ' (kWh)'
bat_out ='Battery Flow Out '+str(j) + ' (kWh)' 
bat_in = 'Battery Flow in '+str(j) + ' (kWh)'
cu ='Curtailment '+str(j) + ' (kWh)'
de = 'Energy Demand '+str(j) + ' (kWh)'
soc = 'SOC '+str(j) + ' (kWh)'
ge ='Gen energy '+str(j) + ' (kWh)'

data = pd.DataFrame()
data['PV Power'] = data_raw[re] - data_raw[cu]
data['GenSet Power'] = data_raw[ge]
data['Demand'] = data_raw[de]
data['Bat Power in'] = data_raw[bat_in]
data[ 'Bat Power out'] = data_raw[bat_out]
data['Curtail Energy'] = data_raw[cu]
data['Bat Power'] = data['Bat Power out'] - data['Bat Power in']  

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
        
        Energy_Distribution['From Bat to Grid'][i] = data['Bat Power'][i]
        Energy_Distribution['From PV to Grid'][i] = data['PV Power'][i]
        Energy_Distribution['From Gen to Grid'][i] = data['GenSet Power'][i]
        Energy_Distribution['From PV to Bat'][i] =  0
        Energy_Distribution['From Gen to Bat'][i] =  0

    elif  data['Bat Power'][i] < 0:
        
        if data['PV Power'][i] > 0 and data['GenSet Power'][i]>0:
            
            Energy_Distribution['From Gen to Bat'][i] = -(Rate_PV_Gen['Rate Gen'][i]*data['Bat Power'][i])                               
            Energy_Distribution['From PV to Bat'][i] = -(Rate_PV_Gen['Rate PV'][i]*data['Bat Power'][i])                                
            Energy_Distribution['From PV to Grid'][i] = (Rate_PV_Gen['Rate PV'][i]*data['Demand'][i])
            Energy_Distribution['From Gen to Grid'][i] = (Rate_PV_Gen['Rate Gen'][i]*data['Demand'][i])
            Energy_Distribution['From Bat to Grid'][i] = 0   
        
        elif data['PV Power'][i] > 0 and data['GenSet Power'][i]==0:
        
                Energy_Distribution['From PV to Bat'][i] = -data['Bat Power'][i]       
                Energy_Distribution['From Gen to Bat'][i] = 0
                Energy_Distribution['From PV to Grid'][i] =  data['Demand'][i] 
                Energy_Distribution['From Gen to Grid'][i] = 0  
                Energy_Distribution['From Bat to Grid'][i] = 0
        
        elif data['PV Power'][i] == 0 and data['GenSet Power'][i]>0:
                
                Energy_Distribution['From PV to Bat'][i] = 0                                  
                Energy_Distribution['From Gen to Bat'][i] = -data['Bat Power'][i]  
                Energy_Distribution['From PV to Grid'][i] =  0
                Energy_Distribution['From Gen to Grid'][i] = data['Demand'][i]
                Energy_Distribution['From Bat to Grid'][i] = 0
                
    elif data['Bat Power'][i] == 0:
        
                Energy_Distribution['From PV to Bat'][i] = 0                                  
                Energy_Distribution['From Gen to Bat'][i] = 0  
                Energy_Distribution['From PV to Grid'][i] =  Rate_PV_Gen['Rate PV'][i]*data['Demand'][i]  
                Energy_Distribution['From Gen to Grid'][i] = Rate_PV_Gen['Rate Gen'][i]*data['Demand'][i]
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
test['Demand'] = data['Demand']
test['dif'] = abs(test['To Grid'] - test['Demand'])
print('Summation of the values of the demand')
print(test.sum())
print('Nan values')
print(test.isna().sum())

test1 = pd.DataFrame()
test1['To Bat'] = Energy_Distribution['To Bat']
test1['Bat Power in'] = data['Bat Power in']
test1['dif'] = abs(test1['To Bat'] - test1['Bat Power in'])
print('Summation of the values of the Battery')
print(test1.sum())
print('Nan values')
print(test1.isna().sum())

#%%

Energy_Production = pd.DataFrame()

Total_Energy_Production = (data['PV Power'].sum()+data['GenSet Power'].sum())

Energy_Production.loc['PV Share', 'Share']  = (data['PV Power'].sum())/Total_Energy_Production
Energy_Production.loc['PV Share', 'Share']  = round(Energy_Production.loc['PV Share', 'Share']*100,0)

Energy_Production.loc['GenSet Share', 'Share']  = (data['GenSet Power'].sum())/Total_Energy_Production
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

From_PV = pd.DataFrame()


Total_PV_Energy = (Energy_Distribution['From PV to Bat'].sum() 
                    + Energy_Distribution['From PV to Grid'].sum())


test2 = pd.DataFrame()
test2['PV 1'] = (Energy_Distribution['From PV to Bat']
                    + Energy_Distribution['From PV to Grid'] +
                   data['Curtail Energy']*Rate_PV_Gen['Rate PV'] )
test2['PV'] = data['PV Power'] 
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


test3= pd.DataFrame()

test3['Gen'] = data['GenSet Power']
test3['Gen 1'] = (Energy_Distribution['From Gen to Grid'] +
                  Energy_Distribution['From Gen to Bat'])
test3['diff'] = test3['Gen'] - test3['Gen 1']

print('Summation of the values of the Gen')
print(test3.sum())
print('Nan values')
print(test3.isna().sum())
#%%


test3= pd.DataFrame()

test3['Gen'] = data['GenSet Power']
test3['Gen 1'] = (Energy_Distribution['From Gen to Grid'] +
                  Energy_Distribution['From Gen to Bat'])
test3['diff'] = test3['Gen'] - test3['Gen 1']

print('Summation of the values of the Gen')
print(test3.sum())
print('Nan values')
print(test3.isna().sum())


#%%


test4 = pd.DataFrame()

test4['Bat in'] = data['Bat Power in']
test4['To Bat'] = (Energy_Distribution['From Gen to Grid'] +
                  Energy_Distribution['From Gen to Bat'])
test4['diff'] = test3['Gen'] - test3['Gen 1']

print('Summation of the values of the Gen')
print(test3.sum())
print('Nan values')
print(test3.isna().sum())


#%%

# Diesel compsuption 
data_gen =  pd.read_excel('optimizations_results/MILP_Renewable_18/Results/Results.xls',sheet_name= 'Generator Time Series'
                                  ,index_col=0,Header=None)
ge_cost = 'Fuel Cost ' +str(j) + ' 1 (USD)'

data['Diesel'] = data_gen[ge_cost]/0.8
LHV = 9.9


#%%
Start = data.index[0]
end = data.index[-1]

Sankey_Data = pd.Series()
# Sankey_Data['Solar energy'] = data['Solar Irradiation'][Start:end].sum()
# Sankey_Data['Solar energy'] = round(Sankey_Data['Solar energy'], 0)/1000000

Sankey_Data['PV energy'] =  data['PV Power'][Start:end].sum()
Sankey_Data['PV energy'] = round(Sankey_Data['PV energy'],0)/(1000)

#Sankey_Data['PV losses'] = Sankey_Data['Solar energy'] - Sankey_Data['PV energy']

Sankey_Data['From PV to Bat'] = Energy_Distribution['From PV to Bat'][Start:end].sum()
Sankey_Data['From PV to Bat'] = round(Sankey_Data['From PV to Bat'],1)/(1000)

Sankey_Data['From PV to Grid'] = Energy_Distribution['From PV to Grid'][Start:end].sum()
Sankey_Data['From PV to Grid'] = round(Sankey_Data['From PV to Grid'],1)/1000

Sankey_Data['Curtailment'] = (data['Curtail Energy'][Start:end].sum())/(1000)

Sankey_Data['From Gen to Bat'] = Energy_Distribution['From Gen to Bat'][Start:end].sum()
Sankey_Data['From Gen to Bat'] = round(Sankey_Data['From Gen to Bat'],1)/1000

Sankey_Data['From Gen to Grid'] = Energy_Distribution['From Gen to Grid'][Start:end].sum()
Sankey_Data['From Gen to Grid'] = round(Sankey_Data['From Gen to Grid'],1)/1000

Sankey_Data['Gen generation'] = (Sankey_Data['From Gen to Grid'] 
                                + Sankey_Data['From Gen to Bat'])

Sankey_Data['Diesel'] = data['Diesel'].sum()*LHV
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


Sankey_Data_3['Label'] = ['400',
                          '400',
                          '400',
                          '400',
                          '400',
                          '400',
                          '400',
                          '400',
                          '400']

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
    size = 1000,
    valuesuffix = "MWh",
    node = dict(
      pad = 1000,
      thickness = 10,
      line = dict(
        color = "Black",
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
  ),
    
    textfont = dict(color='black',
        size=30
        )
    )


fig = dict(data=[data_trace])

plot(fig,validate = False)

