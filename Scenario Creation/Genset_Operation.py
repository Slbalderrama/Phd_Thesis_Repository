# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 13:46:39 2021

@author: Dell
"""

import matplotlib.pyplot as plt
from sklearn import linear_model
import numpy as np
import pandas as pd


Nominal_Capacity = 58

fuel_comsuption = np.array([5,8,12,15])
Partial_load = np.array([0.25*Nominal_Capacity, 0.5*Nominal_Capacity, 
                         0.75*Nominal_Capacity, 1*Nominal_Capacity])


lm = linear_model.LinearRegression(fit_intercept=True)
lm.fit(Partial_load.reshape(-1, 1),fuel_comsuption.reshape(-1, 1))


Partial_load_1 = np.array([0*Nominal_Capacity, 0.3*Nominal_Capacity, 0.6*Nominal_Capacity,
                  0.9*Nominal_Capacity, 1.2*Nominal_Capacity])

y_1 = lm.predict(Partial_load_1.reshape(-1, 1))



plt.scatter(Partial_load, fuel_comsuption)
plt.plot(Partial_load_1, y_1)


#%%

Fuel_Cost = 0.68
Total_Fuel_Cost = np.array([5*Fuel_Cost, 8*Fuel_Cost, 
                                              12*Fuel_Cost,15*Fuel_Cost])

lm2 = linear_model.LinearRegression(fit_intercept=True)
lm2.fit(Partial_load.reshape(-1, 1), Total_Fuel_Cost.reshape(-1, 1))

Total_Fuel_Cost_2 = lm2.predict(Partial_load_1.reshape(-1, 1))

plt.scatter(Partial_load, Total_Fuel_Cost)
plt.plot(Partial_load_1, Total_Fuel_Cost_2)

#lm2.intercept_
#lm2.coef_



#%%

LHV = 9.89
percentage_load = 3

eff = Partial_load[percentage_load]*Fuel_Cost/(Total_Fuel_Cost[percentage_load]*LHV)
eff = round(eff,2)

print('Genset generator efficiency is '+ str(eff))

penalization = lm2.intercept_[0]/Total_Fuel_Cost_2[3]
penalization = round(penalization[0],2)
print('Penalization is ' +  str(penalization*100) + ' %' )


#%%


Diesel_Comsuption = pd.read_excel('Diesel Comsuption.xls',index_col=0)
Diesel_Comsuption = Diesel_Comsuption.fillna(0)
Diesel_Comsuption = Diesel_Comsuption[:-1]
Diesel_Comsuption.index =  pd.to_datetime(Diesel_Comsuption.index)


Power_Data_2 = pd.read_csv('Power_Data_2.csv',index_col=0)
Power_Data_2.index = pd.to_datetime(Power_Data_2.index)
Genset_Power = pd.DataFrame()
Genset_Power['GenSet Power'] = Power_Data_2['GenSet Power']['2017-01-01 00:00:00':'2017-06-30 23:55:00']

Genset_Power_1 = pd.DataFrame()
Genset_Power_1['GenSet Power'] =  Genset_Power['GenSet Power'].loc[Genset_Power['GenSet Power']>0]

limit = 10000

Genset_Power_1['GenSet Power']  =  Genset_Power_1['GenSet Power'].loc[Genset_Power_1['GenSet Power']>limit]




Real_efficiency = (Genset_Power_1['GenSet Power'].sum()*0.083333)/(Diesel_Comsuption['Diesel'].sum()*1000*LHV)
Real_efficiency = round(Real_efficiency,4)
print('The real efficiency of the genset is ' + str(Real_efficiency)+ '%')


Genset_Power_1['month'] = Genset_Power_1.index.month

Genset_Power_Monthly = Genset_Power_1.groupby(['month']).sum()*0.083333

Diesel_Comsuption['month'] = Diesel_Comsuption.index.month
Diesel_Comsuption_Montly = Diesel_Comsuption.groupby(['month']).sum()

Montly_Diesel_Data = pd.DataFrame()
Montly_Diesel_Data['Genset Energy'] = Genset_Power_Monthly['GenSet Power']
Montly_Diesel_Data['Diesel Comsuption'] = Diesel_Comsuption_Montly['Diesel']
Montly_Diesel_Data['Efficiency'] = Montly_Diesel_Data['Genset Energy']/(Montly_Diesel_Data['Diesel Comsuption']*1000*LHV)

for i in range(1,7):
    
    Genset_Power_2 = Genset_Power_1['GenSet Power'].loc[Genset_Power_1['month']==i]
    hours = len(Genset_Power_2)/12 
    Montly_Diesel_Data.loc[i,'Power'] = Genset_Power_2.mean()
    Montly_Diesel_Data.loc[i,'Hours'] = hours 

Montly_Diesel_Data['Diesel per hour'] = Montly_Diesel_Data['Diesel Comsuption']/Montly_Diesel_Data['Hours']
 

Genset_Manufacter_Data = pd.DataFrame()

Genset_Manufacter_Data['Fuel'] = fuel_comsuption
Genset_Manufacter_Data['Power'] = Partial_load*1000
Genset_Manufacter_Data['Efficiency'] = Genset_Manufacter_Data['Power']/(Genset_Manufacter_Data['Fuel']*1000*LHV) 



plt.scatter(Montly_Diesel_Data['Power'], Montly_Diesel_Data['Efficiency'])
plt.plot(Genset_Manufacter_Data['Power'],Genset_Manufacter_Data['Efficiency'])

plt.plot(Genset_Manufacter_Data['Power'], Genset_Manufacter_Data['Fuel'])
plt.scatter(Montly_Diesel_Data['Power'], Montly_Diesel_Data['Diesel per hour'])


X = np.array(Montly_Diesel_Data['Power'][1:]/1000)
X = X.reshape(-1, 1)
y = np.array(Montly_Diesel_Data['Diesel per hour'][1:])
y = y.reshape(-1, 1)

lm3 = linear_model.LinearRegression(fit_intercept=True)
lm3.fit(X, y)

Total_Fuel_3 = lm3.predict(Partial_load_1.reshape(-1, 1))


plt.scatter(Montly_Diesel_Data['Power'][1:]/1000, Montly_Diesel_Data['Diesel per hour'][1:])
plt.plot(Partial_load_1 ,Total_Fuel_3)
plt.plot(Genset_Manufacter_Data['Power']/1000, Genset_Manufacter_Data['Fuel'])

X_4 = X
y_4 = y

X_4 = np.append(X_4,0)  
X_4 = X_4.reshape(-1, 1)
y_4 = np.append(y_4, lm.intercept_)
y_4 = y_4.reshape(-1, 1)

lm4 = linear_model.LinearRegression(fit_intercept=True)
lm4.fit(X_4, y_4)

X_5 = np.array([0, Montly_Diesel_Data['Power'][1:].mean()/1000])
X_5 = X_5.reshape(-1, 1)
y_5 = np.array([lm.intercept_, Montly_Diesel_Data['Diesel per hour'][1:].mean()])
y_5 = y_5.reshape(-1, 1)
lm5 = linear_model.LinearRegression(fit_intercept=True)
lm5.fit(X_5, y_5)

Total_Fuel_5 = lm5.predict(Partial_load_1.reshape(-1, 1))


plt.plot(Partial_load_1 ,Total_Fuel_3)
plt.plot(Partial_load_1 ,Total_Fuel_5)
plt.plot(Genset_Manufacter_Data['Power']/1000, Genset_Manufacter_Data['Fuel'])
plt.scatter(Montly_Diesel_Data['Power'][1:]/1000, Montly_Diesel_Data['Diesel per hour'][1:])

Diesel_Comsuption_Peak_Load = np.array(58)
Diesel_Comsuption_Peak = lm5.predict(Diesel_Comsuption_Peak_Load.reshape(1, -1))
Diesel_Comsuption_Peak = Diesel_Comsuption_Peak[0][0]

efficiency_corrected = 58/(Diesel_Comsuption_Peak*LHV)
penalty_percentage = lm5.intercept_[0]/(Diesel_Comsuption_Peak)

print('The corrected efficiency is ' + str(round(efficiency_corrected,2)*100) + ' %')
print('The corrected cost penalty is ' + str(round(penalty_percentage,2)*100) + ' %')








