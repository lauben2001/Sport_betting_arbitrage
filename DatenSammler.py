# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 15:28:52 2023

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




#SCRAPE FUNCTIONS
global DRIVER_LOCATION
DRIVER_LOCATION = "C://Users/benja//OneDrive//Desktop//Sport Betting/ChromeDriver\\chromedriver.exe"

global TYPE_ODDS
TYPE_ODDS = 'CLOSING' # you can change to 'OPENING' if you want to collect opening odds, any other value will make the program collect CLOSING odds

    
def fi(a):
    try:
        driver.find_element("xpath", a).text
    except:
        return False

def ffi(a):
    if fi(a) != False :
        return driver.find_element("xpath", a).text
            
def fffi(a):
    if TYPE_ODDS == 'OPENING':
        try:
            return get_opening_odd(a) 
        except:
            return ffi(a)  
    else:
        return(ffi(a))

def fi2(a):
    try:
        driver.find_element("xpath", a).click()
    except:
        return False

def ffi2(a):
    if fi2(a) != False :
        fi2(a)
        return(True)
    else:
        return(None)

def fi_link(a):
    try:
        b= driver.find_element("xpath", a).get_attribute('href')        
        return b
    except:
        return False

def fi_open_link(new):
  try:
    driver.get(new)
    a= '((//*[starts-with(@class,"flex text-xs max")])[1]//p)[1]'
    driver.find_element("xpath", a).text
    return True 
  except:
    return False

def find_number_odds(sport, type1):
  type1_one_way = ["Correct Score","Half Time/Full Time"]
  type1_two_way=["Home/Away","Over/Under","Asian Handicap","Both Teams to Score","Draw No Bet",]
  type1_three_way= ["1X2","Double Chance","European Handicap"]
  sport_three_way=['soccer', 'rugby-union', 'rugby-league', 'handball','hockey']
  sport_two_way=['baseball','esports','basketball','darts', 'american-football', 'volleyball']
  
  if type1 != None: 
    if type1 in type1_one_way:
      result = 1
    elif type1 in type1_two_way:
      result = 2
    elif type1 in type1_three_way:
      result = 3
    else: 
      result= 0
  else: 
    if sport in sport_two_way: 
      result = 2
    elif sport in sport_three_way:
      result = 3
    else: 
      result= 0
  return result


def generate_link(link, type1, type2, type3=None):
  try:
        #Mit dieser Funktion kann jedes Element auf einer Seite angesteuert werden 
      layer1 = {"1X2":"#1X2;", 
                "Home/Away":"#home-away;",
                "Over/Under":"#over-under;",
                "Asian Handicap":"/#ah;", 
                "European Handicap":"#eh",
                "Both Teams to Score":"#bts;",
                "Odd or Even":"#odd-even;", 
                "Double Chance":"#double;", 
                "Draw No Bet":"#dnb;", 
                "Correct Score":"#cs;", 
                "Half Time/Full Time":"#ht-ft;"}
    
      layer2 = {"FT including OT":"1",
                "Full Time":"2",
                "1st Half":"3",
                "2nd Half":"4",
                "1st Period":"5", 
                "2nd Period":"6",
                "3rd Period":"7", 
                "1Q":"8",
                "2Q":"9", 
                "3Q":"10", 
                "4Q":"11"}
    
      layer3_HTFT = {"Home/Home":"27",
                "Draw/Home":"28",
                "Away/Home":"29",
                "Home/Draw":"30",
                "Draw/Draw":"31",
                "Away/Draw":"32",
                "Home/Away":"33", 
                "Draw/Away":"34",
                "Away/Away":"35"}
    
      layer3_CS = {"0:0":"1", "1:0":"2", "1:1":"3", "0:1":"4","2:0":"5","2:1":"6","2:2":"7","1:2":"8","0:2":"9","3:0":"10","3:1":"11","3:2":"12","3:3":"13","2:3":"14","1:3":"15","0:3":"16","4:4":"17","4:0":"18","4:1":"19","4:2":"20","4:3":"21","3:4":"22","2:4":"23","1:4":"24", 
          "0:4":"25","5:0":"36","5:1":"37","6:0":"38","6:1":"39","0:5":"40","5:1":"41","0:6":"42","1:6":"43","5:2":"44","5:3":"45","5:4":"46","6:2":"47","6:3":"48","7:0":"50","7:1":"51","5:5":"53","2:5":"54","3:5":"55","4:5":"56","2:6":"57","0:7":"60","1:7":"61","8:0":"66",
          "0:8":"65","8:0":"66","9:0":"68","10:0":"69","0:9":"71","0:10":"72"  
      } 
      
    
      if type3 != None and type1 in ["Over/Under","Asian Handicap", "European Handicap"]:
        layer3= str(type3) + ".00;0"
      elif type3 != None and type1 in ["Correct Score"]: 
        layer3= layer3_CS[type3]                                                #To be continued to much options 
      elif type3 != None and type1 in ["Half Time/Full Time"]:
        layer3= layer3_HTFT[type3]  
      else:
        type3=None
    
      sub_link = (link.rsplit("/",1))[0]
    
      if layer1.get(type1)!= None and layer2.get(type2) != None and type3== None:
        sub_link = sub_link + layer1[type1] + layer2[type2]
      elif layer1.get(type1)!= None and layer2.get(type2) != None and type3 != None:
        sub_link = sub_link + layer1[type1] + layer2[type2] +";" + layer3   
      else: 
        sub_link = link
  except:  
      sub_link = link     
  return sub_link


