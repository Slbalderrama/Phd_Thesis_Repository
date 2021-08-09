
import pandas as pd
import requests
import json
import math as mt
import pvlib

def Initialize_years(model, i):

    '''
    This function returns the value of each year of the project. 
    
    :param model: Pyomo model as defined in the Model_Creation script.
    
    :return: The year i.
    '''    
    return i



Energy_Demand = pd.read_excel('Example/Demand.xls',index_col=0,Header=None) # open the energy demand file
Energy_Demand = Energy_Demand/1000
Energy_Demand = round(Energy_Demand, 3)

def Initialize_Demand(model, i, t):
    '''
    This function returns the value of the energy demand from a system for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
        
    :return: The energy demand for the period t.     
        
    '''
    
    return float(Energy_Demand[i][t])

# PV_Energy = pd.read_excel('Example/PV_Energy.xls') # open the PV energy yield file

def Initialize_PV_Energy(model, i, t):
    '''
    This function returns the value of the energy yield by one PV under the characteristics of the system 
    analysis for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
    
    :return: The energy yield of one PV for the period t.
    '''
    return float(PV_Energy[i][t])

def Initialize_Demand_Dispatch(model, t):
    '''
    This function returns the value of the energy demand from a system for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
        
    :return: The energy demand for the period t.     
        
    '''
    return float(Energy_Demand[1][t])


def Initialize_PV_Energy_Dispatch(model, t):
    '''
    This function returns the value of the energy yield by one PV under the characteristics of the system 
    analysis for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
    
    :return: The energy yield of one PV for the period t.
    '''
    return float(PV_Energy[1][t])
    
    
def Marginal_Cost_Generator_1(model,g):
    
    a = model.Fuel_Cost[g]/(model.Low_Heating_Value[g]*model.Generator_Efficiency[g])
    return a

def Start_Cost(model,i):
    
    a = model.Marginal_Cost_Generator_1[i]*model.Generator_Nominal_Capacity[i]*model.Cost_Increase[i]
    return a

def Marginal_Cost_Generator(model, i):
    a = (model.Marginal_Cost_Generator_1[i]*model.Generator_Nominal_Capacity[i]-model.Start_Cost_Generator[i])/model.Generator_Nominal_Capacity[i] 
    return a 


def Capital_Recovery_Factor(model):
   
    a = model.Discount_Rate*((1+model.Discount_Rate)**model.Years)
    b = ((1 + model.Discount_Rate)**model.Years)-1
    return round(a/b,3)

    
def Battery_Reposition_Cost(model):
   
    unitary_battery_cost = model.Battery_Invesment_Cost - model.Battery_Electronic_Invesmente_Cost
    a = unitary_battery_cost/(model.Battery_Cycles*2*(1-model.Deep_of_Discharge))
    return a 
    
    
Renewable_Energy = pd.read_excel('Example/Renewable_Energy.xls',index_col=0,Header=None) # open the PV energy yield file
Renewable_Energy = Renewable_Energy/1000
Renewable_Energy = round(Renewable_Energy, 3)

def Initialize_Renewable_Energy(model, s,r,t):
    '''
    This function returns the value of the energy yield by one PV under the characteristics of the system 
    analysis for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
    
    :return: The energy yield of one PV for the period t.
    '''

    column = (s-1)*model.Renewable_Source + r 
    return float(Renewable_Energy[column][t])   
    
    
    
def Marginal_Cost_Generator_1_Dispatch(model):
    
    return model.Diesel_Cost/(model.Low_Heating_Value*model.Generator_Efficiency)

def Start_Cost_Dispatch(model):
    
    return model.Marginal_Cost_Generator_1*model.Generator_Nominal_Capacity*model.Cost_Increase

def Marginal_Cost_Generator_Dispatch(model):
    
    return (model.Marginal_Cost_Generator_1*model.Generator_Nominal_Capacity-model.Start_Cost_Generator)/model.Generator_Nominal_Capacity 

