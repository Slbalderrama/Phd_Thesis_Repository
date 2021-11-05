#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 21:34:50 2020

@author: balderrama
"""

import pandas as pd
from random import shuffle
import numpy as np
import random

#%%
data = pd.read_csv('Bolivia/Database_new.csv')  


# Change the name of column Elecpop to ElecPopCalib
data['ElecPopCalib'] = data['ElecPop']

data = data.drop('ElecPop',axis=1)

## change the wind
#data['WindVel'] = 5
#data['WindCF'] = 0.3

# Change small mistakes in elecstart 2012

data.loc[7797,  'ElecStart'] = 0
data.loc[9620,  'ElecStart'] = 0
data.loc[13070, 'ElecStart'] = 0


codes = {7: 'MG_Hydro2012',
         6: 'MG_Wind2012',
         5: 'MG_PV2012',
         4: 'MG_Diesel2012',
         3: 'SA_PV2012',
         2: 'SA_Diesel2012',
         1: 'Grid2012',
         99: 'Non'}

for i in data.index:
    
    tech =  codes[data.loc[i, 'FinalElecCode2012']]
    data.loc[i, 'FinalElecCode2012'] = tech

PV_2012 = pd.read_csv('Bolivia/PV_2012.csv', index_col=0)  

data['PV total output'] = PV_2012['Energy']
data.loc[16141, 'PV total output'] = 500
data.to_csv('Bolivia/Database_new_1.csv')



 