# Defines the modules

import logging
import os

import pandas as pd
from onsset import (SET_ELEC_ORDER, SET_LCOE_GRID, SET_MIN_GRID_DIST, SET_GRID_PENALTY,
                    SET_MV_CONNECT_DIST, SET_WINDCF, SettlementProcessor, Technology)

try:
    from onsset.specs import (SPE_COUNTRY, SPE_ELEC, SPE_ELEC_MODELLED,
                              SPE_ELEC_RURAL, SPE_ELEC_URBAN, SPE_END_YEAR,
                              SPE_GRID_CAPACITY_INVESTMENT, SPE_GRID_LOSSES,
                              SPE_MAX_GRID_EXTENSION_DIST,
                              SPE_NUM_PEOPLE_PER_HH_RURAL,
                              SPE_NUM_PEOPLE_PER_HH_URBAN, SPE_POP, SPE_POP_FUTURE,
                              SPE_START_YEAR, SPE_URBAN, SPE_URBAN_FUTURE,
                              SPE_URBAN_MODELLED)
except ImportError:
    from specs import (SPE_COUNTRY, SPE_ELEC, SPE_ELEC_MODELLED,
                       SPE_ELEC_RURAL, SPE_ELEC_URBAN, SPE_END_YEAR,
                       SPE_GRID_CAPACITY_INVESTMENT, SPE_GRID_LOSSES,
                       SPE_MAX_GRID_EXTENSION_DIST,
                       SPE_NUM_PEOPLE_PER_HH_RURAL,
                       SPE_NUM_PEOPLE_PER_HH_URBAN, SPE_POP, SPE_POP_FUTURE,
                       SPE_START_YEAR, SPE_URBAN, SPE_URBAN_FUTURE,
                       SPE_URBAN_MODELLED)
from openpyxl import load_workbook
from Technologies import technology_creation


logging.basicConfig(format='%(asctime)s\t\t%(message)s', level=logging.DEBUG)


def calibration(specs_path, csv_path, specs_path_calib, calibrated_csv_path):
    """

    Arguments
    ---------
    specs_path
    csv_path
    specs_path_calib
    calibrated_csv_path
    """
    specs_data = pd.read_excel(specs_path, sheet_name='SpecsData')
    settlements_in_csv = csv_path
    settlements_out_csv = calibrated_csv_path

    onsseter = SettlementProcessor(settlements_in_csv)

    num_people_per_hh_rural = float(specs_data.iloc[0][SPE_NUM_PEOPLE_PER_HH_RURAL])
    num_people_per_hh_urban = float(specs_data.iloc[0][SPE_NUM_PEOPLE_PER_HH_URBAN])

    # RUN_PARAM: these are the annual household electricity targets
    tier_1 = 38.7  # 38.7 refers to kWh/household/year. It is the mean value between Tier 1 and Tier 2
    tier_2 = 219
    tier_3 = 803
    tier_4 = 2117
    tier_5 = 2993

    onsseter.prepare_wtf_tier_columns(num_people_per_hh_rural, num_people_per_hh_urban,
                                      tier_1, tier_2, tier_3, tier_4, tier_5)
    onsseter.condition_df()
    onsseter.df[SET_GRID_PENALTY] = onsseter.grid_penalties(onsseter.df)

    onsseter.df[SET_WINDCF] = onsseter.calc_wind_cfs()

    pop_actual = specs_data.loc[0, SPE_POP]
    pop_future_high = specs_data.loc[0, SPE_POP_FUTURE + 'High']
    pop_future_low = specs_data.loc[0, SPE_POP_FUTURE + 'Low']
    urban_current = specs_data.loc[0, SPE_URBAN]
    urban_future = specs_data.loc[0, SPE_URBAN_FUTURE]
    start_year = int(specs_data.loc[0, SPE_START_YEAR])
    end_year = int(specs_data.loc[0, SPE_END_YEAR])

    intermediate_year = 2025
    elec_actual = specs_data.loc[0, SPE_ELEC]
    elec_actual_urban = specs_data.loc[0, SPE_ELEC_URBAN]
    elec_actual_rural = specs_data.loc[0, SPE_ELEC_RURAL]

    pop_modelled, urban_modelled = onsseter.calibrate_current_pop_and_urban(pop_actual, urban_current)

    onsseter.project_pop_and_urban(pop_modelled, pop_future_high, pop_future_low, urban_modelled,
                                   urban_future, start_year, end_year, intermediate_year)

    elec_modelled, rural_elec_ratio, urban_elec_ratio = \
        onsseter.elec_current_and_future(elec_actual, elec_actual_urban, elec_actual_rural, start_year)

    # In case there are limitations in the way grid expansion is moving in a country, 
    # this can be reflected through gridspeed.
    # In this case the parameter is set to a very high value therefore is not taken into account.

    specs_data.loc[0, SPE_URBAN_MODELLED] = urban_modelled
    specs_data.loc[0, SPE_ELEC_MODELLED] = elec_modelled
    specs_data.loc[0, 'rural_elec_ratio_modelled'] = rural_elec_ratio
    specs_data.loc[0, 'urban_elec_ratio_modelled'] = urban_elec_ratio

    book = load_workbook(specs_path)
    writer = pd.ExcelWriter(specs_path_calib, engine='openpyxl')
    writer.book = book
    # RUN_PARAM: Here the calibrated "specs" data are copied to a new tab called "SpecsDataCalib". 
    # This is what will later on be used to feed the model
    specs_data.to_excel(writer, sheet_name='SpecsDataCalib', index=False)
    writer.save()
    writer.close()

    logging.info('Calibration finished. Results are transferred to the csv file')
    onsseter.df.to_csv(settlements_out_csv, index=False)


