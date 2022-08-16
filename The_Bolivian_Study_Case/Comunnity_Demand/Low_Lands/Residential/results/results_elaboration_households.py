# -*- coding: utf-8 -*-
"""
Created on Thu May 16 09:40:26 2019

@author: Lombardi
"""

import pandas as pd
import numpy as np

pop_50_list = [[],[],[],[],[]]
pop_100_list = [[],[],[],[],[]]
pop_150_list = [[],[],[],[],[]]
pop_200_list = [[],[],[],[],[]]
pop_250_list = [[],[],[],[],[]]
pop_300_list = [[],[],[],[],[]]
pop_350_list = [[],[],[],[],[]]
pop_400_list = [[],[],[],[],[]]
pop_450_list = [[],[],[],[],[]]
pop_500_list = [[],[],[],[],[]]
pop_550_list = [[],[],[],[],[]]

scenarios_list = [pop_50_list, pop_100_list, pop_150_list, pop_200_list, pop_250_list,
                  pop_300_list, pop_350_list, pop_400_list, pop_450_list, pop_500_list, pop_550_list]


for s in range(0,11):
    k = s+1
    for sh in range (0,5):
        for j in range((1+4*sh),(5+4*sh)):
            scenarios_list[s][sh].append(pd.read_csv('output_file_%d_%d.csv' % (j,k)).drop('Unnamed: 0', axis=1))
            
pop_50_year_1 = np.array([])
pop_50_year_2 = np.array([])
pop_50_year_3 = np.array([])
pop_50_year_4 = np.array([])
pop_50_year_5 = np.array([])
pop_50_year_list = [pop_50_year_1, pop_50_year_2, pop_50_year_3, pop_50_year_4, pop_50_year_5]

pop_100_year_1 = np.array([])
pop_100_year_2 = np.array([])
pop_100_year_3 = np.array([])
pop_100_year_4 = np.array([])
pop_100_year_5 = np.array([])
pop_100_year_list = [pop_100_year_1, pop_100_year_2, pop_100_year_3, pop_100_year_4, pop_100_year_5]

pop_150_year_1 = np.array([])
pop_150_year_2 = np.array([])
pop_150_year_3 = np.array([])
pop_150_year_4 = np.array([])
pop_150_year_5 = np.array([])
pop_150_year_list = [pop_150_year_1, pop_150_year_2, pop_150_year_3, pop_150_year_4, pop_150_year_5]

pop_200_year_1 = np.array([])
pop_200_year_2 = np.array([])
pop_200_year_3 = np.array([])
pop_200_year_4 = np.array([])
pop_200_year_5 = np.array([])
pop_200_year_list = [pop_200_year_1, pop_200_year_2, pop_200_year_3, pop_200_year_4, pop_200_year_5]

pop_250_year_1 = np.array([])
pop_250_year_2 = np.array([])
pop_250_year_3 = np.array([])
pop_250_year_4 = np.array([])
pop_250_year_5 = np.array([])
pop_250_year_list = [pop_250_year_1, pop_250_year_2, pop_250_year_3, pop_250_year_4, pop_250_year_5]

pop_300_year_1 = np.array([])
pop_300_year_2 = np.array([])
pop_300_year_3 = np.array([])
pop_300_year_4 = np.array([])
pop_300_year_5 = np.array([])
pop_300_year_list = [pop_300_year_1, pop_300_year_2, pop_300_year_3, pop_300_year_4, pop_300_year_5]

pop_350_year_1 = np.array([])
pop_350_year_2 = np.array([])
pop_350_year_3 = np.array([])
pop_350_year_4 = np.array([])
pop_350_year_5 = np.array([])
pop_350_year_list = [pop_350_year_1, pop_350_year_2, pop_350_year_3, pop_350_year_4, pop_350_year_5]

pop_400_year_1 = np.array([])
pop_400_year_2 = np.array([])
pop_400_year_3 = np.array([])
pop_400_year_4 = np.array([])
pop_400_year_5 = np.array([])
pop_400_year_list = [pop_400_year_1, pop_400_year_2, pop_400_year_3, pop_400_year_4, pop_400_year_5]

pop_450_year_1 = np.array([])
pop_450_year_2 = np.array([])
pop_450_year_3 = np.array([])
pop_450_year_4 = np.array([])
pop_450_year_5 = np.array([])
pop_450_year_list = [pop_450_year_1, pop_450_year_2, pop_450_year_3, pop_450_year_4, pop_450_year_5]

pop_500_year_1 = np.array([])
pop_500_year_2 = np.array([])
pop_500_year_3 = np.array([])
pop_500_year_4 = np.array([])
pop_500_year_5 = np.array([])
pop_500_year_list = [pop_500_year_1, pop_500_year_2, pop_500_year_3, pop_500_year_4, pop_500_year_5]

