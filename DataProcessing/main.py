import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import sys

from DataPrediction import *  # imports also ScoreUtils and DataExtraction

if __name__ == "__main__":
    """ Main Data Processing Programm
    """
    # PARAMETERS
    # update_predictionHistory: boolean to indicate if items-record.csv has been updated
    # boolean to indicate if a telegram-data.json has been generated
    generate_telegramHistory = sys.argv[1]
    recognitionOutput = sys.argv[2]  # path to recognition-output.json
    influencers = sys.argv[3]  # path to influencers.csv
    telegramhistory = sys.argv[4]  # path to telegram-history.csv
    telegramdata = sys.argv[5]  # path to telegram-data.json
    predictionhistory = sys.argv[6]  # path to items-record.csv
    trenditems = sys.argv[7]  # path to trend-items.csv
    # parameter to determine the number of weeks that are taken into account for trend evolution
    nweeks = sys.argv[8] if len(sys.argv) > 8 else 3
    # parameter to determine the relevance Telegram results have on the calculus of the influencer score.
    relevance = sys.argv[9] if len(sys.argv) > 9 else 0

    # CORE CODE
    # Data extraction
    postsDataFrame = DataExtraction(
        recognitionOutput, influencers)
    # Data prediction
    # Make prediction (generate trenditems)
    # Actualize prediction history
    DataPrediction(postsDataFrame, influencers, trenditems, predictionhistory)
    update_predictionHistory = True

    # Score update
    # Score must be updated every time either:
    # - A prediction-history file is updated.
    # - A telegram file for a survey is generated.
    nweeks = int(nweeks)
    relevance = float(relevance)

    updateScore(update_predictionHistory, generate_telegramHistory, telegramdata, influencers,
                telegramhistory, predictionhistory, postsDataFrame, relevance, nweeks)
    update_predictionHistory = False
