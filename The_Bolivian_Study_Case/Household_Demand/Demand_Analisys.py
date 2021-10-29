# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 17:20:58 2021

@author: Dell
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.lines as mlines

Lowlands_LI = pd.DataFrame()

for i in range (1,5):
    
    path = 'Scenario_1_' + str(i) + '_new.csv'
    data = pd.read_csv(path, header=0,index_col=0)
    Lowlands_LI[i] = data['0']


Lowlands_HI = pd.DataFrame()

for i in range (1,5):
    
    path = 'Scenario_2_' + str(i) + '_new.csv'
    data = pd.read_csv(path, header=0,index_col=0)
    Lowlands_HI[i] = data['0']
    
Highlands_LI = pd.DataFrame()

for i in range (1,5):
    
    path = 'Scenario_3_' + str(i) + '_new.csv'
    data = pd.read_csv(path, header=0,index_col=0)
    Highlands_LI[i] = data['0']


Highlands_HI = pd.DataFrame()

for i in range (1,5):
    
    path = 'Scenario_4_' + str(i) + '_new.csv'
    data = pd.read_csv(path, header=0,index_col=0)
    Highlands_HI[i] = data['0']
    
#%%




Highlands_HI_legend = mlines.Line2D([], [], color='b',
                                  label='Highlands HI', 
                                  linestyle='-')

Highlands_LI_legend = mlines.Line2D([], [], color='r',
                                  label='Highlands LI', 
                                  linestyle='-')

Lowlands_HI_legend = mlines.Line2D([], [], color='k',
                                  label='Lowlands HI', 
                                  linestyle='-')

Lowlands_LI_legend = mlines.Line2D([], [], color='c',
                                  label='Lowlands LI', 
                                  linestyle='-')

fontsize = '40'
start= 0  #  0
end  = 96 # 24
title_size = 100
fig = plt.figure(figsize=(30,30))
size = [20,20]
label_size = 50
tick_size = 50 
ax1 = fig.add_subplot(211)
pad = 30
mpl.rcParams['xtick.labelsize'] = tick_size
mpl.rcParams['ytick.labelsize'] = tick_size


# Hihglands
ax1.plot(range(start,end), Highlands_HI[1][start:end], c = 'b')
ax1.plot(range(start,end), Highlands_HI[2][start:end], c = 'b')
#ax1.plot(range(start,end), Highlands_HI[3][start:end], c = 'b')
#ax1.plot(range(start,end), Highlands_HI[4][start:end], c = 'b')

ax1.plot(range(start,end), Highlands_LI[1][start:end], c = 'r')
ax1.plot(range(start,end), Highlands_LI[2][start:end], c = 'r')
#ax1.plot(range(start,end), Highlands_LI[3][start:end], c = 'r')
#ax1.plot(range(start,end), Highlands_LI[4][start:end], c = 'r')


ax1.set_xlim([start,end-1]) # ax1.set_xlim([start,end-1]) 
ax1.set_ylim([0, 350]) # ax1.set_ylim([0, 350])
ax1.set_xlabel('Hours', size=label_size)
ax1.set_ylabel('Power (W)', size=label_size)
ax1.set_title('a.', size=title_size,pad=pad, loc = 'left')
plt.legend(handles=[Highlands_HI_legend, Highlands_LI_legend], 
           fontsize=fontsize)

# Lowlands
ax2 = fig.add_subplot(212)
ax2.plot(range(start,end), Lowlands_HI[1][start:end], c = 'k')
ax2.plot(range(start,end), Lowlands_HI[2][start:end], c = 'k')
#ax2.plot(range(start,end), Lowlands_HI[3][start:end], c = 'k')
#ax2.plot(range(start,end), Lowlands_HI[4][start:end], c = 'k')

ax2.plot(range(start,end), Lowlands_LI[1][start:end], c = 'c')
ax2.plot(range(start,end), Lowlands_LI[2][start:end], c = 'c')
#ax2.plot(range(start,end), Lowlands_LI[3][start:end], c = 'c')
#ax2.plot(range(start,end), Lowlands_LI[4][start:end], c = 'c')
ax2.set_xlim([start,end-1])
ax2.set_ylim([0, 300])

ax2.set_xlabel('Hours', size=label_size)
ax2.set_ylabel('Power (W)', size=label_size)
ax2.set_title('b.', size=title_size, pad=pad, loc = 'left')

plt.legend(handles=[Lowlands_HI_legend, Lowlands_LI_legend], 
           fontsize=fontsize)
plt.subplots_adjust(hspace= 0.35)

plt.savefig('Demand_Household_Level.png')

plt.show()

#%%

Table = pd.DataFrame()

Table['Highlands HC'] = Highlands_HI[1]
Table['Highlands LC'] = Highlands_LI[1]
Table['Lowlands HC'] = Lowlands_HI[1]
Table['Lowlands LC'] = Lowlands_LI[1]
Table_Final = Table.describe()