#--------------------------------- TYPE A ----------------------------------------------------------------
def get_data_next_games_typeA(i, link, type1, type2, type3):
    driver.get(global_link)
    reject_ads()
    ffi2('//*[@id="onetrust-accept-btn-handler"]')      #Click away annoying stuff 
    target = '(//*[starts-with(@class,"flex flex-col border-b")]//descendant::a[contains(@class, "flex-col")])[{}]'.format(i)
    #a = ffi2(target)       #We try to retire the click method!
    sub_link = fi_link(target)
    sub_link= generate_link(sub_link, type1, type2, type3)
        
    L = []
    if fi_link(target) != False:
        driver.get(sub_link)
        print('We wait 4 seconds')
        time.sleep(4)
        # Now we collect all bookmaker
        for j in range(1,30): # only first 10 bookmakers displayed
            Book = ffi('((//*[starts-with(@class,"flex text-xs border")])[{}]//p)[1]'.format(j)) # first bookmaker name
            Odd_1=ffi('((//div[contains(@class,"flex text-xs border")])[{}]//div[contains(@class,"flex flex-col items-center")])[1]'.format(j))
            #Unbothered with Errors 
            match = ffi('//div[contains(@class,"flex items-center w-full h-auto")]//p')
            #final_score = "0-0"
            date = ffi('(//div[contains(@class,"flex px")]//child::div)[3]')
            
            print(match, Book, Odd_1, date, i, '/ 500 ')
            L = L + [(match, Book, Odd_1, date)]
            
    return(L)


def scrape_page_next_games_typeA(country, sport, tournament,type1, type2,type3, nmax = 20):
    link = 'https://www.oddsportal.com/{}/{}/{}/'.format(sport, country,tournament)
    DATA = []
    for i in range(1,nmax):
        print(i)
        content = get_data_next_games_typeA(i, link, type1, type2, type3)
        if content != None:
            DATA = DATA + content
    print(DATA)
    return(DATA)


