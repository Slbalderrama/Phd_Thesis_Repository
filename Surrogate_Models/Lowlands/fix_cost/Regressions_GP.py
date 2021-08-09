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
data = pd.read_excel('Data_Base.xls', index_col=0, Header=None)   
#data = data.loc[data['Gap']< 1]

y = pd.DataFrame()
target='NPC'
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
scoring = ['r2', 'neg_mean_absolute_error', 'neg_mean_squared_error']   #'r2' 'neg_mean_absolute_error' # 'neg_mean_squared_error'

for i in scoring:

    lm = linear_model.LinearRegression(fit_intercept=True)
    scores = cross_val_score(lm, X, y, cv=5, scoring=i)
    score = round(scores.mean(),2)
    
    if i == 'neg_mean_squared_error':
        score = sq(-score)    
        print(i + ' for the linear regression with the test data set is ' + str(score))
    else:    
        print(i + ' for the linear regression with the test data set is ' + str(score))


# r2 for the linear regression with the test data set is 0.85
# neg_mean_absolute_error for the linear regression with the test data set is -85059.88
# neg_mean_squared_error for the linear regression with the test data set is 116080.51621409168
    
    
    
    
#%%

# Cross Validation results

scoring = ['r2', 'neg_mean_absolute_error', 'neg_mean_squared_error']   #'r2' 'neg_mean_absolute_error' # 'neg_mean_squared_error'

for i in scoring:
    l = [1,1,1,1,1,1,1,1,1,1]
    
    kernel =  RBF(l)
    gp = GaussianProcessRegressor(kernel=kernel,optimizer = 'fmin_l_bfgs_b', 
                                  n_restarts_optimizer=3000)
    
    Results = cross_validate(gp, X, y, cv=5,return_train_score=True,n_jobs=-1
                             , scoring = i)
    
    scores = Results['test_score']
    score = round(scores.mean(),2)
    
    if i == 'neg_mean_squared_error':
        score = sq(-score)    
        print(i + ' for the linear regression with the test data set is ' + str(score))
    else:    
        print(i + ' for the linear regression with the test data set is ' + str(score))
    
    Results = pd.DataFrame(Results)
    
    path = 'Results_Regressions/Kcross_valiadation_GP_NPC' + '_' +  i + '.csv'
    Results.to_csv(path)

#r2 for the linear regression with the test data set is 0.98
#neg_mean_absolute_error for the linear regression with the test data set is -21775.83
#neg_mean_squared_error for the linear regression with the test data set is 36687.43640144402
#%%

# Cross Validation 
l = [1,1,1,1,1,1,1,1,1,1]
#l = [8.39355389e+02, 3.08601304e+02, 2.76926443e-01, 1.11221067e+04,
#       1.48025407e+03, 8.80945445e-02, 3.32911702e+00, 4.34149233e-01,
#        1.49795551e+02, 1.57835288e+02]
#kernel = (C()**2)*RBF(l)
kernel =  RBF(l)
gp = GaussianProcessRegressor(kernel=kernel,optimizer = 'fmin_l_bfgs_b', 
                              n_restarts_optimizer=3000)

Results = cross_validate(gp, X, y, cv=5,return_train_score=True,n_jobs=-1
                         , scoring = 'r2' #'neg_mean_absolute_error'
                         )
scores = Results['test_score']
scores.mean()


#%%
from sklearn.model_selection import train_test_split
#l = [1,1,1,1,1,1,1,1,1,1]
l = [8.39355389e+02, 3.08601304e+02, 2.76926443e-01, 1.11221067e+04,
        1.48025407e+03, 8.80945445e-02, 3.32911702e+00, 4.34149233e-01,
        1.49795551e+02, 1.57835288e+02]
#kernel =  (C()**2)*RBF(l)
kernel =  RBF(l,(1e-3, 1e4))
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.1,
                                                    random_state=500)

gp = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=50,
                              optimizer = 'fmin_l_bfgs_b'
#                              , normalize_y=True
                              
                              )

gp = gp.fit(X_train, y_train)

R_2_train = round(gp.score(X_train,y_train),4)

print('R^2 for the gaussian process with the train data set is ' + str(R_2_train))

R_2_test = gp.score(X_test, y_test) 

print('R^2 for the gaussian process with the test data set is ' + str(R_2_test))

