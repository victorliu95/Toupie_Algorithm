# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 09:55:59 2020

@author: Auto1-PCP294
"""
import numpy as np 
from math import *
import math as m
from geopy import * 
import geopy.distance


### Trouver le centre d'un cluster ###

### Data ###

Tab_Point = np.array([[4.85,45.75],[5.7,45.1667]])
Point = range(len(Tab_Point))

def Longitude_Latitude_Max(Tab) :
    LongitudeMax=0
    LatitudeMax=0
    for i in Point :
        if(Tab[i][1]>=LongitudeMax):
            LongitudeMax=Tab[i][1]
        if(Tab[i][0]>=LatitudeMax):
            LatitudeMax=Tab[i][0]
    p = [LatitudeMax,LongitudeMax]
    return p
            
def Longitude_Latitude_Min(Tab) :
    LongitudeMin=float('inf')
    LatitudeMin=float('inf')
    for i in Point :
        if(Tab[i][1]<=LongitudeMin):
            LongitudeMin=Tab[i][1]
        if(Tab[i][0]<=LatitudeMin):
            LatitudeMin=Tab[i][0]
    p = [LatitudeMin,LongitudeMin]
    return p     


# Longitude --> Y // Teta --> Longitude
# Latitude --> X // Phi --> Latitude
    
"""
def Cluster_Center_Sum(Pas,Tab):
    Erreur = float('inf')
    Max = Longitude_Latitude_Max(Tab)
    Min = Longitude_Latitude_Min(Tab)
    X = Min[0]
    DeltaLongitude = Max[0]-Min[0]
    DeltaLatitude = Max[1]-Min[1]
    for i in range(Pas):
        X = X + DeltaLongitude/Pas
        Y = Min[1] 
        for j in range(Pas):
            Y = Y + DeltaLatitude/Pas
            print(DeltaLatitude/Pas)
            Pivot = sum(6000*m.acos(m.cos(X)*m.cos(Tab[k][0]) + m.sin(X)*m.sin(Tab[k][0])*m.cos(Tab[k][1]-Y)) for k in range(len(Tab)))
            if (Erreur>=Pivot):
                #print(X,Y)
                Center=[X,Y]
    
    return Center
    
print(Cluster_Center_Sum(50,Tab_Point))                
"""  
              
def Cluster_Center_Min_Max(Pas,Tab):
    #Erreur = float('inf')
    Max = Longitude_Latitude_Max(Tab)
    Min = Longitude_Latitude_Min(Tab)
    X = Min[0]
    List_Max=[]
    ## Pour les deltas on prend les coordonnées approximant les quatre coins de la france
    DeltaLongitude = 10#(Max[1]- Min[1])*10 #8.130568968315126+5.485383463840483
    DeltaLatitude = 10#(Max[0] - Min[0])*10  #51 - 43
    for i in range(Pas):
        X = X +  DeltaLatitude/Pas
        Y = Min[1] 
        Distance_Max=0
        for j in range(Pas):
            Y = Y + DeltaLongitude/Pas
            for k in Point : 
                coord1 = (Tab_Point[k][0],Tab_Point[k][1])
                coord2 = (X,Y)
                if(geopy.distance.geodesic(coord1, coord2).km>=Distance_Max):
                    Distance_Max=geopy.distance.geodesic(coord1, coord2).km
                    p=[X,Y,Distance_Max]
            List_Max.append(p)
    Pivot = float('inf') 
    for l in range(Pas*Pas) : 
        if(List_Max[l][2]< Pivot):
            Pivot = List_Max[l][2]
            Index = l 
    return List_Max[Index]
        
print(Cluster_Center_Min_Max(100,Tab_Point))      
         
        
       
      
            
          
    
   
    
































