import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

def DataExtraction(recognitionOutput, influencers):
  """ Main DataExtraction function

  Params: 

    - recognitionOutput 
    - influencers
  
  Returns: 

    - df: Posts dataFrame
    - df_item0_w = Top woman clothing item dataFrame with counts and valid flag
    - df_item1_w = Bottom woman clothing item dataFrame with counts and valid flag
    - df_item0_m = Top male clothing item dataFrame with counts and valid flag
    - df_item1_m = Bottom male clothing item dataFrame with counts and valid flag
  """
  #Get the general Dataframe
  df = getGeneralDataframe(recognitionOutput, influencers)
  
  #Split the general Dataframe by gender
  df_w= getFilteredDataframe(df,"WOMAN")
  df_m= getFilteredDataframe(df,"MAN")

  #Get a dataframe with the item types, number of aparitions of the item and it is in the top part of the histogram or not
  df_item0_w = getPossibleTrend(df_w,'item0')
  df_item1_w = getPossibleTrend(df_w,'item1')
  df_item0_m = getPossibleTrend(df_m,'item0')
  df_item1_m = getPossibleTrend(df_m,'item1')

  return df, df_item0_m, df_item1_m, df_item0_w, df_item1_w

def getGeneralDataframe(jsonPath, csvPath):
  """ Funcion to obtain a dataFrame with the data of the Json file
      Parameters: json path """

  csvdata = pd.read_csv(csvPath)
  csvdata = csvdata.set_index("username")

  with open(jsonPath) as f:
    data = json.load(f)

  #Create general data frame
  df = pd.DataFrame(columns=[ "gender","user", "followers","likes", "score","item0", "item1","date" ])

  #Put the data in the data frame
  for i in range(0,len(data['output'])):
    df.loc[i] = [data['output'][i]["gender"],data['output'][i]["user"], data['output'][i]["followers"],data['output'][i]["likes"], csvdata.loc[data["output"][i]["user"]].score, data['output'][i]["item0"], data['output'][i]["item1"],data['output'][i]["date"]]

  #replace empty strig for 0
  df = df.replace(r'^\s*$', 0, regex=True)

  #Change the type of followers and likes variables (String to int)
  df['followers']=df['followers'].astype(int)
  df['likes']=df['likes'].astype(int)

  return df

def getFilteredDataframe(df,gender):
  """ Funcion to obtain a dataFrame filtering the general dataframe by a specific gender
      Parameters: Dataframe, gender (writen in the same format that the json gender parameter) """
  df1 = df[df["gender"] == gender]
  return df1

def getHistogram(df,itemCol,title):
  """ Funcion to obtain a Histogram of the items 
      Parameters: Dataframe, name of the column that contains the item. Example 'item0', title of the histogram """

  #Discard the NA
  df = df[df[itemCol] != "N/A N/A"]

  df[itemCol].value_counts().plot(kind='bar')
  plt.title(title)
  plt.xlabel('Item')
  plt.ylabel('Quantity')
  plt.show()

def getPossibleTrend(df,item):
  """ 
  Function to predict the items that may become trends (discard the top 40% of the histogram)
  Parameters: Dataframe, name of the column that contains the item. Example 'item0' """
  
  df_item = pd.DataFrame(columns=["item","counts"])

  #Discard the NA
  df = df[df[item] != "N/A N/A"]
  
  j=0

  # Get the item and the item number of apparitions
  for i in range(0, len(df[item].value_counts())):
    df_item.loc[j]=df[item].value_counts().index.tolist()[i],df[item].value_counts()[i]
    j=j+1
  
 
  # Discard the top 40% of the histogram
  start = (round(len(df[item].value_counts())*0.4))
  v = [0] * len(df[item].value_counts())

  for i in range(start, len(df[item].value_counts())):
    v[i]=1;

  # Add a new column to the dataframe to control if the item is in the top 40% of the histogram
  df_item['valid'] = v

  return df_item

def showResults(df_w, df_m):
  """ Show a histogram for the top and bottom items of each gender """

  getHistogram(df_w,'item0',"Woman top items histogram")
  getHistogram(df_w,'item1',"Woman bottom items histogram")
  getHistogram(df_m,'item0',"Man top items histogram")
  getHistogram(df_m,'item1',"Man bottom items histogram")
