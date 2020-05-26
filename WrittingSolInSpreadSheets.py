# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 14:38:17 2020

@author: Auto1-PCP294
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from DataExtraction import * 
from Utils import *
from RouteSplitter import *


def WriteSolInSpreadSheet(Truck,NbTrucks,NbPeriods,ListOfTotalTrajectory,ListOfTimesTrajectory,TransportedQtyTruckBr2BrList,TransportedQtyTruckBr2LcList,Zone,Fixed_Cost_Truck,SpreadID,SheetID,NumberOfPeriod,SuspiciousLT):
   
### Building lists that will provide informaton to the spreadsheet ###
    
    WrittenItineraries = []
    
    WriteSheetHeaders(Zone,SpreadID,SheetID)
    
    RoutesPerTruckList = []
    TruckKpis = []

    for c in range(NbTrucks) : 
        
        CurrentWrittenItinerary = []
        
        ### Truck writting ###
        
        GoogleFormatTruckList=[]
        ValuesTruckList=[]
        
        ValuesColumnNameList=[['Truck ID'],['Location'],['Address'],['Arr Time'],['Dep Time'],['Current Loading'],['Qty to load']]
        PeriodsValuesList={'2 Periods': [[['Morning Routing 8h-13h']],[['Afternoon Routing 13h-18h']]], '1 Period':[[['Journey Routing']]]}
        
        
        TruckRange = '{}{}{}:{}{}'.format(SheetID, StartColumn, GetRowToWriteIn(NumberOfPeriod, c, "headBegin"), EndColumn, GetRowToWriteIn(NumberOfPeriod, c, "headEnd"))
        
        PeriodRangeList = []
        Period1Row = GetRowToWriteIn(NumberOfPeriod, c, "period1")
        Period2Row = GetRowToWriteIn(NumberOfPeriod, c, "period2")
        PeriodRangeList.append('{}{}{}:{}{}'.format(SheetID,StartColumn,Period1Row,EndColumn,Period1Row))
        PeriodRangeList.append('{}{}{}:{}{}'.format(SheetID,StartColumn,Period2Row,EndColumn,Period2Row))
        
        ColumnNameRangeList=[]
        ColumnHeader1Row = GetRowToWriteIn(NumberOfPeriod, c, "columnHeader1")
        ColumnHeader2Row = GetRowToWriteIn(NumberOfPeriod, c, "columnHeader2")
        ColumnNameRangeList.append('{}{}{}:{}{}'.format(SheetID,StartColumn,ColumnHeader1Row,EndColumn,ColumnHeader1Row))
        ColumnNameRangeList.append('{}{}{}:{}{}'.format(SheetID,StartColumn,ColumnHeader2Row,EndColumn,ColumnHeader2Row))
        
        if(Truck[c].x==1):
            
            ValueDisplayed='Truck ' + str(c+1)
            ValuesTruckList.append(ValueDisplayed)
            GoogleFormatTruckList.append(ValuesTruckList)

            WrittingInSheet(SpreadID, main().spreadsheets(), 'RAW', TruckRange, 'ROWS' , GoogleFormatTruckList)
            
            for t in range(NbPeriods):
                
                WrittingInSheet(SpreadID, main().spreadsheets(), 'RAW', PeriodRangeList[t], 'ROWS' , PeriodsValuesList[NumberOfPeriod][t])
                
                WrittingInSheet(SpreadID, main().spreadsheets(), 'RAW', ColumnNameRangeList[t], 'COLUMNS' , ValuesColumnNameList)

                if len(ListOfTotalTrajectory[t][c])!=0 : 
                    
                    ### Routing Writting ###
                    GoogleFormatBranchList=[]
                
                    for i in range(len(ListOfTotalTrajectory[t][c])):
                    
                        RoutingInfoList=[]
                        Itinerary = []
                        
                        Index=ListOfTotalTrajectory[t][c][i]
                        LastIndex=ListOfTotalTrajectory[t][c][len(ListOfTotalTrajectory[t][c])-1]
                        
                        if(i==0):
                            
                            TruckID = c+1
                            
                            Name=Zone.LcList[Index[0]].GetName()
                            
                            ArrivalTime="None"
                            DepartureTime=int(ListOfTimesTrajectory[t][c][i][0])
                            
                            PickingQty=0
                            TransportedQty=0#TransportedQtyTruckBr2LcList[LastIndex[0]][LastIndex[1]][c][t]
                            
                            GoogleFormatBranchList.append(FillingList(RoutingInfoList,TruckID,Name,PickingQty,TransportedQty,ArrivalTime,DepartureTime))
                            
                            CurrentWrittenItinerary.append(FillingItineraryList(Itinerary,TruckID,Name,PickingQty,ArrivalTime,DepartureTime))                        
                        
                        elif(i==len(ListOfTotalTrajectory[t][c])-1):
                            
                            if(len(ListOfTotalTrajectory[t][c])>2):
                                
                                # Last Branch #
                                RetardedIndex=ListOfTotalTrajectory[t][c][i-1]
                                CurrentIndex=ListOfTotalTrajectory[t][c][i]
                                
                                TruckID = c+1
                                
                                Name=Zone.BranchesList[Index[0]].GetName()
                                Address = Zone.BranchesList[Index[0]].GetAddress()
                                
                                ArrivalTime=int(ListOfTimesTrajectory[t][c][i-1][1])
                                DepartureTime=int(ListOfTimesTrajectory[t][c][i][0])
                                
                                PickingQty=TransportedQtyTruckBr2LcList[Index[0]][Index[1]][c][t]-sum(TransportedQtyTruckBr2BrList[k][Index[0]][c][t] for k in range(Zone.GetNumberOfBranchesInZone()))
                                TransportedQty=TransportedQtyTruckBr2BrList[RetardedIndex[0]][RetardedIndex[1]][c][t]
                                
                                GoogleFormatBranchList.append(FillingList(RoutingInfoList,TruckID,Name,PickingQty,TransportedQty,ArrivalTime,DepartureTime, Address))
                                
                                CurrentWrittenItinerary.append(FillingItineraryList(Itinerary,TruckID,Name,PickingQty,ArrivalTime,DepartureTime))                                
                            else:
                                
                                RetardedIndex=ListOfTotalTrajectory[t][c][i-1]
                                
                                TruckID = c+1
                                
                                Name=Zone.BranchesList[Index[0]].GetName()
                                Address = Zone.BranchesList[Index[0]].GetAddress()
                                
                                ArrivalTime=int(ListOfTimesTrajectory[t][c][i-1][1])
                                DepartureTime=int(ListOfTimesTrajectory[t][c][i][0])
                                
                                PickingQty=TransportedQtyTruckBr2LcList[Index[0]][Index[1]][c][t]-sum(TransportedQtyTruckBr2BrList[k][Index[0]][c][t] for k in range(Zone.GetNumberOfBranchesInZone()))
                                TransportedQty=0
                                
                                
                                GoogleFormatBranchList.append(FillingList(RoutingInfoList,TruckID,Name,PickingQty,TransportedQty,ArrivalTime,DepartureTime, Address))
                                
                                CurrentWrittenItinerary.append(FillingItineraryList(Itinerary,TruckID,Name,PickingQty,ArrivalTime,DepartureTime))
                            # Lc #
                                
                            RoutingInfoList=[]
                            
                            Itinerary = []
                            
                            TruckID = c+1
                            
                            Name=Zone.LcList[Index[1]].GetName()
                            
                            ArrivalTime=int(ListOfTimesTrajectory[t][c][i][1])
                            DepartureTime="None"
                            
                            TransportedQty=TransportedQtyTruckBr2LcList[LastIndex[0]][LastIndex[1]][c][t]
                            PickingQty=0
                           
                            
                            GoogleFormatBranchList.append(FillingList(RoutingInfoList,TruckID,Name,PickingQty,TransportedQty,ArrivalTime,DepartureTime))
                            
                            CurrentWrittenItinerary.append(FillingItineraryList(Itinerary,TruckID,Name,PickingQty,ArrivalTime,DepartureTime))
                       
                        else:
                            
                            RetardedIndex=ListOfTotalTrajectory[t][c][i-1]
                           
                            TruckID = c+1
                            
                            Name=Zone.BranchesList[Index[0]].GetName()
                            Address = Zone.BranchesList[Index[0]].GetAddress()
                            
                            ArrivalTime=int(ListOfTimesTrajectory[t][c][i-1][1])
                            DepartureTime=int(ListOfTimesTrajectory[t][c][i][0])
                            
                            PickingQty=TransportedQtyTruckBr2BrList[Index[0]][Index[1]][c][t]-sum(TransportedQtyTruckBr2BrList[k][Index[0]][c][t] for k in range(Zone.GetNumberOfBranchesInZone()))
                            TransportedQty=TransportedQtyTruckBr2BrList[Index[0]][Index[1]][c][t]-PickingQty
                          
                            GoogleFormatBranchList.append(FillingList(RoutingInfoList,TruckID,Name,PickingQty,TransportedQty,ArrivalTime,DepartureTime, Address))

                            CurrentWrittenItinerary.append(FillingItineraryList(Itinerary,TruckID,Name,PickingQty,ArrivalTime,DepartureTime))
                    
                    GoogleFormatBranchList = PrepareRouteForProcessing(GoogleFormatBranchList)
    
                    if NbPeriods == '1 Period' : 
                        
                        GoogleFormatBranchList = InsertBreakRows(GoogleFormatBranchList)
                        GoogleFormatBranchList = SplitRoute(GoogleFormatBranchList)
                        
                    GoogleFormatBranchList = FormatRouteTimesInHours(GoogleFormatBranchList)
                    GoogleFormatBranchList = ClearExtraRouteInfo(GoogleFormatBranchList)
                    #RoutesPerTruckList.append([c, t, GoogleFormatBranchList, GoogleFormatBranchList[0][2], len(ListOfTotalTrajectory[t][c])])
                    RoutesPerTruckList.append([c, t, GoogleFormatBranchList, GoogleFormatBranchList[0][2], len(GoogleFormatBranchList)])
                
                else : 
                    
                    RowToWrite = GetRowToWriteIn(NumberOfPeriod, c, "RoutingRangeStartIndex2Periods")
                    UnusedTruckRange = SheetID+'B'+str(RowToWrite)+':C'+str(RowToWrite)
                    WrittingInSheet(SpreadID, main().spreadsheets(), 'RAW', UnusedTruckRange, 'COLUMNS' , [['Truck'],['Unused']])
   
            KPITruck = Fixed_Cost_Truck/sum(TransportedQtyTruckBr2LcList[i][l][c][t] for i in range(Zone.GetNumberOfBranchesInZone()) for l in range(Zone.GetNumberOfLcInZone()) for t in range(NbPeriods))
            TruckKpis.append([c, KPITruck])
            
            WriteSuspiciousLTInSheet(Zone,SpreadID, SheetID, main().spreadsheets(),'K')
            
            WrittenItineraries.append(CurrentWrittenItinerary)
            
    if NumberOfPeriod == '1 Period':
        
        RoutesPerTruckList, TruckKpis = SortRoutesAndKpis(RoutesPerTruckList, TruckKpis)

    WriteRoutesInSheet(SpreadID, SheetID, NumberOfPeriod, RoutesPerTruckList)
    
    ### Global KPIs Display ###  
          
    KPI1=sum(TransportedQtyTruckBr2LcList[i][l][c][t] for i in range(Zone.GetNumberOfBranchesInZone()) for l in range(Zone.GetNumberOfLcInZone()) for c in range(NbTrucks) for t in range(NbPeriods))
    
    WrittingInSheet(SpreadID, main().spreadsheets(), 'RAW', SheetID+'C1:E1', 'COLUMNS' , [['KPI1'],['Number of cars to pick up'],[int(KPI1)]])
    

    if len(SuspiciousLT) != 0 : 
        
        WrittingInSheet(SpreadID, main().spreadsheets(),'RAW',SheetID + 'K13:0'+str(13+len(SuspiciousLT)-1),'ROWS',SuspiciousLT)
    
    else : 
        
        WrittingInSheet(SpreadID, main().spreadsheets(),'RAW',SheetID + 'K13:M13','COLUMNS',[["Any Suspicious LeadTime"]])

    return WrittenItineraries

