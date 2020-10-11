import pandas as pd	
import numpy as np	

import matplotlib.pyplot as plt	
import seaborn as sns	

from IPython.display import IFrame	

from VisualizationUtil import VisualizationUtil as VisUtil
from FeatureUtil import FeatureUtil
from DataUtil import DataUtil

game_df = DataUtil.load_game_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\NBA_Thesis\static\data\game_raw_data\11.19.2015.GSW.at.LAC\0021500177.json")

curr_event = DataUtil.load_event_by_num(game_df, 222)	

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

#VisUtil.plot_player_movement(curry)

#dist = FeatureUtil.travel_dist(curry)
#print(dist)

#all_dist = FeatureUtil.travel_dist_all(event_df)
#print(all_dist)

#average_speed = FeatureUtil.average_speed(event_df, curry)
#print(average_speed)

#average_speed_all = FeatureUtil.average_speed_all(event_df)
#print(average_speed_all)

ball_distances = FeatureUtil.distance_between_ball_and_players(event_df)
ball_dist_df = DataUtil.convert_labled_series_to_df('player_name', 'ball_distances', ball_distances)
min_dist_df = DataUtil.get_labled_mins_from_df(ball_dist_df, 'dist_from_ball')
#ball_dist_df.loc[ball_dist_df['ball_distances'] > 3.0, 'player_name'] = pd.NA

print(min_dist_df.shape)
print(min_dist_df)

#bd_df.to_csv('static/data/features/ball_distances.csv')