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

data_raw = pd.read_csv('Data/Data_Espino_Thesis_Fill.csv', header=0,index_col=0)
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

pd.plotting.scatter_matrix(df, alpha=0.2)


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

p0=[23.62, -0.3,   0.1912,   -0.093, -1, 1]
test = PV_efficiency(xdata,*p0)
popt, pcov = curve_fit(PV_efficiency, xdata, ydata, p0=p0)
    
coef = list(popt)

data['eta_pred'] = PV_efficiency(xdata,*coef)


#%% plotting regression
import numpy as np

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





