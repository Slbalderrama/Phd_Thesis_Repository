#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 10:33:54 2019

@author: balderrama
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
import enlopy as el
import matplotlib as mpl
from pandas import ExcelWriter

Village_Population = list(range(50,570,50))

folder_1 = 'Households/'
#folder_2 = 'Cooking/'
path = 'Demand_Expected_Non_Cooking.xls'
writer = ExcelWriter(path, engine='xlsxwriter')

for i in Village_Population:
    instance = pd.DataFrame()
    # No services    
    for j in range(1,6):
        path_1 = folder_1 + 'pop_' + str(i) + '_' + str(j) + '.csv' 
#        path_2 = folder_2 + 'pop_' + str(i) + '_' + str(j) + '.csv'
        Power_Data_1 = pd.read_csv(path_1,index_col=0)
        Power_Data_1.columns = [0]
#        Power_Data_2 = pd.read_csv(path_2,index_col=0)
#        Power_Data_2.columns = [0]
        Power_Data = Power_Data_1[0] #+ Power_Data_2[0][:]
        instance[j] = Power_Data
    # No services + school    
    for j in range(6,11):
        path_3 = 'School.csv'
        Power_Data_3 = pd.read_csv(path_3, index_col=0) 
        Power_Data_3.columns = [0]
        instance[j] = instance[j-5] + Power_Data_3[0]
    # No services + school + hospital    
    for j in range(11,16):
        path_4 = 'Hospital.csv'
        Power_Data_4 = pd.read_csv(path_4, index_col=0) 
        Power_Data_4.columns = [0]
        instance[j] = instance[j-5] + Power_Data_4[0]
        
    instance.index = range(1,8761)
    
    instance1 = pd.DataFrame(index = instance.index)
    instance1[1] = 0
    
    for r in instance.columns:
        
        instance1[1] += instance[r]/15
        
    
    sheet_name = 'village_' +str(i)
    instance1.to_excel(writer, sheet_name=sheet_name)

writer.save()
