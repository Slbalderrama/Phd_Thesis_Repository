# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 18:37:33 2021

@author: Dell
"""


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

data = pd.read_csv('Onsset_Scenarios/onsset_classic/Bolivia/bo-1-0_0_0_0_0_0.csv', index_col=0)  



data_1 = data.copy()
data_1 = data_1.loc[data_1['Elevation']<800]



plot_data = pd.DataFrame()
plot_data['HouseHolds'] = data_1['NewConnections2025']/data_1['NumPeoplePerHH']

plot_data = plot_data.loc[plot_data['HouseHolds']<550]

plot_data = plot_data.loc[plot_data['HouseHolds']>50]

plot_data = plot_data.sort_values('HouseHolds', ascending=False)




plot_data.index = range(1,len(plot_data)+1)


size = [20,15]
label_size = 35
tick_size = 35 

mpl.rcParams['xtick.labelsize'] = tick_size 
mpl.rcParams['ytick.labelsize'] = tick_size 


fig=plt.figure(figsize=size)
ax=fig.add_subplot(111, label="1")

ax.plot(plot_data.index, plot_data['HouseHolds'], c='b', linewidth=5)

ax.set_xlim([0,910])
ax.set_ylim([0,550])

ax.set_xlabel('Number of communities',size=label_size) 
ax.set_ylabel('Number of Households',size=label_size) 
ax.grid()   
#ax.set_aspect('equal')
plt.savefig('Plots/DC_HouseHolds.png', bbox_inches='tight')    
plt.show()   