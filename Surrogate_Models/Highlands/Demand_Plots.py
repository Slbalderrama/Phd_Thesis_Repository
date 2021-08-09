# -*- coding: utf-8 -*-
"""
Created on Mon May 20 11:01:48 2019

@author: Lombardi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
#%% 
'''
Importing csv profiles
'''

hospital = pd.read_csv('Demand/Hospital.csv')
hospital.set_index('Unnamed: 0', inplace=True)

school = pd.read_csv('Demand/School.csv')
school.set_index('Unnamed: 0', inplace=True)

El_Espino_dict = {}

population_sizes = [50,100,150,200,250,300,350,400,450,500,550]

for pop in population_sizes:

    El_Espino_dict[pop] = []

    
    for pov_sh in range(0,5):

        El_Espino_dict[pop].append(pd.read_csv('Demand/Households/pop_%d_%d.csv' %(pop,(pov_sh+1)),
                                               index_col='Unnamed: 0'))


    
#%%
'''
Generating custom plots
'''
        
start = '2015-03-01 00:00:00'
stop = '2015-03-03 23:00:00'
pad = 10
title_size = 100
fontsize = '30'
label_size = 35
tick_size_y = 35
tick_size_x = 35
mpl.rcParams['xtick.labelsize'] = tick_size_x
mpl.rcParams['ytick.labelsize'] = tick_size_y
fig, ((ax2,ax1), (ax4,ax3)) = plt.subplots(2,2, sharex = 'col',
   gridspec_kw = {'height_ratios':[1,1], 'wspace':0.1, 'hspace':0.1}, figsize=(40,30))

pop_size_left = 50
pop_sizes_right = [50,250,500]
x = pd.date_range(start,stop, freq= 'H')

colours_load_contributions = ['#596FB7','#59B777','#D2B244','#D26044']
labels_load_contributions = ['households','hospital','school','cooking']
colours_pop_sizes = ['#596FB7', '#3A4D8C', '#162863']
labels_pop_sizes = ['50 HH', '250 HH', '500 HH']

#El Espino plot with different load contributions, richer population, on ax1
y_rich_left_E = [El_Espino_dict[pop_size_left][0][start:stop].values[:,0]/1e3,
               hospital[start:stop].values[:,0]/1e3,
               school[start:stop].values[:,0]/1e3]

#El Espino plot with different contributions, poorer population, on ax3
y_poor_left_E = [El_Espino_dict[pop_size_left][4][start:stop].values[:,0]/1e3,
               hospital[start:stop].values[:,0]/1e3,
               school[start:stop].values[:,0]/1e3]


#El Espino plot with different population sizes, richer population, on ax2
y1_E = (El_Espino_dict[50][0] + hospital + school)[start:stop].values[:,0]
y2_E =  (El_Espino_dict[250][0] + hospital + school)[start:stop].values[:,0]
y3_E =  (El_Espino_dict[500][0] + hospital + school)[start:stop].values[:,0]

#El Espino plot with different population sizes, poorer population, on ax4
y4_E = (El_Espino_dict[50][4] + hospital + school)[start:stop].values[:,0]
y5_E =  (El_Espino_dict[250][4] + hospital + school)[start:stop].values[:,0]
y6_E =  (El_Espino_dict[500][4] + hospital + school)[start:stop].values[:,0]

#plt.xticks(rotation=45)
ax1.stackplot(x,y_rich_left_E,labels=labels_load_contributions,
              colors=colours_load_contributions)
ax1.margins(x=0)
ax1.margins(y=0)
ax1.set_ylabel('Electricity demand (kW)', size=label_size)
ax1.set_title('b.', size=title_size,pad=pad, loc='left')
#lgd1 = ax1.legend(loc=2) #,  bbox_to_anchor=(2.1,1))

ax3.stackplot(x,y_poor_left_E,labels=labels_load_contributions,
              colors=colours_load_contributions)
ax3.margins(x=0)
ax3.margins(y=0)
ax3.set_ylabel('Electricity demand (kW)', size=label_size)
lgd3 = ax3.legend(loc=2,fontsize=fontsize) #,  bbox_to_anchor=(2.1,1))


ax2.stackplot(x,[y1_E/1e3,y2_E/1e3,y3_E/1e3],labels=labels_pop_sizes,
              colors=colours_pop_sizes)
ax2.margins(x=0)
ax2.margins(y=0)
ax2.set_ylabel('Electricity demand (kW)', size=label_size)
ax2.set_title('a.', size=title_size,pad=pad, loc='left')
#lgd2 = ax2.legend(loc=2)#,  bbox_to_anchor=(1.1,1))

ax4.stackplot(x,[y4_E/1e3,y5_E/1e3,y6_E/1e3],labels=labels_pop_sizes,
              colors=colours_pop_sizes)
ax4.margins(x=0)
ax4.margins(y=0)
ax4.set_ylabel('Electricity demand (kW)', size=label_size)
lgd4 = ax4.legend(loc=2,fontsize=fontsize) #,  bbox_to_anchor=(2.1,1))

for ax in fig.axes:
#    ax.locator_params(nbins=33, axis='x')
    ax.tick_params(pad=25, axis='x')
    ax.set_xticklabels(['Day 1', '', 'Day 2', '','Day 3',''])
plt.savefig('Plots/Demand_Profiles.png', bbox_inches='tight')    
plt.show()       