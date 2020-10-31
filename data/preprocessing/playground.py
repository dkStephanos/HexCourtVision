import pandas as pd	
import numpy as np	

import matplotlib.pyplot as plt	
import seaborn as sns	

from IPython.display import IFrame	

from GraphUtil import GraphUtil
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

game_df = DataUtil.load_game_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\game_raw_data\12.25.2015.LAC.at.LAL\0021500440.json")
print(game_df["events"][200]["eventId"])

game_df = DataUtil.load_game_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\game_raw_data\12.11.2015.GSW.at.BOS\0021500336.json")
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

# get Curry's movements	
curry = event_df[event_df.player_name=="Stephen Curry"]

#all_player_loc = DataUtil.get_all_player_position_data(event_df)
#print(all_player_loc.head())

#print(curry.head())

GraphUtil.plot_player_movement(curry)

#dist = FeatureUtil.travel_dist(curry)
#print(dist)

#all_dist = FeatureUtil.travel_dist_all(event_df)
#print(all_dist)

#average_speed = FeatureUtil.average_speed(event_df, curry)
#print(average_speed)

#average_speed_all = FeatureUtil.average_speed_all(event_df)
#print(average_speed_all)

#ball_distances = FeatureUtil.distance_between_ball_and_players(event_df)
#ball_dist_df = DataUtil.convert_labled_series_to_df('player_name', 'ball_distances', ball_distances)
#min_dist_df = DataUtil.get_labled_mins_from_df(ball_dist_df, 'dist_from_ball')

#min_dist_df.loc[min_dist_df['dist_from_ball'] > 3.0, 'player_name'] = pd.NA

#print(min_dist_df.shape)
#print(min_dist_df)

#min_dist_df.to_csv('static/data/features/ball_handler.csv')