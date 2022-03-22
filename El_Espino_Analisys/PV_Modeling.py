#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data analysis of the PV data from El Espino

@author: sylvain
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import matplotlib.lines as mlines

def plot3D(x,y,z,type='scatter',title='Title',x_label='X',y_label='Y',z_label='Z',marker='+'):
    '''
    Function that generates 3D scatter plot of z vs x,y

    Parameters
    ----------
    x : 1d numpy array
    y : 1d numpy array
    z : 1d numpy array
    type: 'scatter' or 'surface'

    Returns
    -------
    Plot handles

    '''

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(30,-110)
    if type=='scatter':
        ax.scatter(x, y, z, marker=marker)
    else:
        ax.plot_surface(x,y,z)
    ax.set_xlabel(x_label)
    ax.xaxis.label.set_fontsize(16)
    ax.set_ylabel(y_label)
    ax.yaxis.label.set_fontsize(16)
    ax.set_zlabel(z_label)
    ax.zaxis.label.set_fontsize(16)
    plt.title(title,fontsize=16)

    plt.show()
    
    return ax



#%%  load data

data_raw = pd.read_csv('Data/Data_Espino_Thesis_Fill_2.csv', header=0,index_col=0)
index = pd.date_range(start='2016-01-01 00:00:00', periods=166464, freq=('5min'))
data_raw.index = index
Area = 1.65*0.99*240 # 1.61*0.946*240 # 1.65*0.99*240

data = data_raw.loc[data_raw['PV Power']>0]
data.loc[:,'Efficiency'] = (data_raw['PV Power']*1000)/(data_raw['Solar Irradiation']*Area)

data.loc[:,'Hour'] = data.index.hour

# filtering
data = data[data.Efficiency<0.161]
data = data[data.SOC<85]
data = data[data['Solar Irradiation']>250]
#data = data.sample(n=2000)

data_rel = data.loc[:,('Efficiency','SOC','PV Temperature 2','Hour')]

# basic data analysis
df = data.loc[:,('Efficiency','SOC','PV Temperature 2','Hour','Demand','Ambient temperature','Solar Irradiation')]
covariance_matrix = df.cov()

df['Efficiency'] = round(df['Efficiency'],3)
ax = pd.plotting.scatter_matrix(df, alpha=0.2, figsize=[20,15])

labels = ax[0,0].get_yticklabels()

new_labels = []
for i in labels:
    i = round(float(i.get_text()),2)
    new_labels.append(i)
    
    
ax[0,0].set_yticklabels(new_labels)


#ax[0,0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

plt.savefig('Plots/scatter_plot_matrices.png')

# #%%  PCA
# n_components = 3

# #normalizing: 
# from sklearn.preprocessing import StandardScaler
# features = df.loc[:, :].values
# features_scaled = StandardScaler().fit_transform(features) # normalizing the features
# df_normalized = pd.DataFrame(data = features_scaled,index = df.index, columns = df.columns)
# #df_normalized=(df - df.mean()) / df.std()

# pca = PCA(n_components=n_components)
# pca.fit(df_normalized)

# # Reformat and view results
# cols= ['PC%s' % _ for _ in range(n_components)]
# pca_analysis = pd.DataFrame(pca.components_.T,columns=cols,index=df.columns)
# print(pca_analysis)

# #explained variance:
# print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))
# plt.figure(0)
# plt.plot(pca.explained_variance_ratio_)
# plt.ylabel('Explained Variance')
# plt.xlabel('Components')
# plt.show()

# # putting the principal components in a datafrmae:
# pca_df = pd.DataFrame(data = pca.fit_transform(data.values)
#              , columns = cols)

#%%  3D plot

z= data['Efficiency']

x = data['Solar Irradiation']
x = data['SOC']
#x = pca_df['PC0']

#y = data['Hour']
y = data['SOC']
y = data['Ambient temperature']
#y = data['PV Temperature 2']
#y = pca_df['PC1']

plot3D(x, y, z,x_label='SOC [-]',y_label='Ambient Temperature [°C]',z_label='Efficiency')

#%% Air mass calculation
import pvlib
import math


tz = 	'America/La_Paz'
Hourly_Data = pd.DataFrame()

lat, lon = -19.2, -63.3

# Create location object to store lat, lon, timezone
site_location = pvlib.location.Location(lat, lon, tz=tz)

solar_position = site_location.get_solarposition(times=data.index)
    # Use the get_total_irradiance function to transpose the GHI to POA

