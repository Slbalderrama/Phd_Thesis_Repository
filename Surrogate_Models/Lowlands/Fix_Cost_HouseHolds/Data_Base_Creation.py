#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 12:30:09 2019

@author: balderrama
"""

import pandas as pd



Status = pd.read_excel('status.xls', index_col=0, Header=None)

for i in [100,300,500]:
    data = pd.DataFrame()
    for n in range(30):
        path = 'Results/Results_' + str(i) + '_'+ str(n) + '.xls'
        name = str(i) + '_'+ str(n)
        print(name)
        # renewable source data
        Data_Renewable = pd.read_excel(path, index_col=0, Header=None, sheet_name='Data Renewable')        
        data.loc[name, 'Renewable Invesment Cost'] = Data_Renewable['Source 1']['Invesment (USD)']  
        data.loc[name, 'Renewable OyM Cost'] = Data_Renewable['Source 1']['OyM Cost (USD)']
        data.loc[name, 'Renewable Capacity'] = Data_Renewable['Source 1']['Total Nominal Capacity (W)']         

        # Battery data
        Data_Battery = pd.read_excel(path, index_col=0, Header=None, sheet_name='Battery Data')        
        data.loc[name, 'Battery Invesment Cost'] = Data_Battery['Battery']['Invesment Cost (USD)']  
        data.loc[name, 'Battery OyM Cost'] = Data_Battery['Battery']['OyM Cost (USD)']
        data.loc[name, 'Battery Capacity'] = Data_Battery['Battery']['Nominal Capacity (Wh)']   
#        Battery_Discharge_Rate = Data_Battery['Battery']['Nominal Capacity (Wh)'] 
        # generator data        
        Data_Generator = pd.read_excel(path, index_col=0, Header=None, sheet_name='Generator Data')        
        data.loc[name, 'Generator Invesment Cost'] = Data_Generator['Generator 1']['Invesment Generator (USD)']   
        data.loc[name, 'Generator OyM Cost'] = Data_Generator['Generator 1']['OyM Cost (USD)']   


        
        # Time Series Data
        Data_Time_series = pd.read_excel(path, index_col=0, Header=None, sheet_name='Time Series')        

        data.loc[name, 'Max Demand'] = Data_Time_series['Energy Demand 1 (Wh)'].max() 
        data.loc[name, 'Mean Demand'] = Data_Time_series['Energy Demand 1 (Wh)'].mean() 
        data.loc[name, 'Total Demand'] = Data_Time_series['Energy Demand 1 (Wh)'].sum()
        
        Renewable_Energy = Data_Time_series['Renewable Energy 1 (Wh)'].sum() 
        Generator_Energy = Data_Time_series['Gen energy 1 (Wh)'].sum() 
        Renewable_Penetration = Renewable_Energy/(Renewable_Energy+Generator_Energy)
        data.loc[name, 'Renewable Penetration'] = Renewable_Penetration
        
        Curtailment = Data_Time_series['Curtailment 1 (Wh)'].sum()
        data.loc[name, 'Curtailment Percentage'] = (Curtailment/(Renewable_Energy+Generator_Energy))*100
        
        
        Battery_Energy = Data_Time_series['Battery Flow Out 1 (Wh)'].sum() 
        data.loc[name, 'Battery Usage Percentage'] = (Battery_Energy/data.loc[name, 'Total Demand'])*100
        
        
        # Solar time series
        Data_Renewable_series = pd.read_excel(path, index_col=0, Header=None, sheet_name='Renewable Energy Time Series')        
        data.loc[name, 'Renewable Energy Unit Total'] = Data_Renewable_series['Renewable unit 1 1 (Wh)'].sum()
        
        Results =  pd.read_excel(path, index_col=0, Header=None, sheet_name='Results')        
        data.loc[name, 'NPC'] = Results['Data']['NPC (USD)']
        data.loc[name, 'LCOE'] = Results['Data']['LCOE (USD/kWh)']
        data.loc[name, 'Operation Cost'] = Results['Data']['Present Operation Cost Weighted (USD)']
        
        # Variables independientes
        data.loc[name, 'Renewable Unitary Invesment Cost'] = Data_Renewable['Source 1']['Investment Cost (USD/W)']
        data.loc[name, 'Battery Unitary Invesment Cost'] = Data_Battery['Battery']['Unitary Invesment Cost (USD/Wh)']
        data.loc[name, 'Deep of Discharge'] = Data_Battery['Battery']['Deep of Discharge']   
        data.loc[name, 'Battery Cycles'] = Data_Battery['Battery']['Battery Cycles']  
        data.loc[name, 'GenSet Unitary Invesment Cost'] = Data_Generator['Generator 1']['Generator Invesment Cost (USD/W)']  
        data.loc[name, 'Generator Efficiency'] = Data_Generator['Generator 1']['Generator Efficiency']   
        data.loc[name, 'Low Heating Value'] = Data_Generator['Generator 1']['Low Heating Value (Wh/l)']  
        data.loc[name, 'Fuel Cost'] = Data_Generator['Generator 1']['Fuel Cost (USD/l)']           
        data.loc[name, 'Generator Nominal capacity'] = Data_Generator['Generator 1']['Generator Nominal Capacity (W)']   
        data.loc[name, 'Generator Number'] = Data_Generator['Generator 1']['Number of Generators']           
        data.loc[name,'HouseHolds'] = i 
        data.loc[name,'Gap'] = Status.loc[name, 'Gap']
        data.loc[name,'Time'] = Status.loc[name, 'Time']
        data.loc[name,'Y'] = -Status.loc[name, 'Y_deg']



    data = round(data,3)
    data.to_excel('Database_' + str(i)+  '.xls')        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        