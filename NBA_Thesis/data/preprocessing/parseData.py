import pandas as pd	
import numpy as np	

import matplotlib.pyplot as plt	
import seaborn as sns	

from IPython.display import IFrame	

from VisualizationUtil import VisualizationUtil as VisUtil
from FeatureUtil import FeatureUtil

game_df = pd.read_json(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\NBA_Thesis\static\data\game_raw_data\11.19.2015.GSW.at.LAC\0021500177.json")	

curr_event = game_df['events'].iloc[222]	

# A dict containing home players data	
home = curr_event["home"]	
# A dict containig visiting players data	
visitor = curr_event["visitor"]	
# A list containing each moment	
moments = curr_event["moments"]	
# Column labels	
headers = ["team_id", "player_id", "x_loc", "y_loc", 	
           "radius", "moment", "game_clock", "shot_clock"]	

# creates the players list with the home players	
players = home["players"]	
# Then add on the visiting players	
players.extend(visitor["players"])	

# initialize new dictionary	
id_dict = {}	

# Add the values we want	
for player in players:	
    id_dict[player['playerid']] = [player["firstname"]+" "+player["lastname"],	
                                   player["jersey"]]	

id_dict.update({-1: ['ball', np.nan]})	

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

df = pd.DataFrame(player_moments, columns=headers)	

df["player_name"] = df.player_id.map(lambda x: id_dict[x][0])	
df["player_jersey"] = df.player_id.map(lambda x: id_dict[x][1])	

# get Curry's movements	
curry = df[df.player_name=="Stephen Curry"]	

#VisUtil.plot_player_movement(curry)

dist = FeatureUtil.travel_dist(curry)
print(dist)