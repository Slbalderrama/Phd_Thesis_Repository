# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 00:08:45 2021

@author: Dell
"""
import pandas as pd


Data_2 = pd.read_csv('Results/Gutierrez_Data.csv', index_col=0)            

index2 = pd.DatetimeIndex(start='2013-01-01 01:00:00', periods=8760, 
                                   freq=('H'))

start = index2.get_loc('2013-03-21 01:00:00')

Gut_Data_1  = Data_2[start:]
    
end = index2.get_loc('2013-03-21 01:00:00')

Gut_Data_2  = Data_2[:end]

Gut_Data =  Gut_Data_1.append(Gut_Data_2) 

index_3 = pd.DatetimeIndex(start='2016-03-21 01:00:00', periods=8760, 
                                   freq=('H'))

Gut_Data.index = index_3

#### Fix incoherent data
for i in Gut_Data.index:
    a = i.hour
    if any([a==0,a==1,a==2,a==3,a==4,a==5,a==20,a==21,a==22,a==23]):
        
        if Gut_Data.loc[i,'Radiation tilt isotropic'] > 0:
            print(i)
            Gut_Data.loc[i,'Radiation tilt isotropic'] = 0


Gut_Data_describe = Gut_Data.describe() 