def SortRoutesAndKpis(routesPerTruckList, truckKpis):

    sortedTruckKpis = []
    routesPerTruckList.sort(key = lambda x: x[3], reverse=True)

    for i, route in enumerate(routesPerTruckList):
        sortedTruckKpis.append(next(truckKpi for truckKpi in truckKpis if truckKpi[0] == route[0]) )

    for i, route in enumerate(routesPerTruckList):
        route[0] = i
        sortedTruckKpis[i][0] = i

    return routesPerTruckList, sortedTruckKpis

def WriteRoutesInSheet(ssId, sheetId, numberOfPeriods, routesPerTruckList):

    for route in routesPerTruckList:
        truckNumber = route[0]
        currentPeriodNumber = route[1]
        googleFormatBranchList = route[2]
        trajectoryLen = route[4]

        RoutingRangeStartIndex = GetRowToWriteIn(numberOfPeriods, truckNumber, "routingRangeStartIndex", currentPeriodNumber)
        RoutingRangeEndIndex =  GetRowToWriteIn(numberOfPeriods, truckNumber, "routingRangeEndIndex", currentPeriodNumber, trajectoryLen)
        RoutingRange ='{}{}{}:{}{}'.format(sheetId, StartColumn, RoutingRangeStartIndex, EndColumn, RoutingRangeEndIndex)    
        WrittingInSheet(ssId, main().spreadsheets(), 'RAW', RoutingRange, 'ROWS' , googleFormatBranchList)
    

        day1Index = RoutingRangeStartIndex
        day2Index = 0
    
        for i, step in enumerate(googleFormatBranchList):
            if step[0] == "":
                day2Index = RoutingRangeStartIndex + i + 1
                break
        
        Day1Range = '{}{}{}:{}{}'.format(sheetId, "A", day1Index, "A", day1Index)
        WrittingInSheet(ssId, main().spreadsheets(), 'RAW', Day1Range, 'ROWS' , [["Day 1"]])
        if day2Index != 0:
            Day2Range = '{}{}{}:{}{}'.format(sheetId, "A", day2Index, "A", day2Index)
            WrittingInSheet(ssId, main().spreadsheets(), 'RAW', Day2Range, 'ROWS' , [["Day 2"]])


