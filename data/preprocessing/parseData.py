import pandas as pd	
import numpy as np	

import matplotlib.pyplot as plt	
import seaborn as sns	

from IPython.display import IFrame	
import easygui

from utilities.VisualizationUtil import VisualizationUtil as VisUtil
from utilities.FeatureUtil import FeatureUtil
from utilities.DataUtil import DataUtil

# Load game with GUI
#game_path = easygui.fileopenbox(default="C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/", title="Select a game file")
#game_df = DataUtil.load_game_df(game_path)

#easygui.msgbox("Next select corresponding annotation file")
#annotation_path = easygui.fileopenbox(default="C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/", title="Select an annotation file")
#annotation_df = DataUtil.load_annotation_df(annotation_path)

game_df = DataUtil.load_game_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\game_raw_data\12.11.2015.GSW.at.BOS\0021500336.json")
events = game_df['events']

print(game_df.shape)

annotation_df = DataUtil.load_annotation_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\event_annotations\events-20151211GSWBOS.csv")

annotation_df = annotation_df.loc[annotation_df["EVENTMSGTYPE"].isin([1,2,5,6])]

print(annotation_df.shape)

curr_event = DataUtil.load_event_by_num(game_df, "196")	

players_dict = DataUtil.get_players_data(curr_event)

del players_dict[-1]
players_df = pd.DataFrame.from_dict(players_dict, orient='index', columns=['first_name', 'last_name', 'jersey_number', 'position'])
players_df.reset_index(inplace=True)
players_df = players_df.rename(columns={'index': 'player_id'})
print(players_df)