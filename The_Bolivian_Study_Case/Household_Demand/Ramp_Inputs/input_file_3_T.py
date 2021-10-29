# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 08:59:05 2021

@author: Clau
"""

'''
Scenario 3: Highlands, Low Income Households
'''
from core import User, np
User_list = []


#Create new user classes

LI = User("low income",1)
User_list.append(LI)

#Appliances

#Low Income
LI_indoor_bulb = LI.Appliance(LI,5,7,2,300,0.2,10)
LI_indoor_bulb.windows([1080,1440],[0,30],0.35)
    
LI_outdoor_bulb = LI.Appliance(LI,1,13,2,60,0.2,30)
LI_outdoor_bulb.windows([0,420],[1200,1440],0.35)
    
LI_TV = LI.Appliance(LI,1,60,2,240,0.1,30)
LI_TV.windows([540,780],[1080,1440],0.35)
    
LI_Radio = LI.Appliance(LI,1,7,2,240,0.1,30)
LI_Radio.windows([480,720],[1080,1380],0.35)

LI_Phone_charger = LI.Appliance(LI,2,5,2,360,0.2,10)
LI_Phone_charger.windows([1200,1440],[0,420],0.35)
        
LI_Iron = LI.Appliance(LI,1,700,1,30,0.1,1,occasional_use = 0.28, thermal_P_var = 0.4)
LI_Iron.windows([600,1200],[0,0],0.35)


