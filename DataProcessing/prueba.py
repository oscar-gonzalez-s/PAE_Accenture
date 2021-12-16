import pandas as pd
import numpy as np
import json
import csv
import matplotlib.pyplot as plt
from datetime import date

from ScoreUtils import *


def DataPrediction(postsDF, influencers, trenditems, predictionhistory):
    """ Main DataPrediction function that creates trend-items.csv and updates
            prediction-history.csv
    Params:
      - df: Posts dataFrame
      - df_item0_w: Top woman clothing item dataFrame with counts and valid flag
      - df_item1_w: Bottom woman clothing item dataFrame with counts and valid flag
        - df_item0_m: Top male clothing item dataFrame with counts and valid flag
        - df_item1_m: Bottom male clothing item dataFrame with counts and valid flag
        - influencers: path to influencers.csv
        - trenditems: path to trend-items.csv
        - predictionhistory: path to items-record.csv
    """
    # Separate general df by gender
    df_w = getFilteredDataframe(postsDF, "WOMAN").copy()
    df_m = getFilteredDataframe(postsDF, "MAN").copy()
    df_m.reset_index(inplace=True, drop=True)
    

    # Return dataframe with column 'value' generated with (post engagements - intervals average) * intervals weight
    possible_w = getPossibleTrend2(df_w)
    #print(possible_w) OK
    possible_m = getPossibleTrend2(df_m)

    # Dataframe with item counts and valid (1) or not (0) and final_score (sum of the values of a certain item)
    finalTopLabelsDF_w = labelsDF_finalscore(possible_w, 'item0')
    finalBottomLabelsDF_w = labelsDF_finalscore(possible_w, 'item1')
    finalTopLabelsDF_m = labelsDF_finalscore(possible_m, 'item0')
    finalBottomLabelsDF_m = labelsDF_finalscore(possible_m, 'item1')

    # Df with final_score (sum of the values of a certain item)
    winnerTop_w = getwinner(finalTopLabelsDF_w)
    winnerBottom_w = getwinner(finalBottomLabelsDF_w)
    winnerTop_m = getwinner(finalTopLabelsDF_m)
    winnerBottom_m = getwinner(finalBottomLabelsDF_m)

    influencerHasTop_m = ";".join(influencerHas(df_m, winnerTop_m))
    influencerHasBottom_m = ";".join(influencerHas(df_m, winnerBottom_m))
    influencerHasTop_w = ";".join(influencerHas(df_w, winnerTop_w))
    influencerHasBottom_w = ";".join(influencerHas(df_w, winnerBottom_w))

    print(winnerTop_w, winnerBottom_w, winnerTop_m, winnerBottom_m)
    header = ['item', 'gender', 'influencers']
    data = [
        [winnerTop_m, 'MAN', influencerHasTop_m],
        [winnerBottom_m, 'MAN', influencerHasBottom_m],
        [winnerTop_w, 'WOMAN', influencerHasTop_w],
        [winnerBottom_w, 'WOMAN', influencerHasBottom_w],
    ]
    with open(trenditems, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        # write multiple rows
        writer.writerows(data)

    actualizeRecord(postsDF, trenditems, predictionhistory)


def actualizeRecord(df, pathItems, pathRecord):
    """
    Params: 
      - df_item0_m = Top woman clothing item dataFrame with counts and valid flag
      - df_item1_m = Bottom woman clothing item dataFrame with counts and valid flag
      - df_item0_w = Top male clothing item dataFrame with counts and valid flag
      - df_item1_w = Bottom male clothing item dataFrame with counts and valid flag
      - pathItems = the path of the csv that contains the 4 trending items
      - pathRecord = the path of the csv that contains the Record of the trending items ( the first time this file MUST be created and only contains three headers: item,gender,influencers)

    Returns: 
      This function does not return anything. It updates the csv file that contains the record (items-record.csv)
    """

    # Split the general Dataframe by gender
    df_w = getFilteredDataframe(df, "WOMAN")
    df_m = getFilteredDataframe(df, "MAN")
    # Get a dataframe with the item types, number of aparitions of the item and it is in the top part of the histogram or not
    df_item0_w = getPossibleTrend(df_w, 'item0')
    df_item1_w = getPossibleTrend(df_w, 'item1')
    df_item0_m = getPossibleTrend(df_m, 'item0')
    df_item1_m = getPossibleTrend(df_m, 'item1')

    # Start of first function definition
    dfTrends = pd.read_csv(pathItems)

    df_item0_m = df_item0_m.set_index("item")
    df_item1_m = df_item1_m.set_index("item")
    df_item0_w = df_item0_w.set_index("item")
    df_item1_w = df_item1_w.set_index("item")

    # la primera vegada assumim que posa nomes: item,gender
    dfRecord = pd.read_csv(pathRecord)

    # todays date in string format
    today = pd.Timestamp.now(tz='CET').strftime("%d/%m/%Y %H:%M:%Sh")

    # new column for todays record

    dfRecord[today] = np.nan
    leng = len(dfRecord)
    cols = len(dfRecord.columns)

    # create the rows for the new Record
    dfRecord.loc[dfRecord.shape[0]] = np.zeros(cols)
    dfRecord.loc[dfRecord.shape[0]] = np.zeros(cols)
    dfRecord.loc[dfRecord.shape[0]] = np.zeros(cols)
    dfRecord.loc[dfRecord.shape[0]] = np.zeros(cols)

    # calculate new items percentage of aparition
    percentatge1 = round(
        df_item0_m.loc[dfTrends["item"][0]].counts/sum(df_item0_m["counts"]), 4)
    percentatge2 = round(
        df_item1_m.loc[dfTrends["item"][1]].counts/sum(df_item1_m["counts"]), 4)
    percentatge3 = round(
        df_item0_w.loc[dfTrends["item"][2]].counts/sum(df_item0_w["counts"]), 4)
    percentatge4 = round(
        df_item1_w.loc[dfTrends["item"][3]].counts/sum(df_item1_w["counts"]), 4)

    # write the new items record
    dfRecord.loc[leng, ['item', 'gender', 'influencers', today]] = [
        dfTrends["item"][0], dfTrends["gender"][0], dfTrends["influencers"][0], percentatge1]
    dfRecord.loc[leng+1, ['item', 'gender', 'influencers', today]] = [dfTrends["item"]
                                                                      [1], dfTrends["gender"][1], dfTrends["influencers"][1], percentatge2]
    dfRecord.loc[leng+2, ['item', 'gender', 'influencers', today]] = [dfTrends["item"]
                                                                      [2], dfTrends["gender"][2], dfTrends["influencers"][2], percentatge3]
    dfRecord.loc[leng+3, ['item', 'gender', 'influencers', today]] = [dfTrends["item"]
                                                                      [3], dfTrends["gender"][3], dfTrends["influencers"][3], percentatge4]

    # fill the old items actual record with their percentage of apparition in the new trend
    for i in range(leng):
        if(i % 4 == 0):

            if dfRecord["item"][i] in df_item0_m.index:  # si el item antic esta en els nous
                dfRecord.loc[i, [today]] = [
                    round(df_item0_m.loc[dfRecord["item"][i]].counts/sum(df_item0_m["counts"]), 4)]
            else:
                dfRecord.loc[i, [today]] = [0]

        elif(i % 4 == 1):
            if dfRecord["item"][i] in df_item1_m.index:  # si el item antic esta en els nous
                dfRecord.loc[i, [today]] = [
                    round(df_item1_m.loc[dfRecord["item"][i]].counts/sum(df_item1_m["counts"]), 4)]
            else:
                dfRecord.loc[i, [today]] = [0]

        elif(i % 4 == 2):
            if dfRecord["item"][i] in df_item0_w.index:  # si el item antic esta en els nous
                dfRecord.loc[i, [today]] = [
                    round(df_item0_w.loc[dfRecord["item"][i]].counts/sum(df_item0_w["counts"]), 4)]
            else:
                dfRecord.loc[i, [today]] = [0]

        else:
            if dfRecord["item"][i] in df_item1_w.index:  # si el item antic esta en els nous
                dfRecord.loc[i, [today]] = [
                    round(df_item1_w.loc[dfRecord["item"][i]].counts/sum(df_item1_w["counts"]), 4)]
            else:
                dfRecord.loc[i, [today]] = [0]

    # write the dataframe to the record csv
    dfRecord.to_csv(pathRecord, index=False, header=True)

   # MAIN PER VEURE COM CRIDAR LA NOVA FUNCIO


def getPossibleTrend2(df):

    # Create new colum in panda series format in order to calculate difference in days
    # today = pd.to_datetime("today")
    # df['diff_days']= (today - df['date']).dt.days + 1

    df['post_engagement'] = (df['likes'] / df['followers'])*100
    # * (37 - df['diff_days'])

    m0, m1, m2, m3, m4, m5 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    total_avg0, total_avg1, total_avg2, total_avg3, total_avg4, total_avg5 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

    # Sum of post_engagement by intervals according to #followers
    for i in range(0, len(df['followers'])):

        if(0 <= df['followers'][i] < 5000):
            total_avg0 = df['post_engagement'][i] + total_avg0
            m0 = m0 + 1

        elif (5000 <= df['followers'][i] < 20000):
            total_avg1 = df['post_engagement'][i] + total_avg1
            m1 = m1 + 1

        elif (20000 <= df['followers'][i] < 50000):
            total_avg2 = df['post_engagement'][i] + total_avg2
            m2 = m2 + 1

        elif (50000 <= df['followers'][i] < 200000):
            total_avg3 = df['post_engagement'][i] + total_avg3
            m3 = m3 + 1

        elif (200000 <= df['followers'][i] < 500000):
            total_avg4 = df['post_engagement'][i] + total_avg4
            m4 = m4 + 1

        elif (df['followers'][i] > 500000):
            total_avg5 = df['post_engagement'][i] + total_avg5
            m5 = m5 + 1

    '''print(m0,m1,m2,m3,m4,m5)
  print(total_avg0,total_avg1,total_avg2,total_avg3,total_avg4,total_avg5)
  print(total_avg0/m0,total_avg1/m1,total_avg2/m2,total_avg3/m3,total_avg4/m4,total_avg5/m5)'''

    # Column with interval_average_posts_engagement
    df['avg_interval'] = 0.0
    df['value'] = 0.0
    j = 0
    for i in range(0, len(df['followers'])):
        if((0 <= df['followers'][i] < 5000) and (m0 > 0)):
            # Put interval_average_posts_engagement in 'avg_interval' column
            df.loc[j, 'avg_interval'] = total_avg0/m0
            # Compare post_engagement with their interval_average_posts_engagement and weight the interval
            df.loc[j, 'value'] = (df['post_engagement']
                                  [i] - df['avg_interval'][i])*0.5
            j = j+1

        elif((5000 <= df['followers'][i] < 20000) and (m1 > 0)):
            df.loc[j, 'avg_interval'] = total_avg1/m1
            df.loc[j, 'value'] = (df['post_engagement']
                                  [i] - df['avg_interval'][i])*0.5
            j = j+1

        elif((20000 <= df['followers'][i] < 50000) and (m2 > 0)):
            df.loc[j, 'avg_interval'] = total_avg2/m2
            df.loc[j, 'value'] = (df['post_engagement']
                                  [i] - df['avg_interval'][i])*0.5
            j = j+1

        elif((50000 <= df['followers'][i] < 200000) and (m3 > 0)):
            df.loc[j, 'avg_interval'] = total_avg3/m3
            df.loc[j, 'value'] = (df['post_engagement']
                                  [i] - df['avg_interval'][i])*0.5
            j = j+1

        elif((200000 <= df['followers'][i] < 500000) and (m4 > 0)):
            df.loc[j, 'avg_interval'] = total_avg4/m4
            df.loc[j, 'value'] = (df['post_engagement']
                                  [i] - df['avg_interval'][i])*0.5
            j = j+1

        elif ((df['followers'][i] > 500000) and (m5 > 0)):
            df.loc[j, 'avg_interval'] = total_avg5/m5
            df.loc[j, 'value'] = (df['post_engagement']
                                  [i] - df['avg_interval'][i])*0.5
            j = j+1

    return df


def labelsDF_finalscore(df, item):
    """ Parameters: Dataframe, name ofº the column that contains the item. Example 'item0' """

    # New dataframe only with labels and their counts manipulated a posteriori including 'valid' and 'final_score' columns
    df_item = pd.DataFrame(columns=["item", "counts"])

    # Discard the NA
    df_w_NA = df[df[item] != "N/A N/A"]

    j = 0
    # Get the item and the item number of apparitions
    for i in range(0, len(df_w_NA[item].value_counts())):
        df_item.loc[j] = df_w_NA[item].value_counts().index.tolist()[
            i], df_w_NA[item].value_counts()[i]
        j = j+1

    # Discard the top 30% of the histogram
    start = (round(len(df_w_NA[item].value_counts())*0.3))
    v = [0] * len(df_w_NA[item].value_counts())

    for i in range(start, len(df_w_NA[item].value_counts())):
        v[i] = 1
    # Add a new column to the dataframe to control if the item is in the top 30% of the histogram
    df_item['valid'] = v

    # Sum all the 'values' ​​for each label to get its final score
    df_item['final_score'] = 0.0
    for i in range(0, len(df_item)):
        for j in range(0, len(df)):
            if(df_item['item'][i] == df['item0'][j] or df_item['item'][i] == df['item1'][j]):
                df_item.loc[i, 'final_score'] = df_item['final_score'][i] + \
                    df['value'][j]

    # Cancel those labels that are not in the 30%
    df_item['final_score'] = (df_item['final_score'] * df_item['valid'])
    df_item['final_score'] = df_item['final_score']

    return df_item


def getwinner(df_labels):
    # Return the item with maximum final score
    max_score = 0.0
    for i in range(0, len(df_labels)):
        if (df_labels['final_score'][i] >= max_score):
            max_score = df_labels['final_score'][i]
            winner = df_labels['item'][i]
    return winner

if __name__ == "__main__":
    """ Main Data Processing Programm
    """
    # PARAMETERS
    # update_predictionHistory: boolean to indicate if items-record.csv has been updated
    # boolean to indicate if a telegram-data.json has been generated
    # generate_telegramHistory = sys.argv[1]
    # recognitionOutput = sys.argv[2]  # path to recognition-output.json
    # influencers = sys.argv[3]  # path to influencers.csv
    # telegramhistory = sys.argv[4]  # path to telegram-history.csv
    # telegramdata = sys.argv[5]  # path to telegram-data.json
    # predictionhistory = sys.argv[6]  # path to items-record.csv
    # trenditems = sys.argv[7]  # path to trend-items.csv
    # # parameter to determine the number of weeks that are taken into account for trend evolution
    # nweeks = sys.argv[8] if len(sys.argv) > 8 else 3
    # # parameter to determine the relevance Telegram results have on the calculus of the influencer score.
    # relevance = sys.argv[9] if len(sys.argv) > 9 else 0

    # CORE CODE
    # Data extraction
    recognitionOutput = '/veu4/usuaris26/pae2021/pae/PAE_Accenture/assets/recognition-output.json'
    influencers= '/veu4/usuaris26/pae2021/pae/PAE_Accenture/assets/influencers.csv'

    postsDataFrame = DataExtraction(
        recognitionOutput, influencers)
    #print(postsDataFrame)
    # Data prediction
    # Make prediction (generate trenditems)
    # Actualize prediction history
    trenditems = '/veu4/usuaris26/pae2021/pae/PAE_Accenture/assets/trend-items.csv'
    predictionhistory = '/veu4/usuaris26/pae2021/pae/PAE_Accenture/assets/items-record.csv' 
    DataPrediction(postsDataFrame, influencers, trenditems, predictionhistory)
    update_predictionHistory = True

    # # Score update
    # # Score must be updated every time either:
    # # - A prediction-history file is updated.
    # # - A telegram file for a survey is generated.
    # updateScore(update_predictionHistory, generate_telegramHistory, telegramdata, influencers,
    #             telegramhistory, predictionhistory, postsDataFrame, relevance, nweeks)
    # update_predictionHistory = False

# def getPossibleTrend2(df):

#     # Create new colum in panda series format in order to calculate difference in days
#     #today = pd.to_datetime("today")
#     #df['diff_days']= (today - df['date']).dt.days + 1

#     df['post_engagement'] = (df['likes'] / df['followers'])*100
#     # * (37 - df['diff_days'])

#     m0, m1, m2, m3, m4, m5 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
#     total_avg0, total_avg1, total_avg2, total_avg3, total_avg4, total_avg5 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

#     # Sum of post_engagement by intervals according to #followers
#     for i in range(0, len(df['followers'])):

#         if(0 <= df['followers'][i] < 5000):
#             total_avg0 = df['post_engagement'][i] + total_avg0
#             m0 = m0 + 1

#         elif (5000 <= df['followers'][i] < 20000):
#             total_avg1 = df['post_engagement'][i] + total_avg1
#             m1 = m1 + 1

#         elif (20000 <= df['followers'][i] < 50000):
#             total_avg2 = df['post_engagement'][i] + total_avg2
#             m2 = m2 + 1

#         elif (50000 <= df['followers'][i] < 200000):
#             total_avg3 = df['post_engagement'][i] + total_avg3
#             m3 = m3 + 1

#         elif (200000 <= df['followers'][i] < 500000):
#             total_avg4 = df['post_engagement'][i] + total_avg4
#             m4 = m4 + 1

#         elif (df['followers'][i] > 500000):
#             total_avg5 = df['post_engagement'][i] + total_avg5
#             m5 = m5 + 1

#     # Column with interval_average_posts_engagement
#     df['avg_interval'] = 0.0
#     df['value'] = 0.0
#     j = 0
#     for i in range(0, len(df['followers'])):
#         if((0 <= df['followers'][i] < 5000) and (m0 > 0)):
#             # Put interval_average_posts_engagement in 'avg_interval' column
#             df.loc[j, 'avg_interval'] = total_avg0/m0
#             # Compare post_engagement with their interval_average_posts_engagement and weight the interval
#             df.loc[j, 'value'] = (df['post_engagement']
#                                   [i] - df['avg_interval'][i])*0.5
#             j = j+1

#         elif((5000 <= df['followers'][i] < 20000) and (m1 > 0)):
#             df.loc[j, 'avg_interval'] = total_avg1/m1
#             df.loc[j, 'value'] = (df['post_engagement']
#                                   [i] - df['avg_interval'][i])*0.5
#             j = j+1

#         elif((20000 <= df['followers'][i] < 50000) and (m2 > 0)):
#             df.loc[j, 'avg_interval'] = total_avg2/m2
#             df.loc[j, 'value'] = (df['post_engagement']
#                                   [i] - df['avg_interval'][i])*0.5
#             j = j+1

#         elif((50000 <= df['followers'][i] < 200000) and (m3 > 0)):
#             df.loc[j, 'avg_interval'] = total_avg3/m3
#             df.loc[j, 'value'] = (df['post_engagement']
#                                   [i] - df['avg_interval'][i])*0.5
#             j = j+1

#         elif((200000 <= df['followers'][i] < 500000) and (m4 > 0)):
#             df.loc[j, 'avg_interval'] = total_avg4/m4
#             df.loc[j, 'value'] = (df['post_engagement']
#                                   [i] - df['avg_interval'][i])*0.5
#             j = j+1

#         elif ((df['followers'][i] > 500000) and (m5 > 0)):
#             df.loc[j, 'avg_interval'] = total_avg5/m5
#             df.loc[j, 'value'] = (df['post_engagement']
#                                   [i] - df['avg_interval'][i])*0.5
#             j = j+1

#     return df

