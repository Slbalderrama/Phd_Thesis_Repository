#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 19:03:33 2019

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
#%%
# Data manipulation
data = pd.read_excel('Databases/Data_Base.xls', index_col=0, Header=None)  

#%%
y = pd.DataFrame()
target= 'Renewable Capacity' #  'Renewable Capacity' 'Renewable Penetration'
y[target] = data[target]

y=y.astype('float')

X = pd.DataFrame()
X['Renewable Invesment Cost'] = data['Renewable Unitary Invesment Cost']   
X['Battery Unitary Invesment Cost'] = data['Battery Unitary Invesment Cost']
X['Deep of Discharge'] = data['Deep of Discharge']
X['Battery Cycles'] = data['Battery Cycles']
X['GenSet Unitary Invesment Cost'] = data['GenSet Unitary Invesment Cost']
X['Generator Efficiency'] = data['Generator Efficiency']
X['Low Heating Value'] = data['Low Heating Value']
X['Fuel Cost'] = data['Fuel Cost']
X['HouseHolds'] = data['HouseHolds']
X['Renewable Energy Unit Total'] = data['Renewable Energy Unit Total']



feature_list = list(X.columns)
y, X = shuffle(y, X, random_state=10)


#%%
# Linear regression
# Linear Cross validation
scoring =   ['r2', 'neg_mean_absolute_error', 'neg_mean_squared_error'] #'r2' 'neg_mean_absolute_error' # 'neg_mean_squared_error'
for i in scoring:    
    lm = linear_model.LinearRegression(fit_intercept=True)
    scores = cross_val_score(lm, X, y, cv=5, scoring=i)
    score = round(scores.mean(),2)
    
    if i == 'neg_mean_squared_error':
        score = sq(-score)    
        print(i + ' for the linear regression with the test data set is ' + str(score))
    else:    
        print(i + ' for the linear regression with the test data set is ' + str(score))


#r2 for the linear regression with the test data set is 0.78
#neg_mean_absolute_error for the linear regression with the test data set is -22.86
#neg_mean_squared_error for the linear regression with the test data set is 28.039971469315013

#%%
# Cross Validation results


scoring =   ['r2', 'neg_mean_absolute_error', 'neg_mean_squared_error'] #'r2' 'neg_mean_absolute_error' # 'neg_mean_squared_error'
for i in scoring:  
    
    l1 = [1,1,1,1,1,1,1,1,1,1]
    l2 = [1,1,1,1,1,1,1,1,1,1]
        
    
    
    #kernel = (C()**2)*RBF(l)
    kernel =  RBF(l1) + RBF(l2)
    gp = GaussianProcessRegressor(kernel=kernel,optimizer = 'fmin_l_bfgs_b', 
                                  n_restarts_optimizer=3000)
    
    Results = cross_validate(gp, X, y, cv=5,return_train_score=True,n_jobs=-1
                             , scoring = i       )
    
    scores = Results['test_score']
    score = round(scores.mean(),2)
    
    if i == 'neg_mean_squared_error':
        score = sq(-score)    
        print(i + ' for the gaussian process with the test data set is ' + str(score))
    else:    
        print(i + ' for the gaussian process with the test data set is ' + str(score))
    
    Results = pd.DataFrame(Results)
    
    path = 'Results_Regressions/Kcross_valiadation_GP_PV' + '_' +  i + '.csv'
    Results.to_csv(path)
# r2 for the gaussian process with the test data set is 0.93
# neg_mean_absolute_error for the gaussian process with the test data set is -11.26
# neg_mean_squared_error for the gaussian process with the test data set is 15.89842759520576 ok