def WriteTruckKpisInSheet(ssId, sheetId, numberOfPeriods,truckKpis):

    for truckKpi in truckKpis:
        c = truckKpi[0]
        kpiTruck1 = truckKpi[1]

        KPITruckRow = GetRowToWriteIn(numberOfPeriods,c, "kpiTruck")
        KPITruckRange = '{}{}{}:{}{}'.format(sheetId, GetColumnOffset(StartColumn, 1), KPITruckRow, GetColumnOffset(EndColumn, -2), KPITruckRow)
        WrittingInSheet(ssId,main().spreadsheets(),'RAW',KPITruckRange,'COLUMNS',[['KPI Truck '+str(c+1)],['Logistic cost per car for truck (€) '+str(c+1)],[int(kpiTruck1)]])


def GetRowToWriteIn(totalNumberOfPeriods, truckNumber, section, currentPeriodNumber = 0, lenOfTrajectory = 0):

    mainHeaderSizeInRows = 5

    truckSectionSizeInRows = 24
    if totalNumberOfPeriods == '2 Periods':
        truckSectionSizeInRows = 38

    baseRow =  mainHeaderSizeInRows + (truckNumber)*truckSectionSizeInRows 
    
    if section == "headBegin":
        return baseRow
    elif section == "headEnd":
        return baseRow + 2
    elif section == "period1":
        return baseRow + 3
    elif section == "columnHeader1":
        return baseRow + 4
    elif section == "period2":
        return baseRow + 16
    elif section == "columnHeader2":
        return baseRow + 17
    elif section == 'RoutingRangeStartIndex2Periods':
        return baseRow + 18
    elif section == "routingRangeStartIndex":
        return 10 + (13*currentPeriodNumber) + (truckNumber)*truckSectionSizeInRows
    elif section == "routingRangeEndIndex":
        return 10 + (12*currentPeriodNumber) + lenOfTrajectory + 1 + (truckNumber)*truckSectionSizeInRows
    elif section == "kpiTruck":
        return truckSectionSizeInRows * (truckNumber + 1)
    elif section == "notesTruck":
        return (truckSectionSizeInRows * (truckNumber + 1)) + 2
    else:
        return baseRow

