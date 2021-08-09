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
from joblib import dump,load
#%%
Demand = pd. DataFrame()

for i in range(50, 570,50):
    
    Village = 'village_' + str(i)
    Energy_Demand = pd.read_excel('Example/Demand.xls',sheet_name=Village
                                  ,index_col=0,Header=None)
    
    
    Demand[i] = Energy_Demand[1]/1000
    


Demand_1 = Demand.sum()



#%%
y = Demand_1
X = list(Demand_1.index)
#%%

y, X = shuffle(y, X, random_state=10)
#%%
X = np.array(X)
X = X.reshape(-1, 1)
#%%

scoring = 'r2' #'r2' 'neg_mean_absolute_error' # 'neg_mean_squared_error'

lm = linear_model.LinearRegression(fit_intercept=True)

Results = cross_validate(lm, X, y, cv=2,return_train_score=True,n_jobs=-1
                         , scoring = scoring       )

scores = Results['test_score']
score = scores.mean()
if scoring == 'neg_mean_squared_error':
    score = sq(-score)    
    print(scoring + ' for the linear regression with the test data set is ' + str(score))
else:    
    print(scoring + ' for the linear regression with the test data set is ' + str(score))
#%%

lm1 = linear_model.LinearRegression(fit_intercept=True)
lm1 = lm1.fit(X, y)    
dump(lm1, 'Results_Regressions/Demand_LowLands.joblib')  
#%%

