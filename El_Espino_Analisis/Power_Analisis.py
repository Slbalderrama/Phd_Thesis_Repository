# -*- coding: utf-8 -*-
"""
Created on Tue May 11 15:49:16 2021

@author: Dell
"""


import pandas as pd
import numpy as np
data = pd.read_csv('Data_Espino_Thesis.csv', header=0,index_col=0)



test_bat = pd.DataFrame()

test_bat['Bat Power 1'] = data['Bat Power 1']
test_bat['Bat Power 2'] = data['Bat Power 2']
test_bat['Bat Power 3'] = data['Bat Power 3']
test_bat['Power 2 Bat 1'] = data['Power 2 Bat 1']
test_bat['Power 2 Bat 2'] = data['Power 2 Bat 2']
test_bat['Power 2 Bat 3'] = data['Power 2 Bat 3']



bat_info = test_bat.describe()
bat_info_1 = test_bat.info()
# it is important to remeber that bat power, takes in account power in and out of the battery
# The sum show problems in Power 2 bat 3
print(test_bat.sum())
# The mean values, shows that 'Power 2 bat 3' has higher numbers.
print(test_bat.mean())
# higer variation 
print(test_bat.std())

test_bat['dif 1'] = abs(test_bat['Bat Power 1']) - abs(test_bat['Power 2 Bat 1'])
test_bat['dif 2'] = abs(test_bat['Bat Power 2']) - abs(test_bat['Power 2 Bat 2'])
test_bat['dif 3'] = abs(test_bat['Bat Power 3']) - abs(test_bat['Power 2 Bat 3'])

# the inspection shows that Power '2 bat 3' Reachs values higher than 18, many times

# due to the mean, std the value -10 is choosen. There is high varation
# the values of Power 2 Bat 3 cannot be used 
test_bat_1 = test_bat.loc[test_bat['dif 3']<-10]



test_bat['Bat Power 1 sign'] = np.sign(test_bat[['Bat Power 1']])
test_bat['Bat Power 2 sign'] = np.sign(test_bat[['Bat Power 2']])
test_bat['Bat Power 3 sign'] = np.sign(test_bat[['Bat Power 3']])

# if a is equal to b and b is equal to c, then a and c are equal

test_bat['1 to 2'] = test_bat['Bat Power 1 sign'] == test_bat['Bat Power 2 sign'] 
test_bat['2 to 3'] = test_bat['Bat Power 2 sign'] == test_bat['Bat Power 3 sign'] 
test_bat['1 to 2 to 3'] = test_bat['1 to 2'] == test_bat['2 to 3']


test_bat_2 = test_bat.loc[test_bat['1 to 2 to 3'] == False]

test_bat_describe_2 = test_bat_2.describe()
test_bat_info_2 = test_bat_2.info()

test_bat_3 = data.loc[test_bat['1 to 2 to 3'] == False]

test_bat_3_1 = test_bat_3.loc[test_bat_3['Sunny Island State 3'] == '2: Warning']


test_bat_4 = data.loc[data['Sunny Island State 3'] == '2: Warning']

test_bat['1 to 2 dif'] = abs(abs(test_bat['Bat Power 1']) - abs(test_bat['Bat Power 2'])) 
test_bat['2 to 3 dif'] = abs(abs(test_bat['Bat Power 2']) - abs(test_bat['Bat Power 3']))
test_bat['1 to 3 dif'] = abs(abs(test_bat['Bat Power 1']) - abs(test_bat['Bat Power 3']))

test_bat_5_1 = test_bat.loc[test_bat['1 to 2 dif']>2] 
test_bat_5_2 = test_bat.loc[test_bat['2 to 3 dif']>2] 
test_bat_5_3 = test_bat.loc[test_bat['1 to 3 dif']>2] 
