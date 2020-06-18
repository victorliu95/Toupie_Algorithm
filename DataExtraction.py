# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 10:38:36 2020

@author: Auto1-PCP294
"""

### File to test Data extract ###
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle
from Utils import *

#from RandomDemandListCreation import * 


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    global  service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    
    return service
##### function that gathers all parts of the data extraction #####

def ExtractData(PbNameList):
    
    ### Initializing API V4 Sheets service ###
    
    #
    ############################

    
    ### SpreadSheets API ###
    
    SpreadSheetsID='1GmJ1m7jhGMeNs8naSTcAoRC7RYtC1U53tnYk8E8203c'
    Demand_SpreadSheets_ID= '1oVH1jGJibGiLIwbFcP1APdfy64j5DbgxkFJh2FidKOc'
    
    # Call the Sheets API
    
    sheet = main().spreadsheets()
    
    
    ### Extracting Branches Information ###
    
    ### Names ###
    
    BranchesNamesProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Branches Info!D3:D163').execute()
    BranchesNames = BranchesNamesProcessing.get('values',[])
    
    #############
    
    ### Adresses ###
    
    BranchesAdressesProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Branches Info!E3:E163').execute()
    BranchesAdresses=BranchesAdressesProcessing.get('values',[])
    
    ################
    
    ### RelativeZones ###
    
    BranchesRelativeZonesProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Branches Info!A3:A163').execute()
    BranchesRelativeZones = BranchesRelativeZonesProcessing.get('values',[])
    
    #####################
    
    ### TimesIn ###
    
    BranchesTimesInProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Branches Info!G3:G163').execute()
    BranchesTimesIn = BranchesTimesInProcessing.get('values',[])
    
    ###############
    
    ### TimesOut ###
    
    BranchesTimesOutProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Branches Info!H3:H163').execute()
    BranchesTimesOut = BranchesTimesOutProcessing.get('values',[])
    
    ################
    
    ### LoadingTimes ###
    
    BranchesLoadingTimesProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Branches Info!I3:I163').execute()
    BranchesLoadingTimes = BranchesLoadingTimesProcessing.get('values',[])
    
    ####################
    
    ### Latitude & Longitude ###
    
    BranchesLatLongProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Branches Info!F3:F163').execute()
    BranchesLatLong = BranchesLatLongProcessing.get('values',[])
    
    ############################
    
    #######################################
    
    ##### Extracting LCs Information #####
    
    ### Names ###
    
    LcsNamesProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='LC Info!C2:C11').execute()
    LcsNames = LcsNamesProcessing.get('values',[])
    
    #############
    
    ### Adresses ###
    
    LcsAdressesProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='LC Info!D2:D11').execute()
    LcsAdresses = LcsAdressesProcessing.get('values',[])
    
    ################
    
    ### RelativeZones ###
    
    LcsRelativeZonesProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='LC Info!A2:A11').execute()
    LcsRelativeZones = LcsRelativeZonesProcessing.get('values',[])
    
    #####################
    
    ### TimesIn ###
    
    LcsTimesInProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='LC Info!E2:E11').execute()
    LcsTimesIn = LcsTimesInProcessing.get('values',[])
    
    ###############
    
    ### TimesOut ###
    
    LcsTimesOutProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='LC Info!F2:F11').execute()
    LcsTimesOut = LcsTimesOutProcessing.get('values',[])
    
    ################
    
    ### OffLoadingTimes ###
    
    LcsOffLoadingTimesProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='LC Info!G2:G11').execute()
    LcsOffLoadingTimes = LcsOffLoadingTimesProcessing.get('values',[])
    
    #######################
    
    ### Latitude & Longitude ###
    
    LCsLatLongProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='LC Info!H2:H11').execute()
    LCsLatLong = LCsLatLongProcessing.get('values',[])
    
    ############################
    
    ######################################
    
    
    ##### Extracting Branches Demands #####
    
    # TO KNOW : Branches demands extraction is special because we're going to read informations from a pivot table. It means that we have only non null branches demands and then we haven't names of all branches. 
    # TO KNOW : This way we are going to create two lists : One with demands and the other with names of branch where the demand is different of 0. 
    # TO KNOW : Once we are going to build branches objects, we will insert a condition to increment the branch demand. 
    
    BranchesDemandsNames=[]
    BranchesDemandsValues=[]
    
        
    NumberOfBranchesWithPositiveDemandProcessing = sheet.values().get(spreadsheetId=Demand_SpreadSheets_ID, range='Toupie_Demand_Algo!E3').execute()
    NumberOfBranchesWithPositiveDemand = NumberOfBranchesWithPositiveDemandProcessing.get('values',[])
    LastRow = 2 + int(NumberOfBranchesWithPositiveDemand[0][0])-1
    rangeDemandNames = 'Toupie_Demand_Algo!A2:A'+str(LastRow)
    rangeDemandValues =  'Toupie_Demand_Algo!B2:B'+str(LastRow)
    
    BranchesDemandsValuesProcessing = sheet.values().get(spreadsheetId=Demand_SpreadSheets_ID, range=rangeDemandValues).execute()
    
    BranchesDemandsNamesProcessing = sheet.values().get(spreadsheetId=Demand_SpreadSheets_ID, range=rangeDemandNames).execute()
    
    #######################################
    
    BranchesDemandsNames += BranchesDemandsNamesProcessing.get('values',[])
    BranchesDemandsValues += BranchesDemandsValuesProcessing.get('values',[])

    ### Branches & LCS Information Lists building ###
    
    InfosBranchesList = []
    InfosLcsList = []
    
    for i in range(len(BranchesNames)):
        for j in range(len(BranchesDemandsValues)):
            if(str(CleanString(BranchesDemandsNames[j][0]))==str(CleanString(BranchesNames[i][0]))): ## Voir comment faire différement pour remplir les demandes dans InfosBranchesList
                
                print(CleanString(BranchesDemandsNames[j][0]))
                print(CleanString(BranchesNames[i][0]))
                BranchDemand = BranchesDemandsValues[j][0]
                print(BranchesDemandsValues[j][0])
                break
            
            else:
                
                BranchDemand=0
                
        BrItem=(BranchesNames[i][0], BranchesAdresses[i][0], int(BranchesTimesIn[i][0]), int(BranchesTimesOut[i][0]), int(BranchesLoadingTimes[i][0]), BranchesRelativeZones[i][0],BranchesLatLong[i][0],int(BranchDemand))
        InfosBranchesList.append(BrItem)
        
    for i in range(len(LcsNames)):
        
        LcItem=(LcsNames[i][0],'Address',int(LcsTimesIn[i][0]),int(LcsTimesOut[i][0]),int(LcsOffLoadingTimes[i][0]),LcsRelativeZones[i][0],LCsLatLong[i][0])
        InfosLcsList.append(LcItem)
    
    ##################################################### 
    
    return InfosBranchesList, InfosLcsList
    
##################################################################
    
def ExtractDataForTesting():
    
    
    ### Initializing API V4 Sheets service ###
    
    main()
    
    ############################
    
    ### SpreadSheets API ###
    
    SpreadSheetsID='12rD6jvhqIh7haa9-WEVORHfuT2JNbKRlIDQvq5hZrms'
    
    # Call the Sheets API
    
    sheet = service.spreadsheets()
    
    ### Extracting Branches Information ###
    
    ### Names ###
    
    BranchesNamesProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Branches infos for Algo!D3:D142').execute()
    BranchesNames = BranchesNamesProcessing.get('values',[])
    
    #############
    
    ### Adresses ###
    
    BranchesAdressesProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Branches infos for Algo!E3:E142').execute()
    BranchesAdresses=BranchesAdressesProcessing.get('values',[])
    
    ################
    
    ### RelativeZones ###
    
    BranchesRelativeZonesProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Branches infos for Algo!A3:A142').execute()
    BranchesRelativeZones = BranchesRelativeZonesProcessing.get('values',[])
    
    #####################
    
    ### TimesIn ###
    
    BranchesTimesInProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Branches infos for Algo!G3:G142').execute()
    BranchesTimesIn = BranchesTimesInProcessing.get('values',[])
    
    ###############
    
    ### TimesOut ###
    
    BranchesTimesOutProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Branches infos for Algo!H3:H142').execute()
    BranchesTimesOut = BranchesTimesOutProcessing.get('values',[])
    
    ################
    
    ### LoadingTimes ###
    
    BranchesLoadingTimesProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Branches infos for Algo!I3:I142').execute()
    BranchesLoadingTimes = BranchesLoadingTimesProcessing.get('values',[])
    
    ####################
    
    ### Latitude & Longitude ###
    
    BranchesLatLongProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Branches infos for Algo!F3:F142').execute()
    BranchesLatLong = BranchesLatLongProcessing.get('values',[])
    
    ############################
    
    #######################################
    
    ##### Extracting LCs Information #####
    
    ### Names ###
    
    LcsNamesProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Toupie_LC_Informations!C2:C11').execute()
    LcsNames = LcsNamesProcessing.get('values',[])
    
    #############
    
    ### Adresses ###
    
    LcsAdressesProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Toupie_LC_Informations!D2:D11').execute()
    LcsAdresses = LcsAdressesProcessing.get('values',[])
    
    ################
    
    ### RelativeZones ###
    
    LcsRelativeZonesProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Toupie_LC_Informations!A2:A11').execute()
    LcsRelativeZones = LcsRelativeZonesProcessing.get('values',[])
    
    #####################
    
    ### TimesIn ###
    
    LcsTimesInProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Toupie_LC_Informations!E2:E11').execute()
    LcsTimesIn = LcsTimesInProcessing.get('values',[])
    
    ###############
    
    ### TimesOut ###
    
    LcsTimesOutProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Toupie_LC_Informations!F2:F11').execute()
    LcsTimesOut = LcsTimesOutProcessing.get('values',[])
    
    ################
    
    ### OffLoadingTimes ###
    
    LcsOffLoadingTimesProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Toupie_LC_Informations!G2:G11').execute()
    LcsOffLoadingTimes = LcsOffLoadingTimesProcessing.get('values',[])
    
    #######################
    
    ### Latitude & Longitude ###
    
    LCsLatLongProcessing = sheet.values().get(spreadsheetId=SpreadSheetsID, range='Toupie_LC_Informations!H2:H11').execute()
    LCsLatLong = LCsLatLongProcessing.get('values',[])
    
    ############################
    
    ######################################
    
    ##### Extracting Zones Information #####
    
    ### Names ###
    
    
    #############
    
    ########################################
    
    ##### Extracting Branches Demands #####
    
    # TO KNOW : Branches demands extraction is special because we're going to read informations from a pivot table. It means that we have only non null branches demands and then we haven't names of all branches. 
    # TO KNOW : This way we are going to create two lists : One with demands and the other with names of branch where the demand is different of 0. 
    # TO KNOW : Once we are going to build branches objects, we will insert a condition to increment the branch demand. 
    
    #######################################

    ### Branches & LCS Information Lists building ###
    
    InfosBranchesList = []
    InfosLcsList = []
    
    for i in range(len(BranchesNames)):
        BrItem=(BranchesNames[i][0], BranchesAdresses[i][0], int(BranchesTimesIn[i][0]), int(BranchesTimesOut[i][0]), int(BranchesLoadingTimes[i][0]), BranchesRelativeZones[i][0],BranchesLatLong[i][0],int(0))
        InfosBranchesList.append(BrItem)
        
    for i in range(len(LcsNames)):
        LcItem=(LcsNames[i][0],LcsAdresses[i][0],int(LcsTimesIn[i][0]),int(LcsTimesOut[i][0]),int(LcsOffLoadingTimes[i][0]),LcsRelativeZones[i][0],LCsLatLong[i][0])
        InfosLcsList.append(LcItem)
    
    #####################################################
    
    return InfosBranchesList, InfosLcsList
