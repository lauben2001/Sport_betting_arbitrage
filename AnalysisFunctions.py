# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 11:51:17 2023

@author: benja
"""

#All Imports 
import os
import urllib
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import signal
import random
from ScrapeFunctions import *
from Cleaning import *


def odds_analysis(df_SB, sport, df_fees, Exclu_list):
  two_type_sports=['baseball','esports','basketball','darts', 'american-football', 'volleyball']
  df_SB =df_SB.replace("Na",0) 
  Not_Trafo_List=["MatchId","Season","Home_id","Away_id","Date"]  
  for column in df_SB:
    if column not in Not_Trafo_List:
        df_SB[column]=df_SB[column].astype(str)
        df_SB[column]=df_SB[column].astype(float)

  df_SB =df_SB.replace(0, np.nan)
  # USER INPUTS  
  prob_threshold = 1                  #Threshold for Arbitrage
  #Exclu_list = []                     #Exclusion List 
   
  #Copy the df_SB DataFrames for all Sub dfs 
  df_home =df_SB.copy()  
  df_draw =df_SB.copy()
  df_away =df_SB.copy()


  #Lists for Exclusion, Name and ID

  Name_List = ["MatchId",	"Season",	"Home_id",	"Away_id",	"Date"]                #["MatchId","Home_id","Away_id","Date"]
  Id_List = ["_H","_D","_A"]

  #Loop through columns and create the sub dataframes with if checks and deleting columns 
  for column in df_SB:
      if (column[:(len(column)-2)]) in Exclu_list:                #Check if Last two Characters are part of Exclu_list -> YES: Delete            
        del df_home[column]
        del df_draw[column]
        del df_away[column]                                   

      else:                                                      #Type Check -->Delete if specific datatype 
        if not (column[-2] + column[-1]) == "_H":                   
            del df_home[column]
        if not (column[-2] + column[-1]) == "_D": 
            del df_draw[column] 
        if not (column[-2] + column[-1]) == "_A": 
            del df_away[column] 

  #Renaming Columns -> Deduct the last two characters  
  for column in df_home:
    df_home.rename(columns = {column:column[:(len(column)-2)]}, inplace = True)
  for column in df_draw:
    df_draw.rename(columns = {column:column[:(len(column)-2)]}, inplace = True)
  for column in df_away:
    df_away.rename(columns = {column:column[:(len(column)-2)]}, inplace = True)

  #Errorhandling: Align df_fees with df_home to account for missing columns -->They will be deleted in df_fees
  df_fees, df_home = df_fees.align(df_home, join='right', axis=1)

  #Replace all empty values with NaN 
  df_home =df_home.replace("Na",np.nan)
  df_draw= df_draw.replace('Na',np.nan)
  df_away= df_away.replace('Na',np.nan)

  #Empty Containers for final DF 
  game_list = []
  date_list= []
  impli_prob_list = []                   
  home_list= []                   
  draw_list= []
  away_list= []
  home_odd_list = []
  draw_odd_list = []
  away_odd_list = []

  #Adjust the odds for fixed fees [for every row] 
  for row in range(len(df_home.index)):  
    df_home.iloc[row]=df_home.iloc[row]- (df_fees *df_home.iloc[row])
    df_draw.iloc[row]=df_draw.iloc[row]- (df_fees * df_draw.iloc[row]) 
    df_away.iloc[row]=df_away.iloc[row]- (df_fees * df_away.iloc[row])

  if sport not in two_type_sports:                                                #Analysis for the 3 Case 
    #Main Analysis
    for row in range(len(df_home.index)):   
      for col_h in range(len(df_home.columns)):
        for col_d in range(len(df_draw.columns)):     
          for col_a in range(len(df_away.columns)):
            #Berechnung der impli_prob mit den adjustierten Quoten 
            home_odd= df_home.iloc[row, col_h] 
            draw_odd= df_draw.iloc[row, col_d] 
            away_odd= df_away.iloc[row, col_a]               
            impli_prob =(1/home_odd) + (1/draw_odd) + (1/away_odd) 
            if home_odd != np.nan and draw_odd != np.nan and away_odd !=np.nan and impli_prob < prob_threshold:     #Check if Arbitrage   
              #Append the lists with values  
              game_id = df_SB.iloc[row, 2] + " vs " +df_SB.iloc[row, 3]  
              date_list.append(df_SB.iloc[row, 4])
              game_list.append(df_SB.iloc[row, 2] + " vs " +df_SB.iloc[row, 3])          
              impli_prob_list.append(impli_prob)  
              home_list.append(df_home.columns[col_h])           
              draw_list.append(df_draw.columns[col_d])
              away_list.append(df_away.columns[col_a])
              home_odd_list.append(home_odd)
              draw_odd_list.append(draw_odd)
              away_odd_list.append(away_odd)         
    #Create the final DataFrame
    df_trades = pd.DataFrame(
        {"Match": game_list,
          "Date": date_list,
        'Implied Probability': impli_prob_list,
        'Home': home_list,
        'Draw': draw_list,
        'Away': away_list,
        'adj_home_odd': home_odd_list,
        'adj_draw_odd': draw_odd_list,
        'adj_away_odd': away_odd_list    
        })
  
  else:                                                                           #Analysis for the 2 Case
    #Main Analysis
    for row in range(len(df_home.index)):   
      for col_h in range(len(df_home.columns)):     
        for col_a in range(len(df_away.columns)):
          #Berechnung der impli_prob mit den adjustierten Quoten 
          home_odd= df_home.iloc[row, col_h]  
          away_odd= df_away.iloc[row, col_a]               
          impli_prob =(1/home_odd) + (1/away_odd) 
          if home_odd != np.nan and away_odd !=np.nan and impli_prob < prob_threshold:     #Check if Arbitrage   
            #Append the lists with values  
            game_id = df_SB.iloc[row, 2] + " vs " +df_SB.iloc[row, 3]  
            date_list.append(df_SB.iloc[row, 4])
            game_list.append(df_SB.iloc[row, 2] + " vs " +df_SB.iloc[row, 3])          
            impli_prob_list.append(impli_prob)  
            home_list.append(df_home.columns[col_h])           
            away_list.append(df_away.columns[col_a])
            home_odd_list.append(home_odd)
            away_odd_list.append(away_odd)         
    #Create the final DataFrame
    df_trades = pd.DataFrame(
        {"Match": game_list,
          "Date": date_list,
        'Implied Probability': impli_prob_list,
        'Home': home_list,
        'Away': away_list,
        'adj_home_odd': home_odd_list,
        'adj_away_odd': away_odd_list    
        })


  #Sort the final DataFrame & Rescale the index 
  df_trades = df_trades.sort_values(['Date', 'Implied Probability'], ascending=[True, True])
  df_trades = df_trades.reset_index(drop=True)
  #print(df_trades["Implied Probability"].min())
  return df_trades


def best_odd_vector(df_raw, specification,col_name, df_fees ,Exclu_list):
  df_raw =df_raw.replace("Na",0)                                #-->Convert "Na" into 0
  
  Not_Trafo_List=["MatchId","Season","Home_id","Away_id","Date"]  
  for column in df_raw:
    if column not in Not_Trafo_List:
        df_raw[column]=df_raw[column].astype(str)
        df_raw[column]=df_raw[column].astype(float)
  df_raw =df_raw.replace(0,np.nan)      #Convert 0 into np.nan

  ending = {"Home": "_H",
            "Draw":"_D",
            "Away":"_A"}
  
  if ending.get(specification)== None:        #Error Handling: In case of mistakes -->Go for home, bc always there!
    specification = "Home"

  #Delete all irrelevant Columns -->If not relevant with specification  
  df_temp = pd.DataFrame([])
  df_temp["Match"]= df_raw["Home_id"] + " vs. " + df_raw["Away_id"]
  for column in df_raw:
    if (column[-2] + column[-1]) != ending[specification]:
      del df_raw[column]

  #Replace all empty values with NaN 
  df_raw =df_raw.replace("Na",np.nan)
  #Renaming Columns -> Deduct the last two characters  
  for column in df_raw:
    df_raw.rename(columns = {column:column[:(len(column)-2)]}, inplace = True)
  #Errorhandling: Align df_fees with df_home to account for missing columns -->They will be deleted in df_fees
  df_fees, df_raw = df_fees.align(df_raw, join='right', axis=1)
  #Adjust to fees 
  for row in range(len(df_raw.index)):  
    df_raw.iloc[row]=df_raw.iloc[row]- (df_fees *df_raw.iloc[row])
  #Kick items from the exclusion list out!
  for column in df_raw:
    if column in Exclu_list:
      del df_raw[column]
  if len(df_raw.index)!= 0:
    df_raw["adj_odd"]=df_raw.max(axis=1)
    df_raw["Bookie"]=df_raw.idxmax(axis=1, skipna=True)   #This is for the Names
    df_raw = df_raw[['adj_odd', 'Bookie']]
    df_raw["Match"] = df_temp["Match"]
    df_raw = df_raw.rename(columns={'adj_odd': col_name,'Bookie': 'Bookie_' + col_name })
  else:
    print("No Data available for this strategy")
  return df_raw

def multi_odd_analysis(*df_List):
  prob_threshold = 1
  counter = 0
  df_final = pd.DataFrame([])
  for x in df_List:                                                                                           #Loop through every dataframe
    counter = counter +1 
    if counter == 1:                                                                                           #Sonderfall ->erste df
      df_final["Match"] = x["Match"] 
      #df_final= pd.merge(df_final,x)
      df_final["Implied Probability"] = (1/ x["adj_odd"])
      df_final= pd.merge(df_final,x)
    else: 
      df_final= pd.merge(df_final,x)
      df_final["Implied Probability"] = df_final["Implied Probability"] + (1/ df_final["adj_odd"])                       #Alle anderen Dfs
                                                                                                 #Spalte Match löschen
    if hasattr(x, 'name'):
      df_final = df_final.rename(columns={'adj_odd': 'adj_odd_{}'.format(x.name), 'Bookie': 'Bookie_{}'.format(x.name)})      #Rename, if df has a name [Testen, weil sonst Fehler!]
    else:
      df_final = df_final.rename(columns={'adj_odd': 'adj_odd_{}'.format(counter), 'Bookie': 'Bookie_{}'.format(counter)})    #Rename, if df has no name    
    
                                                                                      #Add column to df
  df_final=df_final.drop(df_final[df_final["Implied Probability"] > prob_threshold ].index)                     #Drop irrelevant rows
  df_final = df_final.reset_index(drop=True)                                                                    #Change Index
  return df_final  


