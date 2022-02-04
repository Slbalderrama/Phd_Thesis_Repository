# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 14:53:13 2020

@author: Dell
"""


        # Start by calculating the distribution network required to meet all of the demand
        cluster_mv_lines_length_total, cluster_lv_lines_length_total, no_of_service_transf_total, \
            generation_per_year_total, peak_load_total, total_nodes_total = \
            self.distribution_network(people, total_energy_per_cell, num_people_per_hh, grid_cell_area,
                                      productive_nodes)

        # Next calculate the network that is already there
        cluster_mv_lines_length_existing, cluster_lv_lines_length_existing, no_of_service_transf_existing, \
            generation_per_year_existing, peak_load_existing, total_nodes_existing = \
            self.distribution_network(np.maximum((people - new_connections), 1),
                                      (total_energy_per_cell - energy_per_cell),
                                      num_people_per_hh, grid_cell_area, productive_nodes)
            
        generation_per_year_additional = np.maximum(generation_per_year_total - generation_per_year_existing, 0)    
        # If no distribution network is present, perform the calculations only once
        mv_lines_distribution_length_new, total_lv_lines_length_new, num_transformers_new, generation_per_year_new, \
            peak_load_new, total_nodes_new = self.distribution_network(people, energy_per_cell, num_people_per_hh,
                                                                       grid_cell_area, productive_nodes)
        '''Check if this two are always equal   ''' 
        generation_per_year = np.where((people != new_connections) & (prev_code ),
                                       generation_per_year_additional,
                                       generation_per_year_new)
        
        
        
        
        
        def distribution_network(self, people, energy_per_cell, num_people_per_hh, grid_cell_area,
                             productive_nodes=0):
        """This method calculates the required components for the distribution network
        This includes potentially MV lines, LV lines and service transformers

        Arguments
        ---------
        people : float
            Number of people in settlement
        energy_per_cell : float
            Annual energy demand in settlement (kWh)
        num_people_per_hh : float
            Number of people per household in settlement
        grid_cell_area : float
            Area of settlement (km2)
        productive_nodes : int
            Additional connections (schools, health facilities, shops)

        Notes
        -----
        Based on: https://www.mdpi.com/1996-1073/12/7/1395
        """

        consumption = energy_per_cell  # kWh/year
        average_load = consumption / (1 - self.distribution_losses) / HOURS_PER_YEAR  # kW
        peak_load = average_load / self.base_to_peak_load_ratio  # kW

        if self.standalone:
            cluster_mv_lines_length = 0
            lv_km = 0
            no_of_service_transf = 0
            total_nodes = 0
        else:
            s_max = peak_load / self.power_factor
            max_transformer_area = pi * self.lv_line_max_length ** 2
            total_nodes = (people / num_people_per_hh) + productive_nodes

            no_of_service_transf = np.ceil(
                np.maximum(s_max / self.service_transf_type, np.maximum(total_nodes / self.max_nodes_per_serv_trans,
                                                                        grid_cell_area / max_transformer_area)))

            transformer_radius = ((grid_cell_area / no_of_service_transf) / pi) ** 0.5
            transformer_load = peak_load / no_of_service_transf
            cluster_radius = (grid_cell_area / pi) ** 0.5

            # Sizing lv lines in settlement
            cluster_lv_lines_length = np.where(2 / 3 * cluster_radius * transformer_load * 1000 < self.load_moment,
                                               2 / 3 * cluster_radius * no_of_service_transf,
                                               0)

            cluster_mv_lines_length = np.where(2 / 3 * cluster_radius * transformer_load * 1000 >= self.load_moment,
                                               2 * transformer_radius * no_of_service_transf,
                                               0)

            hh_area = grid_cell_area / total_nodes
            hh_diameter = 2 * ((hh_area / pi) ** 0.5)

            transformer_lv_lines_length = hh_diameter * total_nodes

            lv_km = cluster_lv_lines_length + transformer_lv_lines_length

        return cluster_mv_lines_length, lv_km, no_of_service_transf, consumption, peak_load, total_nodes
    
    
    
     i.get_lcoe(energy_per_cell=self.df[SET_ENERGY_PER_CELL + "{}".format(year)],
                           start_year=year - time_step,
                           end_year=end_year,
                           people=self.df[SET_POP + "{}".format(year)],
                           new_connections=self.df[SET_NEW_CONNECTIONS + "{}".format(year)],
                           total_energy_per_cell=self.df[SET_TOTAL_ENERGY_PER_CELL],
                           prev_code=self.df[SET_DISTRIBUTION_NETWORK + "{}".format(year - time_step)],
                           num_people_per_hh=self.df[SET_NUM_PEOPLE_PER_HH],
                           grid_cell_area=self.df[SET_GRID_CELL_AREA],
                           fuel_cost=self.df[i.name+ 'FuelCost' +  "{}".format(year)],
                           dependant_variables=X)