# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 16:42:41 2023

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
from playsound import playsound
from ScrapeFunctions import *
from Cleaning import *
from AnalysisFunctions import *
from MailAlert import * 
from functools import reduce

general_fee = 0
df_fees = pd.DataFrame(
      {"10x10bet": [general_fee],
        "1xBet": [general_fee],
        "Alphabet": [general_fee],
      "bet-at-home": [general_fee],
      "bet365": [general_fee],
      "bwin": [general_fee],
      "Curebet": [general_fee],
      "Coolbet": [general_fee],
      "GGBET": [general_fee],
      "Interwetten": [general_fee],
      "Lasbet": [general_fee],
      "Marathonbet": [general_fee],
      "Marsbet": [general_fee],
      "Pinnacle": [general_fee],    
      "Unibet": [general_fee],
      "VOBET": [general_fee],
      "William Hill": [general_fee],
      "William Hill": [general_fee],
      })

Exclu_list = ["Alphabet","Marsbet","10x10bet", "VOBET","1xBet","Curebet","GGBET","Lasbet","Marathonbet","Pinnacle","Unibet","William Hill"]


#Final Execution 
sport_list=["soccer"]
country_list = ["germany"]
ligue_list=["bundesliga"]
counter =0
number_games = 22

for nbm in range(len(sport_list)):  
  counter= counter + 1
  sport= (sport_list[nbm])
  country=(country_list[nbm])
  ligue=(ligue_list[nbm])
  print(sport, country, ligue)
  #1. Donwload 1X2 Quotes and create 3 ´vectors [Home, Draw, Away]
  df_raw_data = scrape_oddsportal_next_games(sport = sport, country = country, league = ligue, season = '2022', nmax = number_games +1, type1="1X2",type2="Full Time")
  df_home = best_odd_vector(df_raw = df_raw_data, specification = "Home",col_name="Home", df_fees = df_fees ,Exclu_list =Exclu_list)
  df_draw = best_odd_vector(df_raw = df_raw_data, specification = "Draw",col_name="Draw", df_fees = df_fees ,Exclu_list =Exclu_list)
  df_away = best_odd_vector(df_raw = df_raw_data, specification = "Away",col_name="Away", df_fees = df_fees ,Exclu_list =Exclu_list)
  #2.1 European Handicap: 1 
  df_raw_data = scrape_oddsportal_next_games(sport = sport, country = country, league = ligue, season = '2022', nmax = number_games +1, type1="European Handicap",type2="Full Time", type3=1)  
  df_home_eh1 = best_odd_vector(df_raw = df_raw_data, specification = "Home",col_name="EuroHandicap_1_Home", df_fees = df_fees ,Exclu_list =Exclu_list)
  df_draw_eh1 = best_odd_vector(df_raw = df_raw_data, specification = "Draw",col_name="EuroHandicap_1_Draw", df_fees = df_fees ,Exclu_list =Exclu_list)
  df_away_eh1 = best_odd_vector(df_raw = df_raw_data, specification = "Away",col_name="EuroHandicap_1_Away", df_fees = df_fees ,Exclu_list =Exclu_list) 
  #2.1 European Handicap: -1 
  df_raw_data = scrape_oddsportal_next_games(sport = sport, country = country, league = ligue, season = '2022', nmax = number_games +1, type1="European Handicap",type2="Full Time", type3=-1)  
  df_home_eh_neg_1 = best_odd_vector(df_raw = df_raw_data, specification = "Home",col_name="EuroHandicap_Minus1_Home", df_fees = df_fees ,Exclu_list =Exclu_list)
  df_draw_eh_neg_1 = best_odd_vector(df_raw = df_raw_data, specification = "Draw",col_name="EuroHandicap_Minus1_Draw", df_fees = df_fees ,Exclu_list =Exclu_list)
  df_away_eh_neg_1 = best_odd_vector(df_raw = df_raw_data, specification = "Away",col_name="EuroHandicap_Minus1_Away", df_fees = df_fees ,Exclu_list =Exclu_list)
  #3.1 OverUnder: 0.5 
  df_raw_data = scrape_oddsportal_next_games(sport = sport, country = country, league = ligue, season = '2022', nmax = number_games +1, type1="Over/Under",type2="Full Time", type3=0.5)  
  df_home_ou_05 = best_odd_vector(df_raw = df_raw_data, specification = "Home",col_name="Over/Under_0.5_Home", df_fees = df_fees ,Exclu_list =Exclu_list)
  df_draw_ou_05 = best_odd_vector(df_raw = df_raw_data, specification = "Draw",col_name="Over/Under_0.5__Draw", df_fees = df_fees ,Exclu_list =Exclu_list)
  df_away_ou_05 = best_odd_vector(df_raw = df_raw_data, specification = "Away",col_name="Over/Under_0.5__Away", df_fees = df_fees ,Exclu_list =Exclu_list)

  #3.1 OverUnder: 1.5 
  df_raw_data = scrape_oddsportal_next_games(sport = sport, country = country, league = ligue, season = '2022', nmax = number_games +1, type1="Over/Under",type2="Full Time", type3=1.5)  
  df_home_ou_15 = best_odd_vector(df_raw = df_raw_data, specification = "Home",col_name="Over/Under_1.5_Home", df_fees = df_fees ,Exclu_list =Exclu_list)
  df_draw_ou_15 = best_odd_vector(df_raw = df_raw_data, specification = "Draw",col_name="Over/Under_1.5__Draw", df_fees = df_fees ,Exclu_list =Exclu_list)
  df_away_ou_15 = best_odd_vector(df_raw = df_raw_data, specification = "Away",col_name="Over/Under_1.5__Away", df_fees = df_fees ,Exclu_list =Exclu_list)


  #Merge DataFrames on Match column 
  df_final = reduce(lambda x,y: pd.merge(x,y, on='Match', how='outer'), [df_home, df_draw, df_away,df_home_eh1,df_draw_eh1,df_away_eh1,df_home_eh_neg_1,df_draw_eh_neg_1,df_away_eh_neg_1,df_home_ou_05,df_draw_ou_05,df_away_ou_05,df_home_ou_15,df_draw_ou_15,df_away_ou_15])
 
  print(df_final)
  speicher_link ="C:/Users/benja/OneDrive/Desktop/Sport Betting/Code/Historische Daten/{}.xlsx".format(ligue) 
  df_final.to_excel(speicher_link)