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
  
poverty_level =  ['50 %', '60 %', '70 %', '80 %', '90 %']
     
data_2 = data_1.transpose()
data_2.columns = poverty_level

size = [20,15]
fig=plt.figure(figsize=size)
ax=fig.add_subplot(111, label="1")

ax.plot(data_2.index, data_2['90 %'], linestyle='--', marker='o',c='b')
ax.plot(data_2.index, data_2['80 %'], linestyle='--', marker='o',c='r')
ax.plot(data_2.index, data_2['70 %'], linestyle='--', marker='o',c='c')
ax.plot(data_2.index, data_2['60 %'], linestyle='--', marker='o',c='y')
ax.plot(data_2.index, data_2['50 %'], linestyle='--', marker='o',c='k')

ax.set_xlabel("Households",size=30)
ax.set_ylabel("MWh/year",size=30)

tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
ax.tick_params(axis='x', which='major', labelsize = tick_size )
ax.tick_params(axis='y', which='major', labelsize = tick_size )    

handle1 = mlines.Line2D([], [], color='b',
                                  label='90 %', 
                                  linestyle='--',
                                  marker = 'o')
handle2 = mlines.Line2D([], [], color='r',
                                  label='80 %', 
                                  linestyle='--',
                                  marker = 'o')
handle3 = mlines.Line2D([], [], color='c',
                                  label='70 %', 
                                  linestyle='--',
                                  marker = 'o')
handle4 = mlines.Line2D([], [], color='y',
                                  label='60 %', 
                                  linestyle='--',
                                  marker = 'o')
handle5 = mlines.Line2D([], [], color='k',
                                  label='50 %', 
                                  linestyle='--',
                                  marker = 'o')
        
plt.legend(handles=[handle1, handle2, handle3, handle4, handle5],
           fontsize = 30)        
        
plt.savefig('Total_Demand_Per_Comunnity.png')
plt.show()        
            

Miss_Match_Demand = data_2['90 %']/data_2['50 %']
Miss_Match_Demand = round(Miss_Match_Demand*100, 0)
Miss_Match_Demand_Mean  = round(Miss_Match_Demand.mean(),0)
print('The Mean percentage difference demand between 90 %  and 50 % of low comsuption penetration is '
      + str(Miss_Match_Demand_Mean) + ' %')

