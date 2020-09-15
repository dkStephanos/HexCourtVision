import numpy as np
import pandas as pd

class DataUtil:

    HEADERS = ["team_id", "player_id", "x_loc", "y_loc", 	
           "radius", "moment", "game_clock", "shot_clock"]	

    @staticmethod
    def load_game_df(path):
        game_df = pd.read_json(path)
        
        return game_df

    @staticmethod
    def load_event_by_num(game_df, event_num):
        return game_df['events'].iloc[event_num]

    @staticmethod
    def get_players_data(game_event):
        # A dict containing home players data	
        home = game_event["home"]	
        # A dict containig visiting players data	
        visitor = game_event["visitor"]
        # creates the players list with the home players	
        players = home["players"]	
        # Then add on the visiting players	
        players.extend(visitor["players"])	

        # initialize new dictionary	
        players_dict = {}	

        # Add the values we want for the players (name and jersey number)
        for player in players:	
            players_dict[player['playerid']] = [player["firstname"]+" "+player["lastname"], player["jersey"]]	
        
        # Add an entry for the ball
        players_dict.update({-1: ['ball', np.nan]})	

        return players_dict

    @staticmethod
    def get_player_data(game_df, player_name):
        return game_df[game_df.player_name==player_name]
    
    @staticmethod
    def get_player_position_data(game_df, player_name):
        return game_df[game_df.player_name==player_name][["x_loc", "y_loc"]]