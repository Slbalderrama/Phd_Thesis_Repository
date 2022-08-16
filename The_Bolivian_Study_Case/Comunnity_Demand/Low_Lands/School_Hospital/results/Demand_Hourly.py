# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 18:41:38 2022

@author: Dell
"""

import pandas as pd

school = pd.read_csv('output_file_1_1.csv').drop('Unnamed: 0', axis=1)
hospital = pd.read_csv('output_file_2_1.csv').drop('Unnamed: 0', axis=1)

minutes = pd.date_range('2015-01-01 00:00:00','2015-12-31 23:59:00',freq='T')    

school.index = minutes
hospital.index = minutes

school_hourly =  school.resample('H').mean()
school_hourly.to_csv('School.csv')

hospital_hourly = hospital.resample('H').mean()
hospital_hourly.to_csv('Hospital.csv')