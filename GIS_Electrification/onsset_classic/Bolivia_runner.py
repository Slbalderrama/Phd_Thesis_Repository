
from runner import scenario
import pandas as pd
import os
'''Check if the demand if the constraints are applyied for 2020'''


    # 'Database_lower_ElecPopCalib.csv'
    # 'Database_new_1.csv'
specs_path = os.path.join('Bolivia', 'specs_paper_new.xlsx')
calibrated_csv_path = os.path.join('Bolivia', 'Database_new_1.csv')
results_folder = os.path.join('Bolivia')
summary_folder	= os.path.join('Bolivia')
  
scenario(specs_path, calibrated_csv_path, results_folder, summary_folder)


#%%    
data = pd.read_csv('Bolivia/bo-1-0_0_0_0_0_0.csv', index_col=0)  
summary =  pd.read_csv('Bolivia/bo-1-0_0_0_0_0_0_summary.csv', index_col=0) 
indpendant_variables = pd.read_csv('Bolivia/Independent_Variables2025.csv', index_col=0) 


df = pd.DataFrame()
df['FinalElecCode2012'] = data['FinalElecCode2012']
df['Demand_Name2025'] = data['Demand_Name2025']
df['Elevation'] = data['Elevation']
#df['SA_DieselFuelCost2025'] = data['SA_DieselFuelCost2025']
#df['MG_Hybrid_LowLandsFuelCost2025'] = data['MG_Hybrid_LowLandsFuelCost2025']
df['SA_PV_2025'] = data['SA_PV_2025']
df['MG_PV_2025'] = data['MG_PV_2025']
df['MG_Diesel_2025'] = data['MG_Diesel_2025']
#df['SA_Diesel2025'] = data['SA_Diesel2025']
#df['MG_Hybrid_LowLands2025'] = data['MG_Hybrid_LowLands2025']
#df['MG_Hybrid_LowLands2025'] = data['MG_Hybrid_LowLands2025']
df['Minimum_Tech_Off_grid2025'] = data['Minimum_Tech_Off_grid2025']
df['Grid2025'] = data['Grid2025']
df['MinimumOverall2025'] = data['MinimumOverall2025']
df['HouseHolds'] = indpendant_variables['HouseHolds']
df['NewConnections2025'] = data['NewConnections2025']
df['NewCapacity2025'] = data['NewCapacity2025']
df['MinimumOverallLCOE2025'] = data['MinimumOverallLCOE2025']

df1 = df.loc[df['Demand_Name2025'] == 'LowLands']
df_mg_PV = df1.loc[df1['MinimumOverall2025'] == 'MG_PV_2025']
df_mg_diesel = df1.loc[df1['MinimumOverall2025'] == 'MG_Diesel_2025']
df_sa_PV = df1.loc[df1['MinimumOverall2025'] == 'SA_PV_2025']
df_grid = df1.loc[df1['MinimumOverall2025'] == 'Grid2025']
#df_grid["dif"] = df_grid['MG_Hybrid_LowLands2025'] - df_grid['Grid2025']
#%%
print(df1['MG_Diesel_2025'].mean())
#1.1966938939313396
#new_connections_hybrid = round(df_hybrid['NewConnections2025'].sum(),0)
new_connections_SA_PV = round(df_sa_PV['NewConnections2025'].sum(),0)
new_connections_mg_PV = round(df_mg_PV['NewConnections2025'].sum(),0)
new_connections_mg_diesel = round(df_mg_diesel['NewConnections2025'].sum(),0)

new_connections_grid = round(df_grid['NewConnections2025'].sum(),0)

#print('The number of new connections for the hybrids is ' + str(new_connections_hybrid))
print('The number of new connections for the SA PV is ' + str(new_connections_SA_PV))

print('The number of new connections for the MG PV is ' + str(new_connections_mg_PV))
print('The number of new connections for the MG diesel is ' + str(new_connections_mg_diesel))

print('The number of new connections for the Grid is ' + str(new_connections_grid))

#%%
#install_capacity_hybrid = round(df_hybrid['NewCapacity2025'].sum()/1000,1) 
install_capacity_sa_PV =     round(df_sa_PV['NewCapacity2025'].sum()/1000,1)
install_capacity_mg_PV =     round(df_mg_PV['NewCapacity2025'].sum()/1000,1)
install_capacity_mg_diesel = round(df_mg_diesel['NewCapacity2025'].sum()/1000,1)
install_capacity_grid   =    round(df_grid['NewCapacity2025'].sum()/1000,1)

#print('New install capacity for the hybrid systems is ' + str(install_capacity_hybrid))
print('New install capacity for the SA PV systems is ' + str(install_capacity_sa_PV))
print('New install capacity for the MG PV systems is ' + str(install_capacity_mg_PV))
print('New install capacity for the MG diesel systems is ' + str(install_capacity_mg_diesel))
print('New install capacity for the grid is ' + str(install_capacity_grid))
#%%


# NPC_grid = pd.read_csv('Bolivia/NPC_Grid.csv', index_col=0)  
# NPC_sa_PV = pd.read_csv('Bolivia/NPC_SA_PV_.csv', index_col=0)  
#NPC_hybrid = pd.read_csv('Bolivia/NPC_MG_Hybrid_LowLands.csv', index_col=0)  

#df_hybrid['NPC'] = NPC_hybrid.loc[df_hybrid.index] 


# df_grid['NPC'] = NPC_grid.loc[df_grid.index] 

#npc_hybrid = round(df_hybrid['NPC'].sum()/1000000,0)

#print('Total NPC for the hybrid systems is ' + str(npc_hybrid))

# if new_connections_SA_PV ==0:
#     print('The total NPC for SA PV systems is 0')
# else:    
#     df_sa_PV['NPC'] = NPC_sa_PV.loc[df_sa_PV.index] 
#     npc_sa_pv = round(df_sa_PV['NPC'].sum()/1000000,0)
#     print('Total NPC for the SA PV systems is ' + str(npc_sa_pv))

# npc_grid = round(df_grid['NPC'].sum()/1000000,0)
# print('Total NPC for the grid is ' + str(npc_grid))


# Costs_grid = pd.read_csv('Bolivia/Costs_Grid.csv', index_col=0)  


# Investments_grid = pd.read_csv('Bolivia/Invesments_Grid.csv', index_col=0)  
# OyM_grid = pd.read_csv('Bolivia/Operation_Grid.csv', index_col=0)  
# Fuel_grid = pd.read_csv('Bolivia/Fuel_Grid.csv', index_col=0)  
# Salvage_grid = pd.read_csv('Bolivia/Salvage_Grid.csv', index_col=0)

#%%
#lcoe_hydrid = round(df_hybrid['MinimumOverallLCOE2025'].mean(),2)
lcoe_SA_PV = round(df_sa_PV['MinimumOverallLCOE2025'].mean(),2)
lcoe_mg_PV = round(df_mg_PV['MinimumOverallLCOE2025'].mean(),2)
lcoe_mg_diesel = round(df_mg_diesel['MinimumOverallLCOE2025'].mean(),2)
lcoe_grid = round(df_grid['MinimumOverallLCOE2025'].mean(),2)

#print('Average LCOE for the hybrid systems is ' + str(lcoe_hydrid))
print('Average LCOE for the SA PV systems is ' + str(lcoe_SA_PV))
print('Average LCOE for the MG PV systems is ' + str(lcoe_mg_PV))
print('Average LCOE for the MG diesel systems is ' + str(lcoe_mg_diesel))
print('Average LCOE for the grid is ' + str(lcoe_grid))



