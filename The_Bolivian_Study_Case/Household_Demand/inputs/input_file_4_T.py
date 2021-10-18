# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 09:10:37 2021

@author: Clau
"""

'''
Scenario 3: Toconao, High Income Households
'''

from core import User, np
User_list = []

#Create new user classes
HI = User("high income",1)
User_list.append(HI)

#Appliances


HI_indoor_bulb = HI.Appliance(HI,7,7,2,300,0.2,10)
HI_indoor_bulb.windows([1080,1440],[0,30],0.35)
    
HI_outdoor_bulb = HI.Appliance(HI,1,13,2,300,0.2,30)
HI_outdoor_bulb.windows([0,420],[1200,1440],0.35)
    
HI_TV = HI.Appliance(HI,2,60,2,360,0.1,30)
HI_TV.windows([540,780],[1080,1440],0.35)
    
HI_Radio = HI.Appliance(HI,1,7,2,240,0.1,30)
HI_Radio.windows([480,720],[1080,1380],0.35)
    
HI_Phone_charger = HI.Appliance(HI,4,5,2,360,0.2,10)
HI_Phone_charger.windows([1200,1440],[0,420],0.35)
    
HI_Freezer = HI.Appliance(HI,1,250,1,1440,0,30,'yes',3)
HI_Freezer.windows([0,1440],[0,0])
HI_Freezer.specific_cycle_1(200,20,5,10)
HI_Freezer.specific_cycle_2(200,15,5,15)
HI_Freezer.specific_cycle_3(200,10,5,20)
HI_Freezer.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])
    
HI_Laptop = HI.Appliance(HI,1,70,1,90,0.1,30)
HI_Laptop.windows([960,1440],[0,0],0.35)
    
HI_Iron = HI.Appliance(HI,1,700,1,30,0.1,1,occasional_use = 0.28, thermal_P_var = 0.4)
HI_Iron.windows([600,1200],[0,0],0.35)
