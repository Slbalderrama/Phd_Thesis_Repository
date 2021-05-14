# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 17:15:57 2021

@author: Dell
"""
import pandas as pd
import matplotlib.ticker as mtick
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.lines as mlines

Power_Data_4 = pd.read_csv('Base_Scenario.csv', index_col=0)

index = pd.DatetimeIndex(start='2016-01-01 00:00:00', periods=166464, 
                                   freq=('5min'))

Power_Data_4.index = index

Demand_Hourly = pd.DataFrame()



Power_Data_4['Day'] = 0

foo = 0
iterations = int(len(Power_Data_4)/288)

for i in range(iterations):
    for j in range(288):
        Power_Data_4.iloc[foo,4] = i
        foo += 1
 
Power_Data_4['hour'] = Power_Data_4.index.hour 

Demand_Hourly = Power_Data_4.groupby(['Day','hour']).mean()

index_hourly = pd.DatetimeIndex(start='2016-01-01 01:00:00', periods=13872, 
                                   freq=('1H'))

Demand_Hourly.index = index_hourly

#%%
Demand = pd.DataFrame()

Start = '2016-01-01 01:00:00'  # '2016-03-21 01:00:00' or '2016-01-01 01:00:00'
End   = '2017-08-01 00:00:00'   # '2017-03-21 00:00:00' or '2017-08-01 00:00:00'

Demand["Demand"] = Demand_Hourly['Demand Cre 2'][Start:End]/1000

foo = 0
iterations = int(len(Demand)/24)

for i in range(iterations):
    for j in range(1,25):
        date = Demand.index[foo]
        Demand.loc[date,'hour'] = j
        foo += 1                     


Demand_LDR = Demand.sort_values('Demand', ascending=False)


index_LDR = []
for i in range(len(Demand_LDR)):
        index_LDR.append((i+1)/float(len(Demand_LDR))*100)
Demand_LDR.index = index_LDR

Daily_Curve = Demand.groupby(['hour']).mean()

size = [20,15]
fig=plt.figure(figsize=size)
tick_size = 25    
mpl.rcParams['xtick.labelsize'] = tick_size 
mpl.rcParams['ytick.labelsize'] = tick_size 


ax=fig.add_subplot(111, label="1")
ax2=fig.add_subplot(111, label="2", frame_on=False)

label_size = 25
ax.plot(Demand_LDR.index,Demand_LDR['Demand'])
ax.set_xlim([0,100])
ax.set_xlabel("Percentage (%)",size=label_size)
ax.set_ylabel("Power (kW)",size=label_size)
ax.tick_params(axis='y', which='major', labelsize = tick_size )
ax.tick_params(axis='x', which='major', labelsize = tick_size )

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax2.plot( Daily_Curve.index,Daily_Curve['Demand'],c = 'k',
          linestyle='dashed')

col_labels=['Value']
row_labels=['Average Power (kW)','Standard Deviation (kW)'
            ,'Max Power demand (kW)']
table_vals=[[round(Demand["Demand"].mean(),1)], [round(Demand["Demand"].std(),1)],
             [round(Demand["Demand"].max(),1)]]

the_table = plt.table(cellText=table_vals,
                  colWidths = [0.1]*3,  
                  rowLabels=row_labels,
                  colLabels=col_labels,
                  loc='upper center')
the_table.set_fontsize(25)
the_table.scale(1, 4)

ax2.set_xlim([1,24])
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.set_xlabel('hours',size=label_size) 
ax2.set_ylabel('Power (kW)',size=label_size) 
ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right') 

demand = mlines.Line2D([], [], color='k',
                                  label='Demand', 
                                  linestyle='--')
ldr = mlines.Line2D([], [], color='b',
                                  label='LDC', 
                                  linestyle='-')

plt.legend(handles=[ demand, ldr],
           bbox_to_anchor=(0.67,-0.05),
    frameon=False, ncol=2,fontsize = 30)

plt.savefig('Plots/Demand_LDR.png', bbox_inches='tight')    
plt.show()    
