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

	School = User("school",1)
	User_list.append(School)

	#Create new appliances

	#School
	S_indoor_bulb = School.Appliance(School,8,7,1,60,0.2,10)
	S_indoor_bulb.windows([1020,1080],[0,0],0.35)

	S_outdoor_bulb = School.Appliance(School,6,13,1,60,0.2,10)
	S_outdoor_bulb.windows([1020,1080],[0,0],0.35)

	S_Phone_charger = School.Appliance(School,5,2,2,180,0.2,5)
	S_Phone_charger.windows([510,750],[810,1080],0.35)

	S_PC = School.Appliance(School,18,50,2,210,0.1,10)
	S_PC.windows([510,750],[810,1080],0.35)

	S_Printer = School.Appliance(School,1,20,2,30,0.1,5)
	S_Printer.windows([510,750],[810,1080],0.35)

	S_Freezer = School.Appliance(School,1,200,1,1440,0,30, 'yes',3)
	S_Freezer.windows([0,1440])
	S_Freezer.specific_cycle_1(200,20,5,10)
	S_Freezer.specific_cycle_2(200,15,5,15)
	S_Freezer.specific_cycle_3(200,10,5,20)
	S_Freezer.cycle_behaviour([580,1200],[0,0],[510,579],[0,0],[0,509],[1201,1440])

	S_TV = School.Appliance(School,1,60,2,120,0.1,5, occasional_use = 0.5)
	S_TV.windows([510,750],[810,1080],0.35)

	S_DVD = School.Appliance(School,1,8,2,120,0.1,5, occasional_use = 0.5)
	S_DVD.windows([510,750],[810,1080],0.35)

	S_Stereo = School.Appliance(School,1,150,2,90,0.1,5, occasional_use = 0.33)
	S_Stereo.windows([510,750],[810,1080],0.35)

	return(User_list)