def scrape_next_games_typeA(tournament, sport, country, SEASON,type1, type2,type3, nmax = 30):
    global driver
    ############### NOW WE SEEK TO SCRAPE THE ODDS AND MATCH INFO################################
    DATA_ALL = []
    try:
        driver.quit() # close all widows
    except:
        pass

    driver = webdriver.Chrome(executable_path = DRIVER_LOCATION)
    data = scrape_page_next_games_typeA(country, sport, tournament,type1, type2,type3, nmax)
    DATA_ALL = DATA_ALL + [y for y in data if y != None]
    driver.close()

    data_df = pd.DataFrame(DATA_ALL)
    print(data_df)
    try:
        data_df.columns = ['TeamsRaw', 'Bookmaker', 'OddHome', 'DateRaw']
    except:
        print('Function crashed, probable reason : no games scraped (empty season)')
        return(1)

    data_df["ScoreRaw"] = '0:0'
    ##################### FINALLY WE CLEAN THE DATA AND SAVE IT ##########################
    '''Now we simply need to split team names, transform date, split score'''

    # (0) Filter out None rows
    data_df = data_df[~data_df['Bookmaker'].isnull()].dropna().reset_index()
    data_df["TO_KEEP"] = 1
    for i in range(len(data_df["TO_KEEP"])):
        if len(re.split(':',data_df["ScoreRaw"][i]))<2 :
            data_df["TO_KEEP"].iloc[i] = 0

    data_df = data_df[data_df["TO_KEEP"] == 1]

    # (a) Split team names
    data_df["Home_id"] = [re.split(' - ',y)[0] for y in data_df["TeamsRaw"]]
    data_df["Away_id"] = [re.split(' - ',y)[1] for y in data_df["TeamsRaw"]]

    # (b) Transform date
    data_df["Date"] = [re.split(', ',y)[1] for y in data_df["DateRaw"]]

    # (c) Split score
    data_df["Score_home"] = 0
    data_df["Score_away"] = 0

    # (d) Set season column
    data_df["Season"] = SEASON


    # Finally we save results
    if not os.path.exists('./{}'.format(tournament)):
        os.makedirs('./{}'.format(tournament))
    data_df[['Home_id', 'Away_id', 'Bookmaker', 'OddHome', 'Date', 'Score_home', 'Score_away','Season']].to_csv('./{}/NextGames_{}_{}_08042020.csv'.format(tournament,tournament, SEASON), sep=';', encoding='utf-8', index=False)


    return(data_df)



#---------------------------------------------------------------------------------------------------------

#--------------------------------- TYPE B ----------------------------------------------------------------
def get_data_next_games_typeB(i, link, type1, type2,type3):
    driver.get(global_link)
    reject_ads()
    ffi2('//*[@id="onetrust-accept-btn-handler"]')      #Click away annoying stuff 
    target = '(//*[starts-with(@class,"flex flex-col border-b")]//descendant::a[contains(@class, "flex-col")])[{}]'.format(i)
    #a = ffi2(target)       #We try to retire the click method!
    sub_link = fi_link(target)
    sub_link= generate_link(sub_link, type1, type2,type3)
        
    L = []
    if fi_link(target) != False:
        driver.get(sub_link)
        print('We wait 4 seconds')
        time.sleep(4)
        # Now we collect all bookmaker
        for j in range(1,30): # only first 10 bookmakers displayed
            Book = ffi('((//*[starts-with(@class,"flex text-xs border")])[{}]//p)[1]'.format(j)) # first bookmaker name
            Odd_1=ffi('((//div[contains(@class,"flex text-xs border")])[{}]//div[contains(@class,"flex flex-col items-center")])[1]'.format(j))
            Odd_2=ffi('((//div[contains(@class,"flex text-xs border")])[{}]//div[contains(@class,"flex flex-col items-center")])[2]'.format(j))  
            #Odd_2=ffi('((//div[contains(@class,"flex text-xs max-sm")])[{}]//div[contains(@class,"flex flex-col items-center")])[3]'.format(j))
            #Unbothered with Errors 
            match = ffi('//div[contains(@class,"flex items-center w-full h-auto")]//p')
            #final_score = "0-0"
            date = ffi('(//div[contains(@class,"flex px")]//child::div)[3]')
            
            print(match, Book, Odd_1, Odd_2, date, i, '/ 500 ')
            L = L + [(match, Book, Odd_1, Odd_2, date)]
            
    return(L)


def scrape_page_next_games_typeB(country, sport, tournament,type1, type2,type3, nmax = 20):
    link = 'https://www.oddsportal.com/{}/{}/{}/'.format(sport, country,tournament)
    DATA = []
    for i in range(1,nmax):
        print(i)
        content = get_data_next_games_typeB(i, link, type1, type2,type3)
        if content != None:
            DATA = DATA + content
    print(DATA)
    return(DATA)


