# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 19:28:42 2020

@author: Dell
"""
import pandas as pd

from joblib import load
import matplotlib.pyplot as plt

data = pd.read_csv('Bolivia/bo-1-0_0_0_0_0_0.csv', index_col=0) 
independant_variables = pd.read_csv('Bolivia/Independent_Variables_2025.csv', index_col=0) 
Base_to_Peak_grid = 0.52958

X = independant_variables['HouseHolds']
X = pd.DataFrame(X)
#'Demand_Name'


Base_To_Peak_Villages = pd.DataFrame(index=data.index)

Base_To_Peak_Villages['Base_To_Peak_Ratio'] =  Base_to_Peak_grid

path_LowLands = 'Bolivia/Surrogate_Models/LowLands/Base_to_Peak_Lowlands.joblib'
Base_To_Peak_Function_LowLands = load(path_LowLands) 


Base_to_Peak_Values_LowLands = pd.DataFrame(Base_To_Peak_Function_LowLands.predict(X))

constraints = pd.DataFrame()

constraints['elevation'] = list(data['Elevation'] < 800)
constraints['HouseHold minor'] = list(X['HouseHolds'] < 550)
constraints['HouseHold mayor'] = list(X['HouseHolds'] >= 50)
constraints['Values'] = constraints.all(axis=1)   

Base_To_Peak_Villages.loc[constraints['Values'] ,'Base_To_Peak_Ratio'] = round(Base_to_Peak_Values_LowLands[0],4)


path_HighLands = 'Bolivia/Surrogate_Models/HighLands/Base_to_Peak_Highlands.joblib'
Base_To_Peak_Function_HighLands = load(path_HighLands) 


Base_to_Peak_Values_HighLands = pd.DataFrame(Base_To_Peak_Function_HighLands.predict(X))

constraints_Highlands = pd.DataFrame()

constraints_Highlands['elevation'] = list(data['Elevation'] >= 800)
constraints_Highlands['HouseHold minor'] = list(X['HouseHolds'] < 550)
constraints_Highlands['HouseHold mayor'] = list(X['HouseHolds'] >= 50)
constraints_Highlands['Values'] = constraints_Highlands.all(axis=1)   

Base_To_Peak_Villages.loc[constraints_Highlands['Values'], 'Base_To_Peak_Ratio'] = round(Base_to_Peak_Values_HighLands[0],4)
Base_To_Peak_Villages.to_csv('Bolivia/Base_to_Peak_Grid.csv')

test = pd.DataFrame()
test['Households'] = independant_variables['HouseHolds']
test['elevation'] = data['Elevation']
test['Base_Peak_Ratio'] = Base_To_Peak_Villages['Base_To_Peak_Ratio'] 
test['Base_Peak_Ratio_Low'] = pd.DataFrame(Base_To_Peak_Function_LowLands.predict(X))
test['Base_Peak_Ratio_Low'] = round(test['Base_Peak_Ratio_Low'], 4)
test['Base_Peak_Ratio_High'] = pd.DataFrame(Base_To_Peak_Function_HighLands.predict(X))
test['Base_Peak_Ratio_High'] = round(test['Base_Peak_Ratio_High'], 4)



Test_LowLands = test.loc[test['Households'] >= 50]
Test_LowLands = Test_LowLands.loc[Test_LowLands['Households'] < 550]
Test_LowLands = Test_LowLands.loc[Test_LowLands['elevation'] < 800]
Test_LowLands.loc[:,'Boolean'] =  test['Base_Peak_Ratio']  ==  test['Base_Peak_Ratio_Low']
print(Test_LowLands['Boolean'].all()  )



Test_HighLands = test.loc[test['Households'] >= 50]
Test_HighLands = Test_HighLands.loc[Test_HighLands['Households'] < 550]
Test_HighLands = Test_HighLands.loc[Test_HighLands['elevation'] >= 800]
Test_HighLands.loc[:,'Boolean'] =  test['Base_Peak_Ratio']  ==  test['Base_Peak_Ratio_High']
print(Test_HighLands['Boolean'].all()  )

test_rest_1 = test.loc[test['Households'] >= 550]
test_rest_1.loc[:,'Boolean'] =  test_rest_1['Base_Peak_Ratio']  ==  Base_to_Peak_grid 
print(test_rest_1['Boolean'].all())



test_rest_2 = test.loc[test['Households'] < 50]
test_rest_2.loc[:,'Boolean'] =  test_rest_2['Base_Peak_Ratio']  ==  Base_to_Peak_grid 
print(test_rest_2['Boolean'].all())

