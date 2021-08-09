Surrogate models for rural energy planning: Application to  Bolivian lowlands isolated communities
========================

### Description

The purpose of this page is to serve as a permanent repository for the paper:

"Surrogate models for rural energy planning: Application to  Bolivian lowlands isolated communities" 

Inside this repository it is possible to find the scripts and data to reproduce the results of the paper. 
A brief explanation on how to do this is given below. It is important to note that the paper and this repository are meant to be read as one 
piece, in order to completely understand the theory and practical implementation of the work done. In order to have a complete description of the scripts, information and how to implement the methology, do not hesitate to contact 
any of the Authors with the emails provided or through github.

The first step to generate the surrogate models is the creation of a data base of optimal size microgrids. To do this, 
go to the main folder, open the file Micro-Grids_Surrogate in a development enviroment and run the script. A message regarding the status
of each optimization should appear in the terminal. The results of each optimization are saved in the Results folder with a distinctive name. Once all
optimizations are performed, the database can be created with the Data_Base_Creation script. This database is save in the Dabases folder. This database is 
also used for the creation of the surrogate moodels. Now, it is possible to analyze the results. This is done with the script call Results_Analysis. Once it is run, a message 
in the terminal should appear with a summary of the most important results. Also, Figure 10 and 11 of the paper are saved in 
the folder Plots with the names of  BoxPlot_LCOE_NPC.png and LDC_Renewable_Penetration.png. 

To do the crossvalidation test for each target variable (NPC, LCOE, PV installed capacity, Battery installed capacity) the files that begin with Crossvalidation
must be run. The end of the file depends on the variable that we want to analyze. As the different analyses are performed, a message in the 
terminal will appear with the results. Finally, to create the surrogate models, the files that begin with  Surroagate_Full_Data must be
run. In this case also, the end of the file will depend on the variable that is needed. When the process finishes some information will appear 
in the terminal and the surrogate model file will be saved in the folder Surrogate_Models. To reproduce figure 12 of the paper, the file 
Plot_predicted_Computed must be run. Figure 13 can be reproduced by running the Plot_Predicted_Computed_Fix file. This script needs 4 
additional databases (Database_Fix, Database_100, Database_300, Database_500). To create the first database, the file Micro-Grids_Surrogate_fix
must be run. This file is in the folder Fix_Cost. Additionally, the Data_Base_Creation must be run to create the needed database. 
Finally, this data base must be place in the folder Databases. The other three data bases are created following similar steps in the Fix_Cost_Households 
(they are included already, for the sake of simplicity). The only difference is that the file to run the sizing process is call
Micro-Grids_Surrogate_fix_Households.


In addition to the surrogate model creation and validation process, also in this repository is included  the case studies with Onsset.
these are located in the folder  OnSSET_Scenario. The scenario onsset classic is saved inside the folder Onsset_Scenario/onssset_classic and
can be run from the script Bolivia_runner. In the other hand, the scenario onsset surrogate models can be run from 
Onsset_Scenario/onssset_Surrogate with the help of Bolivia_runner file. The information needed to create Figure 14, can be extracted from 
each scenario if the file Plot_Data is run. The information is saved in two excel files called Plot_data_classic and Plot_data_surrogate. The
coordinates are the X_deg (longitude) and Y_def (latitude) columns.

### Authors

Sergio Balderrana
University of Liege, Belgium - Universidad Mayor de San Simon, Bolivia,
E-mail: slbalderrama@doct.ulg.ac.be / sergiob44_47@hotmail.com

Francesco Lombardi,
Politecnico di milano,
E-mail: francesco.lombardi@polimi.it

Nicolo Stevanato,
Politecnico di milano,
E-mail: nicolo.stevanato@polimi.it; 

Gabriela Peña
Royal Institute of Technology,
E-mail: gabrie@kth.se 

Emanuela Colombo,
Politecnico di milano,
E-mail: emanuela.colombo@polimi.it

Sylvain Quoilin,
University of Liege, Belgium,
E-mail: squoilin@ulg.be 
 

Requirements
============

This repository has been tested in Linux or windows and needs different programs and phyton libraries in order to work. 

Python
------------

First of all Micro-Grids needs Python 3.7 install in the computer. The easiest way to obtain it, is download anaconda in order to 
have all the tools needed to run python scripts.

Python libraries
----------------
 
The most important python libraries needed to run this repository are the following:

*   pyomo 5.7
*   pandas 0.23.4
*   pyDOE 0.3.8
*   joblib 0.14.1
*   scikit-learn 0.20.3 
*   numpy 1.18.1 
*   matplotlib 3.1.3
*   requests 2.22.0
*   pvlib 0.7.2
*   scipy 1.4.1
*   openpyxl 3.0.3


Solver
------

Any of the following solvents can be used during the optimization  process:

* Gurobi


Licence
=======
This is a free software licensed under the “European Union Public Licence" EUPL v1.1. It 
can be redistributed and/or modified under the terms of this license.

