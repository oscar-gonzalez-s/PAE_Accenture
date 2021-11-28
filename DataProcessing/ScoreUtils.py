"""
Created on Thurs Nov 18 17:25:00

@author: Laura Rayón 

Purpose: 
  The purpose of this file is to provide the utilities
  for editing the score associated to each instagrammer. 
  Functions may display a broader explanation of their functionalities 
  before their description, this may be useful to fill documentation
  and overall system integration. A more usage-oriented description is
  provided inside each function. 
"""
import numpy as np
import pandas as pd
import json
import sys 

"""
def ScoreUtils(df): 
  #Test for Main Programm:
  #These parameters can be reveived by sys on real implementation. 
  telegram_data = sys.argv[1] #ex: "telegram-data.json"
  history_csv = sys.argv[2] #ex: "telegram-history.csv"
  influencers_csv = sys.argv[3] #ex: "influencers.csv"
  influencer_name = sys.argv[4] #ex: "raquelreitx"
"""
  
def updateScore(upd_phist, gen_tel, telfilepath, infilepath, thistorypath, phistorypath, dataframe, relevance): 
  """
  Main Programm
  """
  # telfilepath= "path/telegram-data.json", infilepath="path/influencers.csv", thistorypath = "path/telegram-history.csv", phistorypath = "path/prediction-history.csv"
  #DONE 
  if gen_tel == True: 
    #update score based on telegram post
    #Compute engagement for the item of the telegram post
    engagement, item, gender = extraxtTelegramStatistics(telfilepath, thistorypath)
    #Look for all influencers that wore this item, put them on a list
    #filtrate by gender first 
    if gender == "WOMAN":
      df = getFilteredDataframe(df,"WOMAN")
    elif gender == "MAN": 
      df = getFilteredDataframe(df,"MAN")
    influencers = influencerHas(df, item)
    #loop through all influencers, updating their score based on the engagement and the relevance parameter
    for influencer_name in influencers: 
      ConfidenceEditor (infilepath, engagement*relevance, influencer_name)
  #TODO
  if upd_phist == True:
    #update score based on historical data prediction
    #Look for all influencers that wore this item, put them on a list
    None 

"""
  confidenceEditor(filename, success_rate, influencer_name) 
Receives:
  - .csv file containing 3 columns: instagrammer name, instagrammer gender, instagrammer score. 
  - Instagrammer name (the instagrammer that was published that week as the trend predictor)
  - Percentage of success (can be positive or negative, will be computed comparing the 
    interaction success of the post in the telegram channel with the medium interaction 
    value of the telegram channel)
Returns:
  - Modified .csv.

Assumptions:
  - Instagrammers won't change in the initial programm. 
  - Scores are initialized to a 0.5 value 

Possible improvements to this function: 
  - See if there's a new instagrammer, if so, add it to the list.
  - Receive two percentages, one from telegram (already implemented), 
    and another from data processing predictions from the next weeks,
    ensuring if the item selected as trend has experienced an increase
    in #times emergence (meaning success in trend prediction). 
"""

def confidenceEditor (filename, success_rate, influencer_name):
  """Receives a csv (filename), an influencer name and the 
     percentage in which the score of the influencer must be
     modifyed (positively or negatively).
     Example: ConfidenceEditor("influencers.csv", -0.05 ,"raquelreitx")"""

  # reading the csv file
  df = pd.read_csv("influencers.csv")
  #Count #influencers present in file 
  length = pd.read_csv(filename, usecols=[0])
  length = length.values.shape[0]
  #Update the score value of the selected influencer 
    #search influencer (column 1, all rows)
  for i in range (length):
    if str(df.loc[i, 'username']) == influencer_name:
      #Update score
      df.loc[i, 'score'] = float(df.loc[i, 'score'])*(1+success_rate) 
      #if update score is out of bounds, correct 
      if df.loc[i, 'score']>1:
        df.loc[i, 'score'] = 1
      elif df.loc[i, 'score']<0:
        df.loc[i, 'score'] = 0

  # writing into the file
  df.to_csv(filename, index=False)
  
