# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 15:02:51 2021

@author: Dell
"""

import matplotlib.lines as mlines
import matplotlib.markers as markers
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import numpy as np
from sympy import symbols, Eq, solve, Symbol, nsolve
#%%
ll = ['00', '005', '01', '015', '02', '025', '03', '035', '04', '045', '05',
      '1', '2', '3' ,'4', '5' , '6', '7', '8', '9']



data = pd.read_csv('database.csv')
    
#%%
df = pd.DataFrame()

df['LLP'] = data['LLP']/100
df['LCOE 2'] = data['LCOE 2']

# Adding last point
# df.loc[20,'LLP'] = 100
# df.loc[20,'LCOE 2'] = 0

#%%

# Curva pareto front

df.index = range(len(df))


def func(x, a,  b, c, d):
    return  (a/(x+d)**b) + c 

xdata = df['LLP']
ydata=  df['LCOE 2']
popt, pcov = curve_fit(func, xdata, ydata, maxfev=50000 
#                       ,p0 = [2], bounds =[1,3]
                       )


ydata_2 = func( xdata, popt[0]
               ,popt[1]
               ,popt[2]
               ,popt[3]
               )


r_2 = r2_score(ydata, ydata_2)
r_2 = round(r_2, 2)
print(r_2)

#%%

# Secant


slop1 = (df['LCOE 2'][0] -df['LCOE 2'][19])/(df['LLP'][0]- df['LLP'][19])
interceptor1 = df['LCOE 2'][0]

def func1(x,slop1, interceptor1):
    

        
    return slop1*x + interceptor1

xsecant = pd.DataFrame([xdata[0],xdata[19]])
ysecant = func1(xsecant,slop1, interceptor1)



#%%

# iteration process

iteration_range = np.arange(xdata[0], xdata[19], 0.001) 
iteration_range = np.round(iteration_range,3)



slop2 = -1/slop1

r = []

Secant_paralel_intersection = pd.DataFrame()

for i in iteration_range:

    # calculating comun point secant and paralel i
    y_secant = slop1*i + interceptor1 
    
    # remplacing values
    interceptor2 = interceptor1   + (slop1 - slop2)*i 
    Secant_paralel_intersection.loc[i,'interceptor2'] = interceptor2
    
    Secant_paralel_intersection.loc[i,'x'] = i
    Secant_paralel_intersection.loc[i,'y'] = slop2*i + interceptor2

    
    x = Symbol('x')
    y = Symbol('y')
    eq1 = slop2*x+ interceptor2 - y #defining linear equation for the parallel  line to the secnt
    eq2 =  (popt[0]/(x+popt[3])**popt[1]) + popt[2] - y # LCOE vs LLP equation
    sol1 = nsolve((eq1, eq2), (x, y), (0, 1)) # solving the equation
    
    r.append(sol1)
 
r = pd.DataFrame(r)
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
r.index=Secant_paralel_intersection.index
r['interceptor2'] =  Secant_paralel_intersection['interceptor2']
r['secant_paralel_intersection_x'] = Secant_paralel_intersection['x'] 
r['secant_paralel_intersection_Y'] = Secant_paralel_intersection['y']

#%%

# Comparing solution with values of the found 


test_solution = pd.DataFrame()

test_solution['solution_x'] = r['x1']
test_solution['solution_y'] = r['y1']

test_solution['curve_y'] =  func(test_solution['solution_x'], popt[0], popt[1], 
                                   popt[2], popt[3])

test_solution['perpendicular_y'] = slop2*test_solution['solution_x']  + r['interceptor2'] 


test_solution['solution_curve_y'] = test_solution['solution_y'] - test_solution['curve_y'] 
test_solution['solution_perpendicular_y'] = test_solution['solution_y'] - test_solution['perpendicular_y']

#print(test_solution.sum())

#%%

# Critical point calculation

# points in the secant 

r['d']=((r['secant_paralel_intersection_x']-r['x1'])**2
        +(r['secant_paralel_intersection_Y']-r['y1'])**2)**0.5

knee_point = r['d'].idxmax() 

y_kee = r[ 'y1'][knee_point]
x_kee = r[ 'x1'][knee_point] 

print('Lost load probability of the knee point is ' + str(round(x_kee*100,1)) + ' % with an LCOE of ' + 
      str(round(y_kee,2)) + ' USD/kWh.')
#%%

# test of results

iteration_range_2 = np.arange(xdata[0], xdata[19], 0.005) 
iteration_range_2 = np.round(iteration_range_2,3)

s = 200

size = [20,20]
fig=plt.figure(figsize=size)
ax=fig.add_subplot(111, label="1")


handle1 = ax.scatter(xdata*100, ydata, c='b', s=s)
handle2 = ax.plot(r['x1']*100, r['y1'], c='g')
handle3 = ax.plot(xsecant*100, ysecant, c='r')
handle4 = ax.scatter([x_kee*100],[y_kee], c='r', s=s)

x_knee_plot = pd.Series([0, 0.8])
y_knee_plot = [slop2*x_knee_plot[0] + r['interceptor2'][knee_point],
               slop2*x_knee_plot[1] + r['interceptor2'][knee_point]] 

handle5 = ax.plot(x_knee_plot*100, 
                y_knee_plot,
               c= 'k', alpha=1)

for i in iteration_range_2:
    
    
    x_1 = [r['x1'][i]*100, r['secant_paralel_intersection_x'][i]*100]    
    y_1 = [r['y1'][i], r['secant_paralel_intersection_Y'][i]]   
    handle6 = ax.plot(x_1, y_1,c= 'y',alpha=0.3)

ax.set_xlabel("LLP (%)",size=30)
ax.set_ylabel("kWh/USD",size=30)        
#ax.set_xlim(0, 100)
tick_size = 25   
#mpl.rcParams['xtick.labelsize'] = tick_size     
ax.tick_params(axis='x', which='major', labelsize = tick_size )
ax.tick_params(axis='y', which='major', labelsize = tick_size )    

handle1 = mlines.Line2D([], [], color='b', label='Optimization results', 
                        marker = 'o', linestyle='None', markersize=15)
handle2 = mlines.Line2D([], [], color='g', label='Regression curve')
handle3 = mlines.Line2D([], [], color='r', label='Secant')
handle4 = mlines.Line2D([], [], color='k', label='Maximun distance')
handle5 = mlines.Line2D([], [], color='r', label='Parallel lines',c= 'y',alpha=1 )
handle6 = mlines.Line2D([], [], color='r', label='Knee point', marker = 'o', 
                        linestyle='None', markersize=15)


plt.legend(handles=[handle1, handle2, handle3, handle4, handle5, handle6], 
          bbox_to_anchor=(1.05, -0.05), fontsize = 30, frameon=False,  ncol=3)        

       
plt.savefig('Knee_Point.png')