hour_angle = pvlib.solarposition.hour_angle(data.index, lon, solar_position.equation_of_time)/360 * 2 * math.pi
declination = pvlib.solarposition.declination_cooper69(data.index.dayofyear)
zenith = pvlib.solarposition.solar_zenith_analytical(lat, hour_angle, declination)
data['zenith'] = zenith/(2*math.pi) * 360
data['zenith2'] = solar_position['zenith']

data['AM_rel'] = pvlib.atmosphere.get_relative_airmass(90 - solar_position['zenith'])


#%% fitting data 

from scipy.optimize import curve_fit

def PV_efficiency(inputs,p,q,m,r,s,u):
    G_rel = inputs[:,0]
    AM_rel = inputs[:,1]
    T_rel = inputs[:,2]
    eta = p * (q * G_rel + G_rel**m) * (1 + r * T_rel + s * AM_rel + AM_rel**u)
    return eta

data['T_rel'] = T_rel = (data['Ambient temperature'] - 25)/(273+25)
data['G_rel'] = data['Solar Irradiation']/1000
xdata = data.loc[:,('G_rel','AM_rel','T_rel')].values
ydata = data['Efficiency'].values

print('Total data points: ' + str(len(ydata)))

p0=[23.62, -0.3,   0.1912,   -0.093, -1, 1]
test = PV_efficiency(xdata,*p0)
popt, pcov = curve_fit(PV_efficiency, xdata, ydata, p0=p0)

print('The values for p, q, r, m, s, u are:')
print(np.round(popt,4))
    
coef = list(popt)

data['eta_pred'] = PV_efficiency(xdata,*coef)


#%% plotting regression
#import numpy as np

xx = xdata.copy()
xx[:,1] = 1.5
xx[:,2] = 0
y = PV_efficiency(xx,*coef)
plt.figure(1)
plt.scatter(data['Solar Irradiation'],data['Efficiency'])
plt.scatter(data['Solar Irradiation'],y,color='r')
plt.show()

#%% 3D plotting 
from pylab import colormaps
cmaps = colormaps()

xx = xdata.copy()
xx[:,1] = 1.5

G_range = np.arange(10,1000,50)
T_range = np.arange(0,40,2)

X,Y = np.meshgrid(G_range,T_range)

xx = np.array([X.flatten()/1000,np.ones(len(X.flatten())),(Y.flatten() - 25)/(273+25)]).transpose()

eta = np.reshape(PV_efficiency(xx,*coef),np.shape(X))

