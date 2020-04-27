# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:48:58 2020

@author: Auto1-PCP294
"""
import math as m

def SortRouting(List):
    NewList=[]
    Item=List[0]
    NewList.append(List[0])
    if(len(List)>2):
        for i in range(len(List)-1):
            for j in range(len(List)-2):
                if(Item[1]==List[j+1][0]):
                    NewList.append(List[j+1])
                    Item=List[j+1]
    NewList.append(List[len(List)-1])
    return NewList

def BuildIndexTrajectory(Time_Slots,Trucks,Branches,LCs,Truck,Path_Truck_LC2Br,Path_Truck_Br2Br,Path_Truck_Br2LC):      
    ListOfTotalTrajectory=[]
    for t in Time_Slots : 
        ListOfPathTrucks=[]
        for c in Trucks :
            ListOfPathIndex=[]
            if(Truck[c].x>=1):
                for i in Branches : 
                    for l in LCs : 
                        if(Path_Truck_LC2Br[l,i,c,t].x>0):
                            ListOfPathIndex.append((l,i))      
                for i in Branches : 
                    for j in Branches:
                        if(Path_Truck_Br2Br[i,j,c,t].x>0):
                            ListOfPathIndex.append((i,j))
                for l in LCs : 
                    for i in Branches : 
                        if(Path_Truck_Br2LC[i,l,c,t].x>0):
                            ListOfPathIndex.append((i,l))
                if(len(ListOfPathIndex)>=4):
                    ListOfPathTrucks.append(SortRouting(ListOfPathIndex))
                else:
                    ListOfPathTrucks.append(ListOfPathIndex)
        ListOfTotalTrajectory.append(ListOfPathTrucks)
    return ListOfTotalTrajectory

def BuildTimesTrajectory(ListOfTotalTrajectory,Zone,NbBranches,StartingTimes,TimeLc2Br,TimeBr2Br,TransportedQtyTruckBr2BrList,TransportedQtyTruckBr2LcList):
    
    ListOfTimesTrajectory=[]
    for t in range(len(ListOfTotalTrajectory)) : 
        ListOfTimesTrucks=[]
        
        for c in range(len(ListOfTotalTrajectory[t])) : 
            CurrentTime=StartingTimes[t]*60
            ListOfPathTimes=[]
            for k in range(len(ListOfTotalTrajectory[t][c])):
                i=ListOfTotalTrajectory[t][c][k]
                LastItem=ListOfTotalTrajectory[t][c][len(ListOfTotalTrajectory[t][c])-1]
                if(k==0): ### Lc --> Br
                    TimeItem1=CurrentTime
                    CurrentTime+=TimeLc2Br[i[0]][i[1]]+TransportedQtyTruckBr2LcList[LastItem[0]][LastItem[1]][c][t]*Zone.LcList[LastItem[1]].GetOffLoadingTime()+Zone.LcList[LastItem[1]].GetTimeOut()
                    TimeItem2=CurrentTime
                    ListOfPathTimes.append((m.ceil(TimeItem1),m.ceil(TimeItem2)))
                elif(k==(len(ListOfTotalTrajectory[t][c])-1)): ### Br --> Lc
                    CurrentTime+=(TransportedQtyTruckBr2LcList[i[0]][i[1]][c][t] - sum(TransportedQtyTruckBr2BrList[w][i[0]][c][t] for w in range(NbBranches)))*Zone.BranchesList[i[0]].GetLoadingTime()+ Zone.BranchesList[i[0]].GetTimeOut() + Zone.BranchesList[i[0]].GetTimeIn()
                    TimeItem1=CurrentTime
                    CurrentTime+=TimeLc2Br[i[1]][i[0]] #+ Zone.LcList[i[1]].GetTimeIn()
                    TimeItem2=CurrentTime
                    ListOfPathTimes.append((m.ceil(TimeItem1),m.ceil(TimeItem2)))
                else: ### Br --> Br 
                    CurrentTime+=(TransportedQtyTruckBr2BrList[i[0]][i[1]][c][t] - sum(TransportedQtyTruckBr2BrList[k][i[0]][c][t] for k in range(NbBranches))) * Zone.BranchesList[i[0]].GetLoadingTime() + Zone.BranchesList[i[0]].GetTimeIn() +Zone.BranchesList[i[0]].GetTimeOut()
                    TimeItem1=CurrentTime
                    CurrentTime+=TimeBr2Br[i[0]][i[1]]
                    TimeItem2=CurrentTime
                    ListOfPathTimes.append((m.ceil(TimeItem1),m.ceil(TimeItem2)))  
            ListOfTimesTrucks.append(ListOfPathTimes)
        ListOfTimesTrajectory.append(ListOfTimesTrucks)
    return ListOfTimesTrajectory


