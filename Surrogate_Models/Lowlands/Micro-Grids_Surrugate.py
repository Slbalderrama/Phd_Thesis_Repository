# -*- coding: utf-8 -*-

from pyomo.environ import  AbstractModel
from Results import Load_results1, Energy_Mix, Print_Results
from Model_Creation import Model_Creation
from Model_Resolution import Model_Resolution
from Initialize import Solar_Energy_Data
import pandas as pd
from pyDOE import lhs
from pyomo.opt import SolverFactory
import time
from joblib import dump, load

start = time.time()
Status = pd.DataFrame()
#%%

''' This script is used to create the data base for the machine learning Technique'''



model = AbstractModel() # define type of optimization problem
# Optimization model
# Type of problem formulation:
model.formulation = 'MILP'
model.Lost_Load_Probability =  0
model.Curtailment_Unitary_Cost = 0
Renewable_Penetration = 0
Battery_Independency = 0
type_generator = 'Fix' # Fix or Variable
solar_energy = 'Fix' # Fix or Variable
Model_Creation(model, Renewable_Penetration, Battery_Independency,type_generator)  
instance = Model_Resolution(model, Renewable_Penetration, Battery_Independency) 

#%%
# not use parameters
Battery_Independency   =  0    # number of days of battery independency  
Curtailment_Unitary_Cost =  0 # probando curtailment cost 0
#%%
# Renewable energy parameters
Renewable_Invesment_Cost = [1000, 2000]
Maintenance_Operation_Cost_Renewable = [0.02, 0.02]
#%%
# Battery parameters
Battery_Invesment_Cost  = [800, 222]
Maintenance_Operation_Cost_Battery = [0.02, 0.02]
Deep_of_Discharge = [0,0.5]
Battery_Cycles = [1000, 7000]

#%%
# Generator parameters 
Generator_Invesment_Cost = [1000,2000]
Generator_Efficiency  = [0.1, 0.4]
Low_Heating_Value = [7,11]
Fuel_Cost = [0.18,2]
Generator_Nominal_Capacity = 15
Maintenance_Operation_Cost_Generator = [0.02, 0.02]
#%%
# Other parameters
#Lost_Load_Probability  =  0    # Allowed a percentage of unmet demand in the system
#%%


Number_Scenarios = int(instance.Scenarios.extract_values()[None])
Number_Periods = int(instance.Periods.extract_values()[None])
Number_Renewable_Source = int(instance.Renewable_Source.extract_values()[None])
foo = 0
Data = pd.DataFrame()
Results = pd.DataFrame()
Renewable_Nominal_Capacity = instance.Renewable_Nominal_Capacity.extract_values()[1]
village = range(50, 570, 50) #range(50, 570, 50)

Nruns = 150

Data_Villages = pd.read_excel('Data_Base_Low_Lands.xls',index_col=0,Header=None)
# Villages_Already = pd.read_excel('status1.xls',index_col=0,Header=None)
# Data_Villages = Data_Villages.drop(list(Villages_Already['Index']))





