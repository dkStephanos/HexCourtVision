import pandas as pd	
import numpy as np	
import sys

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

games = {
        "1": r'C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.11.2015.GSW.at.BOS/0021500336.json',
        "2": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.25.2015.LAC.at.LAL/0021500440.json",
        "3": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.30.2015.DEN.at.POR/0021500482.json",
        "4": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.30.2015.GSW.at.DAL/0021500480.json",
        "5": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.31.2015.PHX.at.OKC/0021500488.json",
        "6": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/11.06.2015.MIL.at.NYK/0021500079.json"
}
events = {
        "1": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151211GSWBOS.csv",
        "2": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151225LACLAL.csv",
        "3": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151230DENPOR.csv",
        "4": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151230GSWDAL.csv",
        "5": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151231PHXOKC.csv",
        "6": r'C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151106MILNYK.csv'
}
bad_events = {
    "1": [],
    "2": [212, 294, 296, 386],
    "3": [212, 440, 455],
    "4": [],
    "5": [],
    "6": [110],
}
moment_ranges = {
    "1": 7,
    "2": 8,
    "3": 8,
    "4": 8,
    "5": 8,
    "6": 8,
}
event_offset = {
    "1": 0,
    "2": 0,
    "3": 1,
    "4": 1,
    "5": 0,
    "6": 0,
}


game_num = "5"
game_df = DataUtil.load_game_df(games[game_num])
annotation_df = DataUtil.load_annotation_df(events[game_num])

teams_data = DataUtil.get_teams_data(game_df)
players_data = DataUtil.get_players_data(game_df)
players_dict = DataUtil.get_players_dict(game_df)
print(teams_data)
print(players_data)

game_df = DataUtil.add_offset_to_eventnums(game_df, event_offset[game_num])
annotation_df = DataUtil.trim_annotation_rows(annotation_df, bad_events[game_num])
annotation_df = FeatureUtil.determine_possession(annotation_df, teams_data)
annotation_df = DataUtil.generate_event_ids(annotation_df)

annotation_df = DataUtil.trim_annotation_cols(annotation_df)
combined_event_df = DataUtil.combine_game_and_annotation_events(game_df, annotation_df)

# Get direction for each play, and remove moments occuring on the other half of the court
combined_event_df = FeatureUtil.determine_directionality(combined_event_df)
combined_event_df = DataUtil.trim_moments_by_directionality(combined_event_df)


print(combined_event_df.head())
#combined_event_df.to_csv("static/data/test/events.csv")

"""
sample_event = DataUtil.load_combined_event_by_num(combined_event_df, 345)
print(sample_event) 
moments_df = DataUtil.get_moments_from_event(sample_event)
moments_df.to_csv("static/data/test/test.csv")
if len(moments_df) > 0:
    event_passes = FeatureUtil.get_passess_for_event(moments_df, sample_event["possession"], players_data)
    print(event_passes)
    dribble_handoff_candidates = FeatureUtil.get_dribble_handoff_candidates(combined_event_df, moments_df, event_passes, moment_ranges[game_num], players_dict)
    print("Hand off candidates")
    print(dribble_handoff_candidates)

    # get ball movements for event and graph them
    ball_df = moments_df[moments_df.player_id==-1]
    GraphUtil.plot_player_movement(ball_df)
    #ball_df = moments_df[moments_df.player_id==2738]
    #GraphUtil.plot_player_movement(ball_df)

"""
all_candidates = []
succesful = 0
failed = 0
for index, event in combined_event_df.iterrows():
    try:
        moments_df = DataUtil.get_moments_from_event(event)
        if len(moments_df) > 0:
            event_passes = FeatureUtil.get_passess_for_event(moments_df, event["possession"], players_data)
            dribble_handoff_candidates = FeatureUtil.get_dribble_handoff_candidates(combined_event_df, moments_df, event_passes, moment_ranges[game_num], players_dict)
            all_candidates += dribble_handoff_candidates
        else:
            print("No moments for event: " + str(event['EVENTNUM']))
        succesful += 1
    except:
        print("Issue at index: " + str(event['EVENTNUM']), sys.exc_info())
        failed += 1

final_candidates = DataUtil.remove_duplicate_candidates(all_candidates)
print("\nNumber of candidates parsed: " + str(len(final_candidates)) + "\nSuccessful events: " + str(succesful) + "\nFailed events: " + str(failed) + "\nPercent Successful: " + str(round(succesful/(failed + succesful), 2)))

candidate_df = pd.DataFrame(final_candidates)
candidate_df.to_csv('static/data/test/candidates.csv')
