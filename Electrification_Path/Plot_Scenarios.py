# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 17:18:39 2021

@author: Dell
"""


import pandas as pd
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, cross_validate, cross_val_predict
from sklearn.model_selection import GridSearchCV
from sklearn.tree import export_graphviz
import matplotlib as mpl
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import numpy as np
from sklearn import linear_model
from math import sqrt as sq
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt


Ref = pd.read_csv('REf/Bolivia/Microgrids_results.csv', index_col=0)   
sc1 = pd.read_csv('SC1/Bolivia/Microgrids_results.csv', index_col=0)  
sc2 = pd.read_csv('SC2/Bolivia/Microgrids_results.csv', index_col=0)  
sc3 = pd.read_csv('SC3/Bolivia/Microgrids_results.csv', index_col=0)  
sc4 = pd.read_csv('SC4/Bolivia/Microgrids_results.csv', index_col=0)  


print('The number of microgrids in the ref scenario is ' + str(len(Ref)) + '.')
print('The number of microgrids in the SC1 scenario is ' + str(len(sc1)) + '.')
print('The number of microgrids in the SC2 scenario is ' + str(len(sc2)) + '.')
print('The number of microgrids in the SC3 scenario is ' + str(len(sc3)) + '.')
print('The number of microgrids in the SC4 scenario is ' + str(len(sc4)) + '.')




title_size = 70
pad = 30
tick_size = 20
fontsize = '30'
mpl.rcParams['xtick.labelsize'] = tick_size
mpl.rcParams['ytick.labelsize'] = tick_size

fig = plt.figure(figsize=(40,30))
size = [40,40]
label_size = 25
tick_size = 25 


# LCOE plot
ax1 = fig.add_subplot(221)
LCOE = []
LCOE.append(Ref['MinimumOverallLCOE2025'])
LCOE.append(sc1['MinimumOverallLCOE2025'])
LCOE.append(sc2['MinimumOverallLCOE2025'])
LCOE.append(sc3['MinimumOverallLCOE2025'])
LCOE.append(sc4['MinimumOverallLCOE2025'])


ax1.boxplot(LCOE)
ax1.set_xlabel('Scenario', size=label_size)
ax1.set_ylabel('LCOE (USD/kWh)', size=label_size)
ax1.set_title('LCOE', size=title_size,pad=pad)
ax1.set_xticklabels(['Ref', 'SC1', 'SC2', 'SC3', 'SC4'])


# NPC plot
ax2 = fig.add_subplot(222)
NPC = []
NPC.append(Ref['NPC2025']/1000)
NPC.append(sc1['NPC2025']/1000)
NPC.append(sc2['NPC2025']/1000)
NPC.append(sc3['NPC2025']/1000)
NPC.append(sc4['NPC2025']/1000)


ax2.boxplot(NPC)
ax2.set_xlabel('Scenario', size=label_size)
ax2.set_ylabel('NPC (Thousands of USD)', size=label_size)
ax2.set_title('NPC', size=title_size,pad=pad)
ax2.set_xticklabels(['Ref', 'SC1', 'SC2', 'SC3', 'SC4'])

# PV plot
ax3 = fig.add_subplot(212)
PV = []
PV.append(Ref['PVcapacity2025'])
PV.append(sc1['PVcapacity2025'])
PV.append(sc2['PVcapacity2025'])
PV.append(sc3['PVcapacity2025'])
PV.append([0,0,0])


ax3.boxplot(PV)
ax3.set_xlabel('Scenario', size=label_size)
ax3.set_ylabel('PV (kW)', size=label_size)
ax3.set_title('PV installed capacity', size=title_size,pad=pad)
ax3.set_xticklabels(['Ref', 'SC1', 'SC2', 'SC3', 'SC4'])

plt.savefig('Scenarios_Results.png', bbox_inches='tight')    
plt.show()  
