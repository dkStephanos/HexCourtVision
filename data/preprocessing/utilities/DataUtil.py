import numpy as np
import pandas as pd

class DataUtil:

    HEADERS = ["team_id", "player_id", "x_loc", "y_loc", 	
           "radius", "moment", "game_clock", "shot_clock", "event_id"]	

    @staticmethod
    def load_game_df(path):
        game_df = pd.read_json(path)
        
        return game_df

    @staticmethod
    def load_annotation_df(path):
        annotation_df = pd.read_csv(path)
        
        return annotation_df

    @staticmethod
    def load_event_by_num(game_df, event_num):
        for event in game_df['events']:
            if(event['eventId']  == event_num):
                return event

    @staticmethod
    def convert_labled_series_to_df(label_name, series_name, series_to_convert):
        temp_df = pd.DataFrame({label_name:series_to_convert.index, series_name:series_to_convert.values})
        return pd.DataFrame(temp_df[series_name].tolist(), index= temp_df[label_name])

    @staticmethod
    def get_labled_mins_from_df(dataframe, min_value_label):
        return pd.concat([dataframe.idxmin(), dataframe.min()], axis=1, keys=[dataframe.index.name, min_value_label])

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
            players_dict[player['playerid']] = [player["firstname"]+" "+player["lastname"], player["jersey"], player["position"]]	
        
        # Add an entry for the ball
        players_dict.update({-1: ['ball', np.nan]})	

        return players_dict

    @staticmethod
    def get_player_data(event_df, player_name):
        
        return event_df[event_df.player_name==player_name]
    
    @staticmethod
    def get_player_position_data(event_df, player_name):
        
        return event_df[event_df.player_name==player_name][["x_loc", "y_loc"]]

    @staticmethod
    def get_all_player_position_data(event_df):
        group = event_df.groupby("player_name")[["x_loc", "y_loc"]]

        return group

    @staticmethod
    def get_moments_from_event(event_df):
        # A list containing each moment	
        moments = event_df["moments"]	

        # Initialize our new list	
        player_moments = []	

        for moment in moments:	
            # For each player/ball in the list found within each moment	
            for player in moment[5]:	
                # Add additional information to each player/ball	
                # This info includes the index of each moment, the game clock	
                # and shot clock values for each moment	
                player.extend((moments.index(moment), moment[2], moment[3], event_df["eventId"]))	
                player_moments.append(player)


        return pd.DataFrame(player_moments, columns=DataUtil.HEADERS)	