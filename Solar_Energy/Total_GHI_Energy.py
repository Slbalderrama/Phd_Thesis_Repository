# -*- coding: utf-8 -*-
"""
Created on Tue May 11 09:50:09 2021

@author: Dell
"""
import pandas as pd


GHI_Energy_Total = pd.DataFrame()
for j in range(4000):
    
    GHI_Energy = pd.read_csv('Fix_Energy_GHI/GHI_Fix_' + str(j)+'.csv',index_col=0)
    GHI_Energy_Total.loc[j, 'Total GHI Energy'] = GHI_Energy['1'].sum()/1000 