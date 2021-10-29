#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 15:33:58 2019

@author: sergio
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.ticker as mtick
import matplotlib.pylab as pylab
from scipy.stats import pearsonr
from matplotlib.sankey import Sankey
import pylab
import enlopy as el
import matplotlib as mpl
from pandas import ExcelWriter

# summer 183 and winter 182
Village_Population =  list(range(50,570,50))

folder_1 = 'Households/'
Demand = pd.Series()  
data_1 = pd.DataFrame()
for i in Village_Population:
    data = pd.Series()

    for j in range(1,6):
        path_1 = folder_1 + 'pop_' + str(i) + '_' + str(j) + '.csv' 
        Power_Data_1 = pd.read_csv(path_1,index_col=0)
        Power_Data_1.columns = [0] 
        Power_Data_1[0] = pd.to_numeric(Power_Data_1[0])
        Total_Energy = Power_Data_1.sum()
        Total_Energy = Total_Energy[0]
        data.loc[j] = Total_Energy
    
    data_1[i] = data/1000000     
  
poverty_level =  ['90 %', '80 %', '70 %', '60 %', '50 %']
     
data_2 = data_1.transpose()
data_2.columns = poverty_level
data_2.plot(linestyle='--', marker='o')        
        
        
        
        
        
            