
from runner import scenario
import pandas as pd
import os
'''Check if the demand if the constraints are applyied for 2020'''


    # 'Database_lower_ElecPopCalib.csv'
    # 'Database_new_1.csv'
specs_path = os.path.join('Bolivia', 'specs_paper_new.xlsx')
calibrated_csv_path = os.path.join('Bolivia', 'Database_new_1.csv')
results_folder = os.path.join('Bolivia')
summary_folder	= os.path.join('Bolivia')
  
scenario(specs_path, calibrated_csv_path, results_folder, summary_folder)


#%%    

name = ['information_Grid.csv', 'information_MG_Diesel_.csv', 'information_MG_PV_.csv',
        'information_SA_PV_.csv']

for i in name:
    print(i)
    data = pd.read_csv('Bolivia/' + i)
    
    
    data['investment test'] =  (data['Disconunted grid capacity invesment'] +
                        data['Disconunted tech capacity invesment'])
    
    data['Investment boolean'] = (round(data['investment test'],4) 
                                  == round(data['Disconunted invesment'],4))
    
    data['NPC Test'] = (data['Disconunted grid capacity invesment'] +
                        data['Disconunted tech capacity invesment'] +
                        data['Disconunted oym'] +
                        data['Disconunted fuel'] -
                        data['Disconunted salvage'])
    data['lcoe test'] = data['NPC']/data['Disconunted energy']
    
    data['NPC boolean'] = (round(data['NPC'],3) == round(data['NPC Test'],3))
    
    
     
    data['lcoe boolean'] = round(data['lcoe test'],4) == round(data['lcoe'],4) 
    
    print(data['Investment boolean'].all())
    print(data['NPC boolean'].all())
    print(data['lcoe boolean'].all())