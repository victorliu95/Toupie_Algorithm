# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 11:38:29 2020

@author: Auto1-PCP294
"""

import numpy as np;
from DataExtraction import * 
from math import * 
import math as m



##### Data reading #####

class Branch(object): 
    
     def InitBr(self, Name, Address, TimeIn, TimeOut, LoadingTime, RelativeZone,LatLong,Demand):
         self.Name=Name
         self.Address=Address
         self.Demand=Demand
         self.TimeIn=TimeIn
         self.TimeOut=TimeOut
         self.LoadingTime=LoadingTime
         self.RelativeZone=RelativeZone
         self.LatLong=LatLong

##### Constructors & getFunctions #####   
         
     def GetName(self):
         return str(self.Name)
     def GetAddress(self):
         return str(self.Address)
     def GetDemand(self):
         return self.Demand
     def GetTimeIn(self):
         return self.TimeIn
     def GetTimeOut(self):
         return self.TimeOut
     def GetLoadingTime(self):
         return self.LoadingTime
     def GetBrRelativeZone(self):
         return str(self.RelativeZone)
     def GetLatLong(self):
         return self.LatLong
     def SetDemand(self,Demand):
         self.Demand=Demand
#######################################    
    
class Lc(object):
    def InitLc(self, Name, Address, TimeIn, TimeOut, OffLoadingTime,RelativeZone,LatLong):
        self.Name=Name
        self.Address=Address
        self.TimeIn=TimeIn
        self.TimeOut=TimeOut
        self.OffLoadingTime=OffLoadingTime
        self.RelativeZone=RelativeZone
        self.LatLong=LatLong

##### Constructors & getFunctions #####   
        
    def GetName(self):
         return str(self.Name)
    def GetAddress(self):
         return str(self.Address)
    def GetTimeIn(self):
         return self.TimeIn
    def GetTimeOut(self):
         return self.TimeOut
    def GetOffLoadingTime(self):
         return self.OffLoadingTime
    def GetLcRelativeZone(self):
        return str(self.RelativeZone)
    def GetLatLong(self):
         return self.LatLong
     
#######################################    

class Supplier(object):
    
    def InitSupplier(self, Name, Address, RelativeZone, LatLong):
        self.Name=Name
        self.Address=Address
        self.RelativeZone=RelativeZone
        self.LatLong=LatLong
        
    
    def GetName(self):
        return self.Name
    
    def GetAddress(self):
        return self.Address
    
    def GetRelativeZone(self):
        return self.RelativeZone 
    
    def GetLatLong(self):
        return self.LatLong
    
    
        
        
class Zone(object):
    
    def InitZone(self, Name):
        self.Name = Name
        self.BranchesList = []
        self.LcList = []
        self.DemandList = []
        self.SupplierList=[]
        

##### Constructors & getFunctions & BuildingFunctions #####           
        
    def GetName(self):
        return self.Name
    def GetBranchesList(self):
        return self.BranchesList
    def GetNumberOfBranchesInZone(self):
        return len(self.BranchesList)
    def GetNumberOfLcInZone(self):
        return len(self.LcList)
    def GetLcList(self):
        return self.LcList    
    def GetDemandList(self):
        return self.DemandList  
    
    def GetTotalDemand(self):
        sum=0
        for i in range(self.GetNumberOfBranchesInZone()):
            sum+=self.BranchesList[i].GetDemand()
        return sum
    
    def AddBranch(self,Branch):
        self.BranchesList.append(Branch)        
    def AddLc(self,Lc):
        self.LcList.append(Lc)
    def RemoveBranch(self,Branch):
        self.BranchesList.remove(Branch)
    
    def GetSupplierList(self):
        return self.SupplierList
    
    
   
### Function to get the list of Branches into the zone ###
        
    def BuildingInZoneBrList(self, FullBranchesList):
        for i in range(len(FullBranchesList)):
            if(str(FullBranchesList[i].GetBrRelativeZone())==self.GetName()):
                self.AddBranch(FullBranchesList[i])

    def UpdatingInZoneBrList(self):
        BrList=[]
        for i in range(len(self.BranchesList)):
            if(self.BranchesList[i].GetDemand()>=1):
                BrList.append(self.BranchesList[i])
        self.BranchesList=BrList
                
                
########################################################## 
                
### Function to get the list of LC into the zone ###
                
    def BuildingInZoneLcList(self, FullLcList):
        for i in range(len(FullLcList)):
            if(FullLcList[i].GetLcRelativeZone()==self.GetName()):
                self.AddLc(FullLcList[i])
            

####################################################
                
### Function to get the list of suppliers into the cluster ###
                
    def BuildingInZoneSupplierList(self,FullSupplierList):
        for i in range(len(FullSupplierList)):
            if(FullSupplierList[i].GetRelativeZone()==self.GetName()):
                self.SupplierList.append(FullSupplierList[i])
                
### Function to get the list of branches demand into the zone ###
                
    def BuildingDemandList(self):
        for i in range(self.GetNumberOfBranchesInZone()):
            self.DemandList.append(self.BranchesList[i].GetDemand())
            
#################################################################
    
    def BuildingBrTimeIn(self):
        TimeInList = []
        for i in range(self.GetNumberOfBranchesInZone()):
            TimeInList.append(self.BranchesList[i].GetTimeIn())
        return TimeInList
    
    def BuildingBrTimeOut(self):
        TimeOutList = []
        for i in range(self.GetNumberOfBranchesInZone()):
            TimeOutList.append(self.BranchesList[i].GetTimeOut())
        return TimeOutList
     
    def BuildingBrLoadingTime(self):
        LoadingTimeList = []
        for i in range(self.GetNumberOfBranchesInZone()):
            LoadingTimeList.append(self.BranchesList[i].GetLoadingTime())
        return LoadingTimeList
    
    def BuildingBrNamesList(self):
        BrNamesList=[]
        for i in range(self.GetNumberOfBranchesInZone()):
            BrNamesList.append(self.BranchesList[i].GetName())
        return BrNamesList
    
    def BuildingLcOffLoadingTime(self):
        OffLoadingTimeList = []
        for i in range(self.GetNumberOfLcInZone()):
            OffLoadingTimeList.append(self.LcList[i].GetOffLoadingTime())
        return OffLoadingTimeList
    
    def BuildingLcTimeIn(self):
        TimeInList = []
        for i in range(self.GetNumberOfLcInZone()):
            TimeInList.append(self.LcList[i].GetTimeIn())
        return TimeInList
    
    def BuildingLcTimeOut(self):
        TimeOutList = []
        for i in range(self.GetNumberOfLcInZone()):
            TimeOutList.append(self.LcList[i].GetTimeOut())
        return TimeOutList
    
    def BuildingLcsNamesList(self):
        LcsNamesList=[]
        for i in range(self.GetNumberOfLcInZone()):
            LcsNamesList.append(self.LcList[i].GetName())
        return LcsNamesList
    
    def BuildingConstantDemandList(self,TotalDemand,NbBranchesViewed):
        for i in range(self.GetNumberOfBranchesInZone()):
            if(i<NbBranchesViewed-1):
                self.BranchesList[i].SetDemand(TotalDemand//NbBranchesViewed)
            
            elif(i==NbBranchesViewed-1):
                self.BranchesList[i].SetDemand(TotalDemand//NbBranchesViewed+TotalDemand%NbBranchesViewed)
            else:
                self.BranchesList[i].SetDemand(0)
                
    def BuildingRandomDemandList(self,TotalDemand,NbBranchesViewed):
        for i in range(self.GetNumberOfBranchesInZone()):
            if(i<NbBranchesViewed):
                if(random.randrange(10,20,1)>14):
                    self.BranchesList[i].SetDemand(int(random.randrange(0,m.ceil(TotalDemand/(0.25*NbBranches))+1,1)))
                else:
                    self.BranchesList[i].SetDemand(0)
            else:
                self.BranchesList[i].SetDemand(0) 
                
    
                
        
 
###########################################################           


class Problem(object):
    
    def InitPb(self):
        self.Name="Toupie_Remarketing_Algorithm"
        self.ZoneList=[]
        self.AllBranchesList=[]
        self.AllLcList=[]
        self.AllSupplierList=[]
        
        
    def GetBrList(self):
        return self.AllBranchesList
    
    def GetLcList(self):
        return self.AllLcList
    
    def GetSupplierList(self):
        return self.AllSupplierList
    
    def BuildingZoneList(self, ListeZone):
        for i in range(len(ListeZone)):
            self.ZoneList.append(ListeZone[i])
            
    def AddZone(self,Zone):
        self.ZoneList.append(Zone)
            
    def BuildingBrList(self,InfoBranchList):
        for i in range(len(InfoBranchList)):
             PivotBranch=InfoBranchList[i]
             Br = Branch()
             Br.InitBr(PivotBranch[0],PivotBranch[1],PivotBranch[2],PivotBranch[3],PivotBranch[4],PivotBranch[5],PivotBranch[6],PivotBranch[7])
             self.AllBranchesList.append(Br)
             
    def BuildingLcList(self, InfoLcList):
        for i in range(len(InfoLcList)):
            PivotLc=InfoLcList[i]
            LogisticCenter = Lc()
            LogisticCenter.InitLc(PivotLc[0],PivotLc[1],PivotLc[2],PivotLc[3],PivotLc[4],PivotLc[5], PivotLc[6])
            self.AllLcList.append(LogisticCenter)
            
    def BuildingSupplierList(self, InfoSupplierList):
        for i in range(len(InfoSupplierList)):
            PivotSupplier=InfoSupplierList[i]
            TruckSupplier=Supplier().InitSupplier(PivotSupplier[0],PivotSupplier[1],PivotSupplier[2],PivotSupplier[3])
            self.AllSupplierList.append(TruckSupplier)
    
    

def CreatingProblemObject(ZoneNameList,TypeOfDataExtraction):
    
    ProblemObject=Problem()
    ProblemObject.InitPb()
    
    InfoBranchesList, InfoLcsList = TypeOfDataExtraction
    ########################################
    
    ### Branches & LCS Building ###
    
    ProblemObject.BuildingBrList(InfoBranchesList)
    ProblemObject.BuildingLcList(InfoLcsList)
    
    ###############################
    
    ##### Zone Building #####
    
    for i in range(len(ZoneNameList)):
        ZoneObject=None
        ZoneObject = Zone()
        ZoneObject.InitZone(ZoneNameList[i][0])
        ProblemObject.AddZone(ZoneObject)
        # Building In Zone branches & Lc lists #
        
        ZoneObject.BuildingInZoneBrList(ProblemObject.GetBrList())
        ZoneObject.BuildingInZoneLcList(ProblemObject.GetLcList())
        ZoneObject.UpdatingInZoneBrList()
        ZoneObject.BuildingDemandList()
    
    ########################################
    
    return ProblemObject
    ### Inputs Lists building ###
    
def CreatingTestProblemObject(ZoneName,TypeOfDataExtraction,TotalDemand,NbBranchesViewed):
    
    ProblemObject=Problem()
    ProblemObject.InitPb()
    
    InfoBranchesList, InfoLcsList = TypeOfDataExtraction

    ########################################
    
    ### Branches & LCS Building ###
    
    ProblemObject.BuildingBrList(InfoBranchesList)
    ProblemObject.BuildingLcList(InfoLcsList)
    
    ###############################
    
    ##### Zone Building #####
    
    ZoneObject = Zone()
    ZoneObject.InitZone(ZoneName)
    ProblemObject.AddZone(ZoneObject)
    # Building In Zone branches & Lc lists #
    
    ZoneObject.BuildingInZoneBrList(ProblemObject.GetBrList())
    ZoneObject.BuildingInZoneLcList(ProblemObject.GetLcList())
    
    ZoneObject.BuildingConstantDemandList(TotalDemand,NbBranchesViewed)
    
    ZoneObject.UpdatingInZoneBrList()
    ZoneObject.BuildingDemandList()
    
    ########################################
    
    return ProblemObject
    
        
        
        
        
        