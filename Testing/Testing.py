# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 17:29:05 2020

@author: Auto1-PCP294
"""
import sys
import os 
from  DisplayingSolution import * 
from DataExtraction import *
from Zone_LC_Branches_ObjProg import *

from RouteOrganizer import *
from Algo2timePeriod11022020 import  *
import time as t
import logging




## Parameter 1 : The Zone we want to solve the problem on 
## Parameter 3 : Total Demand we want to give to the algorithm as input
## Parameter 4: Number of branches we want to solve the problem on. This parameter must be smaller or equal to the mùaximum number of branches into the zone. 
## Max Parameter for each zone : 

## IDF OUEST :
## Rhône-Alpes :
## Haute Normandie : 
## Basse Normandie : 
## Grand Est : 
## IDF EST : 
## IDF SUD : 
## Oise : 
## Nord : 50 




def Test(ZoneName,TotalDemand,NbBranchesViewed):
    logger = logging.getLogger('GetErrMsg')
    try :
       
        StartTime=t.time()
        Test = CreatingTestProblemObject(ZoneName,ExtractDataForTesting(),TotalDemand,NbBranchesViewed)
        
        ProblemSolving(Test.ZoneList[0],'ToupieOutput!','2 Periods')
        EndTime=t.time()
        
        print("\n Test solving time  = " + str(EndTime-StartTime) +"s")
        
        if(EndTime-StartTime>60): 
            print(' \n Calculation time not acceptable')
        else:
            print(' \n Calculation time acceptable')
            
        
    except IndexError as e : 
        print("Test Index Error \n")
        logger.error(e, exc_info=True)
        
    except TypeError as e : 
        print("Test Type Error \n")
        logger.error(e, exc_info=True)
        
    except ImportError as e : 
        print("Test Libraries importation Error \n")
        logger.error(e, exc_info=True)
        
    except EOFError as e : 
        print("Test End of file condition Error \n")
        logger.error(e, exc_info=True)
        
    except ValueError as e : 
        print("Test Data reading Error \n")
        logger.error(e, exc_info=True)
        
    except SyntaxError  as e : 
        print("Test Syntax Writting Error : \n")
        logger.error(e, exc_info=True)
        
    except Exception as e : 
        print("Test Excpetion Error : \n")
        logger.error(e, exc_info=True)
    
TotalDemandList=[1,6,20,50]
NbBranchesViewedList=[1,2,10,12] 

### AR008 ###

## Test 1 
#Test('Oise',1,1)

## Test 2 
#Test('Oise',6,2)

## Test 3 
#Test('Nord',20,10)

## Test 4 
#Test('Oise',50,12)


### AR011 ###

## Test 1 
#Test('Nord',10,2)

## Test 2 
#Test('Nord',12,4)

## Test 3 
#Test('Nord',30,15)

## Test 4 
#Test('Nord',51,17)

### AR017 ###

#Test('Grand Est',10,4)


