# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 15:02:51 2021

@author: Dell
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from sympy import symbols, Eq, solve, Symbol, nsolve
from numpy import ones,vstack
from numpy.linalg import lstsq
#%%
ll = ['00', '005', '01', '015', '02', '025', '03', '035', '04', '045', '05',
      '1', '2', '3' ,'4', '5' , '6', '7', '8', '9']



data = pd.DataFrame()
data_llp = pd.DataFrame()

#%%
# laod results
for i in ll:
     print(i)
     path_1 = 'HSS_' + i + '/Results/Results.xls'
     results = pd.read_excel(path_1,sheet_name='Results'
                                  ,index_col=0,Header=None)
     data.loc[i, 'NPC'] = results['Data']['NPC LP (USD)']
     data.loc[i, 'LCOE'] = results['Data']['LCOE (USD/kWh)']
     
     battery =pd.read_excel(path_1,sheet_name='Battery Data'
                                  ,index_col=0,Header=None)
     
     data.loc[i, 'Battery Nominal Capacity'] = battery['Battery']['Nominal Capacity (kWh)']
     
     PV =pd.read_excel(path_1,sheet_name='Data Renewable'
                                  ,index_col=0,Header=None)
     
     data.loc[i, 'PV Nominal Capacity'] = PV['Source 1']['Total Nominal Capacity (kW)']

     Project_Data =pd.read_excel(path_1,sheet_name='Project Data'
                                  ,index_col=0,Header=None)
     
     data.loc[i, 'LLP'] = Project_Data[0]['Lost Load Probability (%)']
     
     
     path_2 =   'HSS_' + i + '/Results/Results.xls'
    
     Energy_Flows = pd.read_excel(path_2,sheet_name='Time Series'
                                  ,index_col=0,Header=None)
    
     expected_demand = 0
     for j in range(1,17):
        
        llE = 'Lost Load '+str(j) + ' (kWh)'
        de = 'Energy Demand '+str(j) + ' (kWh)'
        CRF = Project_Data[0]['Capital Recovery Factor']
        
        if i == '00':
            demand = (Energy_Flows[de].sum())/CRF
            data_llp.loc[j,i] = 0
        else:
            demand = (Energy_Flows[de].sum() - Energy_Flows[llE].sum())/CRF
            data_llp.loc[j,i] = Energy_Flows[llE].sum()/Energy_Flows[de].sum()
        
        
        demand = demand*0.0625
        expected_demand += demand
     
     data.loc[i, 'LCOE 2'] = data.loc[i, 'NPC']/expected_demand
     data.loc[i, 'Expected Demand'] = expected_demand
data.index = range(len(data))

data_llp_expected = data_llp*0.0625
data_llp_expected.loc['LLP',:] = data_llp_expected.sum()
#data.columns = range(len(data))
#%%
     
check = pd.DataFrame()

for i in range(1, 20):
    index1 = ll[i] + '-' + ll[i-1]

    check.loc[index1, 'NPC'] =   data.loc[i, 'NPC'] - data.loc[i-1, 'NPC']  
    check.loc[index1, 'Expected Demand'] =   data.loc[i, 'Expected Demand'] - data.loc[i-1, 'Expected Demand']  


for i in ll:
    high = 0
    low = 0
    for j in [1,2,3,4,9,10,11,12]:
        high += data_llp_expected.loc[j,i]

    for n in [5,6,7,8,13,14,15,16]:
        low += data_llp_expected.loc[n,i]    
    
    data_llp_expected.loc['high',i] = high
    data_llp_expected.loc['low',i] = low



for i in ll:
    high2 = 0
    low2 = 0
    for j in [1,2,3,4,9,10,11,12]:
        high2 += data_llp.loc[j,i]/8

    for n in [5,6,7,8,13,14,15,16]:
        low2 += data_llp.loc[n,i]/8    
    
    data_llp.loc['high',i] = high2
    data_llp.loc['low',i] = low2

data_llp_expected = round(data_llp_expected,4)
data = round(data,4)
data_llp = round(data_llp,4)    
    
#%%

data.to_csv('database.csv')