for i in Table_Final.columns:
    
    Table_Final.loc['Monthly Total Energy (kWh)',i] = Table[i].sum()/(12*1000)

Table_Final = round(Table_Final, 1)
print(Table_Final)



#%%

Demand = pd.DataFrame()

Demand[1] = Highlands_HI[1] 
Demand[2] = Highlands_HI[2]
Demand[3] = Highlands_HI[3]
Demand[4] = Highlands_HI[4]

Demand[5] = Highlands_LI[1]
Demand[6] = Highlands_LI[2]
Demand[7] = Highlands_LI[3]
Demand[8] = Highlands_LI[4]

Demand[9] =  Lowlands_HI[1]
Demand[10] = Lowlands_HI[2]
Demand[11] = Lowlands_HI[3]
Demand[12] = Lowlands_HI[4]

Demand[13] = Lowlands_LI[1]
Demand[14] = Lowlands_LI[2]
Demand[15] = Lowlands_LI[3]
Demand[16] = Lowlands_LI[4]

Demand.index = range(1,8761)

Demand.to_excel('Demand.xls')



#%%

index = pd.DatetimeIndex(start='2016-01-01 00:00:00', periods=8760, freq=('1H'))

Demand.index = index

LDC = pd.DataFrame()

index_LDR = []
for i in range(len(Demand)):
        index_LDR.append((i+1)/float(len(Demand))*100)

for i in Demand.columns:
    
    foo = Demand.sort_values(i, ascending=False)
    foo.index = index_LDR
    LDC[i] = foo[i]

fig = plt.figure(figsize=(30,30))

ax1 = fig.add_subplot(111)

ax1.plot(index_LDR, LDC[1], c = 'b')
ax1.plot(index_LDR, LDC[2], c = 'b')
ax1.plot(index_LDR, LDC[3], c = 'b')
ax1.plot(index_LDR, LDC[4], c = 'b')

ax1.plot(index_LDR, LDC[5], c = 'r')
ax1.plot(index_LDR, LDC[6], c = 'r')
ax1.plot(index_LDR, LDC[7], c = 'r')
ax1.plot(index_LDR, LDC[8], c = 'r')

ax1.plot(index_LDR, LDC[9], c = 'k')
ax1.plot(index_LDR, LDC[10], c = 'k')
ax1.plot(index_LDR, LDC[11], c = 'k')
ax1.plot(index_LDR, LDC[12], c = 'k')

ax1.plot(index_LDR, LDC[13], c = 'c')
ax1.plot(index_LDR, LDC[14], c = 'c')
ax1.plot(index_LDR, LDC[15], c = 'c')
ax1.plot(index_LDR, LDC[16], c = 'c')

ax1.set_xlim([0,100])
ax1.set_ylim([0, 500])
ax1.set_xlabel('Percentage (%)', size=label_size)
ax1.set_ylabel('Power (W)', size=label_size)

plt.show()


#%%

Demand_1 = Demand



Demand_1['hour'] = Demand.index.hour

Demand_Hourly = Demand_1.groupby(['hour']).mean()

fig = plt.figure(figsize=(30,30))

ax1 = fig.add_subplot(111)

ax1.plot(Demand_Hourly.index, Demand_Hourly[1], c = 'b')
ax1.plot(Demand_Hourly.index, Demand_Hourly[2], c = 'b')
ax1.plot(Demand_Hourly.index, Demand_Hourly[3], c = 'b')
ax1.plot(Demand_Hourly.index, Demand_Hourly[4], c = 'b')

ax1.plot(Demand_Hourly.index, Demand_Hourly[5], c = 'r')
ax1.plot(Demand_Hourly.index, Demand_Hourly[6], c = 'r')
ax1.plot(Demand_Hourly.index, Demand_Hourly[7], c = 'r')
ax1.plot(Demand_Hourly.index, Demand_Hourly[8], c = 'r')

ax1.plot(Demand_Hourly.index, Demand_Hourly[9], c = 'k')
ax1.plot(Demand_Hourly.index, Demand_Hourly[10], c = 'k')
ax1.plot(Demand_Hourly.index, Demand_Hourly[11], c = 'k')
ax1.plot(Demand_Hourly.index, Demand_Hourly[12], c = 'k')

ax1.plot(Demand_Hourly.index,  Demand_Hourly[13], c = 'c')
ax1.plot(Demand_Hourly.index,  Demand_Hourly[14], c = 'c')
ax1.plot(Demand_Hourly.index,  Demand_Hourly[15], c = 'c')
ax1.plot(Demand_Hourly.index,  Demand_Hourly[16], c = 'c')



ax1.set_xlim([0,23])
ax1.set_ylim([0, 300])
ax1.set_xlabel('hours', size=label_size)
ax1.set_ylabel('Power (W)', size=label_size)
