import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

def DataPrediction(df, df_item0_m, df_item1_m, df_item0_w, df_item1_w, influencers):
  """ Main DataPrediction function that creates trend-items.csv and updates 
  prediction-history.csv 

  Params: 

    - df: Posts dataFrame
    - df_item0_w: Top woman clothing item dataFrame with counts and valid flag
    - df_item1_w: Bottom woman clothing item dataFrame with counts and valid flag
    - df_item0_m: Top male clothing item dataFrame with counts and valid flag
    - df_item1_m: Bottom male clothing item dataFrame with counts and valid flag
    - influencers: 
  """
