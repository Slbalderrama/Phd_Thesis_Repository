# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 15:02:51 2021

@author: Dell
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from sympy import symbols, Eq, solve, Symbol, nsolve
from numpy import ones,vstack
from numpy.linalg import lstsq
#%%
ll = ['00', '005', '01', '015', '02', '025', '03', '035', '04', '045', '05',
      '1', '2', '3' ,'4', '5' , '6', '7', '8', '9']



data = pd.DataFrame()


#%%
# laod results
data = pd.read_csv('database.csv')

#%%
df = pd.DataFrame()

df['LLP'] = data['LLP']/100
df['LCOE'] = data['LCOE']

# Adding last point
df.loc[20,'LLP'] = 1
df.loc[20,'LCOE'] = 0

#%%
df.index = range(21)


def func(x, a, b, c,d,e, f):
    return (a*x-b)/(c*x**e+d+x**f)
xdata = df['LLP']
ydata=df['LCOE']
popt, pcov = curve_fit(func, xdata, ydata, maxfev=50000)

#%% calculating r_square
residuals = ydata- func(xdata, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((ydata-np.mean(ydata))**2)
r_squared = 1 - (ss_res / ss_tot)
popt, pcov = curve_fit(func, xdata, ydata, bounds=(-1, [0, 0, 3, 2.1, 0.4, 0.5]))
residuals = ydata- func(xdata, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((ydata-np.mean(ydata))**2)
r_squared = 1 - (ss_res / ss_tot)

#%%

x_1 = df['LLP']
y_1 = df['LCOE']

# Defining variables of the problem
#a = Symbol('a')
j = Symbol('j')
x = Symbol('x')


points = [df.iloc[0],df.iloc[17]]
x_coords, y_coords = zip(*points)
A = vstack([x_coords,ones(len(x_coords))]).T
# Resuelve la ecuacion lineal
m, c = lstsq(A, y_coords)[0]


#%%
#Definning equations 

y1=m*x+c #defining linear equation
z1=np.array([m, c]) # liner equation parameters in a np array
p1= np.poly1d(z1)
m1=-1/m

f=(popt[0]*x-popt[1])/(popt[2]*x**popt[4]+popt[3]+x**popt[5])
eq3=Eq(f-j)

#%%
#Solucionador iterativo de sistema de ecuaciones no lineales


r=list()
for a in np.arange(-0.7,0.9,0.05):
    l1=m1*x+a #changing the value of the interceptor
    z2=np.array([m1, a])
    p2=np.poly1d(z2)
    eq1=Eq(l1-j)
    eq3=Eq(f-j)
    sol1 = nsolve((eq1, eq3), (x,j), (0.06, 0.55))  # solve equation for the range
    r.append([sol1]) # add solution to the list
r=pd.DataFrame(r)

# splitting the values x and y
r['sol'] = r[0].astype(str)
r[['x','y']] = r.sol.str.split(",",expand=True)
r[['g','g1','x1']] = r.x.str.split("[",expand=True)
del r['g']
del r['g1']
r[['x1','g1']] = r.x1.str.split("]",expand=True)
del r['g1']
r[['y1','g','g1']] = r.y.str.split("]",expand=True)
del r['g1']
del r['g']
r[['g','y2']] = r.y1.str.split("[",expand=True)
del r['g']
del r['y1']
del r['x']
del r['y']
del r[0]
del r['sol']
r = r.rename(columns={'y2': 'y1'})
r['x1'] = r['x1'].astype(float)
r['y1'] = r['y1'].astype(float)
r1=r

points = [df.iloc[0],df.iloc[20]]
x_coords, y_coords = zip(*points)
A = vstack([x_coords,ones(len(x_coords))]).T
m, c = lstsq(A, y_coords)[0]


#print("Line Solution is y = {m}x + {c}".format(m=m,c=c))
y1=m*x+c
z1=np.array([m, c])
p1= np.poly1d(z1)

#Solucionador iteritvo ecuaciones lineales

r=list()
for a in np.arange(-0.7,0.9,0.05):
    l1=m1*x+a
    z2=np.array([m1, a])
    p2=np.poly1d(z2)
    eq1=Eq(l1-j)
    sol = solve((l1-j, y1-j),(x, j))
    x1_1=float(sol[x])
    y1_1=float(sol[j])
    r.append([sol])
r=pd.DataFrame(r)
r['sol'] = r[0].astype(str)
r[['x','y']] = r.sol.str.split(",",expand=True)
r[['g','x1']] = r.x.str.split(":",expand=True)
del r['g']
r[['g1','y1']] = r.y.str.split(":",expand=True)
del r['g1']
r[['y1','g2']] = r.y1.str.split("}",expand=True)
del r['g2']
del r['sol']
del r[0]
del r['x']
del r['y']
r = r.rename(columns={'x1': 'x', 'y1': 'y'})
r['x'] = r['x'].astype(float)
r['y'] = r['y'].astype(float)

rt = pd.concat([r, r1], axis=1, join='inner')
rt['step']=np.arange(-0.7,0.9,0.05)
rt['d']=((rt['x']-rt['x1'])**2+(rt['y']-rt['y1'])**2)**0.5


a=rt['step'].iloc[rt['d'].idxmax()]
l1=m1*x+a
z2=np.array([m1, a])
p2=np.poly1d(z2)

BSAf=popt
BSAr2=r_squared
BSAx=rt['x1'].iloc[rt['d'].idxmax()]
BSAy=rt['y1'].iloc[rt['d'].idxmax()]


plt.figure(figsize=(10,6.7))
xp = np.linspace(0,1, 100)
# data
_ = plt.plot(x_1, y_1, '.',label='data', color='blue')
# fited data 
o= plt.plot(xp, func(xp,*popt), '--', label='fit', color='green')
# Secant 
o1=plt.plot(xp, p1(xp), '-', label='secant', color='red')
# Max distance
_=plt.plot(xp, p2(xp), '-', label='distance', color='black')

# 
#plt.plot(rt['x1'].iloc[rt['d'].idxmax()], rt['y1'].iloc[rt['d'].idxmax()], marker='o', markersize=3, color="green")
#plt.plot(x_1, y_1, '-')
# Critial point
plt.plot(BSAx,BSAy, marker='o', markersize=5, color="red", label='critical point')
#escala real


















plt.ylabel('LCOE [USD/KWh]')
plt.xlabel('LLP')
plt.axis('scaled')
plt.legend()
#plt.savefig('critical point1.png',dpi=600,bbox_inches="tight")
#plt.show()
plt.savefig('Breaking_Point.png')
plt.show()


#Results

print('R2=',r_squared)
print('parameters=',popt)
print('critical point=',BSAx)

optimization_results = data.describe() 
print(optimization_results)     
