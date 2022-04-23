
from runner import scenario
import pandas as pd
import os


specs_path = os.path.join('Bolivia', 'specs_paper_new.xlsx')
calibrated_csv_path = os.path.join('Bolivia', 'Database_new_1.csv')
results_folder = os.path.join('Bolivia')
summary_folder	= os.path.join('Bolivia')
  
scenario(specs_path, calibrated_csv_path, results_folder, summary_folder)

data = pd.read_csv('Bolivia/bo-1-0_0_0_0_0_0.csv', index_col=0)  
summary = pd.read_csv('Bolivia/bo-1-0_0_0_0_0_0_summary.csv', index_col=0)
indpendant_variables = pd.read_csv('Bolivia/Independent_Variables_2025.csv', index_col=0) 

#%%

df= pd.DataFrame()


df['FinalElecCode2012'] = data['FinalElecCode2012']
df['Demand_Name2025'] = data['Demand_Name2025']
df['Elevation'] = data['Elevation']
df['HouseHolds'] = indpendant_variables['HouseHolds']
df['LCOE_SHS2025'] = data['SHS2025']
df['LCOE_MG_Hybrid_LowLands2025'] = data['MG_Hybrid_LowLands2025']
df['LCOE_MG_Hybrid_HighLands2025'] = data['MG_Hybrid_HighLands2025']
df['LCOE_Grid2025'] = data['Grid2025']
df['MinimumOverall2025'] = data['MinimumOverall2025']
df['MinimumOverallLCOE2025'] = data['MinimumOverallLCOE2025']
df['NewConnections2025'] = data['NewConnections2025']
df['PVcapacity2025'] = data['PVcapacity2025']
df['GenSetcapacity2025'] = data['GenSetcapacity2025']
df['Batterycapacity2025'] = data['Batterycapacity2025']
df['NewCapacity2025'] = data['NewCapacity2025']
df['NPC2025'] = data['NPC2025']
df['InvestmentCapita2025'] = data['InvestmentCapita2025']
df['InvestmentCost2025'] = data['InvestmentCost2025']
df['MinGridDist2025'] = data['MinGridDist2025']
df['Pop2025'] = data['Pop2025']
df['ElecPopCalib'] = data['ElecPopCalib']
df['X_deg'] = data['X_deg']
df['Y_deg'] = data['Y_deg']
#%%

df_2012 = df.loc[df['FinalElecCode2012'] !='Grid2012']
df_2012.to_csv('Bolivia/Unconected_2012_Ref.csv')
Grid_Unconnected = len(df_2012)


print('The number of Unconnected communities in Bolivia is ' + str(Grid_Unconnected))

grid_2012 = df.loc[df['FinalElecCode2012'] =='Grid2012']
Grid_Connected_Percentage = (grid_2012['ElecPopCalib'].sum()/data['Pop2012'].sum())*100

print('The % of people connected to the grid in 2012 was ' + str(round(Grid_Connected_Percentage,0)))
#%%



#%%
df_lowlands = df.loc[df['Elevation']<800]
df_lowlands = df_lowlands.loc[df_lowlands['HouseHolds']>=50]
df_lowlands = df_lowlands[df_lowlands['HouseHolds']<550]


df_highlands = df.loc[df['Elevation']>=800]
df_highlands = df_highlands.loc[df_highlands ['HouseHolds']>=50]
df_highlands = df_highlands[df_highlands ['HouseHolds']<550]

df_SHS = df.loc[df['HouseHolds']<50]

df_rest = df.loc[df['HouseHolds']>=550]

#%%
grid_solution = df.loc[df['MinimumOverall2025'] == 'Grid2025'] 
microgrids_solution = df.loc[(df['MinimumOverall2025'] == 'MG_Hybrid_LowLands2025') |
                             (df['MinimumOverall2025'] == 'MG_Hybrid_HighLands2025')]
SHS_solution = df.loc[df['MinimumOverall2025'] == 'SHS2025'] 

Results = pd.DataFrame()

#%%
Results.loc['grid','people'] =  round(grid_solution['NewConnections2025'].sum(),0)

