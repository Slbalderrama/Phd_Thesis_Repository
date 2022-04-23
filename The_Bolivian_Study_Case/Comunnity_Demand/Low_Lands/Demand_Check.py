#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 15:33:58 2019

@author: sergio
"""
import pandas as pd

import matplotlib.pyplot as plt

import matplotlib.lines as mlines



# summer 183 and winter 182
Village_Population =  list(range(50,570,50))

folder_1 = 'Households/'

data_1 = pd.DataFrame()
peak_1 = pd.DataFrame()
for i in Village_Population:
    data = pd.Series()
    peak = pd.Series()
    for j in range(1,6):
        path_1 = folder_1 + 'pop_' + str(i) + '_' + str(j) + '.csv' 
        Power_Data_1 = pd.read_csv(path_1,index_col=0)
        Power_Data_1.columns = [0] 
        Power_Data_1[0] = pd.to_numeric(Power_Data_1[0])
        data.loc[j] = Power_Data_1[0].sum()
        peak.loc[j] = Power_Data_1[0].max()
    
    data_1[i] = data/1000000     
    peak_1[i] = peak/1000
  
poverty_level =  ['S 13', 'S 10', 'S 7', 'S 4', 'S 1']
     
data_2 = data_1.transpose()
data_2.columns = poverty_level

peak_2 = peak_1.transpose() 
peak_2.columns = poverty_level

size = [20,15]
fig=plt.figure(figsize=size)
ax=fig.add_subplot(121, label="1")
ax2=fig.add_subplot(122, label="2") 

ax.plot(data_2.index, data_2['S 13'], linestyle='--', marker='o',c='b')
ax.plot(data_2.index, data_2['S 10'], linestyle='--', marker='o',c='r')
ax.plot(data_2.index, data_2['S 7'], linestyle='--', marker='o',c='c')
ax.plot(data_2.index, data_2['S 4'], linestyle='--', marker='o',c='y')
ax.plot(data_2.index, data_2['S 1'], linestyle='--', marker='o',c='k')

ax.set_xlabel("Households",size=30)
ax.set_ylabel("MWh/year",size=30)

tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
ax.tick_params(axis='x', which='major', labelsize = tick_size )
ax.tick_params(axis='y', which='major', labelsize = tick_size )    



ax2.plot(peak_2.index, peak_2['S 13'], linestyle='--', marker='o',c='b')
ax2.plot(peak_2.index, peak_2['S 10'], linestyle='--', marker='o',c='r')
ax2.plot(peak_2.index, peak_2['S 7'], linestyle='--', marker='o',c='c')
ax2.plot(peak_2.index, peak_2['S 4'], linestyle='--', marker='o',c='y')
ax2.plot(peak_2.index, peak_2['S 1'], linestyle='--', marker='o',c='k')

ax2.set_xlabel("Households",size=30)
ax2.set_ylabel("kW",size=30)

tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
ax2.tick_params(axis='x', which='major', labelsize = tick_size )
ax2.tick_params(axis='y', which='major', labelsize = tick_size )    








handle1 = mlines.Line2D([], [], color='b',
                                  label='S 13', 
                                  linestyle='--',
                                  marker = 'o')
handle2 = mlines.Line2D([], [], color='r',
                                  label='S 10', 
                                  linestyle='--',
                                  marker = 'o')
handle3 = mlines.Line2D([], [], color='c',
                                  label='S 7', 
                                  linestyle='--',
                                  marker = 'o')
handle4 = mlines.Line2D([], [], color='y',
                                  label='S 4', 
                                  linestyle='--',
                                  marker = 'o')
handle5 = mlines.Line2D([], [], color='k',
                                  label='S 1', 
                                  linestyle='--',
                                  marker = 'o')
        
plt.legend(handles=[handle5, handle4, handle3, handle2, handle1],
                            bbox_to_anchor=(0.75, -0.05),fontsize = 30,
                            frameon=False,  ncol=5)        
        
plt.savefig('Total_Demand_Per_Comunnity.png')
plt.show()        
            

Miss_Match_Demand = data_2['S 1']/data_2['S 13']
Miss_Match_Demand = round(Miss_Match_Demand*100, 0)
Miss_Match_Demand_Mean  = round(Miss_Match_Demand.mean(),0)
print('The Mean percentage difference demand between S 13 and S 1 is '
      + str(Miss_Match_Demand_Mean) + ' %')

Miss_Match_Peak = peak_2['S 1']/peak_2['S 13']
Miss_Match_Peak = round(Miss_Match_Peak*100, 0)
Miss_Match_Peak_Mean  = round(Miss_Match_Peak.mean(),0)
print('The Mean percentage difference of peak deman between S 13 and S 1  is '
      + str(Miss_Match_Peak_Mean) + ' %')