def GetColumnOffset(columnLetter, offset):
    return chr(ord(columnLetter) + offset)                     

def WriteSuspiciousLTInSheet(Zone,SpreadID, SheetID, Sheet,StartColumn):
    
    StartColumn = StartColumn
    IndexEndColumn = ConvertIndexIntoA1Notation(StartColumn) + 5
    EndColumn = ConvertA1Notation(IndexEndColumn)
    
    WrittingInSheet(SpreadID,Sheet ,'RAW',SheetID+StartColumn+'10','COLUMNS',[[str(Zone.GetName())]])
    
    WrittingInSheet(SpreadID, Sheet,'RAW',SheetID+StartColumn+'11','COLUMNS',[['Suspicious LT between merchants']])
    
    WrittingInSheet(SpreadID, Sheet,'RAW',SheetID+StartColumn+'12:'+EndColumn+'12','COLUMNS',[['Period'],['Truck'],['Merchant 1'],['Merchant 2'],['Travel Time (min)']])

def WriteSheetHeaders(Zone,SpreadID,SheetID):
    
    InfoList=[]
    
    Name=str(Zone.GetName())
    TotalDemand=str(Zone.GetTotalDemand())
    
    InfoList.append([['Zone'],[Name]])
    InfoList.append([['Zone Demand'],[TotalDemand]])
    
    WrittingInSheet(SpreadID, main().spreadsheets(), 'RAW', SheetID+'A1:B1', 'COLUMNS' , InfoList[0])
    WrittingInSheet(SpreadID, main().spreadsheets(), 'RAW', SheetID+'A2:B2', 'COLUMNS' , InfoList[1])

