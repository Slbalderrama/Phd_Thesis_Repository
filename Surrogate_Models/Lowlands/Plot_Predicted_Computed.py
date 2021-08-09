#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 23:14:23 2019

@author: balderrama
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

# Data manipulation
data = pd.read_excel('Data_Base.xls', index_col=0, Header=None)   
#data = data.loc[data['Gap']< 1]

y_NPC = pd.DataFrame()
y_NPC['NPC'] = data['NPC']

y_LCOE = pd.DataFrame()
y_LCOE['LCOE'] = data['LCOE']

y_PV = pd.DataFrame()
y_PV['Renewable Capacity'] = data['Renewable Capacity']

y_bat = pd.DataFrame()
y_bat['Battery Capacity'] =  data['Battery Capacity']

#y=y.astype('float')

X = pd.DataFrame()
X['Renewable Invesment Cost'] = data['Renewable Unitary Invesment Cost']   
X['Battery Unitary Invesment Cost'] = data['Battery Unitary Invesment Cost']
X['Deep of Discharge'] = data['Deep of Discharge']
X['Battery Cycles'] = data['Battery Cycles']
X['GenSet Unitary Invesment Cost'] = data['GenSet Unitary Invesment Cost']
X['Generator Efficiency'] = data['Generator Efficiency']
X['Low Heating Value'] = data['Low Heating Value']
X['Fuel Cost'] = data['Fuel Cost']
#X['Generator Nominal capacity'] = data['Generator Nominal capacity'] 
X['HouseHolds'] = data['HouseHolds']
X['Renewable Energy Unit Total'] = data['Renewable Energy Unit Total']
#X['Max Demand'] = data['Max Demand']
#X['Y'] = data['Y']


feature_list = list(X.columns)

y_NPC, X_NPC = shuffle(y_NPC, X, random_state=10)

y_LCOE,  X_LCOE = shuffle(y_LCOE, X, random_state=10)

y_PV,  X_PV = shuffle(y_PV, X, random_state=10)

y_bat,  X_bat = shuffle(y_bat, X, random_state=10)

#%%
# Calculated cross validation test results 
l =[1,1,1,1,1,1,1,1,1,1]
kernel =  RBF(l)

gp_NPC = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=3000,
                              optimizer = 'fmin_l_bfgs_b'
#                              , normalize_y=True
    )

y_gp_NPC = cross_val_predict(gp_NPC, X_NPC, y_NPC, cv=5,n_jobs=-1)



lm_NPC = linear_model.LinearRegression(fit_intercept=True)
y_lm_NPC = cross_val_predict(lm_NPC, X_NPC, y_NPC, cv=5,n_jobs=-1)


#%%
l = [1,1,1,1,1,1,1,1,1,1]
kernel =  RBF(l)

gp_LCOE = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=3000,
                              optimizer = 'fmin_l_bfgs_b'
#                              , normalize_y=True
    )

y_gp_LCOE = cross_val_predict(gp_LCOE, X_LCOE, y_LCOE, cv=5,n_jobs=-1)



lm_LCOE = linear_model.LinearRegression(fit_intercept=True)
y_lm_LCOE = cross_val_predict(lm_LCOE, X_LCOE, y_LCOE, cv=5,n_jobs=-1)

#%%

l1 =  [1,1,1,1,1,1,1,1,1,1]
l2 =  [1,1,1,1,1,1,1,1,1,1]

kernel =  RBF(l1) + RBF(l2) 
gp_PV = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=3000,
                              optimizer = 'fmin_l_bfgs_b'
#                              , normalize_y=True
    )

y_gp_PV = cross_val_predict(gp_PV, X_PV, y_PV, cv=5,n_jobs=-1)



lm_PV = linear_model.LinearRegression(fit_intercept=True)
y_lm_PV = cross_val_predict(lm_PV, X_PV, y_PV, cv=5,n_jobs=-1)

#%%

l1 = [1,1,1,1,1,1,1,1,1,1]
l2 = [1,1,1,1,1,1,1,1,1,1]

kernel =  RBF(l1) + RBF(l2) 
gp_bat = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=3000,
                              optimizer = 'fmin_l_bfgs_b'
#                              , normalize_y=True
    )

y_gp_bat = cross_val_predict(gp_bat, X_bat, y_bat, cv=5,n_jobs=-1)



lm_bat = linear_model.LinearRegression(fit_intercept=True)
y_lm_bat = cross_val_predict(lm_bat, X_bat, y_bat, cv=5,n_jobs=-1)



#%%

