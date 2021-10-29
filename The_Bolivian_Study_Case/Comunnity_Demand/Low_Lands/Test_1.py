# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 10:55:03 2021

@author: Dell
"""


import pandas as pd


# summer 183 and winter 182
Village_Population =  list(range(50,570,50))
demand = pd.DataFrame()

for i in Village_Population:


    Village = 'village_' + str(i)
    Demand_1 = pd.read_excel('Demand_Expected_Non_Cooking.xls', sheet_name = Village, index_col=0, Header=None)
    demand[i] = Demand_1[1]
    
    
index_hourly = pd.DatetimeIndex(start='2013-01-01 01:00:00', periods=8760, 
                                   freq=('1H'))    


demand.index = index_hourly

demand['hour'] = demand.index.hour

demand_hourly = demand.groupby(['hour']).mean()
demand_hourly.plot()