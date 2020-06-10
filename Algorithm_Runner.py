# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 16:25:58 2020
@author: Auto1-PCP294
"""


from Zone_LC_Branches_ObjProg import * 
from DataExtraction import * 
from RouteOrganizer import * 
from Utils import * 
from Algo2timePeriod11022020 import ProblemSolving 
from DisplayingSolution import * 
from WrittingSolInSpreadSheets import *


def RunAlgorithm(ZoneNameList,SolOutputRange,SolSpreadSheetId,ItinerariesRange,ItinerariesSpreadSheetId):

    sheet = main().spreadsheets()
    
    Routing = CreatingProblemObject(ZoneNameList, ExtractData(ZoneNameList))
    
    SuspiciousLtList = []
    KpiList = []
    
    for j in range(len(ZoneNameList)):
        
        SheetName = ZoneNameList[j][0]
        
        try :
            
            sheet.values().clear(spreadsheetId=SolSpreadSheetId,range=SolOutputRange[SheetName]+"A1:P100").execute()
            
            Variables, SuspiciousLT, WrittenItineraries, KpiItem = ProblemSolving(Routing.ZoneList[j],SolOutputRange[SheetName],'2 Periods',ZoneNameList[j][1],SolSpreadSheetId)
            
            if SuspiciousLT != None : 
                
                SuspiciousLtList.append([ZoneNameList[j],SuspiciousLT])
            
            KpiList.append(KpiItem)
            
        except AttributeError : 
            
            WrittingInSheet(SolSpreadSheetId,sheet, 'RAW', SolOutputRange[SheetName]+'H1:H2', 'ROWS',[['Any Solution for that Zone'],['Model is infeasible']])
    
    
    WriteSuspiciousLTIntoReport(SolSpreadSheetId,sheet,SuspiciousLtList)
    
    ## Write Itineraries in sheet 

    WriteItinerariesListInSheet(WrittenItineraries,ItinerariesRange,ZoneNameList,ItinerariesSpreadSheetId,KpiList)








