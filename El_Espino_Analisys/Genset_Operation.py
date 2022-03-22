# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 13:46:39 2021

@author: Dell
"""

import matplotlib.pyplot as plt
from sklearn import linear_model
import numpy as np
import pandas as pd

# data from manufacture
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
plt.show()


#%%

Fuel_Cost = 0.7
Total_Fuel_Cost = np.array([5*Fuel_Cost, 8*Fuel_Cost, 
                                              12*Fuel_Cost,15*Fuel_Cost])

lm2 = linear_model.LinearRegression(fit_intercept=True)
lm2.fit(Partial_load.reshape(-1, 1), Total_Fuel_Cost.reshape(-1, 1))

Total_Fuel_Cost_2 = lm2.predict(Partial_load_1.reshape(-1, 1))

plt.scatter(Partial_load, Total_Fuel_Cost)
plt.plot(Partial_load_1, Total_Fuel_Cost_2)
plt.show()
#lm2.intercept_
#lm2.coef_



#%%

LHV = 9.9
percentage_load = 3

eff = Partial_load[percentage_load]/(fuel_comsuption[percentage_load]*LHV)
eff = round(eff*100,1)

print('Genset generator highest efficiency is '+ str(eff))

penalization = lm2.intercept_[0]/Total_Fuel_Cost[3]
penalization = round(penalization,2)
print('Penalization is ' +  str(penalization*100) + ' %' )


#%%


fix_cost = np.array([0,Total_Fuel_Cost[3]])

fix_capacity = np.array([0, Nominal_Capacity])

lm3 = linear_model.LinearRegression(fit_intercept=True)
lm3.fit(fix_capacity.reshape(-1, 1), fix_cost.reshape(-1, 1))

print(lm3.intercept_,lm3.coef_)