# Plotting the required battery size as a function of SSR and SCR:
fig = plt.figure(2,figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.view_init(15,290)
ax.plot_surface(X,Y,eta,cmap=cmaps[32],rstride=1, cstride=1)
plt.title('Predicted Efficiency')
ax.set_xlabel('G [W]')
ax.set_ylabel('T [°C]')
ax.set_zlabel('Efficiency [-]')


plt.savefig('Plots/Predicted_Efficiency_3D.png')


#%%

X = pd.DataFrame()

X['G_rel'] = data_raw['Solar Irradiation']/1000

solar_position2 = site_location.get_solarposition(times=data_raw.index)
X['AM_rel'] = pvlib.atmosphere.get_relative_airmass(90 - solar_position2['zenith'])
X['T_rel'] = (data_raw['Ambient temperature'] - 25)/(273+25)

XX = np.array(X)
efficiency = PV_efficiency(XX,*coef)

data_raw['Optimal Efficiency'] = efficiency

data_raw['Optimal PV Power'] = (data_raw['Optimal Efficiency']*data_raw['Solar Irradiation']*Area)/1000
data_raw['Optimal PV Power'] = np.where(data_raw['Optimal PV Power'] >51, 51, 
                                    data_raw['Optimal PV Power'])

#%%

# Calculations

start = '2016-01-01 00:00:00'
end =   '2017-07-31 23:55:00'

Energy_Real     = round(data_raw['PV Power'][start:end].sum()/(12*1000),1)
Energy_Optimal  = round(data_raw['Optimal PV Power'][start:end].sum()/(12*1000),1)
Lost_Percentage =  1 - Energy_Real/Energy_Optimal 
Lost_Percentage = round(Lost_Percentage*100,1)

print('Total energy with curtailment is ' + str(Energy_Real) + ' MWh')
print('Total energy without curtailment is ' + str(Energy_Optimal) + ' MWh')
print('Extra energy in optimal conditions ' + str(Lost_Percentage) + ' %')

Optimal_Power_Espino = pd.DataFrame()
Optimal_Power_Espino['Optimal PV Power'] = data_raw['Optimal PV Power']


Optimal_Power_Espino.to_csv('Results/Renewable_Energy_Optimal_Espino.csv')


#%%

data_raw['year'] = data_raw.index.year
data_raw['day']  = data_raw.index.dayofyear
data_raw['hour'] = data_raw.index.hour



#%%

daily_plot = data_raw.groupby(['hour']).mean()

size = [25,20]
plt.figure(figsize=size)


ax  = daily_plot['Optimal PV Power'].plot(style = '--',linewidth=5,  color='blue')
#ax  = PV_Energy_1['PV Power Gutierrez'].plot(style = '--',linewidth=5,  color='red')  
ax  = daily_plot['PV Power'].plot(style = ':',linewidth=5, color='green')
ax1 = daily_plot['Solar Irradiation'].plot(c='y', secondary_y=True,linewidth=5)

Espino_regression = mlines.Line2D([], [], color='blue',
                                  label='PV Power without curtailment', 
                                  linestyle='--',linewidth=5)

Espino_measurement = mlines.Line2D([], [], color='green',
                                  label='PV power with curtailment', 
                                  linestyle=':',linewidth=5)


Radiation = mlines.Line2D([], [], color='yellow',
                                  label='Solar irradiation', 
                                  linestyle='-',linewidth=5)

ax.tick_params(axis='x', which='major', labelsize=50)
ax.tick_params(axis='y', which='major', labelsize=50)
ax1.tick_params(axis='y', which='major', labelsize=50)

ax.set_xlabel('hours', labelpad=20, size=60 )
ax.set_ylabel('Power (kW)', labelpad=20, size=60)

ax1.set_ylabel('Irradiation (W/m$^{2}$)', labelpad=20, size=60)


##plt.legend(bbox_to_anchor=(1, -0.1),fontsize = 12,frameon=False, ncol=2)
plt.legend(handles=[Espino_regression, Espino_measurement, Radiation],
           bbox_to_anchor=(0.95,-0.10),
           frameon=False, ncol=2
           ,fontsize = 40)
plt.tight_layout()
plt.show()

plt.savefig('Plots/Daily_PV_Power.png')



#%%

# Hourly data transformation


start = '2016-03-21 00:00:00' # '2017-01-01 00:00:00' '2016-01-01 00:00:00' 
end   = '2017-03-20 23:55:00' # '2017-07-31 23:55:00' '2016-12-31 23:55:00' 
data_hourly = data_raw[start:end] 
data_hourly = data_hourly.groupby(['year','day', 'hour']).mean()

data_hourly_describe = data_hourly.describe()


#%%
# Second PV radiation
Data_2 = pd.read_csv('Results/Gutierrez_Data.csv', index_col=0)            


index2 = pd.date_range(start='2013-01-01 00:00:00', periods=8760, 
                                    freq=('H'))

start = index2.get_loc('2013-03-21 00:00:00')

Gut_Data_1  = Data_2[start:]
    
end = index2.get_loc('2013-03-21 00:00:00')

Gut_Data_2  = Data_2[:end]

Gut_Data =  Gut_Data_1.append(Gut_Data_2) 

index_3 = pd.date_range(start='2016-03-21 00:00:00', periods=8760, 
                                   freq=('H'))

Gut_Data.index = index_3

#### Fix incoherent data
for i in Gut_Data.index:
    a = i.hour
    if any([a==0,a==1,a==2,a==3,a==4,a==5,a==20,a==21,a==22,a==23]):
        
        if Gut_Data.loc[i,'Radiation tilt isotropic'] > 0:
            #print(i)
            Gut_Data.loc[i,'Radiation tilt isotropic'] = 0


Gut_Data_describe = Gut_Data.describe() 


X1 = pd.DataFrame()

X1['G_rel'] = Gut_Data['Radiation tilt isotropic']/1000

solar_position3 = site_location.get_solarposition(times=Gut_Data.index)
X1['AM_rel'] = pvlib.atmosphere.get_relative_airmass(90 - solar_position3['zenith'])
X1['T_rel'] =  (Gut_Data['Temperature'] - 25)/(273+25)

XX1 = np.array(X1)
efficiency1 = PV_efficiency(XX1,*coef)


Gut_Data['Optimal Efficiency'] = efficiency1
Gut_Data['Optimal PV Power'] = (Gut_Data['Optimal Efficiency']*Gut_Data['Radiation tilt isotropic']*Area)/1000



#%%
data_hourly.index = index_3
PV_Energy = pd.DataFrame(index=index_3)

PV_Energy['PV Power Without Curtailment'] = data_hourly['Optimal PV Power']
PV_Energy['PV Power Gutierrez']           = Gut_Data['Optimal PV Power']
PV_Energy['PV Power With Curtailment']    = data_hourly['PV Power']
PV_Energy['Irradiation Gutierrez']        = Gut_Data['Radiation tilt isotropic']
PV_Energy['Irradiation Espino']           = data_hourly['Solar Irradiation']
PV_Energy['hour'] = PV_Energy.index.hour 

    
PV_Energy_1 = PV_Energy.groupby(['hour']).mean()   


Data_Optimization = pd.DataFrame()
Data_Optimization['PV Power Without Curtailment'] = list((PV_Energy['PV Power Without Curtailment']/240)*1000)
Data_Optimization['PV Power Gutierrez'] = list((PV_Energy['PV Power Gutierrez']/240)*1000)



Data_Optimization.index = range(1,8761)
Data_Optimization.columns = [1,2]

Data_Expected_Solar = pd.DataFrame()
Data_Expected_Solar[1] = (Data_Optimization[1]+Data_Optimization[2])/2
Data_Expected_Solar.to_excel('Results/Renewable_Energy_Expected.xls')


Data_Optimization[3] = Data_Optimization[1]
Data_Optimization[4] = Data_Optimization[2]
Data_Optimization[5] = Data_Optimization[1]
Data_Optimization[6] = Data_Optimization[2]
Data_Optimization[7] = Data_Optimization[1]
Data_Optimization[8] = Data_Optimization[2]
Data_Optimization[9] = Data_Optimization[1]
Data_Optimization[10] = Data_Optimization[2]

Data_Optimization.to_excel('Results/Renewable_Energy_Multy_Scenarios.xls')


# data_hourly_2


#%%
#### paper figure
size = [20,15]
plt.figure(figsize=size)


ax  = PV_Energy_1['PV Power Without Curtailment'].plot(style = '--',linewidth=5,  color='blue')
ax  = PV_Energy_1['PV Power Gutierrez'].plot(style = '--',linewidth=5,  color='red')  
ax  = PV_Energy_1['PV Power With Curtailment'].plot(style = ':',linewidth=5, color='green')
ax1 = PV_Energy_1['Irradiation Espino'].plot(c='y', secondary_y=True,linewidth=5)

Espino_regression = mlines.Line2D([], [], color='blue',
                                  label='Espino regression', 
                                  linestyle='--',linewidth=5)

Espino_measurement = mlines.Line2D([], [], color='green',
                                  label='Espino measurement', 
                                  linestyle=':',linewidth=5)


Radiation = mlines.Line2D([], [], color='yellow',
                                  label='Radiation Espino', 
                                  linestyle='-',linewidth=5)

Gutierrez = mlines.Line2D([], [], color='yellow',
                                  label='Radiation Espino', 
                                  linestyle='-',linewidth=5)

ax.tick_params(axis='x', which='major', labelsize=30)
ax.tick_params(axis='y', which='major', labelsize=30)
ax1.tick_params(axis='y', which='major', labelsize=30)
ax.set_xlabel('hours', labelpad=20, size=40 )
ax.set_ylabel('Power (kW)', labelpad=20, size=40)
ax1.set_ylabel('Irradiation (W/m$^{2}$)', labelpad=20, size=40)


##plt.legend(bbox_to_anchor=(1, -0.1),fontsize = 12,frameon=False, ncol=2)
plt.legend(handles=[Espino_regression, Espino_measurement, Radiation, Gutierrez],
           bbox_to_anchor=(1.1, -0.1),frameon=False, ncol=3
           ,fontsize = 30)


#%%

# Demand and renewable energy for the dispatch model

start = '2017-01-01 00:00:00' # '2017-01-01 00:00:00' '2016-01-01 00:00:00' 
end   = '2017-06-30 23:55:00' # '2017-07-31 23:55:00' '2016-12-31 23:55:00' 

data_hourly_2 = data_raw[start:end] 
data_hourly_2 = data_hourly_2.groupby(['year','day', 'hour']).mean()


Demand_Dispatch = pd.DataFrame()
Demand_Dispatch[1] = data_hourly_2['Demand']*1000
Demand_Dispatch.index = range(1,len(Demand_Dispatch)+1)
Demand_Dispatch.to_excel('Results/Demand_Dispatch.xls')

PV_Power = pd.DataFrame()
PV_Power[1] = data_hourly_2['Optimal PV Power']*1000
PV_Power.index = range(1,len(PV_Power)+1)
PV_Power.to_excel('Results/Renewable_Energy_Dispatch.xls')


SOC_Initial = data_hourly['SOC']['2016-12-31 23:00:00']


# SOC_Initial
# Out[8]: 64.61805555555556