def scenario(specs_path, calibrated_csv_path, results_folder, summary_folder):
    """

    Arguments
    ---------
    specs_path : str
    calibrated_csv_path : str
    results_folder : str
    summary_folder : str

    """

    scenario_info = pd.read_excel(specs_path, sheet_name='ScenarioInfo')
    scenarios = scenario_info['Scenario']
    scenario_parameters = pd.read_excel(specs_path, sheet_name='ScenarioParameters')
    specs_data = pd.read_excel(specs_path, sheet_name='SpecsDataCalib')
    print(specs_data.loc[0, SPE_COUNTRY])

    for scenario in scenarios:
        
        country_id = specs_data.iloc[0]['CountryCode']

        pop_index = scenario_info.iloc[scenario]['Population_Growth'] # 0
        tier_index = scenario_info.iloc[scenario]['Target_electricity_consumption_level'] # 0
        five_year_index = scenario_info.iloc[scenario]['Electrification_target_5_years'] # 0
        grid_index = scenario_info.iloc[scenario]['Grid_electricity_generation_cost'] # 0
        pv_index = scenario_info.iloc[scenario]['PV_cost_adjust'] # 0
        diesel_index = scenario_info.iloc[scenario]['Diesel_price'] # 0
        productive_index = scenario_info.iloc[scenario]['Productive_uses_demand'] # 0
        prio_index = scenario_info.iloc[scenario]['Prioritization_algorithm'] # 0

        end_year_pop = scenario_parameters.iloc[pop_index]['PopEndYear'] # 1
        rural_tier = scenario_parameters.iloc[tier_index]['RuralTargetTier'] # 6
        urban_tier = scenario_parameters.iloc[tier_index]['UrbanTargetTier'] # 6
        five_year_target = scenario_parameters.iloc[five_year_index]['5YearTarget'] #0.92
        annual_new_grid_connections_limit = scenario_parameters.iloc[five_year_index][
                                                'GridConnectionsLimitThousands'] * 1000 # 9999999000.0
        grid_price = scenario_parameters.iloc[grid_index]['GridGenerationCost'] # 0.1223
        pv_capital_cost_adjust = scenario_parameters.iloc[pv_index]['PV_Cost_adjust'] #  1
        diesel_price = scenario_parameters.iloc[diesel_index]['DieselPrice'] # 0.2/0.6/1
        productive_demand = scenario_parameters.iloc[productive_index]['ProductiveDemand'] # 1
        prioritization = scenario_parameters.iloc[prio_index]['PrioritizationAlgorithm'] # 2
        auto_intensification = scenario_parameters.iloc[prio_index]['AutoIntensificationKM'] #0
        print('Scenario: Diese Priece = ' + str(diesel_price) + ' USD/l')
        settlements_in_csv = calibrated_csv_path
        settlements_out_csv = os.path.join(results_folder,
                                           '{}-1-{}_{}_{}_{}_{}_{}.csv'.format(country_id, pop_index, tier_index,
                                                                               five_year_index, grid_index, pv_index,
                                                                               prio_index))
        summary_csv = os.path.join(summary_folder,
                                   '{}-1-{}_{}_{}_{}_{}_{}_summary.csv'.format(country_id, pop_index, tier_index,
                                                                               five_year_index, grid_index, pv_index,
                                                                               prio_index))

        onsseter = SettlementProcessor(settlements_in_csv)

        start_year = specs_data.iloc[0][SPE_START_YEAR]
        end_year = specs_data.iloc[0][SPE_END_YEAR]
        

        
        num_people_per_hh_rural = float(specs_data.iloc[0][SPE_NUM_PEOPLE_PER_HH_RURAL])
        num_people_per_hh_urban = float(specs_data.iloc[0][SPE_NUM_PEOPLE_PER_HH_URBAN])
        max_grid_extension_dist = float(specs_data.iloc[0][SPE_MAX_GRID_EXTENSION_DIST])
        annual_grid_cap_gen_limit = specs_data.loc[0, 'NewGridGenerationCapacityAnnualLimitMW'] * 1000 # 1000000

        # RUN_PARAM: Fill in general and technology specific parameters (e.g. discount rate, losses etc.)
        
        technologies, transportation_cost, tech_constraints, demand_constraints = technology_creation(start_year, end_year, 
                                                                grid_price, specs_data, diesel_price, 
                                                                pv_capital_cost_adjust)

        # RUN_PARAM: One shall define here the years of analysis (excluding start year),
        # together with access targets per interval and timestep duration
        yearsofanalysis = [2025]
        eleclimits = {2025:1}
        time_steps = {2025:13}