def scrape_next_games_typeB(tournament, sport, country, SEASON,type1, type2,type3, nmax = 30):
    global driver
    ############### NOW WE SEEK TO SCRAPE THE ODDS AND MATCH INFO################################
    DATA_ALL = []
    try:
        driver.quit() # close all widows
    except:
        pass

    driver = webdriver.Chrome(executable_path = DRIVER_LOCATION)
    data = scrape_page_next_games_typeB(country, sport, tournament,type1, type2,type3, nmax)
    DATA_ALL = DATA_ALL + [y for y in data if y != None]
    driver.close()

    data_df = pd.DataFrame(DATA_ALL)
    print(data_df)
    try:
        data_df.columns = ['TeamsRaw', 'Bookmaker', 'OddHome', 'OddAway', 'DateRaw']
    except:
        print('Function crashed, probable reason : no games scraped (empty season)')
        return(1)

    data_df["ScoreRaw"] = '0:0'
    ##################### FINALLY WE CLEAN THE DATA AND SAVE IT ##########################
    '''Now we simply need to split team names, transform date, split score'''

    # (0) Filter out None rows
    data_df = data_df[~data_df['Bookmaker'].isnull()].dropna().reset_index()
    data_df["TO_KEEP"] = 1
    for i in range(len(data_df["TO_KEEP"])):
        if len(re.split(':',data_df["ScoreRaw"][i]))<2 :
            data_df["TO_KEEP"].iloc[i] = 0

    data_df = data_df[data_df["TO_KEEP"] == 1]

    # (a) Split team names
    data_df["Home_id"] = [re.split(' - ',y)[0] for y in data_df["TeamsRaw"]]
    data_df["Away_id"] = [re.split(' - ',y)[1] for y in data_df["TeamsRaw"]]

    # (b) Transform date
    data_df["Date"] = [re.split(', ',y)[1] for y in data_df["DateRaw"]]

    # (c) Split score
    data_df["Score_home"] = 0
    data_df["Score_away"] = 0

    # (d) Set season column
    data_df["Season"] = SEASON


    # Finally we save results
    if not os.path.exists('./{}'.format(tournament)):
        os.makedirs('./{}'.format(tournament))
    data_df[['Home_id', 'Away_id', 'Bookmaker', 'OddHome', 'OddAway', 'Date', 'Score_home', 'Score_away','Season']].to_csv('./{}/NextGames_{}_{}_08042020.csv'.format(tournament,tournament, SEASON), sep=';', encoding='utf-8', index=False)


    return(data_df)

#---------------------------------------------------------------------------------------------------------

#--------------------------------- TYPE C ----------------------------------------------------------------
def get_data_next_games_typeC(i, link, type1, type2,type3):
    driver.get(global_link)
    reject_ads()
    ffi2('//*[@id="onetrust-accept-btn-handler"]')      #Click away annoying stuff 
    target = '(//*[starts-with(@class,"flex flex-col border-b")]//descendant::a[contains(@class, "flex-col")])[{}]'.format(i)
    #a = ffi2(target)       #We try to retire the click method!
    sub_link = fi_link(target)
    sub_link= generate_link(sub_link, type1, type2,type3)
        
    L = []
    if fi_link(target) != False:
        driver.get(sub_link)
        print('We wait 4 seconds')
        time.sleep(4)
        # Now we collect all bookmaker
        for j in range(1,30): # only first 10 bookmakers displayed
            Book = ffi('((//*[starts-with(@class,"flex text-xs border")])[{}]//p)[1]'.format(j)) # first bookmaker name
            
            Odd_1=ffi('((//div[contains(@class,"flex text-xs border")])[{}]//div[contains(@class,"flex flex-col items-center")])[1]'.format(j))
            Odd_X=ffi('((//div[contains(@class,"flex text-xs border")])[{}]//div[contains(@class,"flex flex-col items-center")])[2]'.format(j))  
            Odd_2=ffi('((//div[contains(@class,"flex text-xs border")])[{}]//div[contains(@class,"flex flex-col items-center")])[3]'.format(j))
            #Unbothered with Errors 
            match = ffi('//div[contains(@class,"flex items-center w-full h-auto")]//p')
            final_score = ffi('//div[contains(@class,"flex max-sm:gap")]//strong')
            date = ffi('(//div[contains(@class,"flex px")]//child::div)[3]')
            print(match, Book, Odd_1, Odd_X, Odd_2, date, final_score, i, '/ 30 ')
            L = L + [(match, Book, Odd_1, Odd_X, Odd_2, date, final_score)]
                        
    return(L)


