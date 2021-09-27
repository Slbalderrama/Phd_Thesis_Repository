#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 16:22:12 2020

@author: balderrama
"""
from onsset import Technology
import pandas as pd

def technology_creation(start_year, end_year, grid_price, specs_data, diesel_price, pv_capital_cost_adjust):
    Base_To_Peak_Grid  = pd.read_csv('Bolivia/Base_to_Peak_Grid.csv', index_col=0)  
    technologies = []

    Technology.set_default_values(base_year=start_year,
                                      start_year=start_year,
                                      end_year=end_year,
                                      discount_rate=0.12)
     
    grid_calc = Technology(om_of_td_lines=0.02,
                               distribution_losses=  float(specs_data.iloc[0]['GridLosses']),
                               connection_cost_per_hh=125,
                               base_to_peak_load_ratio_type = 'surrogate',
                               capacity_factor=1,
                               tech_life=30,
                               grid_capacity_investment=float(specs_data.iloc[0]['GridCapacityInvestmentCost']),
                               grid_penalty_ratio=1,
                               grid_price=grid_price,
                               name = 'Grid',
                               code = 1)
    print('Grid losses ' + str(grid_calc.distribution_losses))
    print('Grid Investment cost ' + str(grid_calc.grid_capacity_investment))
    technologies.append(grid_calc)
    
    Renewable_Invesment_Cost = 1900
    Battery_Unitary_Investment_Cost = 750
    Deep_of_Discharge = 0.2
    Battery_cycles = 5500
    GenSet_Unitary_Investment_Cost = 1900
    Generator_Efficiecy = 0.33
    LHV = 9.9
    
    surrogate_model_1 = {'name': 'MG_Hybrid_LowLands',
                          'path_LCOE': 'Bolivia/Surrogate_Models/LowLands/LCOE_LowLands.joblib' ,
                          'path_NPC': 'Bolivia/Surrogate_Models/LowLands/NPC_Lowlands.joblib', 
                          'path_Investment' : 'Bolivia/Surrogate_Models/LowLands/Investment_Lowlands.joblib',
                          'path_PV_Capacity': 'Bolivia/Surrogate_Models/LowLands/PV_Lowlands.joblib' ,
                          'path_Genset_Capacity': 'Bolivia/Surrogate_Models/LowLands/Genset_Lowlands.joblib' ,
                          'path_Battery_Capacity': 'Bolivia/Surrogate_Models/LowLands/Battery_Lowlands.joblib',
                          'Variables' : 10,
                          'var_1' : 'Renewable Invesment Cost',
                          'value_1': Renewable_Invesment_Cost,
                          'var_2' : 'Battery Unitary Invesment Cost',
                          'value_2': Battery_Unitary_Investment_Cost,
                          'var_3' : 'Deep of Discharge',
                          'value_3': Deep_of_Discharge,
                          'var_4' : 'Battery Cycles',
                          'value_4': Battery_cycles,
                          'var_5':'GenSet Unitary Invesment Cost',
                          'value_5': GenSet_Unitary_Investment_Cost,
                          'var_6' : 'Generator Efficiency',
                          'value_6': Generator_Efficiecy,
                          'var_7' : 'Low Heating Value',
                          'value_7': LHV,
                          'var_8' : 'Fuel Cost',
                          'var_9' : 'HouseHolds',
                          'var_10' : 'Renewable Energy Unit Total',
                          'value_10': 'PV total output'}                                   
    
    
    mg_LowLands_calc = Technology(om_of_td_lines=0.02,
                                  distribution_losses=0.00,
                                  connection_cost_per_hh=125,
                                  base_to_peak_load_ratio_type = 'surrogate',
                                  tech_life=20,
                                  mini_grid=True,
                                  name = 'MG_Hybrid_LowLands',
                                  code = 8,
                                  surrogate_model = True,
                                  surrogate_model_data = surrogate_model_1,
                                  tech_life_surrogate = 20)
    technologies.append(mg_LowLands_calc)
    
    surrogate_model_2 = {'name': 'MG_Hybrid_HighLands',
                          'path_LCOE': 'Bolivia/Surrogate_Models/HighLands/LCOE_HighLands.joblib' ,
                          'path_NPC': 'Bolivia/Surrogate_Models/HighLands/NPC_Highlands.joblib', 
                          'path_Investment' : 'Bolivia/Surrogate_Models/HighLands/Investment_Highlands.joblib',
                          'path_PV_Capacity': 'Bolivia/Surrogate_Models/HighLands/PV_Highlands.joblib' ,
                          'path_Genset_Capacity': 'Bolivia/Surrogate_Models/HighLands/Genset_Highlands.joblib' ,
                          'path_Battery_Capacity': 'Bolivia/Surrogate_Models/HighLands/Battery_Highlands.joblib',
                          'Variables' : 10,
                          'var_1' : 'Renewable Invesment Cost',
                          'value_1': Renewable_Invesment_Cost,
                          'var_2' : 'Battery Unitary Invesment Cost',
                          'value_2': Battery_Unitary_Investment_Cost,
                          'var_3' : 'Deep of Discharge',
                          'value_3': Deep_of_Discharge,
                          'var_4' : 'Battery Cycles',
                          'value_4': Battery_cycles,
                          'var_5':'GenSet Unitary Invesment Cost',
                          'value_5': GenSet_Unitary_Investment_Cost,
                          'var_6' : 'Generator Efficiency',
                          'value_6': Generator_Efficiecy,
                          'var_7' : 'Low Heating Value',
                          'value_7': LHV,
                          'var_8' : 'Fuel Cost',
                          'var_9' : 'HouseHolds',
                          'var_10' : 'Renewable Energy Unit Total',
                          'value_10': 'PV total output'}                                   
    
    
    mg_HighLands_calc = Technology(om_of_td_lines=0.02,
                                  distribution_losses=0,
                                  connection_cost_per_hh=125,
                                  base_to_peak_load_ratio_type = 'surrogate',
                                  tech_life=20,
                                  mini_grid=True,
                                  name = 'MG_Hybrid_HighLands',
                                  code = 8,
                                  surrogate_model = True,
                                  surrogate_model_data = surrogate_model_2,
                                  tech_life_surrogate = 20)
    
    
        
    
    technologies.append( mg_HighLands_calc)
    
    
    surrogate_model_3 = {'name': 'SHS',
                          'path_LCOE': 'Bolivia/Surrogate_Models/SHS/LCOE_SHS.joblib' ,
                          'path_NPC': 'Bolivia/Surrogate_Models/SHS/NPC_SHS.joblib', 
                          'path_Investment' : 'Bolivia/Surrogate_Models/SHS/Investment_SHS.joblib',
                          'path_PV_Capacity': 'Bolivia/Surrogate_Models/SHS/PV_SHS.joblib' ,
                          'path_Genset_Capacity': 'Bolivia/Surrogate_Models/SHS/Genset_SHS.joblib' ,
                          'path_Battery_Capacity': 'Bolivia/Surrogate_Models/SHS/Battery_SHS.joblib',
                          'Variables' : 1,
                          'var_1' : 'HouseHolds'}                                   
    
    
    SHS_calc = Technology(mini_grid=True,
                          name = 'SHS',
                          tech_life=20,
                          code = 8,
                          surrogate_model = True,
                          surrogate_model_data = surrogate_model_3,
                          standalone=True,
                          tech_life_surrogate = 20)
    
    
        
    
    technologies.append(SHS_calc)
    
    
    
    
    
    transportation_cost = []
    

    
    transportation_cost.append({'diesel_price': diesel_price,
                                'fuel_price': diesel_price,
                                'tech_name' :'MG_Hybrid_LowLands',
                                'diesel_truck_consumption': 33.7,
                                'diesel_truck_volume':  15000,
                                'Surrogate_Models': True})       
    
    transportation_cost.append({'diesel_price': diesel_price,
                                'fuel_price': diesel_price,
                                'tech_name' :'MG_Hybrid_HighLands',
                                'diesel_truck_consumption': 33.7,
                                'diesel_truck_volume':  15000,
                                'Surrogate_Models': True})       
    
    # transportation_cost.append({'diesel_price': diesel_price,
    #                             'fuel_price': diesel_price,
    #                             'tech_name' :'SHS',
    #                             'diesel_truck_consumption': 33.7,
    #                             'diesel_truck_volume':  15000,
    #                             'Surrogate_Models': True})   
    
    
    # Constraints
    
    tech_constraints = []
    
 
    
    
    tech_constraints.append({'Type': 'minor',
                              'name': 'MG_Hybrid_LowLands',
                              'Column_name': 'HouseHolds', 
                              'bound'      : 550, 
                              'Years'      :  [2025]                          
                                })
    
    tech_constraints.append({'Type': 'mayor',
                              'name':'MG_Hybrid_LowLands',
                              'Column_name':'HouseHolds', 
                              'bound'      : 50, 
                              'Years'      :  [2025]                          
                                })

    tech_constraints.append({'Type'       : 'minor',
                              'name'       : 'MG_Hybrid_LowLands',
                              'Column_name': 'Elevation', 
                              'bound'      : 800, 
                              'Years'      :  [2025]
                                })

    tech_constraints.append({'Type': 'minor',
                              'name': 'MG_Hybrid_HighLands',
                              'Column_name': 'HouseHolds', 
                              'bound'      : 550, 
                              'Years'      :  [2025]                          
                                })
    
    tech_constraints.append({'Type': 'mayor',
                              'name':'MG_Hybrid_HighLands',
                              'Column_name':'HouseHolds', 
                              'bound'      : 50, 
                              'Years'      :  [2025]                          
                                })

    tech_constraints.append({'Type'       : 'mayor',
                              'name'       : 'MG_Hybrid_HighLands',
                              'Column_name': 'Elevation', 
                              'bound'      : 800, 
                              'Years'      :  [2025]
                                })

    tech_constraints.append({'Type': 'minor',
                              'name': 'SHS',
                              'Column_name': 'HouseHolds', 
                              'bound'      : 50, 
                              'Years'      :  [2025]                          
                                })


    # Constraints
    
    demand_constraints = []
    
    
    demand_constraints.append({'name': 'SHS',
                                'path': 'Bolivia/Surrogate_Models/SHS/demand_regression_SHS.joblib',
                                'path_peak_load_ratio': 'Bolivia/Surrogate_Models/SHS/Base_to_Peak_SHS.joblib',
                                'constraints':1,
                                'Type_1': 'minor',
                                'Column_name_1': 'HouseHolds minor',
                                'bound_1'      : 50, 
                                'Variables' : 1,
                                'Var_1' : 'HouseHolds'
                                })    
    
    demand_constraints.append({'name': 'Lowlands',
                               'path': 'Bolivia/Surrogate_Models/LowLands/Demand_LowLands.joblib',
                               'path_peak_load_ratio': 'Bolivia/Surrogate_Models/LowLands/Base_to_Peak_Lowlands.joblib',
                               'constraints': 3,
                               'Type_1': 'minor',
                               'Column_name_1': 'Elevation',
                               'bound_1'      : 800, 
                               'Type_2': 'mayor',
                               'Column_name_2': 'HouseHolds mayor',
                               'bound_2'      : 50, 
                               'Type_3': 'minor',
                               'Column_name_3': 'HouseHolds minor',
                               'bound_3'      : 550, 
                               'Variables' : 1,
                               'Var_1' : 'HouseHolds'
                                })
    
   

    
    demand_constraints.append({'name': 'Highlands',
                                'path': 'Bolivia/Surrogate_Models/HighLands/Demand_HighLands.joblib',
                                'path_peak_load_ratio': 'Bolivia/Surrogate_Models/HighLands/Base_to_Peak_Highlands.joblib',
                                'constraints': 3,
                                'Type_1': 'mayor',
                                'Column_name_1': 'Elevation',
                                'bound_1'      : 800, 
                                'Type_2': 'mayor',
                                'Column_name_2': 'HouseHolds mayor',
                                'bound_2'      : 50, 
                                'Type_3': 'minor',
                                'Column_name_3': 'HouseHolds minor',
                                'bound_3'      : 550, 
                                'Variables' : 1,
                                'Var_1' : 'HouseHolds'
                                })
    
    
    return technologies, transportation_cost, tech_constraints, demand_constraints
    