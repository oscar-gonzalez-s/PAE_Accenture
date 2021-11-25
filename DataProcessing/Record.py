""" Aquest fitxer es una copia de les funcions que teniem a extraccion de Datos pero amb una nova funcio per actualitzar el Record
    S'ha d'afegir el IMPORT de from datetime import date 
    La nova funcio es: actualizeRecord(df_item0_m, df_item1_m, df_item0_w, df_item1_w, 'trend-items.csv', 'items-record.csv')
    TENIU UN MAIN A BAIX d aquest fitxer per veure com cridar la NOVA FUNCIO """


import pandas as pd
import numpy as np
import json
from datetime import date # NOU IMPORT


# FUNCIONS QUE JA TENIEM
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

# NOVA FUNCIO 

def actualizeRecord(df_item0_m, df_item1_m, df_item0_w, df_item1_w, pathItems, pathRecord):  
  """
  Params: 
    - df_item0_m = Top woman clothing item dataFrame with counts and valid flag
    - df_item1_m = Bottom woman clothing item dataFrame with counts and valid flag
    - df_item0_w = Top male clothing item dataFrame with counts and valid flag
    - df_item1_w = Bottom male clothing item dataFrame with counts and valid flag
    - pathItems = the path of the csv that contains the 4 trending items
    - pathRecord = the path of the csv that contains the Record of the trending items ( the first time this file MUST be created and only contains two headers: item,gender)
  
  Returns: 
    This function does not return anything. It updates the csv file that contains the record
  """
  dfTrends = pd.read_csv(pathItems)

  df_item0_m = df_item0_m.set_index("item")
  df_item1_m = df_item1_m.set_index("item")
  df_item0_w = df_item0_w.set_index("item")
  df_item1_w = df_item1_w.set_index("item")

  dfRecord = pd.read_csv(pathRecord) # la primera vegada assumim que posa nomes: item,gender

  #todays date in string format
  today = pd.Timestamp.now().strftime("%d/%m/%Y %H:%M:%Sh")

  #new column for todays record

  dfRecord[today] = np.nan
  leng = len(dfRecord)
  cols= len(dfRecord.columns)

  #create the rows for the new Record
  dfRecord.loc[dfRecord.shape[0]] = np.zeros(cols)
  dfRecord.loc[dfRecord.shape[0]] = np.zeros(cols)
  dfRecord.loc[dfRecord.shape[0]] = np.zeros(cols)
  dfRecord.loc[dfRecord.shape[0]] = np.zeros(cols)

  #calculate new items percentage of aparition 
  percentatge1 = round(df_item0_m.loc[dfTrends["prendas"][0]].counts/sum(df_item0_m["counts"]),4)
  percentatge2 = round(df_item1_m.loc[dfTrends["prendas"][1]].counts/sum(df_item1_m["counts"]),4)
  percentatge3 = round(df_item0_w.loc[dfTrends["prendas"][2]].counts/sum(df_item0_w["counts"]),4)
  percentatge4 = round(df_item1_w.loc[dfTrends["prendas"][3]].counts/sum(df_item1_w["counts"]),4)

  # write the new items record
  dfRecord.loc[leng, ['item', 'gender', today]] =   [dfTrends["prendas"][0],dfTrends["gender"][0],percentatge1]
  dfRecord.loc[leng+1, ['item', 'gender', today]] = [dfTrends["prendas"][1],dfTrends["gender"][1],percentatge2]
  dfRecord.loc[leng+2, ['item', 'gender', today]] = [dfTrends["prendas"][2],dfTrends["gender"][2],percentatge3]
  dfRecord.loc[leng+3, ['item', 'gender', today]] = [dfTrends["prendas"][3],dfTrends["gender"][3],percentatge4]

  #fill the old items actual record with their percentage of apparition in the new trend
  for i in range (leng):
    if(i%4==0 ):
      
      if dfRecord["item"][i] in df_item0_m.index: #si el item antic esta en els nous
        dfRecord.loc[i, [today]] = [round(df_item0_m.loc[dfRecord["item"][i]].counts/sum(df_item0_m["counts"]),4)]
      else:
        dfRecord.loc[i, [today]] = [0]

    elif(i%4==1):
      if dfRecord["item"][i] in df_item1_m.index: #si el item antic esta en els nous
        dfRecord.loc[i, [today]] = [round(df_item1_m.loc[dfRecord["item"][i]].counts/sum(df_item1_m["counts"]),4)]
      else:
        dfRecord.loc[i, [today]] = [0]

    elif(i%4==2):
      if dfRecord["item"][i] in df_item0_w.index: #si el item antic esta en els nous
        dfRecord.loc[i, [today]] = [round(df_item0_w.loc[dfRecord["item"][i]].counts/sum(df_item0_w["counts"]),4)]
      else:
        dfRecord.loc[i, [today]] = [0]
    
    else:
      if dfRecord["item"][i] in df_item1_w.index: #si el item antic esta en els nous
        dfRecord.loc[i, [today]] = [round(df_item1_w.loc[dfRecord["item"][i]].counts/sum(df_item1_w["counts"]),4)]
      else:
        dfRecord.loc[i, [today]] = [0]

  #write the dataframe to the record csv
  dfRecord.to_csv(pathRecord, index=False, header=True)

  
 # MAIN PER VEURE COM CRIDAR LA NOVA FUNCIO
if __name__ == "__main__":
  df = getGeneralDataframe("recognition-output.json", "influencers.csv")
  df_w= getFilteredDataframe(df,"WOMAN")
  df_m= getFilteredDataframe(df,"MAN")

  df_item0_w = getPossibleTrend(df_w,'item0')
  df_item1_w = getPossibleTrend(df_w,'item1')
  df_item0_m = getPossibleTrend(df_m,'item0')
  df_item1_m = getPossibleTrend(df_m,'item1')
  
  actualizeRecord(df_item0_m, df_item1_m, df_item0_w, df_item1_w, 'trend-items.csv', 'items-record.csv')
