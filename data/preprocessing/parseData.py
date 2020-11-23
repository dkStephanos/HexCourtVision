import pandas as pd	
import numpy as np	

import matplotlib.pyplot as plt	
import seaborn as sns	

from IPython.display import IFrame	
import easygui

from utilities.GraphUtil import GraphUtil
from utilities.FeatureUtil import FeatureUtil
from utilities.DataUtil import DataUtil

# Load game with GUI
#game_path = easygui.fileopenbox(default="C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/", title="Select a game file")
#game_df = DataUtil.load_game_df(game_path)

#easygui.msgbox("Next select corresponding annotation file")
#annotation_path = easygui.fileopenbox(default="C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/", title="Select an annotation file")
#annotation_df = DataUtil.load_annotation_df(annotation_path)

game_df = DataUtil.load_game_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\game_raw_data\12.11.2015.GSW.at.BOS\0021500336.json")

players_data = DataUtil.get_players_data(game_df)

annotation_df = DataUtil.load_annotation_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\event_annotations\events-20151211GSWBOS.csv")

annotation_df = DataUtil.trim_annotation_rows(annotation_df)
annotation_df = FeatureUtil.determine_possession(annotation_df)
annotation_df = DataUtil.generate_event_ids(annotation_df)

annotation_df = DataUtil.trim_annotation_cols(annotation_df)
combined_event_df = DataUtil.combine_game_and_annotation_events(game_df, annotation_df)
#combined_event_df.to_csv("static/data/test/events.csv")
curr_annotation = DataUtil.load_annotation_event_by_num(annotation_df, 196)

# Get direction for each play, and remove moments occuring on the other half of the court
combined_event_df = FeatureUtil.determine_directionality(combined_event_df)
combined_event_df = DataUtil.trim_moments_by_directionality(combined_event_df)

sample_event = combined_event_df.iloc[13]
moments_df = DataUtil.get_moments_from_event(sample_event)
print(sample_event)

# get ball movements for event and graph them
ball_df = moments_df[moments_df.player_id==-1]
#GraphUtil.plot_player_movement(ball_df)

#moments_df.to_csv("static/data/test/test.csv")
event_passes = FeatureUtil.get_passess_for_event(moments_df, sample_event["possession"], players_data)
print(event_passes)
dribble_handoff_candidates = FeatureUtil.get_dribble_handoff_candidates(combined_event_df, moments_df, event_passes)
print("Hand off candidates")
print(dribble_handoff_candidates[0])