import pandas as pd	
import numpy as np	

import matplotlib.pyplot as plt	
import seaborn as sns	

from IPython.display import IFrame	
import easygui

from VisualizationUtil import VisualizationUtil as VisUtil
from FeatureUtil import FeatureUtil
from DataUtil import DataUtil

NORMALIZATION_COEF = 7
PLAYER_CIRCLE_SIZE = 12 / NORMALIZATION_COEF
INTERVAL = 10
DIFF = 6
X_MIN = 0
X_MAX = 100
Y_MIN = 0
Y_MAX = 50
COL_WIDTH = 0.3
SCALE = 1.65
FONTSIZE = 6
X_CENTER = X_MAX / 2 - DIFF / 1.5 + 0.10
Y_CENTER = Y_MAX - DIFF / 1.5 - 0.35

path = easygui.fileopenbox(default="C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/")

game_df = DataUtil.load_game_df(path)

print(game_df.shape)

curr_event = DataUtil.load_event_by_num(game_df, 201)	

players_dict = DataUtil.get_players_data(curr_event)

# A list containing each moment	
moments = curr_event["moments"]	

# Initialize our new list	
player_moments = []	

for moment in moments:	
    # For each player/ball in the list found within each moment	
    for player in moment[5]:	
        # Add additional information to each player/ball	
        # This info includes the index of each moment, the game clock	
        # and shot clock values for each moment	
        player.extend((moments.index(moment), moment[2], moment[3]))	
        player_moments.append(player)	

event_df = pd.DataFrame(player_moments, columns=DataUtil.HEADERS)	

event_df["player_name"] = event_df.player_id.map(lambda x: players_dict[x][0])	
event_df["player_jersey"] = event_df.player_id.map(lambda x: players_dict[x][1])	