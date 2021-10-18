# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 22:26:04 2021

@author: Dell
"""


import pandas as pd


data = pd.read_csv('Database_new_1.csv')# onsset data base


df_new = data.loc[data['Elevation']>800]


df_new.to_excel('Data_Base_High_Lands.xls')



