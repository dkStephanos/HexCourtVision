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
print(game_df.shape)

players_data = DataUtil.get_players_data(game_df)

annotation_df = DataUtil.load_annotation_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\event_annotations\events-20151211GSWBOS.csv")

annotation_df = DataUtil.trim_annotation_rows(annotation_df)
annotation_df = DataUtil.determine_possession(annotation_df)
annotation_df = DataUtil.generate_event_ids(annotation_df)

annotation_df = DataUtil.trim_annotation_cols(annotation_df)
print(annotation_df.shape)
combined_event_df = DataUtil.combine_game_and_annotation_events(game_df, annotation_df)
print(combined_event_df.shape)
#combined_event_df.to_csv("static/data/test/events.csv")
curr_annotation = DataUtil.load_annotation_event_by_num(annotation_df, 196)

thomas_off_charge_play = combined_event_df.iloc[100]
print(thomas_off_charge_play)
moments_df = DataUtil.get_moments_from_event(thomas_off_charge_play)
#moments_df.to_csv("static/data/test/test.csv")
FeatureUtil.get_passess_for_event(moments_df, thomas_off_charge_play["possession"], players_data)