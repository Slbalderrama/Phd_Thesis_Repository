# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 15:51:51 2021

@author: Dell
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.patches as mpatches
import matplotlib.lines as mlines
#import matplotlib.ticker as mtick
import matplotlib.pylab as pylab
#from scipy.stats import pearsonr
#from mpl_toolkits.mplot3d import Axes3D
from sklearn import linear_model
#from sklearn.metrics import r2_score
#import statsmodels.api as sm
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, Matern, ExpSineSquared, RationalQuadratic 
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.ensemble import RandomForestRegressor
#from scipy.stats import randint as sp_randint
#from sklearn.model_selection import RandomizedSearchCV
#from sklearn.model_selection import GridSearchCV

#%%

# load data

data = pd.read_csv('Data/Data_Espino_Thesis_Fill_2.csv', header=0,index_col=0)
index = pd.date_range(start='2016-01-01 00:00:00', periods=166464, freq=('5min'))
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
    
    forest = RandomForestRegressor(random_state=10, n_estimators =1000)
    
    y_f = np.array(y_3)
    y_f = y_f.ravel() 
    
    lm_4 = forest.fit(X_3, y_f)



print(lm_4.score(X_3,y_3))

X_4 = pd.DataFrame()
X_4['Solar Irradiation'] = data['Solar Irradiation']
X_4['PV Temperature 2']  = data['PV Temperature 2']
efficiency = pd.DataFrame(lm_4.predict(X_4), index=data.index)

data['Optimal Efficiency'] = efficiency[0]
data['Optimal PV Power'] = (data['Optimal Efficiency']*data['Solar Irradiation']*Area)/1000

data['Optimal PV Power'] = np.where(data['Optimal PV Power'] >51, 51, data['Optimal PV Power'])



start = '2016-03-21 00:00:00'
end =   '2017-03-20 23:55:00'

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

data['year'] = data.index.year
data['day']  = data.index.dayofyear
data['hour'] = data.index.hour

start = '2016-03-21 00:00:00' # '2017-01-01 00:00:00' '2016-01-01 00:00:00' 
end   = '2017-03-20 23:55:00' # '2017-07-31 23:55:00' '2016-12-31 23:55:00' 
data_hourly = data[start:end] 
data_hourly = data_hourly.groupby(['year','day', 'hour']).mean()

data_hourly_describe = data_hourly.describe()

#%%
Data_2 = pd.read_csv('Results/Gutierrez_Data.csv', index_col=0)            

index2 = pd.date_range(start='2013-01-01 01:00:00', periods=8760, 
                                   freq=('H'))

start = index2.get_loc('2013-03-21 01:00:00')

Gut_Data_1  = Data_2[start:]
    
end = index2.get_loc('2013-03-21 01:00:00')

Gut_Data_2  = Data_2[:end]

Gut_Data =  Gut_Data_1.append(Gut_Data_2) 

index_3 = pd.date_range(start='2016-03-21 01:00:00', periods=8760, 
                                   freq=('H'))

Gut_Data.index = index_3

#### Fix incoherent data
for i in Gut_Data.index:
    a = i.hour
    if any([a==0,a==1,a==2,a==3,a==4,a==5,a==20,a==21,a==22,a==23]):
        if Gut_Data.loc[i,'Radiation tilt isotropic'] > 0:
            Gut_Data.loc[i,'Radiation tilt isotropic'] = 0


Gut_Data_describe = Gut_Data.describe() 


Noct = 44.8
a = (Noct-20)/800

Gut_Data['PV Temperature'] = a*Gut_Data['Radiation tilt isotropic'] + Gut_Data['Temperature']



X_5 = pd.DataFrame()
X_5['Solar Irradiation'] = Gut_Data['Radiation tilt isotropic']
X_5['PV Temperature']  = Gut_Data['PV Temperature']
efficiency_1 = pd.DataFrame(lm_4.predict(X_5), index=Gut_Data.index)

Gut_Data['Optimal Efficiency'] = efficiency_1[0]
Gut_Data['Optimal PV Power'] = (Gut_Data['Optimal Efficiency']*Gut_Data['Radiation tilt isotropic']*Area)/1000







#%%

data_hourly.index = index_3


for i in data_hourly.index:
    a = i.hour
    if a==4:
        if data_hourly.loc[i,'Optimal PV Power']>0:
             data_hourly.loc[i,'Optimal PV Power']=0


PV_Energy = pd.DataFrame(index=index_3)

