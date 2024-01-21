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
from Cleaning import *
from AnalysisFunctions import *

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
            final_score = "0-0"
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

