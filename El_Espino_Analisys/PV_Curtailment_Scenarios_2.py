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

#%%

# load data

data = pd.read_csv('Data/Data_Espino_Thesis_Fill_2.csv', header=0,index_col=0)
index = pd.DatetimeIndex(start='2016-01-01 00:00:00', periods=166464, freq=('5min'))
data.index = index
Area = 1.61*0.946*240 # 1.61*0.946*240 # 1.65*0.99*240

data_1 = data.loc[data['PV Power']>0]
data_1.loc[:,'Efficiency'] = (data['PV Power']*1000)/(data['Solar Irradiation']*Area)

#%%

# Limit creation

a = np.array([200,1600])
b = np.array([0.2,0.1])
c = np.array([0,200])
d = np.array([0.16,0.2])

Delta = 0.05

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

    
regression = 'Linear'

if regression == 'Linear':
        
    lm_4 = linear_model.LinearRegression(fit_intercept=True)
    lm_4.fit(X_3,y_3)
    
     

elif regression == 'Gaussian':     
    l1 = [1,1]
    kernel =  RBF(l1) 
    lm_4 = GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=3000,
                                  optimizer = 'fmin_l_bfgs_b')
    
    lm_4.fit(round(X_3,2),y_3)
    
    

elif regression == 'Forest': 
    
    forest = RandomForestRegressor(random_state=10, n_estimators =1000)
    
    y_f = np.array(y_3)
    y_f = y_f.ravel() 
    
    lm_4 = forest.fit(X_3, y_f)
    print('The number of points use for the regression is ' + str(len(X_3)))


print(lm_4.score(X_3,y_3))

X_4 = pd.DataFrame()
X_4['Solar Irradiation'] = data['Solar Irradiation']
X_4['PV Temperature 2']  = data['PV Temperature 2']
efficiency = pd.DataFrame(lm_4.predict(X_4), index=data.index)

data['Optimal Efficiency'] = efficiency[0]
data['Optimal PV Power'] = (data['Optimal Efficiency']*data['Solar Irradiation']*240 )/1000

data['Optimal PV Power'] = np.where(data['Optimal PV Power'] >51, 51, data['Optimal PV Power'])



start = '2016-01-01 00:00:00'
end =   '2017-07-31 23:55:00'

Energy_Real     = round(data['PV Power'][start:end].sum()/(12*1000),1)
Energy_Optimal  = round(data['Optimal PV Power'][start:end].sum()/(12*1000),1)
Lost_Percentage =  1 - Energy_Real/Energy_Optimal 
Lost_Percentage = round(Lost_Percentage*100,1)

print('Total energy with curtailment is ' + str(Energy_Real) + ' MWh')
print('Total energy without curtailment is ' + str(Energy_Optimal) + ' MWh')
print('Extra energy in optimal conditions ' + str(Lost_Percentage) + ' %')








