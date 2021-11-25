import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import sys

from DataExtraction import *

if __name__ == "__main__":
  """
    sys.argv[1]: path to recognition-output.json
    sys.argv[2]: path to influencers.csv
  """

  # Data extraction
  postsDataFrame, df_item0_m, df_item1_m, df_item0_w, df_item1_w = DataExtraction(sys.argv[1], sys.argv[2])
  print(postsDataFrame, df_item0_m, df_item1_m, df_item0_w, df_item1_w)
  
  # Score update

  # Data prediction
