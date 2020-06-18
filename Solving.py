# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 18:10:59 2020

@author: Auto1-PCP294
"""

from Algorithm_Runner import RunAlgorithm

SolOutputRange={'1 Period':'1 Period ToupieOutput!','2 Periods':'2 Periods ToupieOutput!','IDF OUEST':'2P IDF OUEST!','IDF EST':'2P IDF EST!','IDF SUD':'2P IDF SUD!','Haute Normandie':'2P Haute Normandie!','Basse Normandie':'2P Basse Normandie!','Oise':'2P Oise!','Grand Est':'2P Grand Est!','Rhône-Alpes':'2P Rhône-Alpes!','Nord':'2P Nord!'}
SolSpreadSheetId = '1rdCvKgiyFXlhIF121MDFwpoonRBAMUSGKhOHQysoC14'

ItinerariesRange = {'IDF OUEST':'Zone 5 - Capacity & Route planning (J+1)!','IDF EST':'Zone 4 - Capacity & Route planning (J+1)!','IDF SUD':'Zone 6 - Capacity & Route planning (J+1)!','Haute Normandie':'Zone 3 - Capacity & Route planning (J+1)!','Basse Normandie':'Zone 2 - Capacity & Route planning (J+1)!','Oise':'Zone 7 - Capacity & Route planning (J+1)!','Grand Est':'Zone 8 - Capacity & Route planning (J+1)!','Rhône-Alpes':'Zone 9 - Capacity & Route planning (J+1)!','Nord':'Zone 1 - Capacity & Route planning (J+1)!'}
ItinerariesSpreadSheetId = '1oVH1jGJibGiLIwbFcP1APdfy64j5DbgxkFJh2FidKOc'

#ZoneNameList=[["Nord",2]]#,["IDF OUEST",2],["IDF EST",2],["Nord",2],["Haute Normandie",2],["Basse Normandie",2],["Grand Est",2],["Oise",2],["Rhône-Alpes",2]]

#ZoneNameList=[["Nord",2]]
#ZoneNameList=[["Basse Normandie",2]]
#ZoneNameList=[["Haute Normandie",2]]
#ZoneNameList=[["IDF EST",2]]
#ZoneNameList=[["IDF OUEST",2]]
#ZoneNameList=[["IDF SUD",2]]
#ZoneNameList=[["Oise",2]]
#ZoneNameList=[["Grand Est",2]]
ZoneNameList=[["Rhône-Alpes",2]]

RunAlgorithm(ZoneNameList,SolOutputRange,SolSpreadSheetId,ItinerariesRange,ItinerariesSpreadSheetId)
    