# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 12:54:07 2022

@author: Dell
"""

import pandas as pd

#%%
battery_renewable_12 = pd.read_excel('MILP_Renewable_12/Results/Results.xls',
                                     sheet_name= 'Battery Data', index_col=0, Header=None)
battery_renewable_18 = pd.read_excel('MILP_Renewable_18/Results/Results.xls',
                                     sheet_name= 'Battery Data', index_col=0, Header=None)
bat_12 = battery_renewable_12['Battery']['Nominal Capacity (kWh)']
bat_18 = battery_renewable_18['Battery']['Nominal Capacity (kWh)']
Rate_bat_18_12 = (bat_18-bat_12)/bat_18
Rate_bat_18_12 = round(Rate_bat_18_12*100,0)
print('Increase in battery capacity from 18 to 12 is ' + str(Rate_bat_18_12) + ' %.')
                                

#%%
NPC_expected_18 = pd.read_excel('MILP_Expected_18/Results/Results.xls',
                                     sheet_name= 'Results', index_col=0, Header=None)
NPC_18 = pd.read_excel('MILP_18/Results/Results.xls',
                                     sheet_name= 'Results', index_col=0, Header=None)

npc_expected_18 = NPC_expected_18['Data']['NPC LP (USD)']
npc_18 =NPC_18['Data']['NPC LP (USD)']
Rate_expected_NPC = (npc_18-npc_expected_18)/npc_18
Rate_expected_NPC = round(Rate_expected_NPC*100,0)
print('Decrease in NPC from MILP 18 to expected is ' + str(Rate_expected_NPC) + ' %.')

#%%
Results_R_expected_18 = pd.read_excel('MILP_Expected_Renewable_18/Results/Results.xls',
                                     sheet_name= 'Results', index_col=0, Header=None)
Results_R_18 = pd.read_excel('MILP_Renewable_18/Results/Results.xls',
                                     sheet_name= 'Results', index_col=0, Header=None)

npc_expected_renewable_18 = Results_R_expected_18['Data']['NPC LP (USD)']
npc_renewable_18 =Results_R_18['Data']['NPC LP (USD)']
Rate_expected_R_NPC = (npc_renewable_18-npc_expected_renewable_18)/npc_renewable_18
Rate_expected_R_NPC = round(Rate_expected_R_NPC*100,1)
print('Decrease in NPC from MILP  Renewable 18 to  expected Renewable is ' + str(Rate_expected_R_NPC) + ' %.')


lcoe_expected_renewable_18 = Results_R_expected_18['Data']['LCOE (USD/kWh)']
lcoe_renewable_18 =Results_R_18['Data']['LCOE (USD/kWh)']
Rate_expected_R_lcoe = (lcoe_renewable_18 - lcoe_expected_renewable_18)/lcoe_renewable_18
Rate_expected_R_lcoe = round(Rate_expected_R_lcoe *100,1)
print('Decrease in lcoe from MILP  Renewable 18 to  expected Renewable is ' + str(Rate_expected_R_lcoe) + ' %.')

#%%
PV_LP_18 = pd.read_excel('LP_18/Results/Results.xls',
                                     sheet_name= 'Data Renewable', index_col=0, Header=None)
PV_18 = pd.read_excel('MILP_18/Results/Results.xls',
                                     sheet_name= 'Data Renewable', index_col=0, Header=None)

pv_lp_18 = PV_LP_18['Source 1']['Total Nominal Capacity (kW)']
pv_18 = PV_18['Source 1']['Total Nominal Capacity (kW)']
Rate_lp_milp_pv = (pv_18-pv_lp_18)/pv_18
Rate_lp_milp_pv = round(Rate_lp_milp_pv*100,1)
print('Decrease in PV from MILP 18 to  lp is ' + str(Rate_lp_milp_pv) + ' %.')


