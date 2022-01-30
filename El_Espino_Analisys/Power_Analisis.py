# -*- coding: utf-8 -*-
"""
Created on Wed May 19 14:06:10 2021

@author: Dell
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.ticker as mtick
import matplotlib.pylab as pylab
import enlopy as el
import matplotlib as mpl
from datetime import datetime
import os
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D


'''Data Analsys of El Espino microgrid '''




#%%

# load data

data = pd.read_csv('Data/Data_Espino_Thesis_Fill_2.csv', header=0,index_col=0)
index = pd.DatetimeIndex(start='2016-01-01 00:00:00', periods=166464, freq=('5min'))
data.index = index

#%%
#ok
# Real energy flow

start = '2016-12-24 00:05:00'
end = '2016-12-29 23:55:00'


b_o = 'Discharge energy from the Battery'
b_i = 'Charge energy to the Battery'
pv_c ='PV Corrected'
pv_e ='Energy PV'
de = 'Energy_Demand'
    
Plot_Data = data[start:end].copy()

#    Plot_Data['SOC'] = (Plot_Data['SOC'])/100
    
Plot_Data.columns = ['Energy PV', 'Energy Diesel', 'State_Of_Charge_Battery', 
                     'Ambient temperature', 'Energy_Demand',
                     'Solar Irradiation', 'PV Temperature 2', 'Charge energy to the Battery',
                     'Discharge energy from the Battery']  

  
Plot_Data[b_i] = -Plot_Data[b_i].copy()
 
    
Vec = Plot_Data['Energy PV'] + Plot_Data['Energy Diesel']
Vec2 = (Plot_Data['Energy PV'] + Plot_Data['Energy Diesel'] + 
            Plot_Data['Discharge energy from the Battery'])
    
# for t in Plot_Data.index:
        
        
#     if Plot_Data[pv_c][t]>0 and Plot_Data[b_o][t]>0:
#             Curtailment = Plot_Data[pv_c][t] - Plot_Data[pv_e][t]
#             Plot_Data.loc[t,'Curtailment 2'] = Curtailment + Plot_Data[de][t]
#             Plot_Data.loc[t,pv_c] = Plot_Data[pv_e][t]
#     else:
#             Plot_Data.loc[t,'Curtailment 2'] = Plot_Data[de][t]
    
size = [20,10]    
plt.figure(figsize=size)
    # Gen energy
c_g = 'm'
Alpha_g = 0.3 
hatch_g = '\\'
ax1= Vec.plot(style='y-', linewidth=0) # Plot the line of the diesel energy plus the PV energy
ax1.fill_between(Plot_Data.index, Plot_Data['Energy PV'].values, Vec.values,   
                     alpha=Alpha_g, color = c_g,hatch =hatch_g )
    #ax2= Vec.plot(style='b', linewidth=0.5)
    # PV energy
c_PV = 'yellow'   
Alpha_r = 0.4 
    
ax1.fill_between(Plot_Data.index, 0, Plot_Data['Energy PV'].values, 
                     alpha=Alpha_r, color=c_PV) # Fill the area of the energy produce by the diesel generator
    # Energy Demand
ax3 = Plot_Data['Energy_Demand'].plot(style='k', linewidth=2)
    
    # Battery flow out
alpha_bat = 0.3
hatch_b ='x'
C_Bat = 'green'
    
ax3.fill_between(Plot_Data.index, Vec.values , Vec2.values,
                     alpha=alpha_bat, color=C_Bat, hatch=hatch_b)
    
    # Battery flow in
ax5= Plot_Data['Charge energy to the Battery'].plot(style=C_Bat, linewidth=0) # Plot the line of the energy flowing into the battery
ax5.fill_between(Plot_Data.index, 0, 
                     Plot_Data['Charge energy to the Battery'].values, 
                     alpha=alpha_bat, color=C_Bat, hatch=hatch_b) # Fill the area of the energy flowing into the battery

    # State of charge                 
ax6= Plot_Data['State_Of_Charge_Battery'].plot(style='k--', secondary_y=True,
         linewidth=2, alpha=0.7 ) # Plot the line of the State of charge of the battery
    
    # Curtailment
#    alpha_cu = 0.3
#    hatch_cu = '+'
#    C_Cur = 'blue'
#    ax7 = Plot_Data['PV Corrected'].plot(style='b-', linewidth=0)
#    ax7.fill_between(Plot_Data.index, Plot_Data['Energy PV'].values,
#                     Plot_Data['PV Corrected'].values,
#                     alpha=alpha_cu, color='blue', hatch=hatch_cu)
#    # Curtailment 2
#    #    ax8 = Plot_Data['Curtailment 2'].plot(style='b-', linewidth=0)
#    ax8.fill_between(Plot_Data.index, Plot_Data['Energy_Demand'].values, 
#                     Plot_Data['Curtailment 2'].values,
#                     alpha=alpha_cu, color='blue', hatch=hatch_cu, 
#                     where= Plot_Data['Curtailment 2']>Plot_Data['Energy_Demand'])
    # Define name  and units of the axis
ax1.set_ylabel('Power (kW)',size=30)
ax1.set_xlabel('Time (hours)',size=30)
ax1.set_xlim([start,end])
ax6.set_ylabel('Battery State of charge (%)',size=30)
    
#    ax1.tick_params(axis='x', which='major', labelsize=20)
    
tick_size = 40  
mpl.rcParams['xtick.labelsize'] = tick_size     
ax1.tick_params(axis='y', which='major', labelsize =30 )
ax1.tick_params(axis='x', which='major', labelsize = tick_size )
ax6.tick_params(axis='y', which='major', labelsize = 30 )
        
    # Define the legends of the plot
From_PV = mpatches.Patch(color=c_PV,alpha=Alpha_r, label='From PV')
From_Generator = mpatches.Patch(color=c_g,alpha=Alpha_g,
                                       label='From Generator',hatch =hatch_g)
Battery = mpatches.Patch(color=C_Bat ,alpha=alpha_bat, 
                                 label='Battery Energy Flow',hatch =hatch_b)
#    Curtailment = mpatches.Patch(color=C_Cur ,alpha=alpha_cu, 
#                                 label='Curtailment',hatch =hatch_cu)

Energy_Demand = mlines.Line2D([], [], color='black',label='Energy Demand')
State_Of_Charge_Battery = mlines.Line2D([], [], color='black',
                                                label='State Of Charge Battery',
                                                linestyle='--',alpha=0.7)
plt.legend(handles=[From_Generator, From_PV, Battery, 
#                        Curtailment,
                            Energy_Demand, State_Of_Charge_Battery],
                            bbox_to_anchor=(1.025, -0.25),fontsize = 20,
                            frameon=False,  ncol=4)



plt.savefig('Plots/Energy_Dispatch_Real_Espino.png')



#%%

# demand plot hourly

Demand = pd.DataFrame()

Start = '2016-01-01 00:00:00'
End =   '2017-07-31 23:55:00'
Demand["Demand"] = data['Demand'][Start:End]

Demand_LDR = Demand.sort_values('Demand', ascending=False)


index_LDR = []
for i in range(len(Demand_LDR)):
        index_LDR.append((i+1)/float(len(Demand_LDR))*100)
Demand_LDR.index = index_LDR


Demand['hour'] = Demand.index.hour
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
table_vals=[[round(Demand['Demand'].mean(),1)],
            [round(Demand['Demand'].std(),1)],
            [round(Demand['Demand'].max(),1)]]

the_table = plt.table(cellText=table_vals,
                  colWidths = [0.1]*3,  
                  rowLabels=row_labels,
                  colLabels=col_labels,
                  loc='upper center')
the_table.set_fontsize(25)
the_table.scale(1, 4)

ax2.set_xlim([0,23])
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

plt.savefig('Plots/Demand_LDR.png')

plt.show()

#%%

# Transforming the time step from 5 min to 1 hour
#%%
data['Bat Power'] = data['Bat Power out'] - data['Bat Power in'] 
data['hour'] = data.index.hour
data['day'] = data.index.dayofyear
data['day of the month'] = data.index.day
data['year'] = data.index.year
data['month'] = data.index.month
data_hourly = data.groupby(['hour']).mean()



Power_Data_Hourly = data.groupby(['year','day', 'hour']).mean()
index_hourly = pd.DatetimeIndex(start='2016-01-01 00:00:00', periods=13872, 
                                   freq=('1H'))

Power_Data_Hourly.index = index_hourly

#%%
# Reviewing data in some point

month = 4
year  = 2017
day = 2
Montly_monitoring_Data = data.loc[data['year']==year]
Montly_monitoring_Data = Montly_monitoring_Data.loc[Montly_monitoring_Data['month']==month]
Daily_monitoring_Data = Montly_monitoring_Data.loc[Montly_monitoring_Data['day of the month']==day]


Montly_monitoring_Data_Sum  = Montly_monitoring_Data.groupby(['day of the month']).sum()
Montly_monitoring_Data_Sum  = Montly_monitoring_Data_Sum.transpose()







#%%

# Energy comsuption 
#ok
start = '2016-01-01 00:00:00'
end   = '2016-12-31 23:00:00'

Energy = Power_Data_Hourly.loc[start:end].copy()
Energy['day'] = list(Energy.index.day)
Total_Energy = Energy['Demand'].sum()/1000
Total_Energy = round(Total_Energy, 1)
print('The energy consume in a year is ' + str(Total_Energy) + ' MWh')



#%%
Genset_LDR = data.sort_values('GenSet Power', ascending=False)

index_LDR = []
for i in range(len(Genset_LDR)):
        index_LDR.append((i+1)/float(len(Genset_LDR))*100)
Genset_LDR.index = index_LDR

size = [20,15]
fig=plt.figure(figsize=size)
tick_size = 25    
mpl.rcParams['xtick.labelsize'] = tick_size 
mpl.rcParams['ytick.labelsize'] = tick_size 


ax=fig.add_subplot(111, label="1")
ax2=fig.add_subplot(111, label="2", frame_on=False)
label_size = 25
ax.plot(Genset_LDR.index, Genset_LDR['GenSet Power'])
ax.set_xlim([0,100])
ax.set_ylim([0,58])
ax.set_xlabel("Percentage (%)",size=label_size)
ax.set_ylabel("Power (kW)",size=label_size)
ax.tick_params(axis='y', which='major', labelsize = tick_size )
ax.tick_params(axis='x', which='major', labelsize = tick_size )

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax2.plot(data_hourly.index,  data_hourly['GenSet Power'],c = 'k',
          linestyle='dashed')
ax2.set_xlim([0,23])
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.set_xlabel('hours',size=label_size) 
ax2.set_ylabel('Power (kW)',size=label_size) 
ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right') 

demand = mlines.Line2D([], [], color='k',
                                  label='Genset Power', 
                                  linestyle='--')
ldr = mlines.Line2D([], [], color='b',
                                  label='LDC Genset', 
                                  linestyle='-')

plt.legend(handles=[ demand, ldr],
           bbox_to_anchor=(0.8,-0.05),
    frameon=False, ncol=2,fontsize = 30)

plt.savefig('Plots/Genset_LDR.png')

plt.show()


#%%%
data['hour'] = data.index.hour
data['day'] = data.index.dayofyear
data['year'] = data.index.year
data['Bat Power'] = data['Bat Power out'] - data['Bat Power in'] 

start = '2016-01-01 00:00:00' # '2017-01-01 00:00:00' '2016-01-01 00:00:00' 
end   = '2017-07-31 23:55:00' # '2017-07-31 23:55:00' '2016-12-31 23:55:00' 
data_hourly = data[start:end] 
data_hourly = data_hourly.groupby(['hour']).mean()



data_hourly = round(data_hourly,1)
#%%
Diesel_Comsuption = pd.read_excel('Data/Diesel_Comsuption.xls',index_col=0)
Diesel_Comsuption = Diesel_Comsuption.fillna(0)
Diesel_Comsuption = Diesel_Comsuption[:-1]
Diesel_Comsuption.index =  pd.to_datetime(Diesel_Comsuption.index)

Genset_Power = pd.DataFrame()
Genset_Power['GenSet Power'] = Power_Data_Hourly['GenSet Power']['2017-01-01 00:00:00':'2017-06-30 23:00:00'].copy()


LHV = 9.9
limit = 0
Genset_Power_1 = pd.DataFrame()
Genset_Power_1['GenSet Power']  =  Genset_Power['GenSet Power'].loc[Genset_Power['GenSet Power']>limit]

Real_efficiency = (Genset_Power_1['GenSet Power'].sum())/(Diesel_Comsuption['Diesel'].sum()*LHV)
Real_efficiency = round(Real_efficiency, 4)*100



Genset_Power_1['month'] = Genset_Power_1.index.month

Genset_Power_Monthly = Genset_Power_1.groupby(['month']).sum()

Diesel_Comsuption['month'] = Diesel_Comsuption.index.month
Diesel_Comsuption_Montly = Diesel_Comsuption.groupby(['month']).sum()

Montly_Diesel_Data = pd.DataFrame()
Montly_Diesel_Data['Genset Energy'] = Genset_Power_Monthly['GenSet Power']
Montly_Diesel_Data['Diesel Comsuption'] = Diesel_Comsuption_Montly['Diesel']
Montly_Diesel_Data['Efficiency'] = Montly_Diesel_Data['Genset Energy']/(Montly_Diesel_Data['Diesel Comsuption']*LHV)

for i in range(1,7):
    
    Genset_Power_2 = Genset_Power_1['GenSet Power'].loc[Genset_Power_1['month']==i]
    hours = len(Genset_Power_2) 
    Montly_Diesel_Data.loc[i,'Power'] = Genset_Power_2.mean()
    Montly_Diesel_Data.loc[i,'Hours'] = hours 

Montly_Diesel_Data['Diesel per hour'] = Montly_Diesel_Data['Diesel Comsuption']/Montly_Diesel_Data['Hours']
Montly_Diesel_Data = round(Montly_Diesel_Data, 3) 

print('The real efficiency of the genset is ' + str(round(Montly_Diesel_Data['Efficiency'].mean()*100,1))+ ' %')

#%%

# Battery analysis

Bat_Charging    = data.loc[data['Bat Power']<0]
Bat_0    = data.loc[data['Bat Power']==0]
Bat_Discharging = data.loc[data['Bat Power']>0]

Percentage_1 = len(Bat_Charging)/len(data)
Percentage_1 = round(Percentage_1*100,1)
Percentage_2 = len(Bat_0)/len(data)
Percentage_2 = round(Percentage_2*100,1)
Percentage_3 = len(Bat_Discharging)/len(data)
Percentage_3 = round(Percentage_3*100,1)

print('The percentage of time that the battery is charging is '      + str(Percentage_1) + ' % .' )
print('The percentage of time that the battery is doing nothing is ' + str(Percentage_2) + ' % .' )
print('The percentage of time that the battery is discharging is '   + str(Percentage_3) + ' % .' )

Round_Trip_Efficiency = Power_Data_Hourly['Bat Power out'].sum()/ Power_Data_Hourly['Bat Power in'].sum()
Round_Trip_Efficiency = round(Round_Trip_Efficiency*100, 1)

print('The round trip efficiency of the battery is ' + str(Round_Trip_Efficiency) + ' %.')

#%%

Soc_LDR = data.sort_values('SOC', ascending=False)

index_LDR = []
for i in range(len(Soc_LDR )):
        index_LDR.append((i+1)/float(len(Soc_LDR ))*100)
Soc_LDR .index = index_LDR

size = [20,15]
fig=plt.figure(figsize=size)
tick_size = 25    
mpl.rcParams['xtick.labelsize'] = tick_size 
mpl.rcParams['ytick.labelsize'] = tick_size 


ax=fig.add_subplot(111, label="1")
ax2=fig.add_subplot(111, label="2", frame_on=False)
label_size = 25
ax.plot(Soc_LDR .index, Soc_LDR['SOC'])
ax.set_xlim([0,100])
ax.set_ylim([0, 100])
ax.set_xlabel("Percentage (%)",size=label_size)
ax.set_ylabel("SOC (%)",size=label_size)
ax.tick_params(axis='y', which='major', labelsize = tick_size )
ax.tick_params(axis='x', which='major', labelsize = tick_size )

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax2.plot(data_hourly.index,  data_hourly['Bat Power'],c = 'k',
          linestyle='dashed')
ax2.set_xlim([0,23])
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.set_xlabel('hours',size=label_size) 
ax2.set_ylabel('Power (kW)',size=label_size) 
ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right') 

demand = mlines.Line2D([], [], color='k',
                                  label='Battery Power', 
                                  linestyle='--')
ldr = mlines.Line2D([], [], color='b',
                                  label='LDC Battery', 
                                  linestyle='-')

plt.legend(handles=[ demand, ldr],
           bbox_to_anchor=(0.8,-0.05),
    frameon=False, ncol=2,fontsize = 30)

plt.savefig('Plots/Battery_LDR.png')

plt.show()

#%%



# PV_LDR = data.sort_values('PV Power', ascending=False)

# index_LDR = []
# for i in range(len(Soc_LDR )):
#         index_LDR.append((i+1)/float(len(PV_LDR ))*100)
# PV_LDR .index = index_LDR



size = [20,15]
fig=plt.figure(figsize=size)
tick_size = 25    
mpl.rcParams['xtick.labelsize'] = tick_size 
mpl.rcParams['ytick.labelsize'] = tick_size 


ax=fig.add_subplot(111, label="1")
ax2=fig.add_subplot(111, label="2", frame_on=False)
label_size = 25
ax.plot(data_hourly.index, data_hourly['PV Power'], c = 'b')
ax.set_xlim([0,23])
ax.set_ylim([0, 35])
ax.set_xlabel("Hours",size=label_size)
ax.set_ylabel("Power (kW)",size=label_size)
ax.tick_params(axis='y', which='major', labelsize = tick_size )
ax.tick_params(axis='x', which='major', labelsize = tick_size )

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax2.plot(data_hourly.index,  data_hourly['Solar Irradiation'], c = 'y')
ax2.set_xlim([0,23])
ax2.set_ylim([0,720])
ax2.yaxis.tick_right()
ax2.set_ylabel('Radiation (Wh)',size=label_size) 
#ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right') 

demand = mlines.Line2D([], [], color='b',
                                  label='PV Power', 
                                  linestyle='-')
ldr = mlines.Line2D([], [], color='y',
                                  label='Solar Irradiation', 
                                  linestyle='-')

plt.legend(handles=[ demand, ldr],
           bbox_to_anchor=(0.8,-0.05),
    frameon=False, ncol=2,fontsize = 30)

plt.savefig('Plots/PV_Irradiation.png')

plt.show()


#%%
# PV analysis
PV_data = data.loc[data['PV Power']> 0]

PV_Power_Average = round(PV_data['PV Power'].mean(), 1)
PV_Power_max = round(PV_data['PV Power'].max(), 1)
PV_Production_Time = round((len(PV_data)/len(data))*100, 1)

print('The PV array mean power output is ' + str(PV_Power_Average) + ' kW' )
print('The PV array max power output is ' + str(PV_Power_max) + ' kW' )
print('The PV array produce energy the ' + str(PV_Production_Time ) + ' % of the time' )


#%%
#efficiency plot

Area = 1.65*0.99*240 # 1.61*0.946*240 # 1.65*0.99*240

pv_efficiency = pd.DataFrame()
pv_efficiency = data.loc[data['PV Power']>0]
pv_efficiency.loc[:,'Efficiency'] = (pv_efficiency['PV Power']*1000)/(pv_efficiency['Solar Irradiation']*Area)

pv_efficiency.loc[:,'Hour'] = pv_efficiency.index.hour

# filtering
pv_efficiency = pv_efficiency[pv_efficiency['Efficiency']<0.161]
pv_efficiency = pv_efficiency[pv_efficiency['SOC']<100]
pv_efficiency = pv_efficiency[pv_efficiency['Solar Irradiation']>250]
marker='+'
z= pv_efficiency['Efficiency']

#x = data['Solar Irradiation']
x = pv_efficiency['SOC']
#x = pca_df['PC0']

#y = data['Hour']
#y = data['SOC']
y = pv_efficiency['Ambient temperature']
#y = data['PV Temperature 2']
#y = pca_df['PC1']

x_label='SOC [-]'
y_label='Ambient Temperature [°C]'
z_label='Efficiency'
label_size = 60
size = [40,30]
fig = plt.figure(figsize=size)
tick_size = 50    
mpl.rcParams['xtick.labelsize'] = tick_size 
mpl.rcParams['ytick.labelsize'] = tick_size 
pylab.rcParams['ytick.major.pad']='80'

ax = fig.add_subplot(111, projection='3d')
ax.view_init(30,-110)
ax.scatter(x, y, z, marker=marker)

ax.set_xlabel(x_label,size=label_size, labelpad =120)
#ax.xaxis.label.set_fontsize(16)
ax.set_ylabel(y_label,size=label_size, labelpad =120)
#ax.yaxis.label.set_fontsize(16)
ax.set_zlabel(z_label,size=label_size, labelpad =120)
#ax.zaxis.label.set_fontsize(16)

ax.tick_params(axis='x', which='major', pad=40)
ax.tick_params(axis='y', which='major', pad=50)
ax.tick_params(axis='z', which='major', pad=50)

#plt.title(title,fontsize=16)
plt.savefig('Plots/Efficiency_3D.png')
plt.show()