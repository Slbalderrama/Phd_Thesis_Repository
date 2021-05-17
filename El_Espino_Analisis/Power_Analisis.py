# -*- coding: utf-8 -*-
"""
Created on Mon May 17 15:53:25 2021

@author: Dell
"""


import pandas as pd

data = pd.read_csv('Data_Espino_Thesis.csv', header=0,index_col=0)


Power_Data = pd.DataFrame()


Power_Data['PV Power']  = data['PV Power 1'] + data['PV Power 2'] + data['PV Power 3']
Power_Data['Bat Power'] = data['Bat Power 1'] + data['Bat Power 2'] + data['Bat Power 3']
Power_Data['GenSet Power'] = data['GenSet Power']
Power_Data['Bat SOC'] = (data['Bat Soc 1'] + data['Bat Soc 2'] + data['Bat Soc 3'])/3

#%%