def Min_Bat_Capacity(model):
        
    
    Periods = model.Battery_Independency*24
    Len = int(model.Periods/Periods)
    Grouper = 1
    index = 1
    for i in range(1, Len+1):
        for j in range(1,Periods+1):
            
            Energy_Demand.loc[index, 'Grouper'] = Grouper
            index += 1
            
        Grouper += 1
            
    Period_Energy = Energy_Demand.groupby(['Grouper']).sum()
    
    Period_Average_Energy = Period_Energy.mean()
    
    Available_Energy = sum(Period_Average_Energy[s]*model.Scenario_Weight[s] 
        for s in model.scenario) 
    
    a =  Available_Energy/(1-model.Deep_of_Discharge)
    return round(a,3) 

def Solar_Energy_Data(location,Number_Scenarios,solar_energy):
            # solar energy
        foo = location.index[0]
        lat = location['Y_deg'][foo]
        lat = round(lat,5)
        lon = location['X_deg'][foo]
        lon = round(lon,5)    

        
        start = 2012
        Data = pd.DataFrame()
        for i in range(Number_Scenarios):
            
            
            if solar_energy == 'Variable':
                end = start + 1
                date_from = str(start) + '-01-01'
                date_to = str(end) + '-01-01'
            else:
                date_from = str(2012) + '-01-01'
                date_to = str(2013) + '-01-01'
        
                
            args = {
            'lat': lat,
            'lon': lon,
            'date_from': date_from,
            'date_to': date_to,
            'dataset': 'merra2',
            'capacity': 1.0,
            'system_loss': 0.1,
            'tracking': 0,
            'tilt': -round(lat,0),
            'azim': 180,
            'format': 'json',
            'raw':"True"}
        
            if solar_energy=='Variable':
                Data[i+1]= solar_power(args,solar_energy,start,lat)
                start = end
            
            if solar_energy == 'Fix' and i == 0:
                Data[i+1]= solar_power(args,solar_energy,start,lat)
        
            else:
                Data[i+1] = Data[i]
                
                
        Data.index = range(1,8761)
        return Data
    
    
def solar_power(args,solar_energy,start,lat):
    
            token = '8694d4573138f2f38c686d75d2a44c4b5d33c443 '
            api_base = 'https://www.renewables.ninja/api/'
            s = requests.session()
            # Send token header with each request
            s.headers = {'Authorization': 'Token ' + token}
            
            url = api_base + 'data/pv'
            r = s.get(url, params=args)
    
            # Parse JSON to get a pandas.DataFrame of data and dict of metadata
            parsed_response = json.loads(r.text)
    
            data = pd.read_json(json.dumps(parsed_response['data']), 
                            orient='index')
            index = data.index.tz_localize('utc').tz_convert('America/La_Paz')
            data.index = index
            if solar_energy == 'Variable':
                start_1 = str(start) + '-01-01  00:00:00'
                end_1 = str(start) + '-12-31 23:00:00'
            else:
                start_1 = str(2012) + '-01-01  00:00:00'
                end_1 = str(2012) + '-12-31 23:00:00'
            
            data = data[start_1:end_1]
            data = data[~((data.index.month == 2) & (data.index.day == 29))]
            data.index = range(1,8761)
           

            Noct = 44.8
            a = (Noct-20)/800
            
            cec_modules = pvlib.pvsystem.retrieve_sam('cecmod')
            cecmodule = cec_modules.Yingli_Energy__China__YL250P_29b #select module
            
            data['diffuse'] = data['irradiance_diffuse']
            data['direct'] = data['irradiance_direct']
            
            data['Radiation'] = data['direct'] + data['diffuse']
            data['Radiation'] = data['Radiation']*1000
            
            data['PV temperature'] = a*data['Radiation'] + data['temperature']
            
            photocurrent, saturation_current, resistance_series, resistance_shunt, nNsVth = (
                pvlib.pvsystem.calcparams_desoto(data['Radiation'],
                                     temp_cell=data['PV temperature'],
                                     alpha_sc=cecmodule['alpha_sc'],
                                     a_ref = cecmodule['a_ref'],
                                     I_L_ref = cecmodule['I_L_ref'],
                                     I_o_ref = cecmodule['I_o_ref'],
                                     R_sh_ref = cecmodule['R_sh_ref'],
                                     R_s = cecmodule['R_s'],
                                     EgRef=1.121,
                                     dEgdT=-0.0002677))
            single_diode_out = pvlib.pvsystem.singlediode(photocurrent, saturation_current,
                                      resistance_series, resistance_shunt, nNsVth)
            
            return list(single_diode_out['p_mp']) 