Total_Grid_People = round(grid_solution['Pop2025'].sum(),0)
Total_people =   round(df['Pop2025'].sum(),0)    
rate_grid = Total_Grid_People/Total_people
rate_grid = round(rate_grid*100,0)
print('The number of Unconnected communities in Bolivia is ' + str(rate_grid) + ' %')


print('New connected people with the grid is ' +str(Results.loc['grid','people']))

Results.loc['microgrid','people'] =  round(microgrids_solution['NewConnections2025'].sum(),0)

print('New connected people with microgrid is ' + str(Results.loc['microgrid','people']))

Results.loc['SHS','people'] =  round(SHS_solution['NewConnections2025'].sum(),0)

print('New connected people with SHS is ' +str(Results.loc['SHS','people']))

Results.loc['Total','people'] = (Results.loc['grid','people'] 
                                 + Results.loc['microgrid','people'] 
                                 + Results.loc['SHS','people']) 

print('Total number of new connected  people is ' +str(Results.loc['Total','people']))
rate_grid_2025 = Results.loc['grid','people']/Results.loc['Total','people']
rate_grid_2025 = round(rate_grid_2025*100,1)
print(rate_grid_2025)
rate_microgrid_2025 = Results.loc['microgrid','people']/Results.loc['Total','people']
rate_microgrid_2025 = round(rate_microgrid_2025*100,1)
print(rate_microgrid_2025)
rate_shs_2025 = Results.loc['SHS','people']/Results.loc['Total','people']
rate_shs_2025 = round(rate_shs_2025*100,1)
print(rate_shs_2025)
#%%


Results.loc['grid','NPC'] =  round(grid_solution['NPC2025'].sum()/1000000,0)

print('The total NPC of the grid is ' + str(Results.loc['grid','NPC'])+ 
      ' thousands of millons of USD.')

Results.loc['microgrid','NPC'] =  round(microgrids_solution['NPC2025'].sum()/1000000,0)

print('The total NPC of the microgrid is ' + str(Results.loc['microgrid','NPC']) + 
      ' thousands of millons of USD.')

Results.loc['SHS','NPC'] =  round(SHS_solution['NPC2025'].sum()/1000000,0)

print('The total NPC of the SHS is ' +str(Results.loc['SHS','NPC'])+ 
      ' thousands of millons of USD.')

Results.loc['Total','NPC'] = (Results.loc['grid','NPC'] 
                              + Results.loc['microgrid','NPC'] 
                              + Results.loc['SHS','NPC']) 

print('Total NPC is ' +str(Results.loc['Total','NPC'])+ 
      ' thousands of millons of USD.')

#%%


Results.loc['grid','Capacity'] =  round(grid_solution['NewCapacity2025'].sum()/1000,1)

print('The total new installed capacity of the grid is ' + str(Results.loc['grid','Capacity'])+ 
      '.')

Results.loc['microgrid','Capacity'] =  round((microgrids_solution['PVcapacity2025'].sum()
                                              + microgrids_solution['GenSetcapacity2025'].sum())/1000,1)

print('TThe total new installed capacity of the microgrid is ' + str(Results.loc['microgrid','Capacity']) + 
      '.')

Results.loc['SHS','Capacity'] =  round(SHS_solution['PVcapacity2025'].sum()/1000,1)

print('The total new installed capacity of the SHS is ' +str(Results.loc['SHS','Capacity'])+ 
      '.')

Results.loc['Total','Capacity'] = (Results.loc['grid','Capacity'] 
                              + Results.loc['microgrid','Capacity'] 
                              + Results.loc['SHS','Capacity']) 

print('The total new installed capacity of new connected  people is ' +str(Results.loc['Total','Capacity'])+ 
      '.')

#%%

inv_hh_grid = grid_solution['InvestmentCost2025']/grid_solution['HouseHolds']
Results.loc['grid','Inv per HH'] =  round(inv_hh_grid.mean(), 0)

print('The investment per household for the grid is ' + str(Results.loc['grid','Inv per HH'])+ 
      ' USD.')

