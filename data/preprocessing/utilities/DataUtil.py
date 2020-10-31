import numpy as np
import pandas as pd

class DataUtil:

    HEADERS = ["team_id", "player_id", "x_loc", "y_loc", 	
           "radius", "moment", "game_clock", "shot_clock", "event_id"]

    COLOR_DICT = {
        1610612737: '#E13A3E',
        1610612738: '#008348',
        1610612751: '#061922',
        1610612766: '#1D1160',
        1610612741: '#CE1141',
        1610612739: '#860038',
        1610612742: '#007DC5',
        1610612743: '#4D90CD',
        1610612765: '#006BB6',
        1610612744: '#FDB927',
        1610612745: '#CE1141',
        1610612754: '#00275D',
        1610612746: '#ED174C',
        1610612747: '#552582',
        1610612763: '#0F586C',
        1610612748: '#98002E',
        1610612749: '#00471B',
        1610612750: '#005083',
        1610612740: '#002B5C',
        1610612752: '#006BB6',
        1610612760: '#007DC3',
        1610612753: '#007DC5',
        1610612755: '#006BB6',
        1610612756: '#1D1160',
        1610612757: '#E03A3E',
        1610612758: '#724C9F',
        1610612759: '#BAC3C9',
        1610612761: '#CE1141',
        1610612762: '#00471B',
        1610612764: '#002B5C',
    }

    @staticmethod
    def load_game_df(path):
        game_df = pd.read_json(path)
        
        return game_df

    @staticmethod
    def get_game_data(game_df, annotation_df):
        game_dict = {}

        game_dict["game_id"] = game_df.iloc[0]["gameid"]
        game_dict["game_date"] = game_df.iloc[0]["gamedate"]
        game_dict["home_team"] = game_df.iloc[0]["events"]["home"]["teamid"]
        game_dict["visitor_team"] = game_df.iloc[0]["events"]["visitor"]["teamid"]
        game_dict["final_score"] = annotation_df.iloc[-1]["SCORE"]
        
        return game_dict

    @staticmethod
    def get_teams_data(game_df):
        home_team = {
            "team_id": game_df.iloc[0]["events"]["home"]["teamid"], 
            "name": game_df.iloc[0]["events"]["home"]["name"], 
            "abreviation": game_df.iloc[0]["events"]["home"]["abbreviation"],
            "color": DataUtil.COLOR_DICT[game_df.iloc[0]["events"]["home"]["teamid"]]
        }
        visitor_team = {
            "team_id": game_df.iloc[0]["events"]["visitor"]["teamid"], 
            "name": game_df.iloc[0]["events"]["visitor"]["name"], 
            "abreviation": game_df.iloc[0]["events"]["visitor"]["abbreviation"],
            "color": DataUtil.COLOR_DICT[game_df.iloc[0]["events"]["visitor"]["teamid"]]
        }

        return [home_team, visitor_team]   

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
    def get_players_df(game_event):
        # A dict containing home players data	
        home = game_event["home"]	
        # A dict containig visiting players data	
        visitor = game_event["visitor"]

        # initialize new dictionary	
        players_dict = {}	

        # Add the values we want for the players (name and jersey number)
        for player in home["players"]:	
            players_dict[player['playerid']] = [home["teamid"], player["firstname"], player["lastname"], player["jersey"], player["position"]]
        for player in visitor["players"]:	
            players_dict[player['playerid']] = [visitor["teamid"], player["firstname"], player["lastname"], player["jersey"], player["position"]]	
        
        # Add an entry for the ball
        players_dict.update({-1: ['ball', np.nan]})	

        players_df = pd.DataFrame.from_dict(players_dict, orient='index', columns=['team_id', 'first_name', 'last_name', 'jersey_number', 'position'])
        players_df.reset_index(inplace=True)

        return players_df.rename(columns={'index': 'player_id'})

    @staticmethod 
    def get_players_data(game_df):

        # A dict containing home players data	
        home = game_df["events"][0]["home"]	
        # A dict containig visiting players data	
        visitor = game_df["events"][0]["visitor"]

        # initialize new dictionary	
        all_players = []	

        # Add the values we want for the players (team_id, name, jersey number and position)
        for player in home["players"]:
            all_players.append({
                "player_id": player['playerid'],
                 "team_id": home['teamid'],
                 "first_name": player['firstname'],
                 "last_name": player['lastname'],
                 "jersey_number": player['jersey'],
                 "position": player['position']
                 })
        for player in visitor["players"]:	
            all_players.append({
                "player_id": player['playerid'],
                 "team_id": visitor['teamid'],
                 "first_name": player['firstname'],
                 "last_name": player['lastname'],
                 "jersey_number": player['jersey'],
                 "position": player['position']
                 })

        return all_players	

    @staticmethod
    def get_player_data(event_df, player_id):
        
        return event_df[event_df.player_id==player_id]
    
    @staticmethod
    def get_player_position_data(event_df, player_id):
        
        return event_df[event_df.player_id==player_id][["x_loc", "y_loc"]]

    @staticmethod
    def get_all_player_position_data(event_df):
        group = event_df.groupby("player_id")[["x_loc", "y_loc"]]

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