def scrape_page_next_games_typeC(country,sport,  tournament, type1, type2,type3, nmax = 20):
    link = 'https://www.oddsportal.com/{}/{}/{}/'.format(sport, country,tournament)
    DATA = []
    for i in range(1,nmax):
        print(i)
        content = get_data_next_games_typeC(i, link, type1, type2,type3)
        if content != None:
            DATA = DATA + content
    print(DATA)
    return(DATA)


def scrape_next_games_typeC(tournament, sport, country, SEASON, type1, type2,type3, nmax = 30):
    global driver
    ############### NOW WE SEEK TO SCRAPE THE ODDS AND MATCH INFO################################
    DATA_ALL = []
    try:
        driver.quit() # close all widows
    except:
        pass

 
    driver = webdriver.Chrome(executable_path = DRIVER_LOCATION)
    data = scrape_page_next_games_typeC(country, sport, tournament,type1, type2,type3, nmax)
    DATA_ALL = DATA_ALL + [y for y in data if y != None]
    driver.close()

    data_df = pd.DataFrame(DATA_ALL)
  
    try:
        data_df.columns = ['TeamsRaw', 'Bookmaker', 'OddHome','OddDraw', 'OddAway', 'DateRaw', 'ScoreRaw']
    except:
        print('Function crashed, probable reason : no games scraped (empty season)')
        return(1)
    temp_score = (data_df.iloc[0, -1])
    data_df["ScoreRaw"] = '0:0'
    ##################### FINALLY WE CLEAN THE DATA AND SAVE IT ##########################
    '''Now we simply need to split team names, transform date, split score'''

    # (0) Filter out None rows
    data_df = data_df[~data_df['Bookmaker'].isnull()].dropna().reset_index()
    data_df["TO_KEEP"] = 1
    for i in range(len(data_df["TO_KEEP"])):
        if len(re.split(':',data_df["ScoreRaw"][i]))<2 :
            data_df["TO_KEEP"].iloc[i] = 0

    data_df = data_df[data_df["TO_KEEP"] == 1]

    # (a) Split team names
    data_df["Home_id"] = [re.split(' - ',y)[0] for y in data_df["TeamsRaw"]]
    data_df["Away_id"] = [re.split(' - ',y)[1] for y in data_df["TeamsRaw"]]

    # (b) Transform date
    data_df["Date"] = [re.split(', ',y)[1] for y in data_df["DateRaw"]]

    # (c) Split score
    data_df["Score_home"] = 0
    data_df["Score_away"] = 0

    # (d) Set season column
    data_df["Season"] = temp_score


    # Finally we save results
    if not os.path.exists('./{}'.format(tournament)):
        os.makedirs('./{}'.format(tournament))
    data_df[['Home_id', 'Away_id', 'Bookmaker', 'OddHome','OddDraw', 'OddAway', 'Date', 'Score_home', 'Score_away','Season']].to_csv('./{}/NextGames_{}_{}.csv'.format(tournament,tournament, SEASON), sep=';', encoding='utf-8', index=False)


    return(data_df)



  
