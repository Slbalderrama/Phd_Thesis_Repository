#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 16:57:19 2020

@author: balderrama
"""
import pandas as pd
from sklearn.utils import shuffle
from sklearn import linear_model
from sklearn.model_selection import cross_val_score, cross_validate, cross_val_predict
import numpy as np
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process import GaussianProcessRegressor
from math import sqrt as sq
import matplotlib.pyplot as plt
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from joblib import dump
#%%
Demand = pd. DataFrame()

for i in range(50, 570,50):
    
    Village = 'village_' + str(i)
    Energy_Demand = pd.read_excel('Example/Demand.xls',sheet_name=Village
                                  ,index_col=0,Header=None)
    
    
    Demand[i] = Energy_Demand[1]
    
    
    
Demand_mean = Demand.mean()
Demand_max = Demand.max()

Peak_to_Base = Demand_mean/Demand_max

#%%
y = Peak_to_Base
X = list(Peak_to_Base.index)
#%%

y, X = shuffle(y, X, random_state=10)
#%%
X = np.array(X)
X = X.reshape(-1, 1)

#%%
l1 = [1]
l2 = [1]
kernel =  RBF(l1) + RBF(l2)
gp = GaussianProcessRegressor(kernel=kernel,optimizer = 'fmin_l_bfgs_b', 
                              n_restarts_optimizer=3000)
scoring = 'neg_mean_absolute_error'
#'r2' 'neg_mean_absolute_error' # 'neg_mean_squared_error'

Results = cross_validate(gp, X, y, cv=5,return_train_score=True,n_jobs=-1
                         , scoring = scoring)

scores = Results['test_score']
score = round(scores.mean(),4)
if scoring == 'neg_mean_squared_error':
    score = sq(-score)    
    print(scoring + ' for the gaussian process with the test data set is ' + str(score))
else:    
    print(scoring + ' for the gaussian process with the test data set is ' + str(score))
    
    

#%%

l1 = [1]
l2 = [1]
kernel =  RBF(l1) + RBF(l2)

gp = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=3000,
                              optimizer = 'fmin_l_bfgs_b'
#                              , normalize_y=True
                              
                              )

gp = gp.fit(X, y)

y_Predicted =gp.predict(X)

X_new = np.array(range(70,490,50))
X_new = X_new.reshape(-1, 1)

y_New =gp.predict(X_new)

Plot_Data = pd.DataFrame()

Plot_Data['Real'] = list(y)
Plot_Data['Predicted'] = y_Predicted
Plot_Data.index = X

plt.scatter(X, Plot_Data['Real'])
plt.scatter(X, Plot_Data['Predicted'])
plt.scatter(X_new, y_New)

plt.xlabel('HouseHolds')
plt.ylabel('Peak to base ratio')
filename = 'Results_Regressions/Peak_to_Base.joblib'
dump(gp, filename) 

