#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 00:36:24 2019
132
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
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, Matern, ExpSineSquared, RationalQuadratic 
import numpy as np
from sklearn import linear_model
import time
from sklearn.model_selection import train_test_split
from joblib import dump
data = pd.read_excel('Data_Base.xls', index_col=0, Header=None)  




y = pd.DataFrame()
target= 'Renewable Capacity' 
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

start = time.time()
l1 = [1,1,1,1,1,1,1,1,1,1]
l2 = [1,1,1,1,1,1,1,1,1,1]

kernel =  RBF(l1) + RBF(l2) 
 
gp = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=3000,
                              optimizer = 'fmin_l_bfgs_b')

gp = gp.fit(X, y)

R_2_train = round(gp.score(X,y), 4)

print('R^2 for the gaussian process  is ' + str(R_2_train))

y_gp = gp.predict(X)
MAE_Random =  round(mean_absolute_error(y,y_gp),2)

print('MAE for the gaussian process is ' + str(MAE_Random))

end = time.time()
print('The Regression took ' + str(round(end - start,0)) + ' segundos')    

start = time.time()

filename = 'PV_LowLands.joblib'
dump(gp, filename) 