"""
  extractTelegramStatistics(filename, historyfile)
Receives:
  - .json file from telegram, containing the results of the 
    survey of the week, must have this shape: 
    [{"text": "Si", "voter_count": 2, "item": "camiseta roja", "gender": "WOMAN"}, {"text": "No", "voter_count": 1, "item": "camiseta roja", "gender": "WOMAN"}]
  - historical .csv where survey results from past weeks are stored. Must
    be this shape: 
    [item, gender, yes_votes, no_votes,	total_votes, average_yes_proportion]

Returns: 
  - percentage of yes engagement with respect to the mean, this percentage
    goes from [-1, 1]. This percentage will go directly to modify the 
    instagrammer score. 
  - The item that has achieved this engagement.
  - The gender to which this item is associated. 
    
Assumptions: 
  - Information received in the .json file must have not been received before.
    Meaning survey results will be feeded to the function only one time.
  - Following bullet one, this function will be called with the same periodicity 
    as telegram posts are posted. 
    
Possible improvements to this function:
  - For now, mean engagement is calculated with both women and men posts. Possible
    improvement could include calculating mean engagement for women's and men's
    posts separately. 
"""

def extraxtTelegramStatistics(filename, historyfile): 
  """Receives .json file from telegram and historical .csv to modify
     Considers that the information received in filename has not been
     received before. 
     telegram-data.json is expected to be: 
     [{"text": "Si", "voter_count": 2, "item": "camiseta roja", "gender": }, {"text": "No", "voter_count": 1, "item": "camiseta roja"}]
     telegram-history.csv is expected to be:
     gender, item, yes_votes, no_votes,	total_votes,	average_yes_proportion
     
     Returns the percentage of yes engagement with respect to the mean, not taking into account 
     the gender. This percentage goes from [-1, 1]
  """
  # EXTRACT JSON DATA
  #Read .json file 
  with open(filename) as f:
    data = json.load(f)

  #Create data frame
  df = pd.DataFrame(columns=["text", "voter_count", "item", "gender"])

  #Put data into dataframe
  for i in range(0,len(data)):
    # i=0 Yes votes
    # i=1 No votes
    df.loc[i] = [data[i]["text"], data[i]["voter_count"], data[i]["item"], data[i]["gender"]]

  #Change the type of variables string to int
  df['voter_count']=df['voter_count'].astype(int)

  #Extract item
  item = df.loc[0][2]
  
  #Extract gender
  gender = df.loc[0][3]

  #Count total votes
  total_votes = 0
  for i in range(0,len(df)):
    #df.loc[i][x] -> x=1 references the voter count
    total_votes += df.loc[i][1]

  # MODIFY CSV 
    # read csv file
  dfv = pd.read_csv(historyfile)
    #Count #surveys present in file 
  nsurveys = pd.read_csv(historyfile, usecols=[0])
  nsurveys = nsurveys.values.shape[0]
    #Add data from new survey 
      #Add item 
  dfv.loc[nsurveys, 'item'] = item
      #Add gender
  dfv.loc[nsurveys, 'gender'] = gender
      #Add yes votes
  dfv.loc[nsurveys, 'yes_votes'] = df.loc[0][1]
      #Add no votes 
  dfv.loc[nsurveys, 'no_votes'] = df.loc[1][1]
      #Add total votes 
  dfv.loc[nsurveys, 'total_votes'] = total_votes
    #Recompute average yes proportion ignoring gender
  actualyesprop = df.loc[0][1]/total_votes
  if nsurveys > 1: 
    pastyesprop = dfv.loc[nsurveys-1, 'average_yes_proportion']
    newyesprop = pastyesprop + 1/nsurveys*(actualyesprop-pastyesprop)
  else: 
    newyesprop = actualyesprop
    pastyesprop = actualyesprop

    #Modify average yes proportion 
  dfv.loc[nsurveys, 'average_yes_proportion'] = newyesprop;

   #Writing into the file
  dfv.to_csv(historyfile, index=False)
   
   #Return percentage of yes engagement with respect to the mean
  print("Actual = ", actualyesprop)
  print("Past = ", pastyesprop)
  engagement = actualyesprop/pastyesprop-1 
  return engagement, item, gender


"""
  influencerHas(dataframe, item)
Receives:
  - dataframe obtained from recognition-output.json file, filtered by gender. 
  - item that will be searched in the influencers pictures.
  
Returns: 
  - list of the influencers that have worn the selected item on the pictures
  analysed that week, portrayed in recognition-output.json file.
    
Assumptions: 
  - None remarkable 
  
Possible improvements to this function:
  - None.
"""

def influencerHas (dataframe, item): 
  """Returns a list of the influencers who have been seen wearing 'item'."""
  influencers = []
  #Look for all influencers that had this item on dataframe, put them on a list
  for i in range(len(dataframe['user'])):
    if (item == dataframe['item0'][i] or item == dataframe['item1'][i]):
      influencers.append(dataframe['user'][i])
  #Delete repeated elements from the list, distorted order is not important
  influencers = list(set(influencers))
  return influencers

