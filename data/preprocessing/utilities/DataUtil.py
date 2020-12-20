import numpy as np
import pandas as pd
import math
from .ConstantsUtil import ConstantsUtil

class DataUtil:
    @staticmethod
    def load_game_df(path):
        game_df = pd.read_json(path)
        
        return game_df

    @staticmethod
    def convert_game_clock_to_timestamp(game_clock):
        seconds = int(float(game_clock)/60)
        milliseconds = int(float(game_clock)%60)

        return f'{seconds}:{milliseconds}'

    @staticmethod
    def convert_timestamp_to_game_clock(timestamp):
        time = timestamp.split(':')

        return int(time[0])*60 + int(time[1])

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
            "color": ConstantsUtil.COLOR_DICT[game_df.iloc[0]["events"]["home"]["teamid"]]
        }
        visitor_team = {
            "team_id": game_df.iloc[0]["events"]["visitor"]["teamid"], 
            "name": game_df.iloc[0]["events"]["visitor"]["name"], 
            "abreviation": game_df.iloc[0]["events"]["visitor"]["abbreviation"],
            "color": ConstantsUtil.COLOR_DICT[game_df.iloc[0]["events"]["visitor"]["teamid"]]
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
    def load_combined_event_by_num(combined_event_df, event_num):
        for index, event in combined_event_df.iterrows():
            if(event['EVENTNUM'] == event_num):
                return event

    # Some games are missing the first couple events, so we must offset the numbers to correspond with the annotation data
    @staticmethod
    def add_offset_to_eventnums(game_df, event_offset):
        # If event_offset is zero, we can skip this
        if (event_offset != 0):
            for index, event in enumerate(game_df['events']):
                if index + event_offset < len(game_df):
                    event['eventId'] =  game_df['events'][index + event_offset]['eventId']

        return game_df

    # The only events with interesting positional data are Makes, Misses, Turnovers, Fouls. Narrow to those
    @staticmethod
    def trim_annotation_rows(annotation_df, bad_events = []):
        # First, extract only the make, miss, turnover, foul events
        annotation_df = annotation_df.loc[annotation_df["EVENTMSGTYPE"].isin([1,2,5,6])]

        # Next, trim out the offensive foul events, as they are duplicated as turnovers
        annotation_df = annotation_df[~annotation_df["HOMEDESCRIPTION"].str.contains("Offensive Charge", na=False)]
        annotation_df = annotation_df[~annotation_df["VISITORDESCRIPTION"].str.contains("Offensive Charge", na=False)]
        annotation_df = annotation_df[~annotation_df["HOMEDESCRIPTION"].str.contains("OFF.FOUL", na=False)]
        annotation_df = annotation_df[~annotation_df["VISITORDESCRIPTION"].str.contains("OFF.FOUL", na=False)]

        # Next, trim out technical, loose ball, and personal take fouls, as they don't contain full positional data
        annotation_df = annotation_df[~annotation_df["HOMEDESCRIPTION"].str.contains("T.FOUL", na=False)]
        annotation_df = annotation_df[~annotation_df["VISITORDESCRIPTION"].str.contains("T.FOUL", na=False)]
        annotation_df = annotation_df[~annotation_df["HOMEDESCRIPTION"].str.contains("L.B.FOUL", na=False)]
        annotation_df = annotation_df[~annotation_df["VISITORDESCRIPTION"].str.contains("L.B.FOUL", na=False)]

        # Finally, remove passed eventnums that have bad data
        if len(bad_events) > 0:
            annotation_df = annotation_df[~annotation_df["EVENTNUM"].isin(bad_events)]

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

    # Work through the combined_event_df and del any moment that occurs in the backcourt
    @staticmethod
    def trim_moments_by_directionality(combined_event_df):

        for index, event in combined_event_df.iterrows():
            if event['direction'] == "RIGHT":
                event['moments'][:] = [ x for x in event['moments'] if x[5][0][2] > 45.0]
            else:
                event['moments'][:] = [ x for x in event['moments'] if x[5][0][2] < 45.0]

        return combined_event_df

    # We want unique event_ids for each event, so combine the game_id and event_id in a new col
    @staticmethod
    def generate_event_ids(annotation_df):
        event_ids = []

        for index, row in annotation_df.iterrows():
            event_ids.append(str(row['GAME_ID']) + f"-{row['EVENTNUM']:03}")

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
    def get_players_dict(game_df):
        # A dict containing home players data	
        home = game_df["events"][0]["home"]	
        # A dict containig visiting players data	
        visitor = game_df["events"][0]["visitor"]
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
    def get_possession_team_player_ids(possession, players_data):
        player_ids = []
        
        for player in players_data:
            if player['team_id'] == possession:
                player_ids.append(player['player_id'])

        return player_ids

    @staticmethod
    def get_moments_from_event(event_df):
        # A list containing each moment	
        moments = event_df["moments"]	
        
        # Initialize our new list	
        player_moments = []	
        last_game_clock = 720
        last_shot_clock = 24
        reached_end_of_play = False

        # We only care about positional data for the possession, so if shot clock resets, bail out
        while not reached_end_of_play:
            for moment in moments:	
                # When shot clock expires, it is set to None, convert to 0.0 so we can process it in the loop below
                if moment[3] is None:
                    moment[3] = 0.0
                # Check to see if shot clock is greater than previous entry, if so, break
                if moment[3] > last_shot_clock and moment[2] < DataUtil.convert_timestamp_to_game_clock(event_df['PCTIMESTRING']) :
                    reached_end_of_play = True
                else:
                    last_shot_clock = moment[3]
                    last_game_clock = moment[2]
                    # For each player/ball in the list found within each moment
                    for player in moment[5]:	
                        # Add additional information to each player/ball	
                        # This info includes the index of each moment, the game clock	
                        # and shot clock values for each moment
                        player_copy = player.copy()	
                        player_copy.extend((moments.index(moment), moment[2], moment[3], event_df["event_id"]))	
                        player_moments.append(player_copy)
            reached_end_of_play = True
        
        return pd.DataFrame(player_moments, columns=ConstantsUtil.HEADERS)	

    @staticmethod
    def extend_event_moments(game_df):
        for index in range(1, len(game_df['events'])): 
            if not game_df['events'][index - 1]['moments'] == None:
                moments_copy = game_df['events'][index - 1]['moments'].copy()
                game_df['events'][index]['moments'] = game_df['events'][index]['moments'] + moments_copy

        return game_df

    # Scan ahead in the candidates by some set offset to remove duplicate entries from events with overlapping positional data
    @staticmethod
    def remove_duplicate_candidates(all_candidates):
        final_candidates = []
        offset_length = 5
        duplicate = False

        for index in range(0, len(all_candidates)):
            for offset in range(1, offset_length):
                if not index + offset >= len(all_candidates) and (all_candidates[index]['game_clock'] != all_candidates[index + offset]['game_clock'] or all_candidates[index]['shot_clock'] != all_candidates[index + offset]['shot_clock']):
                    duplicate = False
                else:
                    duplicate = True
                    break
            if duplicate == False:
                final_candidates.append(all_candidates[index])

        return final_candidates