def WriteSuspiciousLTIntoReport(SolSpreadSheetId,Sheet,SuspiciousLtList):

    Sheet.values().clear(spreadsheetId=SolSpreadSheetId,range='FlagLT!A1:F150').execute()
       
    Index = 0
    
    WrittingInSheet(SolSpreadSheetId, Sheet,'RAW','FlagLT!A'+str(Index+1)+':F'+str(Index+1),'COLUMNS',[['Label'],['Period'],['Truck'],['Merchant 1'],['Merchant 2'],['Travel Time (min)']])
    
    if len(SuspiciousLtList) != 0:
        
        for i in range(len(SuspiciousLtList)) : 
            
            WrittingInSheet(SolSpreadSheetId, Sheet,'RAW','FlagLT!A'+str(Index+2)+':F'+str(Index+2+len(SuspiciousLtList[i][1])),'ROWS',SuspiciousLtList[i][1])
        
            Index = Index + len(SuspiciousLtList[i][1])
            
    else: 
        
        WrittingInSheet(SolSpreadSheetId, Sheet,'RAW','FlagLT!A'+str(Index+2)+':C'+str(Index+2),'COLUMNS',[['Any'],['Suspicious'],['LT']])
            
  


def WriteItinerariesListInSheet(WrittenItineraries,ItinerariesRange,ZoneNameList,SpreadSheetId,KpiList):
    
    Sheet = main().spreadsheets()
    
    for i in range(len(ZoneNameList)):
        
        Range = ItinerariesRange[ZoneNameList[i][0]]
        
        Sheet.values().clear(spreadsheetId=SpreadSheetId,range=Range+'A1:BZ3').execute()
        Sheet.values().clear(spreadsheetId=SpreadSheetId,range=Range+'A20:BZ100').execute()

        SheetHeaders = [['Zone'],['#Truck']]
        WrittingInSheet(SpreadSheetId, Sheet, 'RAW', Range+'A1:A2', 'ROWS' , SheetHeaders)

        SheetHeaders = [[ZoneNameList[i][0]],[str(len(WrittenItineraries))]]
        WrittingInSheet(SpreadSheetId, Sheet, 'RAW', Range+'B1:B2', 'ROWS' , SheetHeaders)
        
        Kpi = [['Cost €/PU'],[KpiList[i]]]
        WrittingInSheet(SpreadSheetId, Sheet, 'RAW', Range+'C1:D1', 'COLUMNS' , Kpi)

        StartRowIndex = 20
        
        for j in range(len(WrittenItineraries)): 
            
            ItinerariesHeaders = [['Truck ID'],['Dealer Name'],['Arrival Time'],['Departure Time'],['Status'],['QTY']]
            WrittingInSheet(SpreadSheetId, Sheet, 'RAW', Range+'A'+str(StartRowIndex)+':F'+str(StartRowIndex), 'COLUMNS' , ItinerariesHeaders)
            
            ItinerariesStartIndex = StartRowIndex + 1 
            ItinerariesEndIndex = ItinerariesStartIndex + len(WrittenItineraries[j])
            
            NextItinerariesIndex = ItinerariesStartIndex + 12
            
            WrittingInSheet(SpreadSheetId, Sheet, 'RAW', Range+'A'+str(ItinerariesStartIndex)+':F'+str(ItinerariesEndIndex), 'ROWS' , WrittenItineraries[j])
            
            StartRowIndex = NextItinerariesIndex + 4

            
            
            
            
            
            
            
            
            
# global variables

PeriodsValuesList={'1 Period' : [[['Morning Routing 8h-13h']],[['Afternoon Routing 14h-18h']]], '2 Periods':[['Journey Routing 9h-17h30']]}
StartColumn = "B"
EndColumn = "H"



































        
    
    