y_gp = gp.predict(X_test)
MAE_Random =  round(mean_absolute_error(y_test,y_gp),2)

print('MAE for the gaussian process is ' + str(MAE_Random))


MSE_Random  =  round(mean_squared_error(y_test,y_gp),2)  
RMSE_Random =  sq(MSE_Random)

print('RMSE for the gaussian process is ' + str(RMSE_Random))


#%%
# Predic vs computed plot

import matplotlib.pyplot as plt

# Calculated cross validation test results 
l =[8.26459587e+02, 3.10898721e+02, 2.79234836e-01, 1.00000000e+04,
       1.48768827e+03, 8.85831523e-02, 3.35587188e+00, 4.36428113e-01,
       1.50841521e+02, 1.59367361e+02]
kernel =  RBF(l)

gp = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=10,
                              optimizer = 'fmin_l_bfgs_b'
#                              , normalize_y=True
    )

y_gp = cross_val_predict(gp, X, y, cv=5,n_jobs=-1)



lm = linear_model.LinearRegression(fit_intercept=True)
y_gp_2 = cross_val_predict(lm, X, y, cv=5,n_jobs=-1)


# Plot
size = [20,15]
label_size = 25
tick_size = 25 

fig = plt.subplots(figsize=size)

mpl.rcParams['xtick.labelsize'] = tick_size 
mpl.rcParams['ytick.labelsize'] = tick_size 
ax= plt.scatter(y/1000, y_gp/1000,s = 20, marker='o')
ax2= plt.scatter(y/1000, y_gp_2/1000,s = 20, marker='x')
ax3= plt.plot([0, y.max()/1000], [0, y.max()/1000], 'k-', lw=2)
pylab.ylim([0,1400])
pylab.xlim([0,1400])
plt.xlabel('Computed (thousand USD)', size=label_size)
plt.ylabel('Predicted (thousand USD)', size=label_size)
plt.legend([(ax),(ax2)],['GPR','MVLR'],fontsize = 20)
plt.show()

#%%
# Lenght scale analysis

#l = [8.39355389e+02, 3.08601304e+02, 2.76926443e-01, 1.11221067e+04,
#        1.48025407e+03, 8.80945445e-02, 3.32911702e+00, 4.34149233e-01,
#        1.49795551e+02, 1.57835288e+02] # not normalize
l =[ 7.52542321,  0.75595608,  2.94102693,  3.55769015, 12.05544937,
        0.36818113,  2.79709807,  0.59912631,  1.12407151,  7.26211839] # normalize


kernel =  RBF(l)

gp = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=100,
                              optimizer = 'fmin_l_bfgs_b'
#                              , normalize_y=True
    )

gp= gp.fit(X,y)


importances = gp.kernel_.get_params()['length_scale']
feature = list(X.columns)

feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)# Print out the feature and importances 
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];


####################### Not normalize
#Variable: Battery Cycles       Importance: 8196.86
#Variable: GenSet Unitary Invesment Cost Importance: 1509.19
#Variable: Renewable Invesment Cost Importance: 727.19
#Variable: Battery Unitary Invesment Cost Importance: 323.61
#Variable: Renewable Energy Unit Total Importance: 154.74
#Variable: HouseHolds           Importance: 153.6
#Variable: Low Heating Value    Importance: 3.44
#Variable: Fuel Cost            Importance: 0.43
#Variable: Deep of Discharge    Importance: 0.3
#Variable: Generator Efficiency Importance: 0.09



#%%
# 3-d plot Not normalize
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


l = [8.39355389e+02, 3.08601304e+02, 2.76926443e-01, 1.11221067e+04,
        1.48025407e+03, 8.80945445e-02, 3.32911702e+00, 4.34149233e-01,
        1.49795551e+02, 1.57835288e+02] # Not normalize

kernel =  RBF(l)

gp = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=100,
                              optimizer = 'fmin_l_bfgs_b'
#                              , normalize_y=True
    )

gp= gp.fit(X,y)

print(gp.score(X,y))

# Mesh creation
x_1, x_2 = np.arange(1000, 7000, 100), np.arange(1000,2000, 50)
gx, gy = np.meshgrid(x_1, x_2)
x_2D = np.c_[gx.ravel(), gy.ravel()]
X_2D = pd.DataFrame(x_2D)


