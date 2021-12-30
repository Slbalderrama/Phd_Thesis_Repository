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

data_regression = data_1.loc[data_1['SOC']<80]
data_regression = data_regression.loc[data_1['Efficiency']<1]
data_regression = data_regression.sample(500, random_state=10) 

X_3 = pd.DataFrame()
y_3 = pd.DataFrame()

X_3['Solar Irradiation'] = data_regression['Solar Irradiation'] 
X_3['PV Temperature 2'] = data_regression['PV Temperature 2']
y_3['Efficiency'] = data_regression['Efficiency']

    
regression = 'Forest'

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
    
    forest = RandomForestRegressor(random_state=10
                                   , n_estimators =5000
                                   )
    
    y_f = np.array(y_3)
    y_f = y_f.ravel()

    lm_4 = forest.fit(X_3,y_f )
    print('The number of points use for the regression is ' + str(len(X_3)))


print(lm_4.score(X_3,y_3))

X_4 = pd.DataFrame()
X_4['Solar Irradiation'] = data['Solar Irradiation']
X_4['PV Temperature 2']  = data['PV Temperature 2']
efficiency = pd.DataFrame(lm_4.predict(X_4), index=data.index)

data['Optimal Efficiency'] = efficiency[0]
data['Optimal PV Power'] = (data['Optimal Efficiency']*data['Solar Irradiation']*Area)/1000

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

Optimal_Power_Espino = pd.DataFrame()
Optimal_Power_Espino['Optimal PV Power'] = data['Optimal PV Power']





Optimal_Power_Espino.to_csv('Results/Renewable_Energy_Optimal_Espino.csv')

#%%
size = [20,15]
fig = plt.figure(figsize=size)
ax = fig.add_subplot(111, projection='3d')
      
    
Ys = range(50,1450,50)
Xs = range(5,70,5)
Xs, Ys = np.meshgrid(Xs, Ys)

Xs = pd.DataFrame(Xs)
Ys = pd.DataFrame(Ys)
z = pd.DataFrame()
for i in Xs.columns:
    
    X_3d = pd.DataFrame()
    X_3d['Solar Irradiation'] =  Ys[i]
    X_3d['PV Temperature 2'] = Xs[i]
    z[i] = lm_4.predict(X_3d)

scatter_plot = pd.DataFrame()

scatter_plot['PV Temperature 2'] =data_regression['PV Temperature 2']
scatter_plot['Solar Irradiation'] =data_regression['Solar Irradiation']
scatter_plot['Efficiency'] = data_regression['Efficiency']*100
scatter_plot_2 = scatter_plot.sample(500, random_state=10)

#ax.plot_surface(Xs,Ys,z*100,color='r')
ax.plot_wireframe(Xs,Ys,z*100,color='r')
ax.scatter(scatter_plot_2['PV Temperature 2'], scatter_plot_2['Solar Irradiation'],
                scatter_plot_2['Efficiency'], c='b')    
    

ax.tick_params(axis='x', which='major', labelsize=17)
ax.tick_params(axis='y', which='major', labelsize=17)
ax.tick_params(axis='z', which='major', labelsize=17)
ax.set_xlabel('PV Temperature ($^{o}$C)', labelpad=20, size=20 )
ax.set_ylabel('Irradiation (W/m$^{2}$)', labelpad=20, size=20)
ax.set_zlabel('Efficiency (%)', size=20)
pylab.ylim([0,1400])
pylab.xlim([0,70])
ax.set_zlim(8, 20)
ax.view_init(15,15)
Surface = mpatches.Patch(color='red',alpha=1, label='Superficie')
# plt.legend([(ax2),Surface],["Data", 'model'],
#                 bbox_to_anchor=(0.85,0.75) ,fontsize = 25)
    
plt.tight_layout()




#%%

data['year'] = data.index.year
data['day']  = data.index.dayofyear
data['hour'] = data.index.hour

start = '2016-03-21 00:00:00' # '2017-01-01 00:00:00' '2016-01-01 00:00:00' 
end   = '2017-03-20 23:55:00' # '2017-07-31 23:55:00' '2016-12-31 23:55:00' 
data_hourly = data[start:end] 
data_hourly = data_hourly.groupby(['year','day', 'hour']).mean()

data_hourly_describe = data_hourly.describe()

#%%


daily_plot = data.groupby(['hour']).mean()

size = [25,20]
plt.figure(figsize=size)


ax  = daily_plot['Optimal PV Power'].plot(style = '--',linewidth=5,  color='blue')
#ax  = PV_Energy_1['PV Power Gutierrez'].plot(style = '--',linewidth=5,  color='red')  
ax  = daily_plot['PV Power'].plot(style = ':',linewidth=5, color='green')
ax1 = daily_plot['Solar Irradiation'].plot(c='y', secondary_y=True,linewidth=5)

Espino_regression = mlines.Line2D([], [], color='blue',
                                  label='PV Power without curtailment', 
                                  linestyle='--',linewidth=5)

Espino_measurement = mlines.Line2D([], [], color='green',
                                  label='PV power with curtailment', 
                                  linestyle=':',linewidth=5)


Radiation = mlines.Line2D([], [], color='yellow',
                                  label='Solar irradiation', 
                                  linestyle='-',linewidth=5)

ax.tick_params(axis='x', which='major', labelsize=50)
ax.tick_params(axis='y', which='major', labelsize=50)
ax1.tick_params(axis='y', which='major', labelsize=50)

ax.set_xlabel('hours', labelpad=20, size=60 )
ax.set_ylabel('Power (kW)', labelpad=20, size=60)

ax1.set_ylabel('Irradiation (W/m$^{2}$)', labelpad=20, size=60)


##plt.legend(bbox_to_anchor=(1, -0.1),fontsize = 12,frameon=False, ncol=2)
plt.legend(handles=[Espino_regression, Espino_measurement, Radiation],
           bbox_to_anchor=(1, -0.11),frameon=False, ncol=3
           ,fontsize = 60)
#plt.tight_layout()
plt.show()

plt.savefig('Plots/Daily_PV_Power.png')

