def scrape_oddsportal_next_games(sport = 'football', country = 'france', league = 'ligue-1', season = '2019-2020', nmax = 30, type1 = None, type2 = None, type3=None):
  count_odds= find_number_odds(sport, type1)
  
      
  if count_odds ==2:
    df = scrape_next_games_typeB(tournament = league, sport = sport, country = country, SEASON = season,type1=type1, type2=type2, type3=type3, nmax = nmax)
    df = create_clean_table_two_ways(df)
  elif count_odds== 3:
    df = scrape_next_games_typeC(tournament = league, sport = sport, country = country, SEASON = season,type1=type1, type2=type2,type3=type3, nmax = nmax)
    df = create_clean_table_three_ways(df)
  elif count_odds ==1:
    df = scrape_next_games_typeA(tournament = league, sport = sport, country = country, SEASON = season,type1=type1, type2=type2, type3=type3, nmax = nmax)
    df = create_clean_table_one_ways(df)
  
  return(df)
 
def reject_ads(switch_to_decimal = True):
    # Reject ads
    ffi2('//*[@id="onetrust-reject-all-handler"]')
    ffi2('//*[@id="sg-d-h-desc"]/a')


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


def best_odd_vector(df_raw, specification, df_fees ,Exclu_list):
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
#Clean Functions 
print(os.getcwd())
def create_clean_table_two_ways(df):
  # (a) Count the number of bookmakers
  nbooks = df['Bookmaker'].nunique()
  
  # (b) Assign a number to each game
  L = [0 for i in range(df['Bookmaker'].size)]
  for i in range(1,df['Bookmaker'].size):
    if (df['Date'][i] != df['Date'][i-1]) | (df['Home_id'][i] != df['Home_id'][i-1]) | (df['Away_id'][i] != df['Away_id'][i-1]):
      L[i] = 1

  df['MatchId'] = np.cumsum(L) + 1

  # (c) Create final dataframe containing only one line per match
  df_final = pd.DataFrame(index=range(max(df['MatchId'])), columns=range(7)) #  Home_id, Away_id, Date, Score_home, Score_away, Season, MatchId
  df_final.columns = ['MatchId','Season','Home_id', 'Away_id', 'Date', 'Score_home', 'Score_away']
  c = 0
  for book in df['Bookmaker'].unique():
    print(book)
    df_final['{}_H'.format(book)] = 'Na' # Home victory odds
    df_final['{}_A'.format(book)] = 'Na' # Away victory odds
    for id in range(1, max(df['MatchId']) + 1):
      new_df = df[(df['Bookmaker'] == book) & (df['MatchId'] == id)]
      if new_df.shape[0] > 0:
        #print(id)
        df_final['{}_H'.format(book)].iloc[id-1] = new_df['OddHome'].iloc[0]
        df_final['{}_A'.format(book)].iloc[id-1] = new_df['OddAway'].iloc[0]
        df_final['MatchId'].iloc[id-1] = new_df['MatchId'].iloc[0]
        df_final['Season'].iloc[id-1] = new_df['Season'].iloc[0]
        df_final['Home_id'].iloc[id-1] = new_df['Home_id'].iloc[0]
        df_final['Away_id'].iloc[id-1] = new_df['Away_id'].iloc[0]
        df_final['Date'].iloc[id-1] = new_df['Date'].iloc[0]
        df_final['Score_home'].iloc[id-1] = new_df['Score_home'].iloc[0]
        df_final['Score_away'].iloc[id-1] = new_df['Score_away'].iloc[0]
    c+=1
    
  try : 
    days = df_final['Date'].str[:2]
    months = df_final['Date'].str[3:6]
    years = df_final['Date'].str[7:]
    months[months == 'Jan'] = '01'
    months[months == 'Feb'] = '02'
    months[months == 'Mar'] = '03'
    months[months == 'Apr'] = '04'
    months[months == 'May'] = '05'
    months[months == 'Jun'] = '06'
    months[months == 'Jul'] = '07'
    months[months == 'Aug'] = '08'
    months[months == 'Sep'] = '09'
    months[months == 'Oct'] = '10'
    months[months == 'Nov'] = '11'
    months[months == 'Dec'] = '12'
    date = days + '/' + months + '/' + years
    df_final['Date'] = pd.to_datetime(date, format='%d/%m/%Y')
    df.sort_values(by=['Date'])
  except:
    print('Cannot convert Date into regular Date format')

  return(df_final)

