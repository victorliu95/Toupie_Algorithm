# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 18:10:59 2020

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

#"LC02-Provence-Alpes-Côte d'Azur"
#"LC03-Brittany"
#"LC05-Grand Est"

ZoneNameList=[["LC03-Auvergne-Rhône-Alpes",5]]#,["LC07-Pays de la Loire",3],["LC07-Provence-Alpes-Côte d'Azur",4],["LC08-Bourgogne-Franche-Comté",3]]#,"LC03-Occitanie"]#'LC01-Bour,gogne-Franche-Comté','LC02-Bourgogne-Franche-Comté','LC03-Centre-Val de Loire','LC03-Bourgogne-Franche-Comté',"LC03-Provence-Alpes-Côte d'Azur","LC04-Pays de la Loire","LC05-Île-de-France","LC05-Nouvelle-Aquitaine","LC05-Pays de la Loire","LC06-Nouvelle-Aquitaine","LC06-Occitanie","LC06-Provence-Alpes-Côte d'Azur","LC07-Île-de-France","LC07-Normandy","LC08-Auvergne-Rhône-Alpes","LC08-Occitanie","LC09-Île-de-France"]#,"LC03-Grand Est",'LC01-Île-de-France','LC01-Occitanie','LC02-Auvergne-Rhône-Alpes','LC02-Brittany']#,'Auvergne-Rhône-Alpes','Bourgogne-Franche-Comté','Brittany','Centre-Val de Loire','Grand Est','Hauts-de-France','Île-de-France','Normandy','Nouvelle-Aquitaine','Occitanie',"Provence-Alpes-Côte d'Azur","Seine-Saint-Denis 14","Val-de-Marne"]
SheetAddressList={'2 Periods':['Oise Solution!','Nord Solution!','Haute Normandie Solution!','IDF SUD Solution!','IDF EST Solution!','Basse Normandie Solution!','Grand Est Solution!','Rhône-Alpes Solution!','IDF OUEST Solution!'],'1 Period':['1 Period Oise!', '1 Period Nord!','1 Period Haute Normandie!', '1 Period IDF SUD!','1 Period IDF EST!','1 Period Basse Normandie!','1 Period Grand Est!','1 Period Rhône-Alpes!','1 Period IDF OUEST!']}
OutputSheet={'LC17-Bourgogne-Franche-Comté':'ToupieOutput!','LC17-Île-de-France':'1 Period ToupieOutput!'}
OutputSheetWithName=[]
for j in range(len(ZoneNameList)):
    OutputSheetWithName.append(ZoneNameList[j][0]+'!')

"""

Routing = CreatingProblemObject(ZoneNameList, ExtractData())

sheet = main().spreadsheets()



for i in range(len(ZoneNameList)):
    
    sheet.values().clear(spreadsheetId='1Rfd8oeBIt0uEG_QG5_0VOLHZQQiap5ey2o-KRRoFkHw',range=SheetAddressList['1 Period'][i]+'A1:BZ100').execute()
    sheet.values().clear(spreadsheetId='1Rfd8oeBIt0uEG_QG5_0VOLHZQQiap5ey2o-KRRoFkHw',range=SheetAddressList['2 Periods'][i]+'A1:BZ100').execute()

    if(len(Routing.ZoneList[i].GetDemandList())!=0):
        
        ProblemSolving(Routing.ZoneList[i],SheetAddressList['1 Period'][i],'1 Period')
        ProblemSolving(Routing.ZoneList[i],SheetAddressList['2 Periods'][i],'2 Periods')
        
    else:
        
        WrittingInSheet('1Rfd8oeBIt0uEG_QG5_0VOLHZQQiap5ey2o-KRRoFkHw',sheet, 'RAW', SheetAddressList['1 Period'][i]+'H1:H2', 'ROWS',[['Any Solution for that Zone'],['No registered Demands for Branches']])
        WrittingInSheet('1Rfd8oeBIt0uEG_QG5_0VOLHZQQiap5ey2o-KRRoFkHw',sheet, 'RAW', SheetAddressList['2 Periods'][i]+'H1:H2', 'ROWS',[['Any Solution for that Zone'],['No registered Demands for Branches']])







"""
sheet = main().spreadsheets()

#OutputRange={'1 Period':'1 Period ToupieOutput!A1:BZ100','2 Periods':'ToupieOutput!A1:BZ100'}

#sheet.values().clear(spreadsheetId='1Rfd8oeBIt0uEG_QG5_0VOLHZQQiap5ey2o-KRRoFkHw',range=OutputRange['1 Period']).execute()
#sheet.values().clear(spreadsheetId='1Rfd8oeBIt0uEG_QG5_0VOLHZQQiap5ey2o-KRRoFkHw',range=OutputRange['2 Periods']).execute()

Routing = CreatingProblemObject(ZoneNameList, ExtractData(ZoneNameList))


for j in range(len(ZoneNameList)):
#ProblemSolving(Routing.ZoneList[1],'1 Period ToupieOutput!','1 Period')
    try :
        sheet.values().clear(spreadsheetId='1GDtx0pLI2tDCyWuimuihhBtwEA7Khes5trMjNy39M1M',range=ZoneNameList[j][0]+'!A1:CZ100').execute()
        ProblemSolving(Routing.ZoneList[j],OutputSheetWithName[j],'1 Period',ZoneNameList[j][1])
    
    except AttributeError : 
        WrittingInSheet('1GDtx0pLI2tDCyWuimuihhBtwEA7Khes5trMjNy39M1M',sheet, 'RAW', OutputSheetWithName[j]+'H1:H2', 'ROWS',[['Any Solution for that Zone'],['Model is infeasible']])
        #WrittingInSheet('1GDtx0pLI2tDCyWuimuihhBtwEA7Khes5trMjNy39M1M',sheet, 'RAW', OutputSheetWithName[j]+'H1:H2', 'ROWS',[['Any Solution for that Zone'],['No registered Demands for Branches']])


    