PV_Energy['PV Power Without Curtailment'] = data_hourly['Optimal PV Power']
PV_Energy['PV Power Gutierrez']           = Gut_Data['Optimal PV Power']
PV_Energy['PV Power With Curtailment']    = data_hourly['PV Power']
PV_Energy['Irradiation Gutierrez']        = Gut_Data['Radiation tilt isotropic']
PV_Energy['Irradiation Espino']           = data_hourly['Solar Irradiation']
PV_Energy['hour'] = PV_Energy.index.hour 

    
PV_Energy_1 = PV_Energy.groupby(['hour']).mean()   


Data_Optimization = pd.DataFrame()
Data_Optimization['PV Power Without Curtailment'] = list((PV_Energy['PV Power Without Curtailment']/240)*1000)
Data_Optimization['PV Power Gutierrez'] = list((PV_Energy['PV Power Gutierrez']/240)*1000)



Data_Optimization.index = range(1,8761)
Data_Optimization.columns = [1,2]

Data_Expected_Solar = pd.DataFrame()
Data_Expected_Solar[1] = (Data_Optimization[1]+Data_Optimization[2])/2
Data_Expected_Solar.to_excel('Results/Renewable_Energy_Expected.xls')


Data_Optimization[3] = Data_Optimization[1]
Data_Optimization[4] = Data_Optimization[2]
Data_Optimization[5] = Data_Optimization[1]
Data_Optimization[6] = Data_Optimization[2]
Data_Optimization[7] = Data_Optimization[1]
Data_Optimization[8] = Data_Optimization[2]
Data_Optimization[9] = Data_Optimization[1]
Data_Optimization[10] = Data_Optimization[2]

Data_Optimization.to_excel('Results/Renewable_Energy_Multy_Scenarios.xls')


# data_hourly_2


#%%
#### paper figure
size = [20,15]
plt.figure(figsize=size)


ax  = PV_Energy_1['PV Power Without Curtailment'].plot(style = '--',linewidth=5,  color='blue')
ax  = PV_Energy_1['PV Power Gutierrez'].plot(style = '--',linewidth=5,  color='red')  
ax  = PV_Energy_1['PV Power With Curtailment'].plot(style = ':',linewidth=5, color='green')
ax  = PV_Energy_1['PV Power With Curtailment'].plot(style = ':',linewidth=5, color='green')
ax1 = PV_Energy_1['Irradiation Espino'].plot(c='y', secondary_y=True,linewidth=5)

Espino_regression = mlines.Line2D([], [], color='blue',
                                  label='Espino regression', 
                                  linestyle='--',linewidth=5)
Espino_regression = mlines.Line2D([], [], color='red',
                                  label='Gutierrez regression', 
                                  linestyle='--',linewidth=5)
Espino_measurement = mlines.Line2D([], [], color='green',
                                  label='Espino measurement', 
                                  linestyle=':',linewidth=5)


Radiation = mlines.Line2D([], [], color='yellow',
                                  label='Radiation Espino', 
                                  linestyle='-',linewidth=5)

ax.tick_params(axis='x', which='major', labelsize=30)
ax.tick_params(axis='y', which='major', labelsize=30)
ax1.tick_params(axis='y', which='major', labelsize=30)
ax.set_xlabel('hours', labelpad=20, size=40 )
ax.set_ylabel('Power (kW)', labelpad=20, size=40)
ax1.set_ylabel('Irradiation (W/m$^{2}$)', labelpad=20, size=40)


##plt.legend(bbox_to_anchor=(1, -0.1),fontsize = 12,frameon=False, ncol=2)
plt.legend(handles=[Espino_regression, Espino_measurement, Radiation],
           bbox_to_anchor=(1, -0.1),frameon=False, ncol=3
           ,fontsize = 30)


#%%

# Demand and renewable energy for the dispatch model

start = '2017-01-01 00:00:00' # '2017-01-01 00:00:00' '2016-01-01 00:00:00' 
end   = '2017-06-30 23:55:00' # '2017-07-31 23:55:00' '2016-12-31 23:55:00' 

data_hourly_2 = data[start:end] 
data_hourly_2 = data_hourly_2.groupby(['year','day', 'hour']).mean()


Demand_Dispatch = pd.DataFrame()
Demand_Dispatch[1] = data_hourly_2['Demand']*1000
Demand_Dispatch.index = range(1,len(Demand_Dispatch)+1)
Demand_Dispatch.to_excel('Results/Demand_Dispatch.xls')

PV_Power = pd.DataFrame()
PV_Power[1] = data_hourly_2['Optimal PV Power']*1000
PV_Power.index = range(1,len(PV_Power)+1)
PV_Power.to_excel('Results/Renewable_Energy_Dispatch.xls')


SOC_Initial = data_hourly['SOC']['2016-12-31 23:00:00']

















