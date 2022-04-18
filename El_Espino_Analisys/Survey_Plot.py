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

Datos = pd.read_excel('Data/Survey_Data.xls',index_col=0) 
average = []




Datos['Average'] = (Datos['Exp 1'] + Datos['Exp 2'] + Datos['Exp 3'])/3
Datos = Datos*100
Datos.index = np.arange(0.8, 1.8, 0.1)


size = [20,15]
fig=plt.figure(figsize=size)

ax=Datos['Exp 1'].plot(style=':', c='b')
ax=Datos['Exp 2'].plot(style='.-', c='g')
ax=Datos['Exp 3'].plot(style='--', c='r')
ax=Datos['Average'].plot(style='-',c='c')

tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
ax.tick_params(axis='x', which='major', labelsize = tick_size,pad=10 )
ax.tick_params(axis='y', which='major', labelsize = tick_size )

ax.set_xlim([0.8,1.7])
ax.set_ylim([0,35])

plt.legend(bbox_to_anchor=(0.9,-0.05),frameon=False, ncol=4,
           fontsize = 30)
plt.xlabel('Factor',size=30)
plt.ylabel('Probability of ocurrence (%)',size=30)


plt.savefig('Plots/Probability_Ocurrence.png')

Datos['Percentage of Ocurrence'] = round(Datos['Average']/100,3)

# small fix for the percentage of occurrence column sums 1

Datos.loc[1.5,'Percentage of Ocurrence'] = Datos.loc[1.5,'Percentage of Ocurrence']-0.001

#check that everything is 100 or 1

print(Datos.sum())

print(Datos['Percentage of Ocurrence'])














