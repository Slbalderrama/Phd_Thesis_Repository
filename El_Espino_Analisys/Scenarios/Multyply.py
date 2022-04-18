# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 19:30:30 2021

@author: Dell
"""

import pandas as pd

path1 = 'Demand_2022-03-24-16-46/Mulitply_Scenarios.xls'
path5 = 'Demand_2021-11-05-15-53/Mulitply_Scenarios.xls'

data1 = pd.read_excel(path1, index_col=0)
data5 = pd.read_excel(path5, index_col=0)
#scenario = pd.DataFrame()
#%%

total15  = data1.sum()/data5.sum()
print(total15.mean())

#%%
Max1 = data1.max()

Max5 = data5.max()
max15 = Max5/Max1
print(max15.mean())
#%%

describe_1 = data1.describe()
describe_5 = data5.describe()

describe15 = describe_1/describe_5

print(describe15.mean().mean())






