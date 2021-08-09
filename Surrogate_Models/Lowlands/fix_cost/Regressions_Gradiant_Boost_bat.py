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
from sklearn import linear_model, ensemble
from math import sqrt as sq
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
#%%
# Data manipulation
data = pd.read_excel('Data_Base.xls', index_col=0, Header=None)  
#%% 
data1 = pd.DataFrame()

for i in range(50,570,50):
    
    df = data.loc[data['HouseHolds']==i]
    min_bat = df['Battery Capacity'].min()
    df = df.loc[data['Battery Capacity']>min_bat]
    data1 = data1.append(df)

data = data1
#%%
y = pd.DataFrame()
target= 'Battery Capacity'
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
#X['Generator Nominal capacity'] = data['Generator Nominal capacity'] 
X['HouseHolds'] = data['HouseHolds']
X['Renewable Energy Unit Total'] = data['Renewable Energy Unit Total']
#X['Max Demand'] = data['Max Demand']
#X['Y'] = data['Y']


feature_list = list(X.columns)
y, X = shuffle(y, X, random_state=10)
#%%
y=np.array(y)
y = y.ravel() 
#%%

from sklearn.preprocessing import MinMaxScaler


#y = np.array(y)
#y = y.reshape(1, -1) 


y = MinMaxScaler().fit_transform(y)


X = MinMaxScaler().fit_transform(X)

#y = y.transpose()
X = pd.DataFrame(X, columns=feature_list)
y = pd.DataFrame(y, columns=[target])


#%%
# Linear regression
# Linear Cross validation

scoring =   ['r2', 'neg_mean_absolute_error', 'neg_mean_squared_error'] #'r2' 'neg_mean_absolute_error' # 'neg_mean_squared_error'
for i in scoring:
    
    lm = linear_model.LinearRegression(fit_intercept=False)
    scores = cross_val_score(lm, X, y, cv=5,scoring=i)
    score = round(scores.mean(),2)
    
    if i == 'neg_mean_squared_error':
        score = sq(-score)    
        print(i + ' for the gaussian process with the test data set is ' + str(score))
    else:    
        print(i + ' for the gaussian process with the test data set is ' + str(score))

#r2 for the gaussian process with the test data set is 0.61
#neg_mean_absolute_error for the gaussian process with the test data set is -114.78
#neg_mean_squared_error for the gaussian process with the test data set is 144.46760882633865

#%%
from sklearn.model_selection import train_test_split



X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.1,
                                                    random_state=1)

params = {'n_estimators': 500,
          'max_depth': 6,
          'min_samples_split': 10,
          'learning_rate': 0.01,
          'loss': 'ls'}
reg = ensemble.GradientBoostingRegressor(**params)
reg.fit(X_train, y_train)


R_2_train = round(reg.score(X_train,y_train),4)

print('R^2 for the gradiant boost with the train data set is ' + str(R_2_train))

R_2_test = reg.score(X_test, y_test) 

print('R^2 for the gradiant boost with the test data set is ' + str(R_2_test))

y_reg = reg.predict(X_test)
MAE_Random =  round(mean_absolute_error(y_test,y_reg),2)

print('MAE for the gradiant boost is ' + str(MAE_Random))

#%%

n_estimators = [100, 300, 500]
max_depth = range(5,16,2)
min_samples_split = range(200,1001,200)
min_samples_leaf = range(30,71,10)
max_features = range(1,10,2)

hyper = dict( n_estimators = n_estimators, 
              max_depth = max_depth,  
              min_samples_split = min_samples_split, 
             min_samples_leaf = min_samples_leaf,
            max_features =max_features
                  )

gbr = ensemble.GradientBoostingRegressor(learning_rate = 0.1, subsample=0.8, random_state=10)


gridGBR = GridSearchCV(gbr, hyper, cv = 10, verbose = 1, 
                      n_jobs = -1, scoring='r2')

gridGBR.fit(X, y)

Best_Par = gridGBR.best_params_
Best_index = gridGBR.best_index_
Best_Score = gridGBR.best_score_
Results = gridGBR.cv_results_

print(Best_Par)
print(Best_index)
print(Best_Score)






