for i in village:
    
    # 
    # Demand
    Village = 'village_' + str(i)
    Energy_Demand = pd.read_excel('Example/Demand.xls',sheet_name=Village
                                  ,index_col=0,Header=None)
    Energy_Demand = Energy_Demand/1000
    Energy_Demand = round(Energy_Demand,3)
    
    for s in range(1,Number_Scenarios+1):
        for t in range(1, Number_Periods+1):
            instance.Energy_Demand[s,t] = Energy_Demand.loc[t,s]
    lh = lhs(11, samples=Nruns)
    
    filename = 'latin/lh_' + str(i) +  '.joblib'
    dump(lh, filename) 
    
    max_energy = Energy_Demand.max()
    max_energy = max_energy[1]
    max_bound_PV = (max_energy*8)/0.25
    max_boumd_bat = max_energy*50
    
    instance.Renewable_Units[1].setub(max_bound_PV)
    instance.Battery_Nominal_Capacity.setub(max_boumd_bat)
 #133  
    for n in range(Nruns):
        print(i)
        print(n)
        start_1 =  time.time()
        location = Data_Villages.sample(n=1)
        foo = location.index[0]
        Data_Villages = Data_Villages.drop([foo])
        Solar_Data = Solar_Energy_Data(location,Number_Scenarios,solar_energy )
        Solar_Data = Solar_Data/1000
        Solar_Data = round(Solar_Data,3)
        for s in range(1,Number_Scenarios+1):
            for t in range(1, Number_Periods+1):
                instance.Renewable_Energy_Production[s,1,t] = Solar_Data.loc[t,s]
        name = str(i) + '_' + str(n)
        Status.loc[name, 'Index'] = foo
        Status.loc[name, 'X_deg'] = location['X_deg'][foo]
        Status.loc[name, 'Y_deg'] = location['Y_deg'][foo]
        # Renewable energy parameters
        
        Renewable_Invesment_Cost_1 = Renewable_Invesment_Cost[0] + lh[n,0]*(Renewable_Invesment_Cost[-1]-Renewable_Invesment_Cost[0])
        Renewable_Invesment_Cost_1 = round(Renewable_Invesment_Cost_1,0)
        instance.Renewable_Invesment_Cost[1] = round(Renewable_Invesment_Cost_1,0) 
        
        Maintenance_Operation_Cost_Renewable_1 = Maintenance_Operation_Cost_Renewable[0] + lh[n,1]*(Maintenance_Operation_Cost_Renewable[-1]
                                                                 -Maintenance_Operation_Cost_Renewable[0])  
        Maintenance_Operation_Cost_Renewable_1 = round(Maintenance_Operation_Cost_Renewable_1,2)
        instance.Maintenance_Operation_Cost_Renewable[1] = Maintenance_Operation_Cost_Renewable_1
        
        # Battery parameters
        Battery_Invesment_Cost_1 = Battery_Invesment_Cost[0] + lh[n,2]*(Battery_Invesment_Cost[-1] - Battery_Invesment_Cost[0])
        Battery_Invesment_Cost_1 = round(Battery_Invesment_Cost_1,0)
        instance.Battery_Invesment_Cost  = Battery_Invesment_Cost_1
        
        Deep_of_Discharge_1 =  Deep_of_Discharge[0] + lh[n,3]*(Deep_of_Discharge[-1]-Deep_of_Discharge[0])
        Deep_of_Discharge_1 = round(Deep_of_Discharge_1,2)
        instance.Deep_of_Discharge =  Deep_of_Discharge_1
        
        Battery_Cycles_1 = Battery_Cycles[0] + lh[n,4]*(Battery_Cycles[-1]-Battery_Cycles[0]) 
        Battery_Cycles_1 = round(Battery_Cycles_1,2)
        instance.Battery_Cycles =  Battery_Cycles_1
        
        Maintenance_Operation_Cost_Battery_1 = Maintenance_Operation_Cost_Battery[0] + lh[n,5]*(Maintenance_Operation_Cost_Battery[-1]
                                                                                -Maintenance_Operation_Cost_Battery[0])
        Maintenance_Operation_Cost_Battery_1 = round(Maintenance_Operation_Cost_Battery_1,2)
        instance.Maintenance_Operation_Cost_Battery =  Maintenance_Operation_Cost_Battery_1
        
        # Genset parameters
        Generator_Invesment_Cost_1 = Generator_Invesment_Cost[0] + lh[n,6]*(Generator_Invesment_Cost[-1] - Generator_Invesment_Cost[0])
        Generator_Invesment_Cost_1 = round(Generator_Invesment_Cost_1,0)
        instance.Generator_Invesment_Cost[1] = Generator_Invesment_Cost_1 
        
        Generator_Efficiency_1 = Generator_Efficiency[0] + lh[n,7]*(Generator_Efficiency[-1] - Generator_Efficiency[0])
        Generator_Efficiency_1 = round(Generator_Efficiency_1,2)
        instance.Generator_Efficiency[1]  =  Generator_Efficiency_1 
        
        Low_Heating_Value_1 = Low_Heating_Value[0] + lh[n,8]*(Low_Heating_Value[-1] - Low_Heating_Value[0])
        Low_Heating_Value_1 = round(Low_Heating_Value_1,2)
        instance.Low_Heating_Value[1] = Low_Heating_Value_1 
        
        Fuel_Cost_1 = Fuel_Cost[0] + lh[n,9]*(Fuel_Cost[-1] - Fuel_Cost[0])
        Fuel_Cost_1 = round(Fuel_Cost_1,1)
        instance.Fuel_Cost[1] =Fuel_Cost_1
        
        Maintenance_Operation_Cost_Generator_1 = Maintenance_Operation_Cost_Generator[0] + lh[n,10]*(Maintenance_Operation_Cost_Generator[-1]
                                                                  -Maintenance_Operation_Cost_Generator[0])
        Maintenance_Operation_Cost_Generator_1 =  round(Maintenance_Operation_Cost_Generator_1,2)
        instance.Maintenance_Operation_Cost_Generator[1] = Maintenance_Operation_Cost_Generator_1

        Marginal_Cost_Generator_1 = Fuel_Cost_1/(Low_Heating_Value_1*Generator_Efficiency_1)
        Marginal_Cost_Generator_1 = round(Marginal_Cost_Generator_1,3)
        instance.Marginal_Cost_Generator_1[1] = Marginal_Cost_Generator_1       
        
        if model.formulation == 'MILP': 
            if Number_Scenarios == 1: 
                foo = Energy_Demand.max()
                foo = foo[1]
                Generator_Nominal_Capacity_1 = round(foo*0.75, 0)
            else:
                foo = Energy_Demand.max()
                foo = foo.max()
                foo = foo[1]
                Generator_Nominal_Capacity_1 = round(foo*0.75, 0)
                
            instance.Generator_Nominal_Capacity[1] = Generator_Nominal_Capacity_1

            Cost_Increase_1 = instance.Cost_Increase.extract_values()[1]
            Start_Cost_Generator_1 = Marginal_Cost_Generator_1*Generator_Nominal_Capacity_1*Cost_Increase_1
            Start_Cost_Generator_1 = round(Start_Cost_Generator_1,3)
            instance.Start_Cost_Generator[1] = Start_Cost_Generator_1
            
            Marginal_Cost_Generator_2 = (Marginal_Cost_Generator_1*Generator_Nominal_Capacity_1 \
                                                -Start_Cost_Generator_1)/Generator_Nominal_Capacity_1    
            instance.Marginal_Cost_Generator[1] = round(Marginal_Cost_Generator_2,3)    
        
        Battery_Electronic_Invesmente_Cost  = instance.Battery_Electronic_Invesmente_Cost.extract_values()[None]    
        unitary_battery_cost = Battery_Invesment_Cost_1 - Battery_Electronic_Invesmente_Cost
        Unitary_Battery_Reposition_Cost_1 = unitary_battery_cost/(Battery_Cycles_1*2*(1- Deep_of_Discharge_1))
        instance.Unitary_Battery_Reposition_Cost = round(Unitary_Battery_Reposition_Cost_1,3)   
        
        opt = SolverFactory('gurobi') # Solver use during the optimization    
        opt.options['timelimit'] = 1800
        
        opt.options['Presolve'] = 2
        
