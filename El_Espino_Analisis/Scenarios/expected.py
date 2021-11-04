# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 19:30:30 2021

@author: Dell
"""

import pandas as pd

path1 = 'Demand_2021-10-19-22-14/Expected_Demand.xls'
path2 = 'Demand_2021-11-04-18-53/Expected_Demand.xls'
path3 = 'Demand_2021-11-04-19-08/Expected_Demand.xls'
path4 = 'Demand_2021-11-04-19-13/Expected_Demand.xls'

data1 = pd.read_excel(path1, index_col=0)
data2 = pd.read_excel(path2, index_col=0)
data3 = pd.read_excel(path3, index_col=0)
data4 = pd.read_excel(path4, index_col=0)

data = pd.DataFrame()

data[1] = data1[1]
data[2] = data2[1]
data[3] = data3[1]
data[4] = data4[1]

data['dif'] = data[1] - data[2]

print(data.sum())
print(data.max())
print(data.min())

data_describe = data.describe()