#        elements = ["1.Population", "2.New_Connections", "3.Capacity", "4.Investment"]
#        techs = ["Grid", "SA_Diesel", "SA_PV", "MG_Diesel", "MG_PV", "MG_Wind", "MG_Hydro", "MG_Hybrid"]
#        sumtechs = []
#        for element in elements:
#            for tech in techs:
#                sumtechs.append(element + "_" + tech)
#        total_rows = len(sumtechs)
        df_summary = pd.DataFrame()

        onsseter.current_mv_line_dist()

        for year in yearsofanalysis:
            eleclimit = eleclimits[year]
            time_step = time_steps[year]
            

            if year - time_step == start_year:
                grid_cap_gen_limit = time_step * annual_grid_cap_gen_limit
                grid_connect_limit = time_step * annual_new_grid_connections_limit
            else:
                grid_cap_gen_limit = 9999999999
                grid_connect_limit = 9999999999

            onsseter.set_scenario_variables(year, num_people_per_hh_rural, num_people_per_hh_urban, time_step,
                                            start_year, urban_tier, rural_tier, end_year_pop, productive_demand, 
                                            technologies, demand_constraints)

            onsseter.fuel_cost_columns(transportation_cost, year)

            invesments = onsseter.calculate_off_grid_lcoes(technologies, tech_constraints,year, end_year, time_step)
            
            for i in technologies:
                if i.code ==1:
                    grid_calc = i
            
            
            invesments['Grid'+ "{}".format(year)], grid_cap_gen_limit, grid_connect_limit = \
                onsseter.pre_electrification(grid_price, year, time_step, end_year, grid_calc, grid_cap_gen_limit,
                                             grid_connect_limit)

            onsseter.df[SET_LCOE_GRID + "{}".format(year)], onsseter.df[SET_MIN_GRID_DIST + "{}".format(year)], \
            onsseter.df[SET_ELEC_ORDER + "{}".format(year)], onsseter.df[SET_MV_CONNECT_DIST], invesments['Grid'+ "{}".format(year)] = \
                onsseter.elec_extension(grid_calc,
                                        max_grid_extension_dist,
                                        year,
                                        start_year,
                                        end_year,
                                        time_step,
                                        grid_cap_gen_limit,
                                        grid_connect_limit,
                                        auto_intensification=auto_intensification,
                                        prioritization=prioritization,
                                        new_investment=invesments['Grid'+ "{}".format(year)])
            
            
            onsseter.results_columns(year, time_step, prioritization, auto_intensification, technologies)

            onsseter.calculate_investments(invesments, year)

            onsseter.apply_limitations(eleclimit, year, time_step, prioritization, auto_intensification)

            onsseter.calculate_new_capacity(technologies, year)

            onsseter.calc_summaries(df_summary, technologies, year)

        for i in range(len(onsseter.df.columns)):
            if onsseter.df.iloc[:, i].dtype == 'float64':
                onsseter.df.iloc[:, i] = pd.to_numeric(onsseter.df.iloc[:, i], downcast='float')
            elif onsseter.df.iloc[:, i].dtype == 'int64':
                onsseter.df.iloc[:, i] = pd.to_numeric(onsseter.df.iloc[:, i], downcast='signed')

        df_summary.to_csv(summary_csv)
        onsseter.df.to_csv(settlements_out_csv, index=False)

        logging.info('Finished')
