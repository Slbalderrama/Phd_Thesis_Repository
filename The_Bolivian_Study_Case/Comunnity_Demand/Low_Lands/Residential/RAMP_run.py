# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 14:35:00 2019
This is the code for the open-source stochastic model for the generation of 
multi-energy load profiles in off-grid areas, called RAMP, v.0.2.1-pre.

@authors:
- Francesco Lombardi, Politecnico di Milano
- Sergio Balderrama, Université de Liège
- Sylvain Quoilin, KU Leuven
- Emanuela Colombo, Politecnico di Milano

Copyright 2019 RAMP, contributors listed above.
Licensed under the European Union Public Licence (EUPL), Version 1.1;
you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations
under the License.
"""

#%% Import required modules

from stochastic_process import Stochastic_Process
from post_process import*

# Calls the stochastic process and saves the result in a list of stochastic profiles
# By default, the process runs for only 1 input file ("input_file_1"), but multiple files
# can be run in sequence enlarging the iteration range and naming further input files with
# progressive numbering
for j in range(1,21):
    for k in range(1,12):
        Profiles_list = Stochastic_Process(j,k)
        Profiles_avg, Profiles_list_kW, Profiles_series = Profile_formatting(Profiles_list)    
        export_series(Profiles_series,j,k)
# Post-processes the results and generates plots
Profile_series_plot(Profiles_series)

