# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 19:41:07 2021

@author: Clau
"""

'''
Scenario 2: Lowlands, High Income
'''
from core import User, np
User_list = []

#Create new user classes
HI = User("high income",1)
User_list.append(HI)

#Appliances

#Households

HI_indoor_bulb = HI.Appliance(HI,6,7,2,120,0.2,10)
HI_indoor_bulb.windows([1170,1440],[0,30],0.35)

HI_outdoor_bulb = HI.Appliance(HI,2,13,2,600,0.2,10)
HI_outdoor_bulb.windows([0,330],[1170,1440],0.35)

HI_TV = HI.Appliance(HI,2,60,3,180,0.1,5)
HI_TV.windows([720,900],[1170,1440],0.35,[0,60])

HI_DVD = HI.Appliance(HI,1,8,3,60,0.1,5)
HI_DVD.windows([720,900],[1170,1440],0.35,[0,60])

HI_Antenna = HI.Appliance(HI,1,8,3,120,0.1,5)
HI_Antenna.windows([720,900],[1170,1440],0.35,[0,60])

HI_Phone_charger = HI.Appliance(HI,5,2,2,300,0.2,5)
HI_Phone_charger.windows([1110,1440],[0,30],0.35)

HI_Freezer = HI.Appliance(HI,1,200,1,1440,0,30,'yes',3)
HI_Freezer.windows([0,1440],[0,0])
HI_Freezer.specific_cycle_1(200,20,5,10)
HI_Freezer.specific_cycle_2(200,15,5,15)
HI_Freezer.specific_cycle_3(200,10,5,20)
HI_Freezer.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

HI_Mixer = HI.Appliance(HI,1,50,3,30,0.1,1,occasional_use = 0.33)
HI_Mixer.windows([420,480],[660,750],0.35,[1140,1200])