X1 = pd.DataFrame(index=range(len(X_2D)))
X1['Renewable Invesment Cost'] = 1400
X1['Battery Unitary Invesment Cost'] = 500
X1['Deep of Discharge'] = 0.2
X1['Battery Cycles'] = X_2D[0] #1
X1['GenSet Unitary Invesment Cost'] = X_2D[1] #2
X1['Generator Efficiency'] = 0.3
X1['Low Heating Value'] = 10
X1['Fuel Cost'] = 0.68
#X['Generator Nominal capacity'] = data['Generator Nominal capacity'] 
X1['HouseHolds'] = 100
X1['Renewable Energy Unit Total'] = 450
#X['Max Demand'] = data['Max Demand']
#X['Y'] = data['Y']

y_gp = gp.predict(X1)/1000


# Plot
size = [20,15]
label_size = 25
tick_size = 25 
fig = plt.figure(figsize=size)
ax = plt.gcf().add_subplot(1, 2, 1, projection='3d')
ax.plot_surface(gx, gy, y_gp.reshape(gx.shape), cmap=cm.coolwarm, 
                linewidth=0, alpha=0.2, antialiased=False)
ax.tick_params(axis='x', which='major', labelsize=17)
ax.tick_params(axis='y', which='major', labelsize=17)
ax.tick_params(axis='z', which='major', labelsize=17, pad=10)
ax.set_xlabel('Battery Cycles', labelpad=20, size=20 )
ax.set_ylabel('Genset Cost (USD/kW)', labelpad=20, size=20)
ax.set_zlabel('NPC (thousand USD)', labelpad=23, size=20)
pylab.ylim([1000,2000])
pylab.xlim([1000,7000])



#ax.scatter(X_train[:,0], X_train[:,1], Y_train, c=Y_train, cmap=cm.coolwarm)
#ax.set_title(title)

#%%


# 3-d plot Not normalize
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

l = [ 7.52542321,  0.75595608,  2.94102693,  3.55769015, 12.05544937,
        0.36818113,  2.79709807,  0.59912631,  1.12407151,  7.26211839] # normalize
kernel =  RBF(l)

gp = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=10,
                              optimizer = 'fmin_l_bfgs_b'
#                              , normalize_y=True
    )

gp= gp.fit(X,y)

print(gp.score(X,y))

# Mesh creation
x_1, x_2 = np.arange(0, 1, 0.01), np.arange(0, 1, 0.01)
gx, gy = np.meshgrid(x_1, x_2)
x_2D = np.c_[gx.ravel(), gy.ravel()]
X_2D = pd.DataFrame(x_2D)

# Normalize

#Variable: GenSet Unitary Invesment Cost Importance: 12.06
#Variable: Renewable Invesment Cost Importance: 7.53
#Variable: Renewable Energy Unit Total Importance: 7.26
#Variable: Battery Cycles       Importance: 3.56
#Variable: Deep of Discharge    Importance: 2.94
#Variable: Low Heating Value    Importance: 2.8
#Variable: HouseHolds           Importance: 1.12
#Variable: Battery Unitary Invesment Cost Importance: 0.76
#Variable: Fuel Cost            Importance: 0.6
#Variable: Generator Efficiency Importance: 0.37
X1 = pd.DataFrame(index=range(len(X_2D)))
X1['Renewable Invesment Cost'] = 0.7
X1['Battery Unitary Invesment Cost'] = 0.7
X1['Deep of Discharge'] = 0.7
X1['Battery Cycles'] =  0.7
X1['GenSet Unitary Invesment Cost'] = X_2D[0] #1
X1['Generator Efficiency'] = 0.7
X1['Low Heating Value'] = 0.7
X1['Fuel Cost'] = 0.68
#X['Generator Nominal capacity'] = data['Generator Nominal capacity'] 
X1['HouseHolds'] = 0.7
X1['Renewable Energy Unit Total'] = X_2D[1] #2
#X['Max Demand'] = data['Max Demand']
#X['Y'] = data['Y']

y_gp = gp.predict(X1)


ax = plt.gcf().add_subplot(1, 2, 1, projection='3d')
ax.plot_surface(gx, gy, y_gp.reshape(gx.shape), cmap=cm.coolwarm, linewidth=0, alpha=0.2, antialiased=False)
#ax.scatter(X_train[:,0], X_train[:,1], Y_train, c=Y_train, cmap=cm.coolwarm)
#ax.set_title(title)


