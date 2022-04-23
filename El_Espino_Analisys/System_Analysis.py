# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 17:47:45 2021

Average dispatch plot


@author: Dell
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.ticker as mtick
import matplotlib.pylab as pylab
#import enlopy as el
import matplotlib as mpl
from datetime import datetime
import os
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

#%%

# load data

data = pd.read_csv('Data/Data_Espino_Thesis_Fill_2.csv', header=0,index_col=0)
index = pd.date_range(start='2016-01-01 00:00:00', periods=166464, freq=('5min'))
data.index = index

Optimal_PV = pd.read_csv('Results/Renewable_Energy_Optimal_Espino.csv', header=0,index_col=0 )
Optimal_PV.index = index

data['Curtailment'] = Optimal_PV['Optimal PV Power'] - data['PV Power']
data['hour'] = data.index.hour

#%%

# Average energy flow


b_o = 'Discharge energy from the Battery'
b_i = 'Charge energy to the Battery'
pv_c ='PV Corrected'
pv_e ='Energy PV'
de = 'Energy_Demand'
    
Plot_Data = data.groupby(['hour']).mean()

#    Plot_Data['SOC'] = (Plot_Data['SOC'])/100
    
Plot_Data.columns = ['Energy PV', 'Energy Diesel', 'State_Of_Charge_Battery', 
                     'Ambient temperature', 'Energy_Demand',
                     'Solar Irradiation', 'PV Temperature 2', 'Charge energy to the Battery',
                     'Discharge energy from the Battery', 'Curtailment']  

  
Plot_Data[b_i] = -Plot_Data[b_i].copy()
 

Vec = Plot_Data['Energy PV'] + Plot_Data['Energy Diesel']
Vec2 = (Plot_Data['Energy PV'] + Plot_Data['Energy Diesel'] + 
            Plot_Data['Discharge energy from the Battery'])

Vec3 = (Plot_Data['Energy PV'] + Plot_Data['Energy Diesel'] + 
            Plot_Data['Discharge energy from the Battery'] + Plot_Data['Curtailment'] )
   
# for t in Plot_Data.index:
        
        
#     if Plot_Data[pv_c][t]>0 and Plot_Data[b_o][t]>0:
#             Curtailment = Plot_Data[pv_c][t] - Plot_Data[pv_e][t]
#             Plot_Data.loc[t,'Curtailment 2'] = Curtailment + Plot_Data[de][t]
#             Plot_Data.loc[t,pv_c] = Plot_Data[pv_e][t]
#     else:
#             Plot_Data.loc[t,'Curtailment 2'] = Plot_Data[de][t]
    
size = [20,10]    
plt.figure(figsize=size)
    # Gen energy
c_g = 'm'
Alpha_g = 0.3 
hatch_g = '\\'
ax1= Vec.plot(style='y-', linewidth=0) # Plot the line of the diesel energy plus the PV energy
ax1.fill_between(Plot_Data.index, Plot_Data['Energy PV'].values, Vec.values,   
                     alpha=Alpha_g, color = c_g,hatch =hatch_g )
    #ax2= Vec.plot(style='b', linewidth=0.5)
    # PV energy
c_PV = 'yellow'   
Alpha_r = 0.4 
    
ax1.fill_between(Plot_Data.index, 0, Plot_Data['Energy PV'].values, 
                     alpha=Alpha_r, color=c_PV) # Fill the area of the energy produce by the diesel generator
    # Energy Demand
ax3 = Plot_Data['Energy_Demand'].plot(style='k', linewidth=2)
    
    # Battery flow out
alpha_bat = 0.3
hatch_b ='x'
C_Bat = 'green'
    
ax3.fill_between(Plot_Data.index, Vec.values , Vec2.values,
                     alpha=alpha_bat, color=C_Bat, hatch=hatch_b)
    
    # Battery flow in
ax5= Plot_Data['Charge energy to the Battery'].plot(style=C_Bat, linewidth=0) # Plot the line of the energy flowing into the battery
ax5.fill_between(Plot_Data.index, 0, 
                     Plot_Data['Charge energy to the Battery'].values, 
                     alpha=alpha_bat, color=C_Bat, hatch=hatch_b) # Fill the area of the energy flowing into the battery

    # State of charge                 
ax6= Plot_Data['State_Of_Charge_Battery'].plot(style='k--', secondary_y=True,
         linewidth=2, alpha=0.7 ) # Plot the line of the State of charge of the battery
    
# Curtailment
alpha_cu = 0.3
hatch_cu = '+'
C_Cur = 'blue'
ax7 = Vec3.plot(style='b-', linewidth=0)
ax7.fill_between(Plot_Data.index, Vec2.values,
                    Vec3.values,
                    alpha=alpha_cu, color='blue', hatch=hatch_cu)
#    # Curtailment 2
#    #    ax8 = Plot_Data['Curtailment 2'].plot(style='b-', linewidth=0)
#    ax8.fill_between(Plot_Data.index, Plot_Data['Energy_Demand'].values, 
#                     Plot_Data['Curtailment 2'].values,
#                     alpha=alpha_cu, color='blue', hatch=hatch_cu, 
#                     where= Plot_Data['Curtailment 2']>Plot_Data['Energy_Demand'])
    # Define name  and units of the axis
ax1.set_ylabel('Power (kW)',size=30)
ax1.set_xlabel('Time (hours)',size=30)
ax1.set_xlim([0,23])
ax6.set_ylabel('Battery State of charge (%)',size=30)
    
#    ax1.tick_params(axis='x', which='major', labelsize=20)
    
tick_size = 20  
mpl.rcParams['xtick.labelsize'] = tick_size     
ax1.tick_params(axis='y', which='major', labelsize = tick_size )
ax1.tick_params(axis='x', which='major', labelsize = tick_size )
ax6.tick_params(axis='y', which='major', labelsize = tick_size )
        
    # Define the legends of the plot
From_PV = mpatches.Patch(color=c_PV,alpha=Alpha_r, label='From PV')
From_Generator = mpatches.Patch(color=c_g,alpha=Alpha_g,
                                       label='From Generator',hatch =hatch_g)
Battery = mpatches.Patch(color=C_Bat ,alpha=alpha_bat, 
                                 label='Battery Energy Flow',hatch =hatch_b)
Curtailment = mpatches.Patch(color=C_Cur ,alpha=alpha_cu, 
                                label='Curtailment',hatch =hatch_cu)

Energy_Demand = mlines.Line2D([], [], color='black',label='Energy Demand')
State_Of_Charge_Battery = mlines.Line2D([], [], color='black',
                                                label='State Of Charge Battery',
                                                linestyle='--',alpha=0.7)
plt.legend(handles=[From_Generator, From_PV, Battery, 
                        Curtailment,
                            Energy_Demand, State_Of_Charge_Battery],
                            bbox_to_anchor=(1.025, -0.1),fontsize = 20,
                            frameon=False,  ncol=4)



plt.savefig('Plots/Energy_Dispatch_Average_Espino.png', bbox_inches='tight')
plt.show()