def create_clean_table_three_ways(df):
  # (a) Count the number of bookmakers
  nbooks = df['Bookmaker'].nunique()
  
  # (b) Assign a number to each game
  L = [0 for i in range(df['Bookmaker'].size)]
  for i in range(1,df['Bookmaker'].size):
    if (df['Date'][i] != df['Date'][i-1]) | (df['Home_id'][i] != df['Home_id'][i-1]) | (df['Away_id'][i] != df['Away_id'][i-1]):
      L[i] = 1

  df['MatchId'] = np.cumsum(L) + 1

  # (c) Create final dataframe containing only one line per match
  df_final = pd.DataFrame(index=range(max(df['MatchId'])), columns=range(7)) #  Home_id, Away_id, Date, Score_home, Score_away, Season, MatchId
  df_final.columns = ['MatchId','Season','Home_id', 'Away_id', 'Date', 'Score_home', 'Score_away']
  c = 0
  for book in df['Bookmaker'].unique():
    print(book)
    df_final['{}_H'.format(book)] = 'Na' # Home victory odds
    df_final['{}_D'.format(book)] = 'Na' # Draw odds
    df_final['{}_A'.format(book)] = 'Na' # Away victory odds
    for id in range(1, max(df['MatchId']) + 1):
      new_df = df[(df['Bookmaker'] == book) & (df['MatchId'] == id)]
      if new_df.shape[0] > 0:
        #print(id)
        df_final['{}_H'.format(book)].iloc[id-1] = new_df['OddHome'].iloc[0]
        df_final['{}_D'.format(book)].iloc[id-1] = new_df['OddDraw'].iloc[0]
        df_final['{}_A'.format(book)].iloc[id-1] = new_df['OddAway'].iloc[0]
        df_final['MatchId'].iloc[id-1] = new_df['MatchId'].iloc[0]
        df_final['Season'].iloc[id-1] = new_df['Season'].iloc[0]
        df_final['Home_id'].iloc[id-1] = new_df['Home_id'].iloc[0]
        df_final['Away_id'].iloc[id-1] = new_df['Away_id'].iloc[0]
        df_final['Date'].iloc[id-1] = new_df['Date'].iloc[0]
        df_final['Score_home'].iloc[id-1] = new_df['Score_home'].iloc[0]
        df_final['Score_away'].iloc[id-1] = new_df['Score_away'].iloc[0]
    c+=1
    
  try : 
    days = df_final['Date'].str[:2]
    months = df_final['Date'].str[3:6]
    years = df_final['Date'].str[7:]
    months[months == 'Jan'] = '01'
    months[months == 'Feb'] = '02'
    months[months == 'Mar'] = '03'
    months[months == 'Apr'] = '04'
    months[months == 'May'] = '05'
    months[months == 'Jun'] = '06'
    months[months == 'Jul'] = '07'
    months[months == 'Aug'] = '08'
    months[months == 'Sep'] = '09'
    months[months == 'Oct'] = '10'
    months[months == 'Nov'] = '11'
    months[months == 'Dec'] = '12'
    date = days + '/' + months + '/' + years
    df_final['Date'] = pd.to_datetime(date, format='%d/%m/%Y')
    df.sort_values(by=['Date'])
  except:
    print('Cannot convert Date into regular Date format')

  return(df_final)



