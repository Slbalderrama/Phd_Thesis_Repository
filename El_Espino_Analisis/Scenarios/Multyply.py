# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 19:30:30 2021

@author: Dell
"""

import pandas as pd

path1 = 'Demand_2021-10-19-22-14/Mulitply_Scenarios.xls'
path2 = 'Demand_2021-11-04-18-53/Mulitply_Scenarios.xls'
path3 = 'Demand_2021-11-04-19-08/Mulitply_Scenarios.xls'
path4 = 'Demand_2021-11-04-19-13/Mulitply_Scenarios.xls'

data1 = pd.read_excel(path1, index_col=0)
data2 = pd.read_excel(path2, index_col=0)
data3 = pd.read_excel(path3, index_col=0)
data4 = pd.read_excel(path4, index_col=0)

#scenario = pd.DataFrame()
#%%
total12 = data1.sum()/data2.sum()    
print(total12.mean())

total13 = data1.sum()/data3.sum()    
print(total13.mean())

total14 = data1.sum()/data4.sum()    
print(total14.mean())

#%%
Max1 = data1.max()
Max2 = data2.max()

max12 = Max1/Max2    
print(max12 )

Max3 = data3.max()
max13 = Max3/Max1    
print(max13)

Max4  = data4.max()
max14 = Max4/Max1  
print(max14)