inv_hh_microgrid = microgrids_solution['InvestmentCost2025']/microgrids_solution['HouseHolds']
Results.loc['microgrid','Inv per HH'] =  round(inv_hh_microgrid.mean(), 0)

print('The investment per household for the microgrid is ' 
      + str(Results.loc['microgrid','Inv per HH']) +   ' USD.')


inv_hh_SHS = SHS_solution['InvestmentCost2025']/SHS_solution['HouseHolds']
Results.loc['SHS','Inv per HH'] =  round(inv_hh_SHS.mean(),0)

print('The investment per household for the microgrid is ' +str(Results.loc['SHS','Inv per HH'])+ 
      ' USD.')

inv_hh_total = df['InvestmentCost2025']/df['HouseHolds']
Results.loc['Total','Inv per HH'] = round(inv_hh_total.mean(),0)

print('The average investment per household for new connected  people is ' +str(Results.loc['Total','Inv per HH'])+ 
     ' USD.')

Results.to_csv('Bolivia/OnSSET_Results.csv')

microgrids_solution.to_csv('Bolivia/Microgrids_results.csv')
SHS_solution.to_csv('Bolivia/SHS_Results.csv')



check_1 = pd.DataFrame()

for i in microgrids_solution.index:
    
    check_1.loc[i,'boolean'] = df_2012.index.contains(i)
    
print(check_1['boolean'].all())    


check_2 = pd.DataFrame()

for i in SHS_solution.index:
    
    check_2.loc[i,'boolean'] = df_2012.index.contains(i)
    
print(check_2['boolean'].all())    

Grid_Unconnected_solution = df_2012.loc[df_2012['MinimumOverall2025'] == 'Grid2025']

microgrids_solution.to_csv('Bolivia/Microgrids_results.csv')
SHS_solution.to_csv('Bolivia/SHS_Results.csv')
Grid_Unconnected_solution.to_csv('Bolivia/grid_Solution_No_Electricity.csv')

test = microgrids_solution.index
test = test.append(SHS_solution.index)
test = test.append(Grid_Unconnected_solution.index)
test = pd.DataFrame(test)

test = test[0].sort_values()

test1 = test == df_2012.index

test1 = pd.DataFrame(test1)

print(test1[0].all())


Number_microgrids = len(microgrids_solution)
print('The number of microgrids is ' + str(Number_microgrids) + '.')


isolated_solutions = len(microgrids_solution)+len(SHS_solution)
isolated_households  = microgrids_solution['HouseHolds'].sum() + SHS_solution['HouseHolds'].sum()
SHS_households = SHS_solution['HouseHolds'].sum()
print('The number of communities with isolated solution is ' +str(round(isolated_solutions,0)))
print('The number of households with isolated solution is  ' + str(round(isolated_households,0)))
print('The number of households with SHS solution is  ' + str(round(SHS_households,0)))


# The number of Unconnected communities in Bolivia is 8671
# The % of people connected to the grid in 2012 was 76.0
# New connected people with the grid is 3308928.0
# New connected people with microgrid is 53140.0
# New connected people with SHS is 493225.0
# Total number of new connected  people is 3855293.0
# The total NPC of the grid is 1635.0 thousands of millons of USD.
# The total NPC of the microgrid is 44.0 thousands of millons of USD.
# The total NPC of the SHS is 236.0 thousands of millons of USD.
# Total NPC is 1915.0 thousands of millons of USD.
# The total new installed capacity of the grid is 279.8.
# TThe total new installed capacity of the microgrid is 2.8.
# The total new installed capacity of the SHS is 66.4.
# The total new installed capacity of new connected  people is 349.0.
# The investment per household for the grid is 1811.0 USD.
# The investment per household for the microgrid is 2413.0 USD.
# The investment per household for the microgrid is 1326.0 USD.
# The average investment per household for new connected  people is 1636.0 USD.
# True
# True
# True
# The number of microgrids is 221.
# The number of communities with isolated solution is 7446
# The number of households with isolated solution is  159798.0
# The number of households with SHS solution is  144256.0