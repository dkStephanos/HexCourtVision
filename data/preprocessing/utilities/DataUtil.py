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
    def load_game_event_by_num(game_df, event_num):
        for event in game_df['events']:
            if(event['eventId']  == event_num):
                return event
    
    @staticmethod
    def load_annotation_event_by_num(annotation_df, event_num):
        return annotation_df[annotation_df["EVENTNUM"] == event_num]

    # The only events with interesting positional data are Makes, Misses, Turnovers, Fouls. Narrow to those
    @staticmethod
    def trim_annotation_rows(annotation_df):
        # First, extract only the make, miss, turnover, foul events
        annotation_df = annotation_df.loc[annotation_df["EVENTMSGTYPE"].isin([1,2,5,6])]

        # Next, trim out the offensive charge events, as they are duplicated as turnovers
        annotation_df = annotation_df[~annotation_df["HOMEDESCRIPTION"].str.contains("Offensive Charge", na=False)]
        annotation_df = annotation_df[~annotation_df["VISITORDESCRIPTION"].str.contains("Offensive Charge", na=False)]
        
        return annotation_df
    
    @staticmethod
    def trim_annotation_cols(annotation_df):
        # remove the columns we don't need
        annotation_df.drop(annotation_df.columns[[0]], axis = 1, inplace = True) 
        del annotation_df["WCTIMESTRING"]
        del annotation_df["NEUTRALDESCRIPTION"]
        del annotation_df["SCOREMARGIN"]
        del annotation_df["PERSON1TYPE"]
        del annotation_df["PLAYER1_NAME"]
        del annotation_df["PLAYER1_TEAM_ID"]
        del annotation_df["PLAYER1_TEAM_CITY"]
        del annotation_df["PLAYER1_TEAM_NICKNAME"]
        del annotation_df["PLAYER1_TEAM_ABBREVIATION"]
        del annotation_df["PERSON2TYPE"]
        del annotation_df["PLAYER2_NAME"]
        del annotation_df["PLAYER2_TEAM_ID"]
        del annotation_df["PLAYER2_TEAM_CITY"]
        del annotation_df["PLAYER2_TEAM_NICKNAME"]
        del annotation_df["PLAYER2_TEAM_ABBREVIATION"]
        del annotation_df["PERSON3TYPE"]
        del annotation_df["PLAYER3_NAME"]
        del annotation_df["PLAYER3_TEAM_ID"]
        del annotation_df["PLAYER3_TEAM_CITY"]
        del annotation_df["PLAYER3_TEAM_NICKNAME"]
        del annotation_df["PLAYER3_TEAM_ABBREVIATION"]

        return annotation_df

    # We need to know which team has possesssion for each event, deduce from event type and add col to df
    @staticmethod
    def determine_possession(annotation_df):
        possession = []
        # Step through each possession
        # For Make, Miss, Turnover events, set possesion to PLAYER_1_TEAM_ID
        # For a Foul, set possesion to PLAYER_2_TEAM_ID
        for index, row in annotation_df.iterrows():
            if row['EVENTMSGTYPE'] in [1,2,5]:
                possession.append(row['PLAYER1_TEAM_ID'])
            if row['EVENTMSGTYPE'] == 6:
                possession.append(row['PLAYER2_TEAM_ID'])
        
        # Add the list of team_ids to the dataframe as the possession col
        annotation_df['possession'] = possession

        return annotation_df   

    # We want unique event_ids for each event, so combine the game_id and event_id in a new col
    @staticmethod
    def generate_event_ids(annotation_df):
        event_ids = []

        for index, row in annotation_df.iterrows():
            event_ids.append(int(str(row['GAME_ID']) + str(row['EVENTNUM'])))

        annotation_df["event_id"] = event_ids

        return annotation_df

    @staticmethod
    def combine_game_and_annotation_events(game_df, annotation_df):
        moments = []
        
        for event in game_df['events']:
            if np.any(annotation_df['EVENTNUM'] == int(event['eventId'])):
                moments.append({'EVENTNUM': int(event['eventId']), 'moments': event['moments']})

        moments_df = pd.DataFrame(moments)

        return annotation_df.merge(moments_df, how="inner")
        

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
        print(moments.head())
        # Initialize our new list	
        player_moments = []	

        for moment in moments:	
            # For each player/ball in the list found within each moment	
            for player in moment[5]:	
                # Add additional information to each player/ball	
                # This info includes the index of each moment, the game clock	
                # and shot clock values for each moment	
                player.extend((moments.index(moment), moment[2], moment[3], event_df["event_id"]))	
                player_moments.append(player)


        return pd.DataFrame(player_moments, columns=DataUtil.HEADERS)	
