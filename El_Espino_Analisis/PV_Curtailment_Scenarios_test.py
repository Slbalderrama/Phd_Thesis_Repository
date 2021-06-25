# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 15:51:51 2021

@author: Dell
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.ticker as mtick
import matplotlib.pylab as pylab
from scipy.stats import pearsonr
from mpl_toolkits.mplot3d import Axes3D
from sklearn import linear_model
from sklearn.metrics import r2_score
import statsmodels.api as sm
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, Matern, ExpSineSquared, RationalQuadratic 
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import randint as sp_randint
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle
#%%

# load data

data = pd.read_csv('Data/Data_Espino_Thesis_Fill.csv', header=0,index_col=0)
index = pd.DatetimeIndex(start='2016-01-01 00:00:00', periods=166464, freq=('5min'))
data.index = index
Area = 1.65*0.99*240 # 1.61*0.946*240 # 1.65*0.99*240

data_1 = data.loc[data['PV Power']>0]
data_1.loc[:,'Efficiency'] = (data['PV Power']*1000)/(data['Solar Irradiation']*Area)


#%%

# Limit creation

a = np.array([200,1600])
b = np.array([0.187,0.09])
c = np.array([0,200])
d = np.array([0.16,0.187])

Delta = 0.045

foo = float(d[1]) - Delta 

f = np.array([0.07,foo])


b_1 = b - Delta

a = a.reshape((2,1))
b = b.reshape((2,1))
b_1 = b_1.reshape((2,1))

lm = linear_model.LinearRegression(fit_intercept=True)
lm.fit(a,b)
lm_1 = linear_model.LinearRegression(fit_intercept=True)
lm_1.fit(a, b_1)



c = c.reshape((2,1))
d = d.reshape((2,1))
f = f.reshape((2,1))


lm_2 = linear_model.LinearRegression(fit_intercept=True)
lm_2.fit(c,d)
lm_3 = linear_model.LinearRegression(fit_intercept=True)
lm_3.fit(c, f)



#%%


ax1 = plt.scatter(data_1['Solar Irradiation'], data_1['Efficiency'])
ax1 = plt.plot(a,lm.predict(a), c='r') 
ax1 = plt.plot(c,lm_2.predict(c), c='r')

ax1 = plt.plot(a, lm_1.predict(a), c='g')
ax1 = plt.plot(c, lm_3.predict(c), c='g')

plt.xlabel('Irradiation (W/m^2)')
plt.ylabel('Efficiency (%)')
pylab.ylim([0,0.25])
pylab.xlim([0,1600])

plt.show()


data_paper_1 = pd.DataFrame()



# all the data mayor to 200  of irradiation
data_1_1 = data_1.loc[data_1['Solar Irradiation']>200]

X_1 = pd.DataFrame()
X_1['Solar Irradiation'] = data_1_1['Solar Irradiation']

Upper_Limit_1 = pd.DataFrame(lm.predict(X_1)  , index = data_1_1.index)
Lower_Limit_1 = pd.DataFrame(lm_1.predict(X_1), index = data_1_1.index)

data_1_1.loc[:,'Upper Limit'] = Upper_Limit_1[0]
data_1_1.loc[:,'Lower Limit'] = Lower_Limit_1[0]

data_regression_1 = data_1_1.loc[data_1_1['Efficiency'] > data_1_1['Lower Limit']]
data_regression_1 = data_regression_1.loc[data_regression_1['Efficiency'] < data_regression_1['Upper Limit']]


# all the data minor to 200  of irradiation
data_1_2 = data_1.loc[data_1['Solar Irradiation']<200]

X_2 = pd.DataFrame()
X_2['Solar Irradiation'] = data_1_2['Solar Irradiation']

Upper_Limit_2 = pd.DataFrame(lm_2.predict(X_2)  , index = data_1_2.index)
Lower_Limit_2 = pd.DataFrame(lm_3.predict(X_2), index = data_1_2.index)

