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

	Hospital = User("hospital",1)
	User_list.append(Hospital)

	#Create new appliances


	#Hospital
	Ho_indoor_bulb = Hospital.Appliance(Hospital,12,7,2,690,0.2,10)
	Ho_indoor_bulb.windows([480,720],[870,1440],0.35)

	Ho_outdoor_bulb = Hospital.Appliance(Hospital,1,13,2,690,0.2,10)
	Ho_outdoor_bulb.windows([0,330],[1050,1440],0.35)

	Ho_Phone_charger = Hospital.Appliance(Hospital,8,2,2,300,0.2,5)
	Ho_Phone_charger.windows([480,720],[900,1440],0.35)

	Ho_Fridge = Hospital.Appliance(Hospital,1,150,1,1440,0,30, 'yes',3)
	Ho_Fridge.windows([0,1440],[0,0])
	Ho_Fridge.specific_cycle_1(150,20,5,10)
	Ho_Fridge.specific_cycle_2(150,15,5,15)
	Ho_Fridge.specific_cycle_3(150,10,5,20)
	Ho_Fridge.cycle_behaviour([580,1200],[0,0],[420,579],[0,0],[0,419],[1201,1440])

	Ho_Fridge2 = Hospital.Appliance(Hospital,1,150,1,1440,0,30, 'yes',3)
	Ho_Fridge2.windows([0,1440],[0,0])
	Ho_Fridge2.specific_cycle_1(150,20,5,10)
	Ho_Fridge2.specific_cycle_2(150,15,5,15)
	Ho_Fridge2.specific_cycle_3(150,10,5,20)
	Ho_Fridge2.cycle_behaviour([580,1200],[0,0],[420,579],[0,0],[0,299],[1201,1440])

	Ho_Fridge3 = Hospital.Appliance(Hospital,1,150,1,1440,0.1,30, 'yes',3)
	Ho_Fridge3.windows([0,1440],[0,0])
	Ho_Fridge3.specific_cycle_1(150,20,5,10)
	Ho_Fridge3.specific_cycle_2(150,15,5,15)
	Ho_Fridge3.specific_cycle_3(150,10,5,20)
	Ho_Fridge3.cycle_behaviour([580,1200],[0,0],[420,479],[0,0],[0,419],[1201,1440])

	Ho_PC = Hospital.Appliance(Hospital,2,50,2,300,0.1,10)
	Ho_PC.windows([480,720],[1050,1440],0.35)

	Ho_Mixer = Hospital.Appliance(Hospital,1,50,2,60,0.1,1,occasional_use = 0.33)
	Ho_Mixer.windows([480,720],[1050,1440],0.35)

	return(User_list)