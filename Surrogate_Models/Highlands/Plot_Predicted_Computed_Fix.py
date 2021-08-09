# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 18:48:53 2020

@author: Dell
"""


import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from sklearn import linear_model
from sklearn.gaussian_process import GaussianProcessRegressor
import matplotlib.pylab as pylab
from joblib import load

data_1 = pd.read_excel('Databases/Database_Fix.xls', index_col=0, Header=None)   
data_2 = pd.read_excel('Databases/Data_Base.xls')

name = 'Fuel Cost'
data_1 = data_1.sort_values(name, ascending=True)

X = pd.DataFrame()
X['Renewable Invesment Cost'] = data_2['Renewable Unitary Invesment Cost']   
X['Battery Unitary Invesment Cost'] = data_2['Battery Unitary Invesment Cost']
X['Deep of Discharge'] = data_2['Deep of Discharge']
X['Battery Cycles'] = data_2['Battery Cycles']
X['GenSet Unitary Invesment Cost'] = data_2['GenSet Unitary Invesment Cost']
X['Generator Efficiency'] = data_2['Generator Efficiency']
X['Low Heating Value'] = data_2['Low Heating Value']
X['Fuel Cost'] = data_2['Fuel Cost']
X['HouseHolds'] = data_2['HouseHolds']
X['Renewable Energy Unit Total'] = data_2['Renewable Energy Unit Total']


X_1 = pd.DataFrame()
X_1['Renewable Invesment Cost'] = data_1['Renewable Unitary Invesment Cost']   
X_1['Battery Unitary Invesment Cost'] = data_1['Battery Unitary Invesment Cost']
X_1['Deep of Discharge'] = data_1['Deep of Discharge']
X_1['Battery Cycles'] = data_1['Battery Cycles']
X_1['GenSet Unitary Invesment Cost'] = data_1['GenSet Unitary Invesment Cost']
X_1['Generator Efficiency'] = data_1['Generator Efficiency']
X_1['Low Heating Value'] = data_1['Low Heating Value']
X_1['Fuel Cost'] = data_1['Fuel Cost']
X_1['HouseHolds'] = data_1['HouseHolds']
X_1['Renewable Energy Unit Total'] = data_1['Renewable Energy Unit Total']

size = [20,15]
tick_size = 25 


#%%

y_NPC = pd.DataFrame()
target= 'NPC' #  'Renewable Capacity' 'Renewable Penetration'
y_NPC[target] = data_2[target]

lm = linear_model.LinearRegression(fit_intercept=True)

lm_NPC = lm.fit(X,y_NPC)

gp_NPC = load('NPC_LowLands.joblib')

y_gp_NPC, std_NPC = gp_NPC.predict(X_1, return_std=True)
y_lm_NPC = lm_NPC.predict(X_1)
# plot NPC
fig=plt.figure(figsize=size)

mpl.rcParams['xtick.labelsize'] = tick_size 
mpl.rcParams['ytick.labelsize'] = tick_size 

ax1=plt.plot(data_1['Fuel Cost'], y_gp_NPC/1000, c='r', label='GPR')
ax2=plt.plot(data_1['Fuel Cost'], y_lm_NPC/1000, c='g', label='MVLR')
ax3_NPC = plt.scatter(data_1['Fuel Cost'], data_1['NPC']/1000, c='y', marker='o', label='Computed NPC')

#ax1.fill_between(data_2['Fuel Cost'], y_gp_NPC[:, 0]/1000 - std_NPC[:]/1000, 
#                y_gp_NPC[:, 0]/1000 + std_NPC[:]/1000, color='darkorange',
#                 alpha=0.2)
pylab.ylim([0,700])
GPR_NPC_line = mlines.Line2D([], [], color='r', label='NPC with GPR')
lm_NPC_line = mlines.Line2D([], [], color='g', label='NPC with MVLR')

plt.legend(handles=[GPR_NPC_line,lm_NPC_line,(ax3_NPC)])


#%%

y_lcoe = pd.DataFrame()
target= 'LCOE' #  'Renewable Capacity' 'Renewable Penetration'
y_lcoe[target] = data_2[target]

lm = linear_model.LinearRegression(fit_intercept=True)

lm_lcoe = lm.fit(X,y_lcoe)

gp_lcoe = load('LCOE_LowLands.joblib')

y_gp_lcoe, std_lcoe = gp_lcoe.predict(X_1, return_std=True)
y_lm_lcoe = lm_lcoe.predict(X_1)

fig=plt.figure(figsize=size)

mpl.rcParams['xtick.labelsize'] = tick_size 
mpl.rcParams['ytick.labelsize'] = tick_size 

ax1=plt.plot(data_1['Fuel Cost'], y_gp_lcoe, c='r', label='LCOE with GPR')
ax2=plt.plot(data_1['Fuel Cost'], y_lm_lcoe, c='g', label='LCOE with MVLR')
ax3_LCOE=plt.scatter(data_1['Fuel Cost'], data_1['LCOE'], c='y', marker='o', label='LCOE Computed')

#ax1.fill_between(data_2['Fuel Cost'], y_gp_NPC[:, 0]/1000 - std_NPC[:]/1000, 
#                y_gp_NPC[:, 0]/1000 + std_NPC[:]/1000, color='darkorange',
#                 alpha=0.2)
pylab.ylim([0,0.6])
GPR_LCOE_line = mlines.Line2D([], [], color='r', label='LCOE with GPR')
lm_LCOE_line = mlines.Line2D([], [], color='g', label='LCOE with MVLR')

plt.legend(handles=[GPR_LCOE_line,lm_LCOE_line,(ax3_LCOE)])


#%%

y_PV = pd.DataFrame()
target= 'Renewable Capacity' #  'Renewable Capacity' 'Renewable Penetration'
y_PV[target] = data_2[target]

lm = linear_model.LinearRegression(fit_intercept=True)

lm_PV = lm.fit(X,y_PV)

gp_PV = load('PV_LowLands.joblib')

y_gp_PV, std_PV = gp_PV.predict(X_1, return_std=True)
y_lm_PV = lm_PV.predict(X_1)


# plot PV
fig=plt.figure(figsize=size)

mpl.rcParams['xtick.labelsize'] = tick_size 
mpl.rcParams['ytick.labelsize'] = tick_size 

ax1=plt.plot(data_1['Fuel Cost'], y_gp_PV, c='r', label='PV with GPR')
ax2=plt.plot(data_1['Fuel Cost'], y_lm_PV, c='g', label='PV with MVLR')
ax3_PV=plt.scatter(data_1['Fuel Cost'], data_1['Renewable Capacity'], c='y', marker='o', label='Computed PV Capacity')
#ax4=plt.plot(data_2['Fuel Cost'], y_gp_PV_1, c='b', label='PV with GPR with two SQ kernels')
#ax5=plt.plot(data_2['Fuel Cost'], y_gp_PV_2, c='b', label='PV with GPR with varaiable fuel cost')

#ax1.fill_between(data_2['Fuel Cost'], y_gp_NPC[:, 0]/1000 - std_NPC[:]/1000, 
#                y_gp_NPC[:, 0]/1000 + std_NPC[:]/1000, color='darkorange',
#                 alpha=0.2)
pylab.ylim([0,120])
GPR_PV_line = mlines.Line2D([], [], color='r', label='PV capacity with GPR')
lm_PV_line = mlines.Line2D([], [], color='g', label='PV capacity with MVLR')

plt.legend(handles=[GPR_PV_line,lm_PV_line,(ax3_PV)])


#%%

name = 'Fuel Cost'
data_100 = pd.read_excel('Databases/Database_100.xls')
data_100 = data_100.sort_values(name, ascending=True)
data_300 = pd.read_excel('Databases/Database_300.xls')
data_300 = data_300.sort_values(name, ascending=True)
data_500 = pd.read_excel('Databases/Database_500.xls')
data_500 = data_500.sort_values(name, ascending=True)

X_100 = pd.DataFrame()
X_100['Renewable Invesment Cost'] = data_100['Renewable Unitary Invesment Cost']   
X_100['Battery Unitary Invesment Cost'] = data_100['Battery Unitary Invesment Cost']
X_100['Deep of Discharge'] = data_100['Deep of Discharge']
X_100['Battery Cycles'] = data_100['Battery Cycles']
X_100['GenSet Unitary Invesment Cost'] = data_100['GenSet Unitary Invesment Cost']
X_100['Generator Efficiency'] = data_100['Generator Efficiency']
X_100['Low Heating Value'] = data_100['Low Heating Value']
X_100['Fuel Cost'] = data_100['Fuel Cost']
X_100['HouseHolds'] = data_100['HouseHolds']
X_100['Renewable Energy Unit Total'] = data_100['Renewable Energy Unit Total']

y_gp_PV_100, std_PV_100 = gp_PV.predict(X_100, return_std=True)


X_200 = pd.DataFrame()

X_200['Renewable Invesment Cost'] = data_100['Renewable Unitary Invesment Cost']   
X_200['Battery Unitary Invesment Cost'] = data_100['Battery Unitary Invesment Cost']
X_200['Deep of Discharge'] = data_100['Deep of Discharge']
X_200['Battery Cycles'] = data_100['Battery Cycles']
X_200['GenSet Unitary Invesment Cost'] = data_100['GenSet Unitary Invesment Cost']
X_200['Generator Efficiency'] = data_100['Generator Efficiency']
X_200['Low Heating Value'] = data_100['Low Heating Value']
X_200['Fuel Cost'] = data_100['Fuel Cost']
X_200['HouseHolds'] = 200
X_200['Renewable Energy Unit Total'] = data_100['Renewable Energy Unit Total']

y_gp_PV_200, std_PV_200 = gp_PV.predict(X_200, return_std=True)

X_300 = pd.DataFrame()
X_300['Renewable Invesment Cost'] = data_300['Renewable Unitary Invesment Cost']   
X_300['Battery Unitary Invesment Cost'] = data_300['Battery Unitary Invesment Cost']
X_300['Deep of Discharge'] = data_300['Deep of Discharge']
X_300['Battery Cycles'] = data_300['Battery Cycles']
X_300['GenSet Unitary Invesment Cost'] = data_300['GenSet Unitary Invesment Cost']
X_300['Generator Efficiency'] = data_300['Generator Efficiency']
X_300['Low Heating Value'] = data_300['Low Heating Value']
X_300['Fuel Cost'] = data_300['Fuel Cost']
X_300['HouseHolds'] = data_300['HouseHolds']
X_300['Renewable Energy Unit Total'] = data_300['Renewable Energy Unit Total']

y_gp_PV_300, std_PV_300 = gp_PV.predict(X_300, return_std=True)

X_400 = pd.DataFrame()

X_400['Renewable Invesment Cost'] = data_100['Renewable Unitary Invesment Cost']   
X_400['Battery Unitary Invesment Cost'] = data_100['Battery Unitary Invesment Cost']
X_400['Deep of Discharge'] = data_100['Deep of Discharge']
X_400['Battery Cycles'] = data_100['Battery Cycles']
X_400['GenSet Unitary Invesment Cost'] = data_100['GenSet Unitary Invesment Cost']
X_400['Generator Efficiency'] = data_100['Generator Efficiency']
X_400['Low Heating Value'] = data_100['Low Heating Value']
X_400['Fuel Cost'] = data_100['Fuel Cost']
X_400['HouseHolds'] = 400
X_400['Renewable Energy Unit Total'] = data_100['Renewable Energy Unit Total']

y_gp_PV_400, std_PV_400 = gp_PV.predict(X_400, return_std=True)

X_500 = pd.DataFrame()
X_500['Renewable Invesment Cost'] = data_500['Renewable Unitary Invesment Cost']   
X_500['Battery Unitary Invesment Cost'] = data_500['Battery Unitary Invesment Cost']
X_500['Deep of Discharge'] = data_500['Deep of Discharge']
X_500['Battery Cycles'] = data_500['Battery Cycles']
X_500['GenSet Unitary Invesment Cost'] = data_500['GenSet Unitary Invesment Cost']
X_500['Generator Efficiency'] = data_500['Generator Efficiency']
X_500['Low Heating Value'] = data_500['Low Heating Value']
X_500['Fuel Cost'] = data_500['Fuel Cost']
X_500['HouseHolds'] = data_500['HouseHolds']
X_500['Renewable Energy Unit Total'] = data_500['Renewable Energy Unit Total']

y_gp_PV_500, std_PV_500 = gp_PV.predict(X_500, return_std=True)


fig=plt.figure(figsize=size)

mpl.rcParams['xtick.labelsize'] = tick_size 
mpl.rcParams['ytick.labelsize'] = tick_size 

ax1_fix = plt.scatter(data_100['Fuel Cost'], data_100['Renewable Capacity'], c='g', marker='o')
ax1_fix = plt.plot(data_100['Fuel Cost'], y_gp_PV_100, c='g')
ax2_fix = plt.scatter(data_300['Fuel Cost'], data_300['Renewable Capacity'], c='r', marker='o')
ax2_fix = plt.plot(data_300['Fuel Cost'], y_gp_PV_300, c='r')
ax3_fix = plt.scatter(data_500['Fuel Cost'], data_500['Renewable Capacity'], c='b', marker='o')
ax3_fix = plt.plot(data_500['Fuel Cost'], y_gp_PV_500, c='b')
ax1_fix = plt.plot(data_100['Fuel Cost'], y_gp_PV_200, c='y', ls='--')
ax1_fix = plt.plot(data_100['Fuel Cost'], y_gp_PV_400, c='y', ls='--')


#%%

fig = plt.figure(figsize=(40,30))
size = [40,40]
label_size = 35
tick_size = 35 
fontsize = '30'
s = 100
title_size = 70
pad = 30

mpl.rcParams['xtick.labelsize'] = tick_size 
mpl.rcParams['ytick.labelsize'] = tick_size 

ax1 = fig.add_subplot(221)

# NPC plot
ax1.plot(data_1['Fuel Cost'], y_gp_NPC/1000, c='r', label='NPC with GPR')
ax1.plot(data_1['Fuel Cost'], y_lm_NPC/1000, c='g', label='NPC with MVLR')
ax1.scatter(data_1['Fuel Cost'], data_1['NPC']/1000, c='y', marker='o', label='Computed NPC',s=s)
ax1.set_ylim([100,650])
ax1.set_xlim([0.1,2])
ax1.set_xlabel('Fuel Cost (USD/l)', size=label_size)
ax1.set_ylabel('NPC (thousand USD)', size=label_size)
ax1.set_title('NPC', size=title_size,pad=pad)
plt.legend(handles=[GPR_NPC_line,lm_NPC_line,(ax3_NPC)],fontsize=fontsize)

# LCOE plot
ax2 = fig.add_subplot(222)
ax2.plot(data_1['Fuel Cost'], y_gp_lcoe, c='r', label='LCOE with GPR')
ax2.plot(data_1['Fuel Cost'], y_lm_lcoe, c='g', label='LCOE with MVLR')
ax2.scatter(data_1['Fuel Cost'], data_1['LCOE'], c='y', marker='o', label='LCOE Computed', s=s)
ax2.set_ylim([0.1,0.6])
ax2.set_xlabel('Fuel Cost (USD/l)', size=label_size)
ax2.set_ylabel('LCOE (USD/kWh)', size=label_size)
ax2.set_title('LCOE', size=title_size,pad=pad)
plt.legend(handles=[GPR_LCOE_line,lm_LCOE_line,(ax3_LCOE)],fontsize=fontsize)

# PV plot

ax3 = fig.add_subplot(223)
ax3.plot(data_1['Fuel Cost'], y_gp_PV, c='r', label='PV with GPR')
ax3.plot(data_1['Fuel Cost'], y_lm_PV, c='g', label='PV with MVLR')
ax3.scatter(data_1['Fuel Cost'], data_1['Renewable Capacity'], c='y', marker='o', label='Computed PV Capacity', s=s)
ax3.set_ylim([0,100])
ax3.set_xlabel('Fuel Cost (USD/l)', size=label_size)
ax3.set_ylabel('PV (kW)', size=label_size)
ax3.set_title('PV Installed Capacity', size=title_size,pad=pad)
plt.legend(handles=[GPR_PV_line,lm_PV_line,(ax3_PV)],fontsize=fontsize)

# PV 2 plot

ax4 = fig.add_subplot(224)
ax4.plot(data_100['Fuel Cost'], y_gp_PV_100, c='g', label= '100 Households Predicted')
ax4.plot(data_100['Fuel Cost'], y_gp_PV_200, c='y', ls='--', label= '200 Households Predicted')
ax4.scatter(data_100['Fuel Cost'], data_100['Renewable Capacity'], c='g', marker='o', label= '100 Households Calculated', s=s)
ax4.plot(data_300['Fuel Cost'], y_gp_PV_300, c='r', label= '300 Households Predicted')
ax4.scatter(data_300['Fuel Cost'], data_300['Renewable Capacity'], c='r', marker='o', label= '300 Households Calculated', s=s)
ax4.plot(data_100['Fuel Cost'], y_gp_PV_400, c='c', ls='--', label= '400 Households Predicted')
ax4.plot(data_500['Fuel Cost'], y_gp_PV_500, c='b', label= '500 Households Predicted')
ax4.scatter(data_500['Fuel Cost'], data_500['Renewable Capacity'], c='b', marker='o', label= '500 Households Calculated', s=s)
ax4.set_xlim([0.1,2])
ax4.set_ylim([0,175])
ax4.set_xlabel('Fuel Cost (USD/l)', size=label_size)
ax4.set_ylabel('PV Capacity (kWh)', size=label_size)
ax4.set_title('PV Installed Capacity Households', size=title_size,pad=pad)
ax4.legend(fontsize=fontsize)

plt.subplots_adjust(hspace= 0.3)

plt.savefig('Plots/Variable_Fuel_Price.png')




