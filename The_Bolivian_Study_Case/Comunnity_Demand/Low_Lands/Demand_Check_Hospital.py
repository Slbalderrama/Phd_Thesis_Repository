# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 18:48:16 2022

@author: Dell
"""

import pandas as pd

school_1 = pd.read_csv('School.csv')
school_2 = pd.read_csv('School_Hospital/Results/School.csv')
hospital_1 =  pd.read_csv('Hospital.csv')
hospital_2 = pd.read_csv('School_Hospital/Results/Hospital.csv')

data = pd.DataFrame()

data['school 1'] = school_1['0']
data['school 2'] = school_2['0']
data['hospital 1'] = hospital_1['0']
data['hospital 2'] = hospital_2['0']

index = index_hourly = pd.date_range(start='2013-01-01 00:00:00', periods=8760, 
                                   freq=('1H'))
data.index = index
data_hourly = data.groupby(data.index.hour).mean()


data['school 1-2'] = data['school 1'] - data['school 2']
data['hospital 1-2'] = data['hospital 1'] - data['hospital 2']



data_describre = data.describe()

data_hourly.plot()