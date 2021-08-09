# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 19:28:42 2020

@author: Dell
"""
import pandas as pd

from joblib import load
import matplotlib.pyplot as plt

data = pd.read_csv('Onsset_Scenarios/onsset_Surrogate/Bolivia/bo-1-0_0_0_0_0_0.csv', index_col=0) 
independant_variables = pd.read_csv('Onsset_Scenarios/onsset_Surrogate/Bolivia/Independent_Variables2025.csv', index_col=0)
Base_to_Peak_grid = 0.5

X = independant_variables['HouseHolds']
X = pd.DataFrame(X)
#'Demand_Name'


Base_To_Peak_Villages = pd.DataFrame(index=data.index)

Base_To_Peak_Villages['Base_To_Peak_Ratio'] =  Base_to_Peak_grid

path = 'Peak_to_Base.joblib'
Base_To_Peak_Function = load(path) 

Base_to_Peak_Values = pd.DataFrame(Base_To_Peak_Function.predict(X))

constraints = pd.DataFrame()

constraints['elevation'] = list(data['Elevation'] < 800)
constraints['HouseHold minor'] = list(X['HouseHolds'] < 550)
constraints['HouseHold mayor'] = list(X['HouseHolds'] >= 50)
constraints['Values'] = constraints.all(axis=1)   

Base_To_Peak_Villages.loc[constraints['Values'] ,'Base_To_Peak_Ratio'] = round(Base_to_Peak_Values[0],2)

test = Base_to_Peak_Values.loc[constraints['Values']]
test['HouseHolds'] = X['HouseHolds'].loc[constraints['Values']]


Demand = pd. DataFrame()

for i in range(50, 570,50):
    
    Village = 'village_' + str(i)
    Energy_Demand = pd.read_excel('Example/Demand.xls',sheet_name=Village
                                  ,index_col=0,Header=None)
    
    
    Demand[i] = Energy_Demand[1]
    
    
    
Demand_mean = Demand.mean()
Demand_max = Demand.max()

Peak_to_Base = Demand_mean/Demand_max



plt.scatter(test['HouseHolds'], test[0])
plt.scatter(Peak_to_Base.index,Peak_to_Base)

plt.xlabel('HouseHolds')
plt.ylabel('Peak to base ratio')

df = constraints.loc[constraints['Values']==True]
print(len(df))

Base_To_Peak_Villages.to_csv('Base_to_Peak/Base_to_Peak_SA_Diesel.csv')