## Plot
#size = [40,40]
#label_size = 25
#tick_size = 25 
#
#fig, axs = plt.subplots(1, 2, figsize=(20, 15))
#
#mpl.rcParams['xtick.labelsize'] = tick_size 
#mpl.rcParams['ytick.labelsize'] = tick_size 
#axs[0].scatter(y_NPC/1000, y_gp_NPC/1000,s = 20, marker='o')
#axs[0].scatter(y_NPC/1000, y_lm_NPC/1000,s = 20, marker='x')
#axs[0].plot([0, 1500], [0, 1500], 'k-', lw=2)
#axs[0].set_xlim([0,1500])
#axs[0].set_ylim([-250,1500])
#axs[0].set_xlabel('Calculado (Miles USD)', size=label_size)
#axs[0].set_ylabel('Predecido (Miles USD)', size=label_size)
#
#axs[1].scatter(y_LCOE, y_gp_LCOE,s = 20, marker='o')
#axs[1].scatter(y_LCOE, y_lm_LCOE,s = 20, marker='x')
#axs[1].plot([0, 0.8], [0, 0.8], 'k-', lw=2)
#axs[1].set_xlim([0,0.8])
#axs[1].set_xlim([0,0.8])
#axs[1].set_xlabel('Calculado (USD/kWh)', size=label_size)
#axs[1].set_ylabel('Predecido (USD/kWh)', size=label_size)
#
#plt.show()



#%%
title_size = 70
pad = 30
tick_size = 20
fontsize = '30'
marker_1 = plt.scatter(0,0, marker='o',c='b')
marker_2 =  plt.scatter(0,0, marker='x',c='orange')
mpl.rcParams['xtick.labelsize'] = tick_size
mpl.rcParams['ytick.labelsize'] = tick_size

fig = plt.figure(figsize=(40,30))
size = [40,40]
label_size = 25
tick_size = 25 
ax1 = fig.add_subplot(221)

# NPC plot
ax1.scatter(y_NPC/1000, y_gp_NPC/1000,s = 5, marker='o')
ax1.scatter(y_NPC/1000, y_lm_NPC/1000,s = 5, marker='x')
ax1.plot([0, 1500], [0, 1500], 'k-', lw=2)
ax1.plot([0, 1500], [0, 1500], 'k-', lw=2)
ax1.set_xlim([0,1500])
ax1.set_ylim([-250,1500])
ax1.set_xlabel('Computed (thousand USD)', size=label_size)
ax1.set_ylabel('Predicted (thousand USD)', size=label_size)
ax1.set_title('NPC', size=title_size,pad=pad)
plt.legend(handles=[marker_1,marker_2], labels=['GPR',"MVLR"],fontsize=fontsize)
# LCOE plot
ax2 = fig.add_subplot(222)
ax2.scatter(y_LCOE, y_gp_LCOE,s = 10, marker='o')
ax2.scatter(y_LCOE, y_lm_LCOE,s = 10, marker='x')
ax2.plot([0, 1], [0, 1], 'k-', lw=2)
ax2.set_xlim([0,1])
ax2.set_ylim([-0.2,1])
ax2.set_xlabel('Computed (USD/kWh)', size=label_size)
ax2.set_ylabel('Predicted (USD/kWh)', size=label_size)
ax2.set_title('LCOE', size=title_size,pad=pad)
plt.legend(handles=[marker_1,marker_2], labels=['GPR',"MVLR"],fontsize=fontsize)
# PV plot
ax3 = fig.add_subplot(223)
ax3.scatter(y_PV, y_gp_PV, s = 10, marker='o')
ax3.scatter(y_PV, y_lm_PV, s = 10, marker='x')
ax3.plot([0, 220], [0, 220], 'k-', lw=2)
ax3.set_xlim([0,220])
ax3.set_ylim([-50,220])
ax3.set_xlabel('Computed (kW)', size=label_size)
ax3.set_ylabel('Predicted (kW)', size=label_size)
ax3.set_title('PV Nominal Capacity', size=title_size,pad=pad)
plt.legend(handles=[marker_1,marker_2], labels=['GPR',"MVLR"],fontsize=fontsize)
# Bat plot
ax4 = fig.add_subplot(224)
ax4.scatter(y_bat, y_gp_bat, s = 10, marker='o')
ax4.scatter(y_bat, y_lm_bat, s = 10, marker='x')
ax4.plot([0, 1050], [0, 1050], 'k-', lw=2)
ax4.set_xlim([0,1050])
ax4.set_ylim([-200,1050])
ax4.set_xlabel('Computed (kWh)', size=label_size)
ax4.set_ylabel('Predicted (kWh)', size=label_size)
ax4.set_title('Battery Nominal Capacity', size=title_size,pad=pad)
plt.legend(handles=[marker_1,marker_2], labels=['GPR',"MVLR"],fontsize=fontsize)
plt.subplots_adjust(hspace= 0.25)