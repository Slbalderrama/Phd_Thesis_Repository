
from runner import scenario
import pandas as pd
import os



    # 'Database_lower_ElecPopCalib.csv'
    # 'Database_new_1.csv'
specs_path = os.path.join('Bolivia', 'specs_paper_new.xlsx')
calibrated_csv_path = os.path.join('Bolivia', 'Database_new_1.csv')
results_folder = os.path.join('Bolivia')
summary_folder	= os.path.join('Bolivia')
  
scenario(specs_path, calibrated_csv_path, results_folder, summary_folder)

data = pd.read_csv('Bolivia/bo-1-0_0_0_0_0_0.csv', index_col=0)  
summary = pd.read_csv('Bolivia/bo-1-0_0_0_0_0_0_summary.csv', index_col=0)
indpendant_variables = pd.read_csv('Bolivia/Independent_Variables_2025.csv', index_col=0) 



df= pd.DataFrame()

df['Demand_Name2025'] = data['Demand_Name2025']
df['Elevation'] = data['Elevation']
df['HouseHolds'] = indpendant_variables['HouseHolds']
df['LCOE_SHS2025'] = data['SHS2025']
df['LCOE_MG_Hybrid_LowLands2025'] = data['MG_Hybrid_LowLands2025']
df['LCOE_MG_Hybrid_HighLands2025'] = data['MG_Hybrid_HighLands2025']
df['LCOE_Grid2025'] = data['Grid2025']
df['PVcapacity2025'] = data['PVcapacity2025']
df['GenSetcapacity2025'] = data['GenSetcapacity2025']
df['Batterycapacity2025'] = data['Batterycapacity2025']
df['NPC2025'] = data['NPC2025']
df['InvestmentCapita2025'] = data['InvestmentCapita2025']


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




























