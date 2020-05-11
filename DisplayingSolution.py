# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:06:06 2020

@author: Auto1-PCP294
"""
from geopy.geocoders import Nominatim
from Zone_LC_Branches_ObjProg import *
import folium 
from folium import plugins
import numpy as np
from Utils import * 
from RouteOrganizer import * 
from DataExtraction import *


def AddAntPath(LatLong1,LatLong2,Color,PopUp,ToolTip,Map):
    plugins.AntPath((LatLong1,LatLong2),color=Color,popup=PopUp,tooltip=ToolTip).add_to(Map)
            
def DisplayingSolOnMap(BranchesList, LcList, TransportedQtyTruckBr2BrList, TransportedQtyTruckBr2LcList,PathTruckBr2BrList,PathTruckBr2LcList,PathTruckLc2BrList,ClusterCenter,NumberOfTruck,NumberOfPeriod,ListOfTotalTrajectory,ListOfTimesTrajectory):

    
### TO KNOW : For the lists like BranchesList, LcList given as inputs for the function, we will get them throught the oriented object file. These two lists will be the returns of the functions : BuildingBrList & BuildingLcList
### TO KNOW : For others lists, we will get them throught the algorithm file after solving 
### TO KNOW : considering the fact that we didn't link yet the oriented object programing file with the main algortihm, we will construct the two lists BranchesList, LcList with loops to do tests and corrections. After the merging time between the two last files, we won't need anymore creating those two lists 

    ### Initializing part ### Creating empty lists, maps and also the geolocator ###
    
    LatLongBr = []
    LatLongLc = []
    Colors = ["blue","purple","green","red","orange","black","brown","pink","yellow"] ### Each truck will have its own color on the maps relatively to its index 
    MorningMap = folium.Map(location=ClusterCenter,zoom_start=20)
    AfternoonMap = folium.Map(location=ClusterCenter,zoom_start=20)
    Maps=[MorningMap,AfternoonMap]
    MapsNames=['MorningRoutingsMap','AfternoonRoutingsMap']
    
##############################################################################
    
### Putting markers on the map : Branches & LC ###
    
    ### Branches Markers###
    
    for i in range(len(BranchesList)):
        
        LongLat=convertToTuple(BranchesList[i].GetLatLong())
        ItemLatLongBr=(LongLat[0],LongLat[1])
        
        LatLongBr.append(ItemLatLongBr)
        Info=str(BranchesList[i].GetName()) + " has a demand of " + str(BranchesList[i].GetDemand()) + " cars"
        folium.Marker(LatLongBr[i],popup=Info, icon=folium.Icon(color='blue')).add_to(MorningMap)
        folium.Marker(LatLongBr[i],popup=Info,icon=folium.Icon(color='blue')).add_to(AfternoonMap)
    
    #######################    
    
    ### LC Markers ###
    
    for i in range(len(LcList)):
        
        LongLat=convertToTuple(LcList[i].GetLatLong())
        ItemLatLongLc=(LongLat[0],LongLat[1])
        LatLongLc.append(ItemLatLongLc)
        folium.Marker(LatLongLc[i],popup=LcList[i].GetName(),icon=folium.Icon(color='red')).add_to(MorningMap)
        folium.Marker(LatLongLc[i],popup=LcList[i].GetName(),icon=folium.Icon(color='red')).add_to(AfternoonMap)
        
    ##################
        
##################################################   

### Representing flows of cars between nodes of the graph #### 
    
    for t in range(len(ListOfTotalTrajectory)):
        
        
        ### To draw properly the flows within the map, we consider every path that trucks can take 
        
        ### Drawing Maps ### 
        for c in range(len(ListOfTotalTrajectory[t])):
            if(len(ListOfTotalTrajectory[t][c])>0):
                
                # Last Path Br --> Lc
                PathIndexes=ListOfTotalTrajectory[t][c][len(ListOfTotalTrajectory[t][c])-1]
                PathTimes = ListOfTimesTrajectory[t][c][len(ListOfTotalTrajectory[t][c])-1]
                
                PopUp= " The truck " + str(c+1) + " transports "  + str(TransportedQtyTruckBr2LcList[PathIndexes[0]][PathIndexes[1]][c][t]) + " cars."
                ToolTip=str(ReturningDepartureTime(BranchesList[PathIndexes[0]].GetName(), PathTimes[0]))+" || "+ str(ReturningArrivalTime(LcList[PathIndexes[1]].GetName(),PathTimes[1]))
                
                plugins.AntPath((LatLongBr[PathIndexes[0]],LatLongLc[PathIndexes[1]]),color=Colors[c],popup=PopUp,tooltip=ToolTip).add_to(Maps[t])
                
                for i in range(len(ListOfTotalTrajectory[t][c])-2):
                     # Path Br --> Br    
                    PathIndexes=ListOfTotalTrajectory[t][c][i+1]
                    PathTimes = ListOfTimesTrajectory[t][c][i+1]
                    
                    PopUp=" The truck " + str(c+1) + " transports "  + str(TransportedQtyTruckBr2BrList[PathIndexes[0]][PathIndexes[1]][c][t]) + " cars."
                    ToolTip=str(ReturningDepartureTime(BranchesList[PathIndexes[0]].GetName(), PathTimes[0]))+" || "+str(ReturningArrivalTime(BranchesList[PathIndexes[1]].GetName(),PathTimes[1]))
                    
                    plugins.AntPath((LatLongBr[PathIndexes[0]],LatLongBr[PathIndexes[1]]),color=Colors[c],popup=PopUp,tooltip=ToolTip).add_to(Maps[t])
        Maps[t].save(MapsNames[t]+'.html')
        
        #########################################
        
##############################################################     



### function to display the written solution ###

def DisplaySolInConsole(PathTruckBr2BrList,PathTruckBr2LcList,PathTruckLc2BrList,TransportedQtyTruckBr2BrList,TransportedQtyTruckBr2LcList,NbTrucks,NbPeriods,NbBranches,Zone,StartingTimes,ListOfTotalTrajectory,TimeBr2Br,TimeLc2Br,TimeSlotNames,Obj,FixedCostTruck,TruckPeriodUsingArray,ListOfTimesTrajectory):

    print ("Le coût de la solution est de " + '%g'% Obj + " euros avec un coût fixe par camion de " + str(FixedCostTruck) + " euros et un coût variable de 1 euros/minute d'utilisation.")
    print("Voici quelques paramètres visuels afin d'identifier le résultats du routing plus facilement dans l'affichage écrit : \n" )
    print(" - Les concessions apparaissent en  Bleu. \n")
    print(" - Les centres logistiques apparaissent en Rouge. \n")
    
    TotalDemand=0
    for i in range(NbBranches) : 
        TotalDemand+=Zone.BranchesList[i].GetDemand()
        
    print("La demande totale en voiture à ramasser sur la zone est égale à " +'%g'%TotalDemand + ".")
        
    
    ### TO KNOW : Arrival Time considers the time to enter into the branch/Logistic Center
    ### TO KNOW : Departure time considers the time to exit from Branch/Logistic Center
    
   
    for t in range(NbPeriods):
    
        print ("\n Voici les routings camion entre " + TimeSlotNames[t] + " : \n" )
        
        for c in range(NbTrucks):
            
            ### Start displaying Lc-->1st Br ###*
            
            if(TruckPeriodUsingArray[c][t]==1):
                
                PathTimes=ListOfTimesTrajectory[t][c][0]
                
                PathIndexes=ListOfTotalTrajectory[t][c][0]
                PrintingPathUsedLc2Br(c, Zone.LcList[PathIndexes[0]].GetName(), Zone.BranchesList[PathIndexes[1]].GetName(), '\x1b[31;1m','\x1b[0m','\x1b[34;1m')
                
                PrintingDepartureTime(Zone.LcList[PathIndexes[0]].GetName(), PathTimes[0], '\x1b[31;1m','\x1b[0m')
                
                PrintingArrivalTime(Zone.BranchesList[PathIndexes[1]].GetName(), PathTimes[1],'\x1b[34;1m','\x1b[0m')
                
                print("\n")
                
                ####################################
                
                ### Branch to Branch Displaying ###
                
                if(len(ListOfTotalTrajectory[t][c])>=3):
                    
                    for j in range(len(ListOfTotalTrajectory[t][c])-2):
                        
                        PathTimes=ListOfTimesTrajectory[t][c][j+1]
                        PathIndexes=ListOfTotalTrajectory[t][c][j+1]
                        
                        PrintingPathUsedBr2Br(c,t,PathTimes[0],Zone.BranchesList[PathIndexes[0]].GetName(), Zone.BranchesList[PathIndexes[1]].GetName(), '\x1b[34;1m','\x1b[0m',TransportedQtyTruckBr2BrList,PathIndexes,Zone,NbBranches)
                        
                        PrintingDepartureTime(Zone.BranchesList[PathIndexes[0]].GetName(), PathTimes[0], '\x1b[34;1m','\x1b[0m')
                        
                        PrintingArrivalTime(Zone.BranchesList[PathIndexes[1]].GetName(), PathTimes[1],'\x1b[34;1m','\x1b[0m')
                        print("\n")
                                
                ###################################
                
                ### End Displaying Branch to Lc ###
                
                PathIndexes=ListOfTotalTrajectory[t][c][len(ListOfTotalTrajectory[t][c])-1]
                PathTimes=ListOfTimesTrajectory[t][c][len(ListOfTotalTrajectory[t][c])-1]
                
                
                PrintingPathUsedBr2Lc(c, t,TransportedQtyTruckBr2LcList,TransportedQtyTruckBr2BrList,PathIndexes,NbBranches,Zone.BranchesList[PathIndexes[0]].GetName(), Zone.LcList[PathIndexes[1]].GetName(),'\x1b[34;1m', '\x1b[31;1m', '\x1b[0m' )
                
                PrintingDepartureTime(Zone.BranchesList[PathIndexes[0]].GetName(), PathTimes[0], '\x1b[34;1m','\x1b[0m')
                    
                PrintingArrivalTime(Zone.LcList[PathIndexes[1]].GetName(), PathTimes[1],'\x1b[31;1m','\x1b[0m')
                
                EndTime = PathTimes[1] + TransportedQtyTruckBr2LcList[PathIndexes[0]][PathIndexes[1]][c][t]*Zone.LcList[PathIndexes[1]].GetOffLoadingTime()
                print("\n")

                PrintingEndTimeOffload(EndTime)
                
                print("\n")
                

            ###################################
            

### Function to display KPIs ###

def GetAndDisplayKPIsInConsole(Truck,Branches,Trucks,LCs,Fixed_Cost_Truck,Time_Slots,Transported_Qty_Truck_Br2LC):
    KPI1=0
    KPI2=0
    Total_Truck_Cost=0
    print("Etablissons les KPIs suivants : le coût d'enlèvement par voiture ainsi que le nombre de véhicules enlevés sur la journée : \n")
    for c in Trucks :
        Total_Truck_Cost+=Truck[c].x*Fixed_Cost_Truck
        for t in Time_Slots : 
            for i in Branches : 
                for l in LCs :
                    KPI1 += Transported_Qty_Truck_Br2LC[i,l,c,t].x 
    KPI2 = Total_Truck_Cost/KPI1
    
    print("- Nombre de voiture enelevé dans la journée : " + str(KPI1) + "\n")
    print("- Coût d'enlévement unitaire : " + '%g'%KPI2 + " euros")
            
    return int(KPI2)
            
################################

def PrintingArrivalTime(ArrivalName, CurrentTime,CouleurStart,CouleurEnd):
    print("Arrivée à " +CouleurStart + ArrivalName + CouleurEnd + " estimée à " + str(CurrentTime//60) + "H" + str(int(CurrentTime%60)))


def PrintingDepartureTime(DepartureName, CurrentTime, CouleurStart,CouleurEnd):
    print("Départ de " + CouleurStart + DepartureName +CouleurEnd + " estimé à " + str(CurrentTime//60) + "H" + str(int(CurrentTime%60)))

def PrintingPathUsedLc2Br(TruckIndex, DepartureName, ArrivalName, DepartureColorStart,ColorEnd,ArrivalColorStart):
    print("- Le camion "+ str(TruckIndex+1) + " part du centre logistique de " + DepartureColorStart +DepartureName+ColorEnd + " pour aller vers la concession " + ArrivalColorStart +  ArrivalName +ColorEnd +":"+ "\n")
    
def PrintingPathUsedBr2Br(TruckIndex,TimeIndex,CurrentTime,DepartureName, ArrivalName, DepartureColorStart,ColorEnd,TransportedQtyTruckBr2BrList,PathIndexes,Zone,NbBranches):
    print("-Le camion " + str(TruckIndex+1) + " charge " + str('%g'%(TransportedQtyTruckBr2BrList[PathIndexes[0]][PathIndexes[1]][TruckIndex][TimeIndex]-sum(TransportedQtyTruckBr2BrList[k][PathIndexes[0]][TruckIndex][TimeIndex] for k in range(NbBranches)))) + " voitures de la concession " + DepartureColorStart +  Zone.BranchesList[PathIndexes[0]].GetName() +ColorEnd + " et se dirige vers la concession de " + DepartureColorStart +  Zone.BranchesList[PathIndexes[1]].GetName() +ColorEnd+":"+ "\n")
    
def PrintingPathUsedBr2Lc(TruckIndex, TimeIndex,TransportedQtyTruckBr2LcList,TransportedQtyTruckBr2BrList,PathIndexes,NbBranches,DepartureName, ArrivalName,DepartureColorStart, ArrivalColorStart, ColorEnd ):  
    print("-Le camion "+ str(TruckIndex+1) + " charge " + str('%g'%(TransportedQtyTruckBr2LcList[PathIndexes[0]][PathIndexes[1]][TruckIndex][TimeIndex]-sum(TransportedQtyTruckBr2BrList[k][PathIndexes[0]][TruckIndex][TimeIndex] for k in range(NbBranches)))) + " voitures de la concession " + DepartureColorStart +  DepartureName +ColorEnd + " et se dirige avec une quantité totale de "+ str('%g'%TransportedQtyTruckBr2LcList[PathIndexes[0]][PathIndexes[1]][TruckIndex][TimeIndex])+" voitures au centre logistique de " + ArrivalColorStart + ArrivalName+ColorEnd+":"+ "\n")
    
def PrintingEndTimeOffload(CurrentTime):    
    print("Fin du déchargement estimée à " + str(CurrentTime//60) +"H" + str(int(CurrentTime%60))+"\n")
    
def ReturningArrivalTime(ArrivalName, CurrentTime):
    return "Arrivée à "  + ArrivalName  + " estimée à " + str(CurrentTime//60) + "H" + str(int(CurrentTime%60))


def ReturningDepartureTime(DepartureName, CurrentTime):
    return "Départ de "  + DepartureName  + " estimé à " + str(CurrentTime//60) + "H" + str(int(CurrentTime%60))
    
    

    
    
    
    
   
