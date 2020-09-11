import pandas as pd	
import numpy as np	

import matplotlib.pyplot as plt	
import seaborn as sns	

from IPython.display import IFrame	

from VisualizationUtil import VisualizationUtil as VisUtil

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
# read in the court png file	
court = plt.imread(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\NBA_Thesis\static\data\imgs\fullcourt.png")	

plt.figure(figsize=(15, 11.5))	

# Plot the movemnts as scatter plot	
# using a colormap to show change in game clock	
plt.scatter(curry.x_loc, -curry.y_loc, c=curry.game_clock,	
            cmap=plt.cm.Blues, s=1000, zorder=1, edgecolors='k')	
# Darker colors represent moments earlier on in the game	
cbar = plt.colorbar(orientation="horizontal")	
cbar.ax.invert_xaxis()	

VisUtil.draw_court()	

# extend the x-values beyond the court b/c Harden	
# goes out of bounds	
plt.xlim(-7,101)	
plt.ylim(-50, 0)	

plt.show() 