import pandas as pd
import numpy as np
import sys

import matplotlib.pyplot as plt
import seaborn as sns

from IPython.display import IFrame

from utilities.GraphUtil import GraphUtil
from utilities.FeatureUtil import FeatureUtil
from utilities.DataLoader import DataLoader  # Updated import
from utilities.ConstantsUtil import ConstantsUtil


game = "20151228SACGSW"
game_df = DataLoader.load_game_df(ConstantsUtil.games[game]['raw_data'])  # Updated import
annotation_df = DataLoader.load_annotation_df(ConstantsUtil.games[game]['events'])  # Updated import

teams_data = DataLoader.get_teams_data(game_df)  # Updated import
players_data = DataLoader.get_players_data(game_df)  # Updated import
players_dict = DataLoader.get_players_dict(game_df)  # Updated import

annotation_df = DataLoader.trim_annotation_rows(annotation_df, ConstantsUtil.games[game]['bad_events'])  # Updated import
annotation_df = FeatureUtil.determine_possession(annotation_df, teams_data)
annotation_df = DataLoader.generate_event_ids(annotation_df)  # Updated import
print(DataLoader.load_combined_event_by_num(annotation_df, 427))  # Updated import

annotation_df = DataLoader.trim_annotation_cols(annotation_df)  # Updated import
combined_event_df = DataLoader.combine_game_and_annotation_events(game_df, annotation_df)  # Updated import

# Get direction for each play and remove moments occurring on the other half of the court
combined_event_df = FeatureUtil.determine_directionality(combined_event_df)
combined_event_df = DataLoader.trim_moments_by_directionality(combined_event_df)  # Updated import

print(combined_event_df.head())
# combined_event_df.to_csv("static/backend/test/events.csv")

sample_event = DataLoader.load_combined_event_by_num(combined_event_df, 427)  # Updated import
print(sample_event)
moments_df = DataLoader.get_moments_from_event(sample_event)  # Updated import
# moments_df.to_csv("static/backend/test/test.csv")
if len(moments_df) > 0:
    event_passes = FeatureUtil.get_passess_for_event(moments_df, sample_event["possession"], players_data)
    print(event_passes)
    dribble_handoff_candidates = FeatureUtil.get_dribble_handoff_candidates(
        combined_event_df, moments_df, event_passes, ConstantsUtil.games[game]['moment_range'], players_dict)
    print("Hand off candidates")
    print(dribble_handoff_candidates)
    # get ball movements for event and graph them
    ball_df = moments_df[moments_df.player_id == -1]
    GraphUtil.plot_player_movement(ball_df)

"""
all_candidates = []
successful = 0
failed = 0
for index, event in combined_event_df.iterrows():
    try:
        moments_df = DataLoader.get_moments_from_event(event)  # Updated import
        if len(moments_df) > 0:
            event_passes = FeatureUtil.get_passess_for_event(moments_df, event["possession"], players_data)
            dribble_handoff_candidates = FeatureUtil.get_dribble_handoff_candidates(
                combined_event_df, moments_df, event_passes, ConstantsUtil.games[game]['moment_range'], players_dict)
            all_candidates += dribble_handoff_candidates
        else:
            print("No moments for event: " + str(event['EVENTNUM']))
        successful += 1
    except:
        print("Issue at index: " + str(event['EVENTNUM']), sys.exc_info())
        failed += 1

final_candidates = DataLoader.remove_duplicate_candidates(all_candidates)  # Updated import
print("\nNumber of candidates parsed: " + str(len(final_candidates)) + "\nSuccessful events: " + str(
    successful) + "\nFailed events: " + str(failed) + "\nPercent Successful: " + str(
    round(successful / (failed + successful), 2)))

candidate_df = pd.DataFrame(final_candidates)
candidate_df.to_csv(f'static/backend/test/candidates.csv')
"""