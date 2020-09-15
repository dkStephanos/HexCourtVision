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

df = pd.DataFrame(player_moments, columns=DataUtil.HEADERS)	

df["player_name"] = df.player_id.map(lambda x: players_dict[x][0])	
df["player_jersey"] = df.player_id.map(lambda x: players_dict[x][1])	

# get Curry's movements	
curry = df[df.player_name=="Stephen Curry"]	

#VisUtil.plot_player_movement(curry)

#dist = FeatureUtil.travel_dist(curry)
#print(dist)

#all_dist = FeatureUtil.travel_dist_all(df)
#print(all_dist)

#average_speed = FeatureUtil.average_speed(df, curry)
#print(average_speed)

average_speed_all = FeatureUtil.average_speed_all(df)
print(average_speed_all)