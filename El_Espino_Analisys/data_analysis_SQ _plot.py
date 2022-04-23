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
    plt.savefig('Plots/Test.png')
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
data = data[data.SOC<100]
data = data[data['Solar Irradiation']>250]
data = data.sample(n=2000)


#%%  3D plot

z= data['Efficiency']

#x = data['Solar Irradiation']
x = data['SOC']
#x = pca_df['PC0']

#y = data['Hour']
#y = data['SOC']
y = data['Ambient temperature']
#y = data['PV Temperature 2']
#y = pca_df['PC1']

plot3D(x, y, z,x_label='SOC [-]',y_label='Ambient Temperature [°C]',z_label='Efficiency')