data_1_2.loc[:,'Upper Limit'] = Upper_Limit_2[0]
data_1_2.loc[:,'Lower Limit'] = Lower_Limit_2[0]

data_regression_2 = data_1_2.loc[data_1_2['Efficiency'] > data_1_2['Lower Limit']]
data_regression_2 = data_regression_2.loc[data_regression_2['Efficiency'] < data_regression_2['Upper Limit']]

data_regression = pd.DataFrame()

data_regression = data_regression.append(data_regression_1)
data_regression = data_regression.append(data_regression_2)


X_3 = pd.DataFrame()
y_3 = pd.DataFrame()

X_3['Solar Irradiation'] = data_regression['Solar Irradiation'] 
X_3['PV Temperature 2'] = data_regression['PV Temperature 2']
y_3['Efficiency'] = data_regression['Efficiency']

y_3, X_3 = shuffle(y_3, X_3, random_state=10)
lm_4 = linear_model.LinearRegression(fit_intercept=True)
lm_4.fit(X_3,y_3)
    
     


    # l1 = [1,1]
    # kernel =  RBF(l1) 
    # lm_4 = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=3000,
    #                               optimizer = 'fmin_l_bfgs_b')
    
    # lm_4.fit(round(X_3,2),y_3)
    
Optimize = True

forest = RandomForestRegressor(random_state=10)

    
y_f = np.array(y_3)
y_f = y_f.ravel() 

if Optimize == True:    
    
    n_estimators = [500]
#    max_depth    = [None, 15, 25, 30]
    min_samples_split = [2, 5, 10, 15]
    min_samples_leaf = [ 5, 10,15] 
    max_features = [0.2,0.3,0.4]
    
    hyperF = dict(n_estimators = n_estimators, 
#                  max_depth = max_depth,  
    min_samples_split = min_samples_split, 
    min_samples_leaf = min_samples_leaf,
    max_features =max_features
                      )
    
   
    
    gridF = GridSearchCV(forest, hyperF, cv = 10, verbose = 1, 
                          n_jobs = 10, scoring='r2')

    
    bestF = gridF.fit(X_3, y_f)
    Best_Par = bestF.best_params_
    Best_index = bestF.best_index_
    Best_Score = bestF.best_score_
    Results = bestF.cv_results_    
    
    
    
    print(Best_Par)
    print(Best_Score)    


forest1 = RandomForestRegressor(random_state=10, n_estimators=Best_Par['n_estimators'], 
#                                max_depth = Best_Par['max_depth'] 
                                )
  
forest1.fit(X_3, y_f)



print(lm_4.score(X_3,y_3))
print(forest1.score(X_3,y_3))




X_4 = pd.DataFrame()
X_4['Solar Irradiation'] = data['Solar Irradiation']
X_4['PV Temperature 2']  = data['PV Temperature 2']


efficiency_1 = pd.DataFrame(lm_4.predict(X_4), index=data.index)
efficiency_2 = pd.DataFrame(forest1.predict(X_4), index=data.index)

data1 = pd.DataFrame()

data1['Optimal Efficiency Linear'] = efficiency_1[0]
data1['Optimal Efficiency Forest'] = efficiency_2[0]

data1['Optimal PV Power Linear'] = (data1['Optimal Efficiency Linear']*data['Solar Irradiation']*Area)/1000
data1['Optimal PV Power Forest'] = (data1['Optimal Efficiency Forest']*data['Solar Irradiation']*Area)/1000
data1['PV Power Real'] = data['PV Power']




#%%

data1['hour'] = data.index.hour

data_hourly = data1
data_hourly = data_hourly.groupby(['hour']).mean()

data_hourly_describe = data_hourly.describe()

data_hourly['Optimal PV Power Linear'].plot()
data_hourly['Optimal PV Power Forest'].plot()
data_hourly['PV Power Real'].plot()

plt.legend()


