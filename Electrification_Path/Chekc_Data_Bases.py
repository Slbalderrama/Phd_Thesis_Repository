# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 16:54:42 2022

@author: Dell
"""

import pandas as pd

microgrids_solution =  pd.read_csv('REF/Bolivia/Microgrids_results.csv', index_col=0)
SHS_solution =  pd.read_csv('REF/Bolivia/SHS_Results.csv', index_col=0)
Grid_Unconnected_solution =  pd.read_csv('REF/Bolivia/grid_Solution_No_Electricity.csv', index_col=0)

result_old = pd.read_csv('REF_Old/Bolivia/Unconnected_2012_results.csv', index_col=0)


test = microgrids_solution.index
test = test.append(SHS_solution.index)
test = test.append(Grid_Unconnected_solution.index)
test = pd.DataFrame(test)

test = test[0].sort_values()

test1 = test == result_old.index

print(test1.any())


test2 = result_old['HouseHolds'].sum() - (microgrids_solution['HouseHolds'].sum() 
                                           + SHS_solution['HouseHolds'].sum() 
                                           + Grid_Unconnected_solution['HouseHolds'].sum())

print(test2)


test3 = result_old['HouseHolds'] - (microgrids_solution['HouseHolds']
                                           + SHS_solution['HouseHolds'] 
                                           + Grid_Unconnected_solution['HouseHolds'])

print(test3.sum())