def create_clean_table_one_ways(df):
  # (a) Count the number of bookmakers
  nbooks = df['Bookmaker'].nunique()
  
  # (b) Assign a number to each game
  L = [0 for i in range(df['Bookmaker'].size)]
  for i in range(1,df['Bookmaker'].size):
    if (df['Date'][i] != df['Date'][i-1]) | (df['Home_id'][i] != df['Home_id'][i-1]) | (df['Away_id'][i] != df['Away_id'][i-1]):
      L[i] = 1

  df['MatchId'] = np.cumsum(L) + 1

  # (c) Create final dataframe containing only one line per match
  df_final = pd.DataFrame(index=range(max(df['MatchId'])), columns=range(7)) #  Home_id, Away_id, Date, Score_home, Score_away, Season, MatchId
  df_final.columns = ['MatchId','Season','Home_id', 'Away_id', 'Date', 'Score_home', 'Score_away']
  c = 0
  for book in df['Bookmaker'].unique():
    print(book)
    df_final['{}_H'.format(book)] = 'Na' # Home victory odds
    #df_final['{}_A'.format(book)] = 'Na' # Away victory odds
    for id in range(1, max(df['MatchId']) + 1):
      new_df = df[(df['Bookmaker'] == book) & (df['MatchId'] == id)]
      if new_df.shape[0] > 0:
        #print(id)
        df_final['{}_H'.format(book)].iloc[id-1] = new_df['OddHome'].iloc[0]
        #df_final['{}_A'.format(book)].iloc[id-1] = new_df['OddAway'].iloc[0]
        df_final['MatchId'].iloc[id-1] = new_df['MatchId'].iloc[0]
        df_final['Season'].iloc[id-1] = new_df['Season'].iloc[0]
        df_final['Home_id'].iloc[id-1] = new_df['Home_id'].iloc[0]
        df_final['Away_id'].iloc[id-1] = new_df['Away_id'].iloc[0]
        df_final['Date'].iloc[id-1] = new_df['Date'].iloc[0]
        df_final['Score_home'].iloc[id-1] = new_df['Score_home'].iloc[0]
        df_final['Score_away'].iloc[id-1] = new_df['Score_away'].iloc[0]
    c+=1
    
  try : 
    days = df_final['Date'].str[:2]
    months = df_final['Date'].str[3:6]
    years = df_final['Date'].str[7:]
    months[months == 'Jan'] = '01'
    months[months == 'Feb'] = '02'
    months[months == 'Mar'] = '03'
    months[months == 'Apr'] = '04'
    months[months == 'May'] = '05'
    months[months == 'Jun'] = '06'
    months[months == 'Jul'] = '07'
    months[months == 'Aug'] = '08'
    months[months == 'Sep'] = '09'
    months[months == 'Oct'] = '10'
    months[months == 'Nov'] = '11'
    months[months == 'Dec'] = '12'
    date = days + '/' + months + '/' + years
    df_final['Date'] = pd.to_datetime(date, format='%d/%m/%Y')
    df.sort_values(by=['Date'])
  except:
    print('Cannot convert Date into regular Date format')

  return(df_final)

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
sport_list=["soccer" ,"soccer", "soccer", "soccer", "soccer"]
country_list = ["france", "germany", "england", "england", "italy"]
ligue_list=["ligue-1", "bundesliga","premier-league", "championship","serie-a"]

for nbm in range(len(sport_list)):
  sport= (sport_list[nbm])
  country=(country_list[nbm])
  ligue=(ligue_list[nbm])
  print(sport, country, ligue)
  saison_list = ["2021-2022","2020-2021","2019-2020","2018-2019","2017-2018", "2016-2017"]
  counter = 0
  for saison in saison_list: 
      for page in range(1,8):
              counter = counter +1
              global_link = "https://www.oddsportal.com/{}/{}/{}-{}/results/#/page/{}/".format(sport, country,ligue,saison, page)
              if counter ==1:
                  df_final = scrape_oddsportal_next_games(sport = sport, country = country, league = ligue, season = '2022', nmax = 80, type1="1X2",type2="Full Time")
              else:
                  df_temp = scrape_oddsportal_next_games(sport = sport, country = country, league = ligue, season = '2022', nmax = 80, type1="1X2",type2="Full Time")
                  df_final= pd.concat([df_temp, df_final], axis=0)
      
  #Nach dem Durchlauf einer Liga für 5 Saisons --> Excel Datei     
  speicher_link ="C:/Users/benja/OneDrive/Desktop/Sport Betting/Code/Historische Daten/{}.xlsx".format(ligue) 
  df_final.to_excel(speicher_link)  
  print("Eine weitere Liga iust durchgenudelt")


