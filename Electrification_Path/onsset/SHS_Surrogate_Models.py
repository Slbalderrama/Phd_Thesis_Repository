# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 17:14:52 2021

@author: Dell
"""


import pandas as pd
from joblib import dump
from sklearn import linear_model

#%%
y = pd.DataFrame(index=range(10))
y['LCOE'] = 0.35
y['NPC'] = 1591
y['Battery'] = 1.1
y['PV'] = 0.4
y['Investment'] = 1293
y['Genset'] = 0

X =  pd.DataFrame(index=range(10))
X['Fuel Cost'] = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
X['HouseHolds'] =  list(range(50,505,50))

#%%


lm_lcoe = linear_model.LinearRegression(fit_intercept=True)
lm_lcoe.fit(X, y['LCOE'])


filename_lcoe = 'Bolivia/Surrogate_Models/SHS/LCOE_SHS.joblib'
dump(lm_lcoe, filename_lcoe) 


#%%


lm_NPC = linear_model.LinearRegression(fit_intercept=True)
lm_NPC.fit(X, y['NPC'])


filename_NPC = 'Bolivia/Surrogate_Models/SHS/NPC_SHS.joblib'
dump(lm_NPC, filename_NPC) 



#%%


lm_Battery = linear_model.LinearRegression(fit_intercept=True)
lm_Battery.fit(X, y['Battery'])


filename_Battery = 'Bolivia/Surrogate_Models/SHS/Battery_SHS.joblib'
dump(lm_Battery, filename_Battery) 

#%%


lm_PV = linear_model.LinearRegression(fit_intercept=True)
lm_PV.fit(X, y['PV'])


filename_PV = 'Bolivia/Surrogate_Models/SHS/PV_SHS.joblib'
dump(lm_PV, filename_PV) 

#%%


lm_Genset = linear_model.LinearRegression(fit_intercept=True)
lm_Genset.fit(X, y['Genset'])


filename_Genset = 'Bolivia/Surrogate_Models/SHS/Genset_SHS.joblib'
dump(lm_Genset, filename_Genset) 


#%%


lm_Investment = linear_model.LinearRegression(fit_intercept=True)
lm_Investment.fit(X, y['Investment'])


filename_Investment = 'Bolivia/Surrogate_Models/SHS/Investment_SHS.joblib'
dump(lm_Investment, filename_Investment) 


#%%


X1 = pd.DataFrame()
X1[1] = range(1,50)

y1 = 603*X1

lm_demand = linear_model.LinearRegression(fit_intercept=True) 
lm_demand.fit(X1,y1) 

filename_demand = 'Bolivia/Surrogate_Models/SHS/demand_regression_SHS.joblib'
dump(lm_demand, filename_demand) 

#%%

X2 = pd.DataFrame()
X2[1] = range(1,50)

y2 = 0*X1

lm_demand = linear_model.LinearRegression(fit_intercept=True) 
lm_demand.fit(X2,y2) 

filename_demand = 'Bolivia/Surrogate_Models/SHS/Base_to_Peak_SHS.joblib'
dump(lm_demand, filename_demand) 


