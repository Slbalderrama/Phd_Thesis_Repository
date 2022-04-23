
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
df['LCOE_SA_PV_2025'] = data['SA_PV_2025']
df['LCOE_MG_PV_2025'] = data['MG_PV_2025']
df['LCOE_MG_Diesel_2025'] = data['MG_Diesel_2025']
df['LCOE_Grid2025'] = data['Grid2025']
df['MinimumOverall2025'] = data['MinimumOverall2025']
df['MinimumOverallLCOE2025'] = data['MinimumOverallLCOE2025']
df['NewConnections2025'] = data['NewConnections2025']
#df['PVcapacity2025'] = data['PVcapacity2025']
#df['GenSetcapacity2025'] = data['GenSetcapacity2025']
#df['Batterycapacity2025'] = data['Batterycapacity2025']
df['NewCapacity2025'] = data['NewCapacity2025']
df['NPC2025'] = data['NPC2025']
df['InvestmentCapita2025'] = data['InvestmentCapita2025']
df['InvestmentCost2025'] = data['InvestmentCost2025']
df['MinGridDist2025'] = data['MinGridDist2025']
df['X_deg'] = data['X_deg']
df['Y_deg'] = data['Y_deg']

#%%

print(df.isna().any())

df_describe = df.describe()

#%%

df_2012 = df.loc[df['FinalElecCode2012'] !='Grid2012']

Grid_Unconnected = len(df_2012)

print('The number of Unconnected communities in Bolivia is ' + str(Grid_Unconnected))

#%%
# df_lowlands = df.loc[df['Elevation']<800]
df_mg = df.loc[df['HouseHolds']>=50]
df_mg = df_mg.loc[df_mg['HouseHolds']<550]

df_SHS = df.loc[df['HouseHolds']<50]

# df_rest = df.loc[df['HouseHolds']>=550]

#%%
grid_solution = df.loc[df['MinimumOverall2025'] == 'Grid2025'] 

microgrids_PV = df.loc[df['MinimumOverall2025'] == 'MG_PV_2025'] 
microgrids_diesel = df.loc[df['MinimumOverall2025'] == 'MG_Diesel_2025'] 

SHS_solution = df.loc[df['MinimumOverall2025'] == 'SA_PV_2025'] 

Results = pd.DataFrame()

#%%
Results.loc['grid','people'] =  round(grid_solution['NewConnections2025'].sum(),0)

print('New connected people with the grid is ' +str(Results.loc['grid','people']))

Results.loc['PV microgrid','people'] =  round(microgrids_PV['NewConnections2025'].sum(),0)

print('New connected people with a PV microgrid is ' + str(Results.loc['PV microgrid','people']))

Results.loc['Diesel microgrid','people'] =  round(microgrids_diesel['NewConnections2025'].sum(),0)

print('New connected people with a Diesel microgrid is ' + str(Results.loc['Diesel microgrid','people']))


Results.loc['SHS','people'] =  round(SHS_solution['NewConnections2025'].sum(),0)

print('New connected people with SHS is ' +str(Results.loc['SHS','people']))

Results.loc['Total','people'] = Results['people'].sum() 

print('Total number of new connected  people is ' +str(Results.loc['Total','people']))

#%%


lcoe_grid = round(grid_solution['MinimumOverallLCOE2025'].mean(),2)

print('The average LCOE for grid communities is ' +str(lcoe_grid) + ' USD/kWh')

lcoe_pv = round(microgrids_PV['MinimumOverallLCOE2025'].mean(),2) 

print('The average LCOE for PV microgrid communities is ' +str(lcoe_pv) + ' USD/kWh')

lcoe_diesel = round(microgrids_diesel['MinimumOverallLCOE2025'].mean(),2) 

print('The average LCOE for diesel minigrid communities is ' +str(lcoe_diesel ) + ' USD/kWh')

lcoe_shs = round(SHS_solution['MinimumOverallLCOE2025'].mean(),2) 

print('The average LCOE for SHS communities is ' +str(lcoe_shs) + ' USD/kWh')

#%%

Results.loc['grid','NPC'] =  round(grid_solution['NPC2025'].sum()/1000000,0)

print('The total NPC with the grid is ' +str(Results.loc['grid','NPC']))

Results.loc['PV microgrid','NPC'] =  round(microgrids_PV['NPC2025'].sum()/1000000,0)

print('The total NPC with the PV microgrid is ' + str(Results.loc['PV microgrid','NPC']))

Results.loc['Diesel microgrid','NPC'] =  round(microgrids_diesel['NPC2025'].sum()/1000000,0)

print('The total NPC with the Diesel microgrid is ' + str(Results.loc['Diesel microgrid','NPC']))


Results.loc['SHS','NPC'] =  round(SHS_solution['NPC2025'].sum()/1000000,0)

print('The total NPC with the SHS is ' +str(Results.loc['SHS','NPC']))

Results.loc['Total','NPC'] = Results['NPC'].sum() 

print('The total NPC is ' +str(Results.loc['Total','NPC']))


df_2012.to_csv('Bolivia/Unconnected_2012_results.csv')

# The number of Unconnected communities in Bolivia is 8671
# New connected people with the grid is 3306339.0
# New connected people with a PV microgrid is 36340.0
# New connected people with a Diesel microgrid is 44014.0
# New connected people with SHS is 468601.0
# Total number of new connected  people is 3855294.0
# The average LCOE for grid communities is 0.16 USD/kWh
# The average LCOE for grid communities is 0.51 USD/kWh
# The average LCOE for grid communities is 0.59 USD/kWh
# The average LCOE for grid communities is 0.49 USD/kWh
# The total NPC with the grid is 1628.0
# The total NPC with the PV microgrid is 26.0
# The total NPC with the Diesel microgrid is 31.0
# The total NPC with the SHS is 281.0
# The total NPC is 1966.0

# 2022-02-04 16:45:13,743         Electrification loop 1 with 11993 electrified
# 2022-02-04 16:45:13,874         Electrification loop 2 with 54 electrified
# 2022-02-04 16:45:13,996         Electrification loop 3 with 9 electrified
# 2022-02-04 16:45:14,108         Electrification loop 4 with 1 electrified