pop_550_year_1 = np.array([])
pop_550_year_2 = np.array([])
pop_550_year_3 = np.array([])
pop_550_year_4 = np.array([])
pop_550_year_5 = np.array([])
pop_550_year_list = [pop_550_year_1, pop_550_year_2, pop_550_year_3, pop_550_year_4, pop_550_year_5]

slices = [90,91,92,92]
minutes = pd.date_range('2015-01-01 00:00:00','2015-12-31 23:59:00',freq='T')    

for sh in range(0,5):
    for season in range(len(pop_50_list[sh])):
        pop_50_year_list[sh] = np.append(pop_50_year_list[sh],pop_50_list[sh][season][0:(slices[season]*1440)])
        pop_100_year_list[sh] = np.append(pop_100_year_list[sh],pop_100_list[sh][season][0:(slices[season]*1440)])
        pop_150_year_list[sh] = np.append(pop_150_year_list[sh],pop_150_list[sh][season][0:(slices[season]*1440)])
        pop_200_year_list[sh] = np.append(pop_200_year_list[sh],pop_200_list[sh][season][0:(slices[season]*1440)])
        pop_250_year_list[sh] = np.append(pop_250_year_list[sh],pop_250_list[sh][season][0:(slices[season]*1440)])
        pop_300_year_list[sh] = np.append(pop_300_year_list[sh],pop_300_list[sh][season][0:(slices[season]*1440)])
        pop_350_year_list[sh] = np.append(pop_350_year_list[sh],pop_350_list[sh][season][0:(slices[season]*1440)])
        pop_400_year_list[sh] = np.append(pop_400_year_list[sh],pop_400_list[sh][season][0:(slices[season]*1440)])
        pop_450_year_list[sh] = np.append(pop_450_year_list[sh],pop_450_list[sh][season][0:(slices[season]*1440)])
        pop_500_year_list[sh] = np.append(pop_500_year_list[sh],pop_500_list[sh][season][0:(slices[season]*1440)])
        pop_550_year_list[sh] = np.append(pop_550_year_list[sh],pop_550_list[sh][season][0:(slices[season]*1440)])
        
    pop_50_year_list[sh] = pd.DataFrame(pop_50_year_list[sh], dtype= 'float32', index=minutes)
    pop_100_year_list[sh] = pd.DataFrame(pop_100_year_list[sh], dtype= 'float32', index=minutes)
    pop_150_year_list[sh] = pd.DataFrame(pop_150_year_list[sh], dtype= 'float32', index=minutes)
    pop_200_year_list[sh] = pd.DataFrame(pop_200_year_list[sh], dtype= 'float32', index=minutes)
    pop_250_year_list[sh] = pd.DataFrame(pop_250_year_list[sh], dtype= 'float32', index=minutes)
    pop_300_year_list[sh] = pd.DataFrame(pop_300_year_list[sh], dtype= 'float32', index=minutes)
    pop_350_year_list[sh] = pd.DataFrame(pop_350_year_list[sh], dtype= 'float32', index=minutes)
    pop_400_year_list[sh] = pd.DataFrame(pop_400_year_list[sh], dtype= 'float32', index=minutes)
    pop_450_year_list[sh] = pd.DataFrame(pop_450_year_list[sh], dtype= 'float32', index=minutes)
    pop_500_year_list[sh] = pd.DataFrame(pop_500_year_list[sh], dtype= 'float32', index=minutes)
    pop_550_year_list[sh] = pd.DataFrame(pop_550_year_list[sh], dtype= 'float32', index=minutes)


#%% Saving output

for sh in range(0,5):

    pop_50_year_list[sh].resample('H').mean().to_csv('processed/pop_50_%d.csv' %(sh+1))
    pop_100_year_list[sh].resample('H').mean().to_csv('processed/pop_100_%d.csv' %(sh+1))
    pop_150_year_list[sh].resample('H').mean().to_csv('processed/pop_150_%d.csv' %(sh+1))
    pop_200_year_list[sh].resample('H').mean().to_csv('processed/pop_200_%d.csv' %(sh+1))
    pop_250_year_list[sh].resample('H').mean().to_csv('processed/pop_250_%d.csv' %(sh+1))
    pop_300_year_list[sh].resample('H').mean().to_csv('processed/pop_300_%d.csv' %(sh+1))
    pop_350_year_list[sh].resample('H').mean().to_csv('processed/pop_350_%d.csv' %(sh+1))
    pop_400_year_list[sh].resample('H').mean().to_csv('processed/pop_400_%d.csv' %(sh+1))
    pop_450_year_list[sh].resample('H').mean().to_csv('processed/pop_450_%d.csv' %(sh+1))
    pop_500_year_list[sh].resample('H').mean().to_csv('processed/pop_500_%d.csv' %(sh+1))
    pop_550_year_list[sh].resample('H').mean().to_csv('processed/pop_550_%d.csv' %(sh+1))

