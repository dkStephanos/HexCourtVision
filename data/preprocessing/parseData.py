import pandas as pd	
import numpy as np	

import matplotlib.pyplot as plt	
import seaborn as sns	

from IPython.display import IFrame	
import easygui

from utilities.VisualizationUtil import VisualizationUtil as VisUtil
from utilities.FeatureUtil import FeatureUtil
from utilities.DataUtil import DataUtil

game_path = easygui.fileopenbox(default="C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/", title="Select a game file")

game_df = DataUtil.load_game_df(game_path)

events = game_df['events']

print(game_df.shape)

easygui.msgbox("Next select corresponding annotation file")

annotation_path = easygui.fileopenbox(default="C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/", title="Select an annotation file")

annotation_df = DataUtil.load_annotation_df(annotation_path)

annotation_df = annotation_df.loc[annotation_df["EVENTMSGTYPE"].isin([1,2,5,6])]

print(annotation_df.shape)

curr_event = DataUtil.load_event_by_num(game_df, "201")	

players_dict = DataUtil.get_players_data(curr_event)

print(players_dict)

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

event_df.to_csv("static/data/test/test.csv")