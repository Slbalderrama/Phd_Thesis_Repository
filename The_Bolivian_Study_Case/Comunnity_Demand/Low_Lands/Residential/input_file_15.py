# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 14:59:08 2018

@author: stevo
"""

#%% Definition of the inputs
'''
Input data definition (this is planned to be externalised in a separate script)
'''



def input_file(k):
    from core import User
    User_list = []
            
    
    #Create new user classes
    HI = User("high income",10*k,3)
    User_list.append(HI)
    
    LI = User("low income",40*k,3)
    User_list.append(LI)
    
    Public_lighting = User("public lighting",k*1)
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
    
    
    #High-Income Like the HI from Original Paper buth with only 1 Freezer
    
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
    
    
    #Low Income
    LI_indoor_bulb = LI.Appliance(LI,2,7,2,120,0.2,10)
    LI_indoor_bulb.windows([1170,1440],[0,30],0.35)
    
    LI_outdoor_bulb = LI.Appliance(LI,1,13,2,600,0.2,10)
    LI_outdoor_bulb.windows([0,330],[1170,1440],0.35)
    
    LI_TV = LI.Appliance(LI,1,60,3,90,0.1,5)
    LI_TV.windows([750,840],[1170,1440],0.35,[0,30])
    
    LI_DVD = LI.Appliance(LI,1,8,3,30,0.1,5)
    LI_DVD.windows([750,840],[1170,1440],0.35,[0,30])
    
    LI_Antenna = LI.Appliance(LI,1,8,3,60,0.1,5)
    LI_Antenna.windows([750,840],[1170,1440],0.35,[0,30])
    
    LI_Phone_charger = LI.Appliance(LI,2,2,1,300,0.2,5)
    LI_Phone_charger.windows([1080,1440],[0,0],0.35)
    
    return(User_list)