#        filename = 'Instance/instance_' + str(i) + '_' + str(n) +  '.joblib'
#        dump(instance, filename) 
        
        logname = 'Results/instance_' + str(i) + '_' + str(n) +  '.log'
        results = opt.solve(instance, tee=True, options_string="mipgap=0.01",
                            warmstart=False,keepfiles=True,
                            load_solutions=False,
                            logfile=logname) # Solving a model instance 
       
        Status.loc[name,'Time'] = results.solver.wall_time
        Status.loc[name,'Upper Bound'] = results.problem.upper_bound 
        Status.loc[name,'Lower Bound'] = results.problem.lower_bound 
        Status.loc[name,'Gap'] = (Status.loc[name,'Upper Bound']- Status.loc[name,'Lower Bound']) \
                                    /Status.loc[name,'Upper Bound']
        Status.loc[name,'Gap'] = Status.loc[name,'Gap']*100
                                  
        instance.solutions.load_from(results) # Loading solution into instance
        Data = Load_results1(instance, i, n,type_generator)
        
        NPC = Data[0]        
        Status.loc[name,'Status'] = NPC.loc['Status','Data']
        end_1 = time.time()        
        Status.loc[name,'Time'] = end_1 - start_1
        print('The optimization took ' + str(round(end_1 - start_1,0)) + ' segundos')  
        Status.to_excel('status.xls')
        

        
end = time.time()
print('The optimizations took ' + str(round(end - start,0)) + ' segundos')        
        
        
        
        

