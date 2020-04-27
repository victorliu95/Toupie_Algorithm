# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 16:25:58 2020
@author: Auto1-PCP294
"""


from Zone_LC_Branches_ObjProg import * 
from DataExtraction import * 
from RouteOrganizer import * 
from Utils import * 
#from RandomDemandListCreation import * 
from Algo2timePeriod11022020 import ProblemSolving 
from DisplayingSolution import * 
from WrittingSolInSpreadSheets import *



ZoneNameList=[["LC02-Auvergne-Rhône-Alpes",5]]#,["LC07-Pays de la Loire",3],["LC07-Provence-Alpes-Côte d'Azur",4],["LC08-Bourgogne-Franche-Comté",3]]#,"LC03-Occitanie"]#'LC01-Bour,gogne-Franche-Comté','LC02-Bourgogne-Franche-Comté','LC03-Centre-Val de Loire','LC03-Bourgogne-Franche-Comté',"LC03-Provence-Alpes-Côte d'Azur","LC04-Pays de la Loire","LC05-Île-de-France","LC05-Nouvelle-Aquitaine","LC05-Pays de la Loire","LC06-Nouvelle-Aquitaine","LC06-Occitanie","LC06-Provence-Alpes-Côte d'Azur","LC07-Île-de-France","LC07-Normandy","LC08-Auvergne-Rhône-Alpes","LC08-Occitanie","LC09-Île-de-France"]#,"LC03-Grand Est",'LC01-Île-de-France','LC01-Occitanie','LC02-Auvergne-Rhône-Alpes','LC02-Brittany']#,'Auvergne-Rhône-Alpes','Bourgogne-Franche-Comté','Brittany','Centre-Val de Loire','Grand Est','Hauts-de-France','Île-de-France','Normandy','Nouvelle-Aquitaine','Occitanie',"Provence-Alpes-Côte d'Azur","Seine-Saint-Denis 14","Val-de-Marne"]



sheet = main().spreadsheets()

OutputRange={'1 Period':'1 Period ToupieOutput!','2 Periods':'ToupieOutput!'}


Routing = CreatingProblemObject(ZoneNameList, ExtractData(ZoneNameList))

y=Routing.ZoneList[0].BranchesList
#sheet.values().clear(spreadsheetId='1Rfd8oeBIt0uEG_QG5_0VOLHZQQiap5ey2o-KRRoFkHw',range=OutputRange['2 Periods']).execute()

SuspiciousLtList = []

for j in range(len(ZoneNameList)):
    
    try :
        
        sheet.values().clear(spreadsheetId='1Rfd8oeBIt0uEG_QG5_0VOLHZQQiap5ey2o-KRRoFkHw',range=OutputRange['1 Period']+"A1:BZ100").execute()
        Variables, SuspiciousLT = ProblemSolving(Routing.ZoneList[j],OutputRange['1 Period'],'1 Period',ZoneNameList[j][1],'1Rfd8oeBIt0uEG_QG5_0VOLHZQQiap5ey2o-KRRoFkHw')
        
        if SuspiciousLT != None : 
            SuspiciousLtList.append([ZoneNameList[j],SuspiciousLT])
        
    except AttributeError : 
        
        WrittingInSheet('1Rfd8oeBIt0uEG_QG5_0VOLHZQQiap5ey2o-KRRoFkHw',sheet, 'RAW', '1 Period ToupieOutput!'+'H1:H2', 'ROWS',[['Any Solution for that Zone'],['Model is infeasible']])
        #WrittingInSheet('1GDtx0pLI2tDCyWuimuihhBtwEA7Khes5trMjNy39M1M',sheet, 'RAW', OutputSheetWithName[j]+'H1:H2', 'ROWS',[['Any Solution for that Zone'],['No registered Demands for Branches']])


sheet.values().clear(spreadsheetId='1Rfd8oeBIt0uEG_QG5_0VOLHZQQiap5ey2o-KRRoFkHw',range='FlagLT!A1:F150').execute()
   
Dim = 1
if len(SuspiciousLtList) != 0:
    for i in range(len(SuspiciousLtList)) : 
        
        WrittingInSheet('1Rfd8oeBIt0uEG_QG5_0VOLHZQQiap5ey2o-KRRoFkHw',sheet, 'RAW', 'FlagLT!'+'A'+str(Dim), 'ROWS',[SuspiciousLtList[i][0]])
        WrittingInSheet('1Rfd8oeBIt0uEG_QG5_0VOLHZQQiap5ey2o-KRRoFkHw', sheet,'RAW','FlagLT!B'+str(Dim+1)+':F'+str(Dim+1),'COLUMNS',[['Period'],['Truck'],['Merchant 1'],['Merchant 2'],['Travel Time (min)']])
        WrittingInSheet('1Rfd8oeBIt0uEG_QG5_0VOLHZQQiap5ey2o-KRRoFkHw', sheet,'RAW','FlagLT!B'+str(Dim+2)+':F'+str(Dim+2+len(SuspiciousLtList[i][1])),'ROWS',SuspiciousLtList[i][1])
    
        Dim = Dim+2+len(SuspiciousLtList[i][1])