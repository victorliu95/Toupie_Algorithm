# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 12:27:28 2020

@author: Auto1-PCP294
"""

import sys
import gurobipy as gp 
from gurobipy import GRB
import numpy as np
from DisplayingSolution import * 
from DataExtraction import *
from Zone_LC_Branches_ObjProg import * 
from geopy import distance
from geopy import geocoders
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from RouteOrganizer import *
from WrittingSolInSpreadSheets import * 
from Utils import *



def ProblemSolving(Zone,SheetID,NumberOfPeriod,Setting,OutPutSpreadsheet):
    
    ### Time Matrix Calculation ###

    
    TimeMatrixBr2Br, TimeMatrixLc2Br = ComputeNodesDistances(Zone)
         
    ########################## Input Datas ##########################
    
    Branch_Name=Zone.BuildingBrNamesList()
    LC_Name=Zone.BuildingLcsNamesList()
    
        
    
    TimeSlotNames={'1 Period':['8h00 et 18h00'],'2 Periods':[" 8h00 et 13h00 ", " 14h00 et 18h00 "]}
    StartingTimes={'1 Period':[8],'2 Periods':[8,13]}
    Time_Period_In_Mins  ={'1 Period': np.array([600*Setting]),'2 Periods':np.array([300,300])}
    Time_Slots = {'1 Period' : range(1) , '2 Periods' : range(2)}

    
    Branches = range(len(Zone.BranchesList))
    LCs = range(len(Zone.LcList))
    Trucks = range(10)
    Maximal_Number_Path = len(Branches)*len(Branches)
    
    
    ### Datas about Branches ###  
    Time_Br2Br     = TimeMatrixBr2Br
    Demand_Cars_Br =  Zone.DemandList
    Time_In_Br     =  Zone.BuildingBrTimeIn()
    Time_Out_Br    =  Zone.BuildingBrTimeOut()
    
    
    #############################
    
    
    ### Datas about LC ###
    Time_Load_1_Car_Br    =  Zone.BuildingBrLoadingTime()
    Time_LC2Br            =  TimeMatrixLc2Br
    Time_In_LC            =  Zone.BuildingLcTimeIn()
    Time_Out_LC           =  Zone.BuildingLcTimeOut()
    Time_Offload_1_Car_LC =  Zone.BuildingLcOffLoadingTime()
    
    ######################
    
    
    ### Datas about trucks ###
    
    Truck_Capacity = 8
    Fixed_Cost_Truck =  750
    
    ##########################
    
    #################################################################
    
    ##### Decision Variables ######
    
    model = gp.Model('Remarketing_algorithm_optimization')
    
    ### Integer variables meaning transported cars by a truck between two points (Branch/Logistic Center) ###
    
    Transported_Qty_Truck_Br2Br = model.addVars(Branches,Branches,Trucks, Time_Slots[NumberOfPeriod], vtype=GRB.INTEGER, name="Transported_Qty_Truck_Br2Br")
    Transported_Qty_Truck_Br2LC = model.addVars(Branches,LCs,Trucks, Time_Slots[NumberOfPeriod],vtype=GRB.INTEGER,name="Transported_Qty__Truck_Br2LC")
    Transported_Qty_Truck_LC2Br = model.addVars(LCs,Branches,Trucks, Time_Slots[NumberOfPeriod], vtype=GRB.INTEGER, name="Transported_Qty_Truck_LC2Br")
    
    ### Binary Variables meaning if path used or not by a truck between two points (Branch/Logistic center) ###
    
    Path_Truck_Br2Br = model.addVars(Branches,Branches,Trucks, Time_Slots[NumberOfPeriod], vtype=GRB.BINARY,name="Path_Truck_Br2Br")
    Path_Truck_Br2LC = model.addVars(Branches,LCs,Trucks, Time_Slots[NumberOfPeriod],vtype=GRB.BINARY, name="Path_Truck_Br2LC")
    Path_Truck_LC2Br = model.addVars(LCs,Branches, Trucks, Time_Slots[NumberOfPeriod],vtype=GRB.BINARY, name="Path_Truck_LC2Br")
    
    ### Binary variables meaning if a truck is used or not ###
    
    Truck = model.addVars(Trucks,lb=0, vtype=GRB.BINARY, name="Truck")
    
    ################################
    
    ### Binary variable meaning if a truck is used of not during a period t ###
    
    TruckUsedPerPeriod = model.addVars(Trucks,Time_Slots[NumberOfPeriod],lb=0, vtype=GRB.BINARY, name="TruckUsedPerPeriod")
    
    ###########################################################################
    
    ### Objective ###
    
    model.setObjective(sum(Truck[i]*Fixed_Cost_Truck for i in Trucks) + sum(Path_Truck_Br2Br[i,j,c,t]*(1+Time_Br2Br[i,j]) for i in Branches for j in Branches for c in Trucks for t in Time_Slots[NumberOfPeriod]) + sum((Path_Truck_Br2LC[i,l,c,t]+Path_Truck_LC2Br[l,i,c,t])*Time_LC2Br[l,i] for i in Branches for l in LCs for c in Trucks for t in Time_Slots[NumberOfPeriod]), GRB.MINIMIZE)
    #################
    model.write('RemarketingflowsPY.lp')
    ### Constraints ###
    
    # Flows constraint #
    
    for i in Branches : 
        model.addConstr((sum(Transported_Qty_Truck_Br2Br[j, i, c, t] for j in Branches for c in Trucks for t in Time_Slots[NumberOfPeriod]) + Demand_Cars_Br[i] == sum(Transported_Qty_Truck_Br2Br[i, k, c, t] for k in Branches for c in Trucks for t in Time_Slots[NumberOfPeriod]) + sum(Transported_Qty_Truck_Br2LC[i, l, c, t] for l in LCs for c in Trucks for t in Time_Slots[NumberOfPeriod])), "Flows constraint")

    for t in Time_Slots[NumberOfPeriod]:
        for c in Trucks:
            for i in Branches:
                model.addConstr((sum(Transported_Qty_Truck_Br2Br[j, i, c, t] for j in Branches) <= sum(Transported_Qty_Truck_Br2Br[i, k, c, t] for k in Branches) + sum(Transported_Qty_Truck_Br2LC[i, l, c, t] for l in LCs)), "Flows constraint")

    ####################
        
    # Respect of truck capacity #
        
    for t in Time_Slots[NumberOfPeriod]:
        for c in Trucks : 
            for i in Branches :
                for j in Branches :
                    model.addConstr( Transported_Qty_Truck_Br2Br[i, j, c, t] <= Truck_Capacity ) #Respect of truck capacity for each path used between 2 branches
                    
            for i in Branches : 
                for l in LCs :
                    model.addConstr(Transported_Qty_Truck_Br2LC[i, l, c, t] <= Truck_Capacity )  #Respect of truck capacity for each path used between 1 branch and the logistic center
                    model.addConstr(Transported_Qty_Truck_LC2Br[l, i, c, t] <= Truck_Capacity )  #Respect of truck capacity for each path used between the logistic center and 1 branch
                    
    #############################
                
    ### Boolean Truck Variable update ###
    # If a truck is using a path between two nodes of the graph --> The boolean variable of the truck using will be equal to ²
    
    for t in Time_Slots[NumberOfPeriod] :           
        for c in Trucks : 
            model.addConstr(sum(Path_Truck_Br2Br[i,j,c,t] for i in Branches for j in Branches)<=Maximal_Number_Path*TruckUsedPerPeriod[c,t])
            model.addConstr(sum(Path_Truck_Br2LC[i,l,c,t] for i in Branches for l in LCs )==TruckUsedPerPeriod[c,t]) #Truck using --> He finishes at the LC
            model.addConstr(sum(Path_Truck_LC2Br[l,i,c,t] for l in LCs for i in Branches)==TruckUsedPerPeriod[c,t]) #Truck using --> He starts from the LC
    
    #####################################
    
    ### Edge boolean variables updates according to Transported_Qty_Truck variables ###
    # If a quantity is transported between two nodes of the graph, this way we used the path between these two points and the boolean variable that representes the path using will be equal to 1
    
    for t in Time_Slots[NumberOfPeriod] :    
        for c in Trucks : 
            for i in Branches :
                for j in Branches :
                    
                    model.addConstr(Transported_Qty_Truck_Br2Br[i,j,c,t]<=Truck_Capacity*Path_Truck_Br2Br[i,j,c,t])
                    model.addConstr(Transported_Qty_Truck_Br2Br[i,j,c,t]>=0)
                    
                for l in LCs :
                    
                    model.addConstr(Transported_Qty_Truck_Br2LC[i,l,c,t]<=Truck_Capacity*Path_Truck_Br2LC[i,l,c,t])
    
    #################################################################################    
    
    ### Truck routing continuity constraints ###
    
    for t in Time_Slots[NumberOfPeriod] :             
        for c in Trucks : 
            for j in Branches : 
                
                model.addConstr(sum(Path_Truck_Br2Br[i,j,c,t] for i in Branches) + sum(Path_Truck_LC2Br[l,j,c,t] for l in LCs)==sum(Path_Truck_Br2Br[j,k,c,t] for k in Branches)+ sum(Path_Truck_Br2LC[j,l,c,t] for l in LCs)) #If a truck is going to the node j coming from another node or from the logistic center, he must leave to another node (branch) or to the logistic center
    
    ############################################
            
    ### Time period respect ###
    
    # Here, as you can see below, we constrained each truck ativity to a time period representing here the morning period & the afternoon period
    # We approximate the truck activity time with the different parameters like the time to enter, exit the different nodes and also time needed to load and offload cars from the truck
    
    for t in Time_Slots[NumberOfPeriod] : 
        for c in Trucks : 
            #model.addConstr(time_Period[0]<= sum(Path_Truck_Br2Br[i,j,c]*Time_Br2Br[i,j] for i in Branches for j in Branches)+sum(Path_Truck_Br2LC[i,l,c]*(Time_LC2Br[i]+Time_In_LC) for i in Branches for l in LCs)+sum(Path_Truck_LC2Br[l,i,c]*(Time_LC2Br[i]+Time_Out_LC) for i in Branches for l in LCs) + sum(Path_Truck_Br2Br[i,j,c]*(Time_In_Br[j]+Time_Out_Br[i]) for i in Branches for j in Branches)+sum((Transported_Qty_Truck_Br2Br[j,k,c]-Transported_Qty_Truck_Br2Br[k,i,c])/(len(Branches))*Time_Load_1_Car_Br[k] for k in Branches for j in Branches for i in Branches) + sum(Transported_Qty_Truck_Br2LC[i,l,c]*Time_Offload_1_Car_LC for i in Branches for l in LCs))
            model.addConstr(sum(Path_Truck_Br2LC[i,l,c,t]*Time_LC2Br[l,i] for l in LCs for i in Branches)+sum(Path_Truck_Br2Br[i,j,c,t]*Time_Br2Br[i,j] for i in Branches for j in Branches)+sum(Path_Truck_LC2Br[l,i,c,t]*(Time_LC2Br[l,i]+Time_Out_LC[l]) for i in Branches for l in LCs) + sum(Path_Truck_Br2Br[i,j,c,t]*(Time_In_Br[j]+Time_Out_Br[i]) for i in Branches for j in Branches)+sum(Transported_Qty_Truck_Br2LC[i,l,c,t]*Time_Load_1_Car_Br[i] for i in Branches for l in LCs) + sum(Transported_Qty_Truck_Br2LC[i,l,c,t]*Time_Offload_1_Car_LC[l] for i in Branches for l in LCs)<= Time_Period_In_Mins[NumberOfPeriod][t])
    
    ###########################
    
    ### Subtours constraint ###
       
    for t in Time_Slots[NumberOfPeriod] : 
        for c in Trucks : 
            for i in Branches : 
                for j in Branches : 
                    model.addConstr(1-Path_Truck_Br2Br[i,j,c,t]>=Path_Truck_Br2Br[j,i,c,t])
    
    ###########################
                
    ### Path between one point itself elimination constraint ###
    
    for t in Time_Slots[NumberOfPeriod] : 
        for c in Trucks : 
            for i in Branches : 
                    model.addConstr(Path_Truck_Br2Br[i,i,c,t]==0)
    
    ############################################################
        
    ### Trucks Using Constraint ###
                        
    for c in Trucks : 
        model.addConstr(sum(TruckUsedPerPeriod[c,t] for t in Time_Slots[NumberOfPeriod])<=2*Truck[c])
        
    ###############################
        
    ### Constraint to use truck from index i = 0 (in the correct order) ###
        
    for c in range(len(Trucks)-1) :
        model.addConstr(Truck[c]>=Truck[c+1])
        
    #######################################################################   
    
    ### constraint to use the truck in the morning instead of the afternoon if the algo has to choose ###
        
    for c in Trucks :
        for t in range(len(Time_Slots[NumberOfPeriod])-1) : 
            model.addConstr(TruckUsedPerPeriod[c,t]>=TruckUsedPerPeriod[c,t+1])
        
    #####################################################################################################
    
    ### Solving ### 
    
    model.optimize()
    for v in model.getVars():
        if v.X != 0:
            print("%s %f" % (v.Varname, v.X))
    
    ###############
    
    ####################################            
          
    ### Convert Gurobi Variables into into a list containing only variables values ###
                

    GurobiVarDict = GurobiVarToValueList(Branches,LCs,Trucks,Time_Slots[NumberOfPeriod],TruckUsedPerPeriod,Transported_Qty_Truck_Br2Br,Path_Truck_LC2Br,Path_Truck_Br2Br,Path_Truck_Br2LC,Transported_Qty_Truck_Br2LC)                              
    
    PathTruckBr2BrList= GurobiVarDict['Br to Br Path']
    PathTruckBr2LcList= GurobiVarDict['Br to Lc Path']
    PathTruckLc2BrList= GurobiVarDict['Lc to Br Path']
    
    TransportedQtyTruckBr2BrList= GurobiVarDict['Br to Br Qty']
    TransportedQtyTruckBr2LcList= GurobiVarDict['Br to Lc Qty']
    
    TruckPeriodUsingArray= GurobiVarDict['Truck per Period']
    
    
    ### Creating Indexex trajectory list & times trajectory list ###
    
    ListOfTotalTrajectory=BuildIndexTrajectory(Time_Slots[NumberOfPeriod],Trucks,Branches,LCs,Truck,Path_Truck_LC2Br,Path_Truck_Br2Br,Path_Truck_Br2LC)
    ListOfTimesTrajectory=BuildTimesTrajectory(ListOfTotalTrajectory,Zone,len(Branches),StartingTimes[NumberOfPeriod],Time_LC2Br,Time_Br2Br,TransportedQtyTruckBr2BrList,TransportedQtyTruckBr2LcList)
    
                 
    ### Printing solution & KPIs ###
    
    DisplaySolInConsole(PathTruckBr2BrList,PathTruckBr2LcList,PathTruckLc2BrList,TransportedQtyTruckBr2BrList,TransportedQtyTruckBr2LcList,len(Trucks),len(Time_Slots[NumberOfPeriod]),len(Branches),Zone,StartingTimes[NumberOfPeriod],ListOfTotalTrajectory,TimeMatrixBr2Br,TimeMatrixLc2Br,TimeSlotNames[NumberOfPeriod],model.objVal,Fixed_Cost_Truck,TruckPeriodUsingArray,ListOfTimesTrajectory)              
    KPI = GetAndDisplayKPIsInConsole(Truck,Branches,Trucks,LCs,Fixed_Cost_Truck,Time_Slots[NumberOfPeriod],Transported_Qty_Truck_Br2LC)
    DisplayingSolOnMap(Zone.BranchesList,Zone.LcList,TransportedQtyTruckBr2BrList,TransportedQtyTruckBr2LcList,PathTruckBr2BrList,PathTruckBr2LcList,PathTruckLc2BrList,[46.2276,2.2137],len(Trucks),len(Time_Slots[NumberOfPeriod]),ListOfTotalTrajectory,ListOfTimesTrajectory)


    SuspiciousLT = SuspiciousLT=ReportSuspiciousLTIndexes(Zone,TimeMatrixBr2Br,30,ListOfTotalTrajectory)

    WrittenItineraries = WriteSolInSpreadSheet(Truck,len(Trucks),len(Time_Slots[NumberOfPeriod]),ListOfTotalTrajectory,ListOfTimesTrajectory,TransportedQtyTruckBr2BrList,TransportedQtyTruckBr2LcList,Zone,Fixed_Cost_Truck,OutPutSpreadsheet,SheetID,NumberOfPeriod,SuspiciousLT)
    
    
    if len(SuspiciousLT)==0 : 
        
        return model.getVars(), None, WrittenItineraries,KPI

    else :
        return model.getVars(),SuspiciousLT, WrittenItineraries, KPI
    