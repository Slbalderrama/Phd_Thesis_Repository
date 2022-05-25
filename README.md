Optimal design and deployment of isolated energy systems: The Bolivian pathway to 100% rural electrification
========================

### Description

The purpose of this page is to serve as a permanent repository for the PhD thesis entitled:

"Optimal design and deployment of isolated energy systems: The Bolivian pathway to 100% rural electrification" 

Inside this repository it is possible to find the scripts and data to reproduce the results of the thesis. 
It is important to note that the paper and this repository are meant to be read as one 
piece, in order to completely understand the theory and practical implementation of the work done. In order to have a complete description of the scripts, information and how to implement the methodology, do not hesitate to contact 
the Author with the emails provided or through github.


### Author

Sergio Balderrama
University of Liege, Belgium - Universidad Mayor de San Simon, Bolivia,
E-mail: slbalderrama@doct.ulg.be / sergiob44_47@hotmail.com


### Requirements

This repository has been tested in Linux or windows and needs different programs and phyton libraries in order to work. 

Python
-------

First of all, Python 3.7 should be installed on the computer. The easiest way to obtain it, is download anaconda in order to have all the tools needed to run python scripts.

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


Repository Composition
======================

Each of the folders represent one of the chapters of the PhD thesis, the correspondence is:

- Demand_Modeling has the scripts and data from chapter 2.
- The_Bolivian_Study_Case has the scripts and data from chapter 3.
- El_Espino_Analisys has the scripts from chapter 5.
- Home_Solar_Systems has the scripts and data from chapter 6.
- Gis_Electrification has the scripts and data from chapter 7. 
- Surrogate_Models has the scripts and data from chapter 8.
- Electrification_Path has the scripts and data from chapter 9.

Inside of each folder, you can find a README that gives further information of the data and scripts.

Licence
=======
This is a free software licensed under the “European Union Public License" EUPL v1.1. It 
can be redistributed and/or modified under the terms of this license.


