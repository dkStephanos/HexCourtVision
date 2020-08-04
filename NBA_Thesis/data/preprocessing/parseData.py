import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from IPython.display import IFrame

from matplotlib.patches import Circle, Rectangle, Arc

# Function to draw the basketball court lines
def draw_court(ax=None, color="gray", lw=1, zorder=0):
    
    if ax is None:
        ax = plt.gca()

    # Creates the out of bounds lines around the court
    outer = Rectangle((0,-50), width=94, height=50, color=color,
                      zorder=zorder, fill=False, lw=lw)

    # The left and right basketball hoops
    l_hoop = Circle((5.35,-25), radius=.75, lw=lw, fill=False, 
                    color=color, zorder=zorder)
    r_hoop = Circle((88.65,-25), radius=.75, lw=lw, fill=False,
                    color=color, zorder=zorder)
    
    # Left and right backboards
    l_backboard = Rectangle((4,-28), 0, 6, lw=lw, color=color,
                            zorder=zorder)
    r_backboard = Rectangle((90, -28), 0, 6, lw=lw,color=color,
                            zorder=zorder)

    # Left and right paint areas
    l_outer_box = Rectangle((0, -33), 19, 16, lw=lw, fill=False,
                            color=color, zorder=zorder)    
    l_inner_box = Rectangle((0, -31), 19, 12, lw=lw, fill=False,
                            color=color, zorder=zorder)
    r_outer_box = Rectangle((75, -33), 19, 16, lw=lw, fill=False,
                            color=color, zorder=zorder)

    r_inner_box = Rectangle((75, -31), 19, 12, lw=lw, fill=False,
                            color=color, zorder=zorder)

    # Left and right free throw circles
    l_free_throw = Circle((19,-25), radius=6, lw=lw, fill=False,
                          color=color, zorder=zorder)
    r_free_throw = Circle((75, -25), radius=6, lw=lw, fill=False,
                          color=color, zorder=zorder)

    # Left and right corner 3-PT lines
    # a represents the top lines
    # b represents the bottom lines
    l_corner_a = Rectangle((0,-3), 14, 0, lw=lw, color=color,
                           zorder=zorder)
    l_corner_b = Rectangle((0,-47), 14, 0, lw=lw, color=color,
                           zorder=zorder)
    r_corner_a = Rectangle((80, -3), 14, 0, lw=lw, color=color,
                           zorder=zorder)
    r_corner_b = Rectangle((80, -47), 14, 0, lw=lw, color=color,
                           zorder=zorder)
    
    # Left and right 3-PT line arcs
    l_arc = Arc((5,-25), 47.5, 47.5, theta1=292, theta2=68, lw=lw,
                color=color, zorder=zorder)
    r_arc = Arc((89, -25), 47.5, 47.5, theta1=112, theta2=248, lw=lw,
                color=color, zorder=zorder)

    # half_court
    # ax.axvline(470)
    half_court = Rectangle((47,-50), 0, 50, lw=lw, color=color,
                           zorder=zorder)

    hc_big_circle = Circle((47, -25), radius=6, lw=lw, fill=False,
                           color=color, zorder=zorder)
    hc_sm_circle = Circle((47, -25), radius=2, lw=lw, fill=False,
                          color=color, zorder=zorder)

    court_elements = [l_hoop, l_backboard, l_outer_box, outer,
                      l_inner_box, l_free_throw, l_corner_a,
                      l_corner_b, l_arc, r_hoop, r_backboard, 
                      r_outer_box, r_inner_box, r_free_throw,
                      r_corner_a, r_corner_b, r_arc, half_court,
                      hc_big_circle, hc_sm_circle]

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

game_df = pd.read_json(r"C:\Users\Stephanos\Documents\Dev\NBA Thesis\NBA_Thesis\NBA_Thesis\static\data\game_raw_data\11.19.2015.GSW.at.LAC\0021500177.json")

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
court = plt.imread("../../static/data/imgs/fullcourt.png")

plt.figure(figsize=(15, 11.5))

# Plot the movemnts as scatter plot
# using a colormap to show change in game clock
plt.scatter(curry.x_loc, -curry.y_loc, c=curry.game_clock,
            cmap=plt.cm.Blues, s=1000, zorder=1, edgecolors='k')
# Darker colors represent moments earlier on in the game
cbar = plt.colorbar(orientation="horizontal")
cbar.ax.invert_xaxis()

draw_court()

# extend the x-values beyond the court b/c Harden
# goes out of bounds
plt.xlim(-7,101)
plt.ylim(-50, 0)

plt.show()