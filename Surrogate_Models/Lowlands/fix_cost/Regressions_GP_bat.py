#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 19:03:33 2019

@author: balderrama
"""

import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import cross_val_score, cross_validate, cross_val_predict
import matplotlib as mpl
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, WhiteKernel
import numpy as np
from sklearn import linear_model
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
# Cross Validation results
scoring =   [ 'neg_mean_squared_error'] #'r2' 'neg_mean_absolute_error' # 'neg_mean_squared_error'
for i in scoring:        
        
    l1 = [1,1,1,1,1,1,1,1,1,1]
    l2 = [1,1,1,1,1,1,1,1,1,1]
    
    #kernel = (C()**2)*RBF(l)
    kernel = RBF(l1) + RBF(l2) # + RBF(l3)
    gp = GaussianProcessRegressor(kernel=kernel,optimizer = 'fmin_l_bfgs_b', 
                                  n_restarts_optimizer=3000)
    scoring ='neg_mean_squared_error' #'r2' 'neg_mean_absolute_error' # 'neg_mean_squared_error'
    
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
    
    path = 'Results_Regressions/Kcross_valiadation_GP_Bat' + '_' +  i + '.csv'
    Results.to_csv(path)

# 0.86
# 53.18
# neg_mean_squared_error for the gaussian process with the test data set is 86.02249705745585
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
l1 = [1,1,1,1,1,1,1,1,1,1]
l2 = [1,1,1,1,1,1,1,1,1,1]


kernel =  RBF(l1) + RBF(l2) + WhiteKernel(noise_level_bounds=(1e-10, 1e10))
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.2,
                                                    random_state=1)

gp = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=3000,
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
#%%
# Predic vs computed plot

import matplotlib.pyplot as plt

# Calculated cross validation test results 
# 2 kernels
l1 = [6.48, 0.0117, 1.47e+04, 1.72e-05, 0.000536, 0.0456, 7.55e+03, 2.76e+04, 5.21e+04, 929]
l2 = [1.49e+03, 195, 0.368, 7.61e+03, 1e+05, 0.0817, 3.59, 0.346, 262, 95.4]

# r2 = 0.79
# MAE = 47.34
# RMSE = 81.6

# 3 kernels
#l1 = [1.48e+03, 451, 0.634, 1.01e+04, 1e+05, 0.136, 5.1, 0.524, 289, 287]
#l2 = [0.143, 1.23, 0.00335, 0.000134, 464, 71.8, 6.74e-05, 0.241, 0.0238, 2.05]
#l3 = [0.000179, 0.0629, 0.0855, 3.54e+04, 1.7, 0.000562, 2.87, 1.79e+03, 0.0507, 0.00199]

# r2 = 0.76
# MAE = 43.44
# RMSE = 87.1
#kernel = (C()**2)*RBF(l)
kernel = RBF(l1) + RBF(l2) # + RBF(l3)

gp = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=12,
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
ax= plt.scatter(y, y_gp,s = 20, marker='o')
ax2= plt.scatter(y, y_gp_2,s = 20, marker='x')
ax3= plt.plot([0, y.max()], [0, y.max()], 'k-', lw=2)
pylab.ylim([-250,1100])
pylab.xlim([0,1100])
plt.xlabel('Computed (thousand USD)', size=label_size)
plt.ylabel('Predicted (thousand USD)', size=label_size)
plt.legend([(ax),(ax2)],['GPR','MVLR'],fontsize = 20)
plt.show()

#%%
# Lenght scale analysis

l = [8.39355389e+02, 3.08601304e+02, 2.76926443e-01, 1.11221067e+04,
        1.48025407e+03, 8.80945445e-02, 3.32911702e+00, 4.34149233e-01,
        1.49795551e+02, 1.57835288e+02]
kernel =  RBF(l)

gp = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=1000,
                              optimizer = 'fmin_l_bfgs_b'
#                              , normalize_y=True
    )

gp= gp.fit(X,y)


importances = gp.kernel_.get_params()['length_scale']
feature = list(X.columns)

feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)# Print out the feature and importances 
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];



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
# 3-d plot
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
l = [8.39355389e+02, 3.08601304e+02, 2.76926443e-01, 1.11221067e+04,
        1.48025407e+03, 8.80945445e-02, 3.32911702e+00, 4.34149233e-01,
        1.49795551e+02, 1.57835288e+02]
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

y_gp = gp.predict(X1)


ax = plt.gcf().add_subplot(1, 2, 1, projection='3d')
ax.plot_surface(gx, gy, y_gp.reshape(gx.shape), cmap=cm.coolwarm, linewidth=0, alpha=0.2, antialiased=False)
#ax.scatter(X_train[:,0], X_train[:,1], Y_train, c=Y_train, cmap=cm.coolwarm)
#ax.set_title(title)




