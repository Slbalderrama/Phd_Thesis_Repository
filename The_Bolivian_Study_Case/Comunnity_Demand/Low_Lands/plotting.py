# -*- coding: utf-8 -*-
"""
Created on Mon May 20 11:01:48 2019

@author: Lombardi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

minutes = pd.date_range('2015-01-01 00:00:00','2015-12-31 23:59:00',freq='T')    

hospital = pd.read_csv('Hospital.csv')
hospital.set_index('Unnamed: 0', inplace=True)

school = pd.read_csv('School.csv')
school.set_index('Unnamed: 0', inplace=True)

pop_50_households = []
pop_100_households = []
pop_150_households = []
pop_200_households = []
pop_250_households = []
pop_300_households = []
pop_350_households = []
pop_400_households = []
pop_450_households = []
pop_500_households = []
pop_550_households = []

pop_50_cooking = []
pop_100_cooking = []
pop_150_cooking = []
pop_200_cooking = []
pop_250_cooking = []
pop_300_cooking = []
pop_350_cooking = []
pop_400_cooking = []
pop_450_cooking = []
pop_500_cooking = []
pop_550_cooking = []

for sh in range(0,5):

    #Households
    pop_50_households.append(pd.read_csv('Households/pop_50_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_100_households.append(pd.read_csv('Households/pop_100_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_150_households.append(pd.read_csv('Households/pop_150_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_200_households.append(pd.read_csv('Households/pop_200_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_250_households.append(pd.read_csv('Households/pop_250_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_300_households.append(pd.read_csv('Households/pop_300_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_350_households.append(pd.read_csv('Households/pop_350_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_400_households.append(pd.read_csv('Households/pop_400_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_450_households.append(pd.read_csv('Households/pop_450_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_500_households.append(pd.read_csv('Households/pop_500_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_550_households.append(pd.read_csv('Households/pop_550_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    
    #Cooking
    pop_50_cooking.append(pd.read_csv('Cooking/pop_50_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_100_cooking.append(pd.read_csv('Cooking/pop_100_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_150_cooking.append(pd.read_csv('Cooking/pop_150_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_200_cooking.append(pd.read_csv('Cooking/pop_200_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_250_cooking.append(pd.read_csv('Cooking/pop_250_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_300_cooking.append(pd.read_csv('Cooking/pop_300_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_350_cooking.append(pd.read_csv('Cooking/pop_350_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_400_cooking.append(pd.read_csv('Cooking/pop_400_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_450_cooking.append(pd.read_csv('Cooking/pop_450_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_500_cooking.append(pd.read_csv('Cooking/pop_500_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    pop_550_cooking.append(pd.read_csv('Cooking/pop_550_%d.csv' %(sh+1), index_col='Unnamed: 0'))
    
#%% plot test
start = '2015-03-01 00:00:00'
stop = '2015-03-03 23:00:00'

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2,3, sharex = 'col', sharey = 'row', gridspec_kw = {'height_ratios':[1,1], 'wspace':0.1, 'hspace':0.3}, figsize=(12,6))

x = pd.date_range(start,stop, freq= 'H')
y1 = [pop_50_households[0][start:stop].values[:,0],hospital[start:stop].values[:,0],school[start:stop].values[:,0],pop_50_cooking[0][start:stop].values[:,0]]
y2 = [pop_250_households[0][start:stop].values[:,0],hospital[start:stop].values[:,0],school[start:stop].values[:,0],pop_250_cooking[0][start:stop].values[:,0]]
y3 = [pop_500_households[0][start:stop].values[:,0],hospital[start:stop].values[:,0],school[start:stop].values[:,0],pop_500_cooking[0][start:stop].values[:,0]]

y4 = [pop_50_households[4][start:stop].values[:,0],hospital[start:stop].values[:,0],school[start:stop].values[:,0],pop_50_cooking[4][start:stop].values[:,0]]
y5 = [pop_250_households[4][start:stop].values[:,0],hospital[start:stop].values[:,0],school[start:stop].values[:,0],pop_250_cooking[4][start:stop].values[:,0]]
y6 = [pop_500_households[4][start:stop].values[:,0],hospital[start:stop].values[:,0],school[start:stop].values[:,0],pop_500_cooking[4][start:stop].values[:,0]]

colours = ['#596FB7','#59B777','#D2B244','#D26044']
labels = ['households','hospital','school','cooking']

ax1.stackplot(x,y1,labels=labels,colors=colours)
ax1.margins(x=0)
ax1.margins(y=0)
#ax1.text(0.5,0.9, 'population: 50 hh', weight='bold', transform=ax1.transAxes, verticalalignment='top', horizontalalignment='center')

ax2.stackplot(x,y2,labels=labels,colors=colours)
ax2.margins(x=0)
ax2.margins(y=0)
#ax2.text(0.5,0.9, 'population: 250 hh', weight='bold', transform=ax2.transAxes, verticalalignment='top', horizontalalignment='center')
ax2.set_title('poverty share: 50%', weight='bold')

ax3.stackplot(x,y3,labels=labels,colors=colours)
ax3.margins(x=0)
ax3.margins(y=0)
#ax3.text(0.5,0.9, 'population: 500 hh', weight='bold', transform=ax3.transAxes, verticalalignment='top', horizontalalignment='center')
lgd = ax3.legend(loc=2,  bbox_to_anchor=(1.1,1))

ax4.stackplot(x,y4,labels=labels,colors=colours)
ax4.margins(x=0)
ax4.margins(y=0)

ax5.stackplot(x,y5,labels=labels,colors=colours)
ax5.set_title('poverty share: 90%', weight='bold')
ax5.margins(x=0)
ax5.margins(y=0)

ax6.stackplot(x,y6,labels=labels,colors=colours)
ax6.margins(x=0)
ax6.margins(y=0)

ax4.xaxis.set_major_locator(plt.MaxNLocator(3))
ax4.xaxis.set_major_formatter(plt.FixedFormatter(['day1','day2','day3']))
ax5.xaxis.set_major_locator(plt.MaxNLocator(3))
ax5.xaxis.set_major_formatter(plt.FixedFormatter(['day1','day2','day3']))
ax6.xaxis.set_major_locator(plt.MaxNLocator(3))
ax6.xaxis.set_major_formatter(plt.FixedFormatter(['day1','day2','day3']))

#%% zoom on small population
#%% plot test
start = '2015-03-01 00:00:00'
stop = '2015-03-03 23:00:00'

fig, ((ax1), (ax4)) = plt.subplots(2,1, sharex = 'col', sharey = 'row', gridspec_kw = {'height_ratios':[1,1], 'wspace':0.1, 'hspace':0.3}, figsize=(12,6))

x = pd.date_range(start,stop, freq= 'H')
y1 = [pop_50_households[0][start:stop].values[:,0],hospital[start:stop].values[:,0],school[start:stop].values[:,0],pop_50_cooking[0][start:stop].values[:,0]]

y4 = [pop_50_households[4][start:stop].values[:,0],hospital[start:stop].values[:,0],school[start:stop].values[:,0],pop_50_cooking[4][start:stop].values[:,0]]

colours = ['#596FB7','#59B777','#D2B244','#D26044']
labels = ['households','hospital','school','cooking']

ax1.stackplot(x,y1,labels=labels,colors=colours)
ax1.margins(x=0)
ax1.margins(y=0)
#ax1.text(0.5,0.9, 'population: 50 hh', weight='bold', transform=ax1.transAxes, verticalalignment='top', horizontalalignment='center')

lgd = ax1.legend(loc=2,  bbox_to_anchor=(1.1,1))

ax4.stackplot(x,y4,labels=labels,colors=colours)
ax4.margins(x=0)
ax4.margins(y=0)

ax4.xaxis.set_major_locator(plt.MaxNLocator(3))
ax4.xaxis.set_major_formatter(plt.FixedFormatter(['day1','day2','day3']))
