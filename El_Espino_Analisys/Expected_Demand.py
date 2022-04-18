#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 19:25:39 2018

@author: Sergio Balderrama
ULg-UMSS
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

Datos = pd.read_excel('Datos.xls',index_col=0) 
average = []

for i in range(1,len(Datos)+1):
    a = 0
    for j in Datos.columns:
        a += Datos [j][i]
        
    
    average.append(a/3)


Datos['Average'] = average
Datos = Datos*100
Datos.index = np.arange(0.8, 1.8, 0.1)


size = [20,15]
fig=plt.figure(figsize=size)

ax=Datos['Exp 1'].plot(style=':')
ax=Datos['Exp 2'].plot(style='.-')
ax=Datos['Exp 3'].plot(style='--')
ax=Datos['Average'].plot(style='-')

tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
ax.tick_params(axis='x', which='major', labelsize = tick_size,pad=10 )
ax.tick_params(axis='y', which='major', labelsize = tick_size )

plt.legend(bbox_to_anchor=(0.9,-0.05),frameon=False, ncol=4,
           fontsize = 30)
plt.xlabel('Factor',size=30)
plt.ylabel('Probability of ocurrence (%)',size=30)


