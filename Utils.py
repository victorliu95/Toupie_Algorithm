# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:59:18 2020

@author: Auto1-PCP294
"""
import ast
import math as m
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import *
from DataExtraction import *
 


def convertToTuple(x):
    return ast.literal_eval(x)

def ConvertA1Notation(Index):
    Alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    if(Index//26==0):
        A1Notation=str(Alphabet[Index%26])
    else:
        A1Notation=str(Alphabet[(Index//26)-1]+Alphabet[Index%26])
    return A1Notation

def ConvertIndexIntoA1Notation(A1Notation):
    Alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    Index = 0
    for Letter in A1Notation : 
        Index += Alphabet.index(Letter) +1
    return Index

def ConvertSecToHoursMin(TimeValue):
    
    if(TimeValue>=1440):
        return str('%g'%((TimeValue-1440)//60)+' H '+'%g'%(m.ceil((TimeValue-1440)%60))+' min')
    
    elif(TimeValue>=2880):
        return str('%g'%((TimeValue-2880)//60)+' H '+'%g'%(m.ceil((TimeValue-2880)%60))+' min')
    
    else :
        return str('%g'%(TimeValue//60)+' H '+'%g'%(m.ceil(TimeValue%60))+' min')

def FillingList(List,TruckID,Name,Qty,TransportedQty,ArrivalTime,DepartureTime, Address = ""):
    
    List.append(int(TruckID))
    
    List.append(str(Name))
    List.append(str(Address))

    List.append(ArrivalTime)
    List.append(DepartureTime)

    List.append(int(TransportedQty))
    List.append(int(Qty))
    
    return List

def FillingItineraryList(List, TruckID,Name,Qty,ArrivalTime,DepartureTime):

    List.append(int(TruckID))
    
    List.append(str(Name))

    if ArrivalTime == 'None' : 
        List.append(ArrivalTime)

    else :     
        List.append(ConvertSecToHoursMin(ArrivalTime))
        
    if DepartureTime == 'None' : 
            List.append(DepartureTime)  
    else : 
        List.append(ConvertSecToHoursMin(DepartureTime))

    if(Qty>0):
        List.append("Pick up")
    else : 
        List.append("Drop Off")

    List.append(int(Qty))
    
    
    
    return List


def WrittingInSheet(SpreadSheetID,sheet, ValueInputOption, Range, MajorDimensions,Values):
    
    RequestWritting=sheet.values().update(spreadsheetId=SpreadSheetID,valueInputOption=ValueInputOption,range=Range,body=dict(majorDimension=MajorDimensions,values=Values))
    RequestWritting.execute()
    

def CleanString(String):
    return(String.translate({ord(' '):None}))
    
def ReportSuspiciousLTIndexes(Zone,TimeBr2Br,TravelTimeBound,ListOfTotalTrajectory):
    SuspiciousLTTuples = []
    
    for t in range(len(ListOfTotalTrajectory)) : 
        for c in range(len(ListOfTotalTrajectory[t])) : 
            for i in range(len(ListOfTotalTrajectory[t][c])-2):
                TupleItem=ListOfTotalTrajectory[t][c][i+1]
                if (TimeBr2Br[TupleItem[0],TupleItem[1]]>=TravelTimeBound):
                    LtItem=None
                    LtItem = [Zone.GetName(),str(t+1), str(c+1), Zone.GetBranchesList()[TupleItem[0]].GetName(),Zone.GetBranchesList()[TupleItem[1]].GetName(),int(TimeBr2Br[TupleItem[0],TupleItem[1]])]
                    SuspiciousLTTuples.append(LtItem)
                    
    return SuspiciousLTTuples


    
def ReportSuspiciousLT(Zone,TimeBr2Br,TravelTimeBound = 120):
    SuspiciousLT = []
    for i in range(TimeBr2Br.shape[0]):
        for j in range(i,TimeBr2Br.shape[0]):
            CurrentList=[]
            if(TimeBr2Br[i,j]>=TravelTimeBound):
                CurrentList.append(Zone.BuildingBrNamesList()[i])
                CurrentList.append(Zone.BuildingBrNamesList()[j])
                CurrentList.append(m.ceil(TimeBr2Br[i,j]))
                SuspiciousLT.append(CurrentList)
               
    return np.array(SuspiciousLT)
    

def DisplaySuspiciousLT(SuspiciousLT) :
    if(SuspiciousLT.shape[0]>0):
        print("Suspicious LT : \n")
        for k in range(SuspiciousLT.shape[0]):
            print( str(k+1) + " : " + SuspiciousLT[k,0] + " - " + SuspiciousLT[k,1] +" : " + str(SuspiciousLT[k,2]) + " mins")
    else : 
        print("Any suspicious lead time")


def GetSheetID(Com_API, SpreadID ,SheetID_Name):
    
    service = Com_API
    
    SpreadSheet = service.get(spreadsheetId=SpreadID).execute()
    
    Sheets = SpreadSheet.get('sheets', '')
    
    for i in range(len(Sheets)):
    
        Title = Sheets[i].get("properties", {}).get("title", "Sheet1")

        if(Title==SheetID_Name):
            SheetID_Int = Sheets[i].get("properties", {}).get("sheetId",0)
        
    return SheetID_Int
 
def GurobiVarToValueList(Branches,LCs,Trucks,Time_Slots_Period,TruckUsedPerPeriod,Transported_Qty_Truck_Br2Br,Path_Truck_LC2Br,Path_Truck_Br2Br,Path_Truck_Br2LC,Transported_Qty_Truck_Br2LC):

    PathTruckBr2BrList=np.full((len(Branches),len(Branches),len(Trucks),len(Time_Slots_Period)), 0)
    PathTruckBr2LcList=np.full((len(Branches),len(LCs),len(Trucks),len(Time_Slots_Period)), 0)
    PathTruckLc2BrList=np.full((len(LCs),len(Branches),len(Trucks),len(Time_Slots_Period)), 0)
    TransportedQtyTruckBr2BrList=np.full((len(Branches),len(Branches),len(Trucks),len(Time_Slots_Period)), 0)
    TransportedQtyTruckBr2LcList=np.full((len(Branches),len(LCs),len(Trucks),len(Time_Slots_Period)), 0)
    TruckPeriodUsingArray=np.full((len(Trucks),len(Time_Slots_Period)),0)
    
    for t in Time_Slots_Period : 
        for c in Trucks:
            if(TruckUsedPerPeriod[c,t].x==1):
                TruckPeriodUsingArray[c][t]=1
            for i in Branches : 
                for j in Branches : 
                    if(Transported_Qty_Truck_Br2Br[i,j,c,t].x>0):
                        TransportedQtyTruckBr2BrList[i][j][c][t]=Transported_Qty_Truck_Br2Br[i,j,c,t].x
                        PathTruckBr2BrList[i][j][c][t]=Path_Truck_Br2Br[i,j,c,t].x
                    else : 
                        TransportedQtyTruckBr2BrList[i][j][c][t]=0
                        PathTruckBr2BrList[i][j][c][t]=Path_Truck_Br2Br[i,j,c,t].x
                for l in LCs : 
                    if(Transported_Qty_Truck_Br2LC[i,l,c,t].x>0):
                        
                        TransportedQtyTruckBr2LcList[i][l][c][t]=Transported_Qty_Truck_Br2LC[i,l,c,t].x
                        PathTruckBr2LcList[i][l][c][t]=Path_Truck_Br2LC[i,l,c,t].x
                    else: 
                        TransportedQtyTruckBr2LcList[i][l][c][t]=0
                        PathTruckBr2LcList[i][l][c][t]=0
                for l in LCs : 
                    if(Path_Truck_LC2Br[l,i,c,t].x>0):
                        PathTruckLc2BrList[l][i][c][t]=Path_Truck_LC2Br[l,i,c,t].x
                    else:
                        PathTruckLc2BrList[l][i][c][t]=Path_Truck_LC2Br[l,i,c,t].x
    
    FinalDict = {'Br to Br Path':PathTruckBr2BrList, 'Br to Lc Path':PathTruckBr2LcList,'Lc to Br Path' :PathTruckLc2BrList, 'Br to Br Qty':TransportedQtyTruckBr2BrList, 'Br to Lc Qty':TransportedQtyTruckBr2LcList, 'Truck per Period':TruckPeriodUsingArray}
    
    return FinalDict

