#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 16:22:12 2020

@author: balderrama
"""
from onsset import Technology
import pandas as pd

def technology_creation(start_year, end_year, grid_price, specs_data, diesel_price, pv_capital_cost_adjust):
#    Base_To_Peak_Grid  = pd.read_csv('Bolivia/Base_to_Peak_Grid.csv', index_col=0)  
    technologies = []

    Technology.set_default_values(base_year=start_year,
                                      start_year=start_year,
                                      end_year=end_year,
                                      discount_rate=0.12)
     
    grid_calc = Technology(om_of_td_lines=0.02,
                               distribution_losses=  float(specs_data.iloc[0]['GridLosses']),
                               connection_cost_per_hh=125,
                               base_to_peak_load_ratio_type = 0.529,
                               capacity_factor=1,
                               tech_life=30,
                               grid_capacity_investment=float(specs_data.iloc[0]['GridCapacityInvestmentCost']),
                               grid_penalty_ratio=1,
                               grid_price=grid_price,
                               name = 'Grid',
                               code = 1)

    technologies.append(grid_calc)
    
    sa_pv_calc = Technology(base_to_peak_load_ratio_type = 0.9,
                                tech_life = 15,
                                om_costs = 0.02,
                                capital_cost={float("inf"): 5070 * pv_capital_cost_adjust, # 5070
                                              0.200: 5780 * pv_capital_cost_adjust,        # 5780
                                              0.100: 7660 * pv_capital_cost_adjust,        # 7660
                                              0.050: 11050 * pv_capital_cost_adjust,       # 11050
                                              0.020: 20000 * pv_capital_cost_adjust        # 20000
                                              },
                                standalone=True,
                                name = 'SA_PV_',
                                code = 3)
    
    technologies.append(sa_pv_calc)
 
    mg_pv_calc = Technology(om_of_td_lines=0.02,
                            distribution_losses=0,
                            connection_cost_per_hh=125,
                            base_to_peak_load_ratio_type=0.9,
                            tech_life=20,
                            om_costs=0.02,
                            capital_cost={float("inf"): 3500},
                            mini_grid=True,
                            name = 'MG_PV_',
                            code = 5)
    
    technologies.append(mg_pv_calc)

    mg_diesel_calc = Technology(om_of_td_lines=0.02,
                                distribution_losses=0,
                                connection_cost_per_hh=125,
                                base_to_peak_load_ratio_type=0.529,
                                capacity_factor=0.7,
                                tech_life=20,
                                om_costs=0.02,
                                capital_cost={float("inf"): 1480},
                                mini_grid=True,
                                name = 'MG_Diesel_',
                                code = 4)

    technologies.append(mg_diesel_calc)
    
    transportation_cost = []
    
    transportation_cost.append({'diesel_price': diesel_price,
                                'fuel_price': diesel_price,
                                'tech_name': 'MG_Diesel_',
                                'efficiency': 0.39,
                                'fuel_LHV': 9.9,
                                'diesel_truck_consumption': 33.7,
                                'diesel_truck_volume': 15000})
   

    
    
    # Constraints
    
    tech_constraints = []
    
 
    
    
    tech_constraints.append({'Type': 'minor',
                              'name': 'MG_PV_',
                              'Column_name': 'HouseHolds', 
                              'bound'      : 550, 
                              'Years'      :  [2025]                          
                                })
    
    tech_constraints.append({'Type': 'mayor',
                              'name':'MG_PV_',
                              'Column_name':'HouseHolds', 
                              'bound'      : 50, 
                              'Years'      :  [2025]                          
                                })

    # tech_constraints.append({'Type'       : 'minor',
    #                           'name'       : 'MG_Hybrid_LowLands',
    #                           'Column_name': 'Elevation', 
    #                           'bound'      : 800, 
    #                           'Years'      :  [2025]
    #                             })

    tech_constraints.append({'Type': 'minor',
                              'name': 'MG_Diesel_',
                              'Column_name': 'HouseHolds', 
                              'bound'      : 550, 
                              'Years'      :  [2025]                          
                                })
    
    tech_constraints.append({'Type': 'mayor',
                              'name':'MG_Diesel_',
                              'Column_name':'HouseHolds', 
                              'bound'      : 50, 
                              'Years'      :  [2025]                          
                                })

    # tech_constraints.append({'Type'       : 'mayor',
    #                           'name'       : 'MG_Hybrid_HighLands',
    #                           'Column_name': 'Elevation', 
    #                           'bound'      : 800, 
    #                           'Years'      :  [2025]
    #                             })

    tech_constraints.append({'Type': 'minor',
                              'name': 'SA_PV_',
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
    