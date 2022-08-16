# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 14:59:08 2018

@author: stevo
"""

#%% Definition of the inputs
'''
Data from Field Campaign Pistolese-Stevanato 2017
'''



def input_file(k):
    from core import User
    User_list = []
            
    
    #Create new user classes
    HI = User("high income",25*k,3)
    User_list.append(HI)
    
    LI = User("low income",25*k,3)
    User_list.append(LI)
    
    Public_lighting = User("public lighting",k)
    User_list.append(Public_lighting)
    
    Church = User("church",3)
    User_list.append(Church)
    
    #Create new appliances
    
    #Church
    Ch_indoor_bulb = Church.Appliance(Church,10,26,1,210,0.2,60,'yes', flat = 'yes')
    Ch_indoor_bulb.windows([1200,1440],[0,0],0.1)
    
    Ch_outdoor_bulb = Church.Appliance(Church,7,26,1,240,0.2,60, 'yes', flat = 'yes')
    Ch_outdoor_bulb.windows([1200,1440],[0,0],0.1)
    
    Ch_speaker = Church.Appliance(Church,1,100,1,240,0.2,60)
    Ch_speaker.windows([1200,1350],[0,0],0.1)
    
    #Public lighting
    Pub_lights = Public_lighting.Appliance(Public_lighting,4,40,2,310,0.1,300, 'yes', flat = 'yes')
    Pub_lights.windows([0,375],[1116,1440],0.2)
    
    Pub_lights_2 = Public_lighting.Appliance(Public_lighting,9,150,2,310,0.1,300, 'yes', flat = 'yes')
    Pub_lights_2.windows([0,375],[1116,1440],0.2)
    
    
    #High-Income 
    
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

    return(User_list)