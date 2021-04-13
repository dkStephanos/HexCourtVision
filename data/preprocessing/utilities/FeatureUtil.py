import math
import numpy as np
import pandas as pd
from .DataUtil import DataUtil
from scipy.spatial.distance import euclidean
from scipy.stats import linregress

class FeatureUtil:

    # We need to know which team has possesssion for each event, deduce from event type and add col to df
    @staticmethod
    def determine_possession(annotation_df, teams_data):
        possession = []
        # Step through each possession
        # For Make, Miss, Turnover events, set possesion to PLAYER_1_TEAM_ID
        # For a Foul, set possesion to PLAYER_2_TEAM_ID
        for index, row in annotation_df.iterrows():
            if row['EVENTMSGTYPE'] in [1,2]:
                possession.append(row['PLAYER1_TEAM_ID'])
            elif 'Turnover: Shot Clock' in str(row['HOMEDESCRIPTION']) or 'Turnover: Shot Clock' in str(row['VISITORDESCRIPTION']):
                possession.append(row['PLAYER1_ID'])
            elif 'Def. 3 Sec' in str(row['HOMEDESCRIPTION']) or 'Def. 3 Sec' in str(row['VISITORDESCRIPTION']):
                if row['PLAYER1_TEAM_ID'] == teams_data[0]['team_id']:
                    possession.append(teams_data[1]['team_id'])
                else:
                    possession.append(teams_data[0]['team_id'])
            elif 'T.Foul' in str(row['HOMEDESCRIPTION']) or 'T.Foul' in str(row['VISITORDESCRIPTION']):
                possession.append(row['PLAYER1_TEAM_ID'])
            elif row['EVENTMSGTYPE'] == 5:
                possession.append(row['PLAYER1_TEAM_ID'])
            elif row['EVENTMSGTYPE'] == 6:
                possession.append(row['PLAYER2_TEAM_ID'])
        
        # Add the list of team_ids to the dataframe as the possession col
        annotation_df['possession'] = possession

        return annotation_df   

    # Find the first FG instance, and determine which side of the court it was on, then set directionality for every event
    @staticmethod
    def determine_directionality(combined_event_df):
        reached_end_of_play = False
        last_moment = []
        last_event = []
        team_basket = {'team': -1, 'direction': ''}

        # Loop through the events, looking for a made field goal in the first half
        for index, row in combined_event_df.iterrows():
            if row['EVENTMSGTYPE'] == 1 and row['PERIOD'] < 3:
                event_time = DataUtil.convert_timestamp_to_game_clock(row['PCTIMESTRING'])
                # we want to find the end of the play, so we can determine which basket was scored on
                for moment in row['moments']:
                    if (moment[2] <= event_time + 1) and (moment[2] >= event_time - 1):
                        last_event = row
                        last_moment = moment
                        reached_end_of_play = True
                        break
                if reached_end_of_play:
                    break

        # Once we have found it, check the x_loc of the ball to determine basket
        team_basket['team'] = last_event['possession']
        if last_moment[5][0][2] >= 47.0:
            team_basket['direction'] = 'RIGHT'
        else:
            team_basket['direction'] = 'LEFT'
        other_direction = 'RIGHT' if team_basket['direction'] == 'LEFT' else 'LEFT'
        
        # Next, set up the conditions and values for directionality, direction flips after the second period
        conditions = [
            (combined_event_df['possession'] == team_basket['team']) & (combined_event_df['PERIOD'] < 3),
            (combined_event_df['possession'] != team_basket['team']) & (combined_event_df['PERIOD'] < 3),
            (combined_event_df['possession'] == team_basket['team']) & (combined_event_df['PERIOD'] >= 3),
            (combined_event_df['possession'] != team_basket['team']) & (combined_event_df['PERIOD'] >= 3),
        ]
        values = [team_basket['direction'], other_direction, other_direction, team_basket['direction']]

        # Finally, map the direction onto each event and return the combined event dataframe
        combined_event_df['direction'] = np.select(conditions, values)

        return combined_event_df

    @staticmethod
    # Uses euclidean distance between consecutive points to calculate distance traveled 
    def travel_dist(player):
        # pull player_location data off player
        player_locations = player[["x_loc", "y_loc"]]
        
        # get the differences for each column
        diff = np.diff(player_locations, axis=0)
        
        # square the differences and add them,
        # then get the square root of that sum
        dist = np.sqrt((diff ** 2).sum(axis=1))
        
        # Then return the sum of all the distances
        return dist.sum()
    
    @staticmethod
    def travel_dist_all(event_df):
        player_travel_dist = event_df.groupby('player_id')[['x_loc', 'y_loc']].apply(FeatureUtil.travel_dist)
        
        return player_travel_dist

    @staticmethod
    def average_speed(event_df, player_id):
        # get the number of seconds for the play
        seconds = event_df.game_clock.max() - event_df.game_clock.min()
        # feet per second
        if (player_id is None):
            player_fps = FeatureUtil.travel_dist(event_df[event_df['player_id'].isna()]) / seconds
        else:
            player_fps = FeatureUtil.travel_dist(event_df[event_df['player_id'] == player_id]) / seconds
        # convert to miles per hour
        player_mph = 0.681818 * player_fps
        
        return player_mph

    @staticmethod
    def average_speed_all(event_df):
        # get the number of seconds for the play
        seconds = event_df.game_clock.max() - event_df.game_clock.min()
        # apply travel_dist_all and divide by total num seconds
        player_speeds = (FeatureUtil.travel_dist_all(event_df)/seconds) * 0.681818

        return player_speeds

    @staticmethod
    # Function to find the distance between players at a given moment
    def distance_between_players_at_moment(player_a, player_b):
        # Returns a tuple with (Distance, Moment#)
        return euclidean(player_a, player_b)

    @staticmethod
    # Function to find the distance between players at a moment
    def distance_between_players(player_a, player_b):
        # Make sure we know when to stop
        player_range = 0
        if len(player_a) < len(player_b):
            player_range = len(player_a)
        else:
            player_range = len(player_b)

        # Returns a tuple with (Distance, Moment#)
        return [(euclidean(player_a.iloc[i], player_b.iloc[i]))
                for i in range(player_range)]

    @staticmethod
    # Function to find the distance between players at each moment
    def distance_between_players_with_moment(player_a, player_b):
        print('inside distance_between_players_with_moment with: ', player_a, player_b)
        # Make sure we know when to stop
        player_range = 0
        if len(player_a) < len(player_b):
            player_range = len(player_a)
        else:
            player_range = len(player_b)

        # Returns a tuple with (Distance, Moment#)
        return [(euclidean(player_a.iloc[i][:1], player_b.iloc[i][:1]), player_a.iloc[i][2])
                for i in range(player_range)]

    @staticmethod
    def distance_between_ball_and_players(moments_df, player_ids):
        group = moments_df[moments_df.player_id.isin(player_ids)].groupby("player_id")[["x_loc", "y_loc"]]
        
        ball_distances = group.apply(FeatureUtil.distance_between_players, moments_df[moments_df.player_id.isin([-1, None])][["x_loc", "y_loc"]])
        
        return ball_distances

    @staticmethod
    def distance_between_player_and_other_players(player_id, defending_ids, moments_df):
        print('inside distance_between_player_and_other_players with: ', player_id, defending_ids)
        print(moments_df[moments_df.player_id.isin(defending_ids)])
        group = moments_df[moments_df.player_id.isin(defending_ids)].groupby("player_id")[["x_loc", "y_loc"]]
    
        return group.apply(FeatureUtil.distance_between_players_with_moment, moments_df[moments_df.player_id == player_id][["x_loc", "y_loc"]])

    # Takes in data for ball/players for a moment, returns an int containing the amount of players on the side of the court with the ball
    @staticmethod
    def num_players_past_halfcourt(moment_df):
        # First, grab x_loc of ball to determine side of court
        ball_loc = moment_df.iloc[0]['x_loc']
        
        count = 0
        if (ball_loc > 47.0):
            for index, row in moment_df[1:].iterrows():
                if (row['x_loc'] > 47.0):
                    count += 1
        else:
            for index, row in moment_df[1:].iterrows():
                if (row['x_loc'] < 47.0):
                    count += 1

        return count

    @staticmethod
    def possession_at_moment(moment_df):
        distances = []

        for player in moment_df[5][1:]:
            distances.append([euclidean([moment_df[5][0][3], moment_df[5][0][4]], [player[3], player[4]]), player[0]])

        return min(distances, key=lambda x: x[0])[1]

    def convert_ball_handler_to_passes(ball_handler_df):
        passes = []
        passer = pd.NA
        pass_moment = 0
        receiver = pd.NA
        receive_moment = 0
        
        for i in range(0, len(ball_handler_df)):
            if pd.isna(passer) and not pd.isna(ball_handler_df.iloc[i]['player_id']):
                passer = ball_handler_df.iloc[i]['player_id']
            elif (not pd.isna(passer) and pass_moment == 0) and pd.isna(ball_handler_df.iloc[i]['player_id']):
                pass_moment = ball_handler_df.iloc[i - 1]['index']
            elif (not pd.isna(passer) and not pd.isna(ball_handler_df.iloc[i]['player_id'])) and passer == ball_handler_df.iloc[i]['player_id'] and pass_moment != 0:
                pass_moment = 0
            elif not pd.isna(passer) and (not pd.isna(ball_handler_df.iloc[i]['player_id']) and ball_handler_df.iloc[i]['player_id'] != passer):
                receiver = ball_handler_df.iloc[i]['player_id']
                receive_moment = ball_handler_df.iloc[i]['index']
                pass_moment = ball_handler_df.iloc[i - 1]['index'] if not pd.isna(ball_handler_df.iloc[i-1]['player_id']) else pass_moment
                passes.append({'passer': passer, 'pass_moment': pass_moment, 'receiver': receiver, 'receive_moment': receive_moment}) if len(passes) == 0 or passes[-1]['passer'] != passer or pass_moment > passes[-1]['pass_moment'] + 10 else ""
                passer = pd.NA
                receiver = pd.NA
                pass_moment = 0
        
        return passes

    # Checks the start and end location of the ball to determine if the pass occurs in the paint, returns a boolean
    @staticmethod
    def check_for_paint_pass(moments_df, event_pass):
        paint_pass = False
        start_loc = moments_df.loc[(moments_df['index'] == event_pass['pass_moment']) & (moments_df['player_id'] == -1)]
        end_loc = moments_df.loc[(moments_df['index'] == event_pass['receive_moment']) & (moments_df['player_id'] == -1)]

        if (((((start_loc['x_loc'] >= 0.0) & (start_loc['x_loc'] <= 19.0)) | ((start_loc['x_loc'] >= 71.0) & (start_loc['x_loc'] <= 90.0))) & ((start_loc['y_loc'] >= 17.0) & (start_loc['y_loc'] <= 33.0))).all()):
            paint_pass = True
        if (((((end_loc['x_loc'] >= 0.0) & (end_loc['x_loc'] <= 19.0)) | ((end_loc['x_loc'] >= 71.0) & (end_loc['x_loc'] <= 90.0))) & ((end_loc['y_loc'] >= 17.0) & (end_loc['y_loc'] <= 33.0))).all()):
            paint_pass = True

        return paint_pass

    # Checks the start and end location of the ball to determine if it is an inbound pass, returns a boolean
    @staticmethod
    def check_for_inbound_pass(moments_df, event_pass):
        inbound_pass = False
        start_loc = moments_df.loc[(moments_df['index'] == event_pass['pass_moment']) & (moments_df['player_id'] == event_pass['passer'])]

        if ((((start_loc['x_loc'] <= 0.0) | (start_loc['x_loc'] >= 94.0))) | ((start_loc['y_loc'] >= 50.0) | (start_loc['y_loc'] <= 0.0))).all():
            inbound_pass = True

        return inbound_pass

    @staticmethod
    def get_ball_handler_for_event(moments_df, player_ids):
        # First, calculate the distances between players and the ball, and get a min dist data frame
        ball_distances = FeatureUtil.distance_between_ball_and_players(moments_df, player_ids)
        #moments_df.to_csv("static/data/test/moments.csv")
        ball_dist_df = DataUtil.convert_labled_series_to_df('player_id', 'ball_distances', ball_distances)
        ball_handler_df = DataUtil.get_labled_mins_from_df(ball_dist_df, "dist_from_ball")
        # Also eliminate any moment where no player was within 3 feet of the ball
        ball_handler_df.loc[ball_handler_df['dist_from_ball'] > 3.3, 'player_id'] = pd.NA
        
        # Add the moment to the ball_handler_df
        moment_nums = []
        for index, row in ball_handler_df.iterrows():
            moment_nums.append(int(moments_df.iloc[index * 11]['index']))
        
        ball_handler_df['index'] = moment_nums

        # We also need to check the ball radius to make sure we aren't counting shot attempts 
        for i in range(0, len(ball_handler_df)):
            if moments_df.iloc[i*11]['radius'] >= 10.0:
                ball_handler_df.iat[i, 0] = pd.NA

        #ball_handler_df.to_csv("static/data/test/ball_handler.csv")
        return ball_handler_df

    @staticmethod
    def get_defender_for_player(moment_df, player_id, defensive_team_ids):
        print("Inside get_defender_for_player", player_id, defensive_team_ids)
        # First, calculate the distances between players and the defensive players, and get a min dist data frame
        ball_distances = FeatureUtil.distance_between_player_and_other_players(str(player_id), defensive_team_ids, moment_df)
        print(ball_distances)
        ball_dist_df = DataUtil.convert_labled_series_to_df('player_id', 'ball_distances', ball_distances)
        print(ball_dist_df)
        closest_defender_df = DataUtil.get_labled_mins_from_df(ball_dist_df, "dist_from_player")

        closest_defender_df.to_csv("static/data/test/defender.csv")
        return closest_defender_df

    @staticmethod
    def get_passess_for_event(moments_df, possession, players_data):
        # Get the player ids for the team in possession, we wan't to exclude defensive players
        player_ids = DataUtil.get_possession_team_player_ids(possession, players_data)
        ball_handler_df = FeatureUtil.get_ball_handler_for_event(moments_df, player_ids)    
        # Next, step through each moment and find the passes
        passes = FeatureUtil.convert_ball_handler_to_passes(ball_handler_df)

        return passes

    # Takes list of event_passes, and filters out dribble_hand_off candidates based on pass/receive moments within provided moment_range
    @staticmethod
    def get_dribble_handoff_candidates(combined_event_df, moments_df, event_passes, moment_range, players_dict, offset = 0):
        candidates = []
        candidate_count = 0
        for event_pass in event_passes:
            if (not FeatureUtil.check_for_paint_pass(moments_df, event_pass) and not FeatureUtil.check_for_inbound_pass(moments_df, event_pass) and event_pass['pass_moment'] + moment_range >= event_pass['receive_moment']):
                moment = moments_df.loc[(moments_df['index'] == event_pass['pass_moment']) & (moments_df['player_id'] == event_pass['passer'])]
                event_id = moment['event_id'].values[0]
                if offset > 0:
                    event_id = f"{event_id.split('-')[0]}-{int(event_id.split('-')[0]) + offset}"
                event = combined_event_df.loc[(combined_event_df['event_id'] == event_id)]
                candidate_count += 1
                candidates.append({
                    'candidate_id': f"{event_id}-{candidate_count}",
                    'event_id': event_id,
                    'classification_type': 'dribble-hand-off',
                    'manual_label': pd.NA,
                    'period': event['PERIOD'].values[0],
                    'game_clock': DataUtil.convert_game_clock_to_timestamp(moment['game_clock']),
                    'shot_clock': moment['shot_clock'].values[0],
                    'player_a': event_pass['passer'],
                    'player_a_name': players_dict[event_pass['passer']][0],
                    'player_b': event_pass['receiver'],
                    'player_b_name': players_dict[event_pass['receiver']][0]})
        
        return candidates

    @staticmethod
    def convert_coordinate_to_hexbin_vertex(x_loc, y_loc, vertices):
        min_distance = 10000
        temp_distance = 0
        closest_vertex = -1

        for vertex in vertices:
            temp_distance = abs(abs(x_loc) - abs(vertex[0])) + abs(abs(y_loc) - abs(vertex[1]))
            if temp_distance < min_distance:
                min_distance = temp_distance
                closest_vertex = vertex

        return f"({closest_vertex[0]},{closest_vertex[1]})"

    @staticmethod
    def get_lingress_results_for_player_trajectory(player_trajectory):
        return linregress(player_trajectory['x_loc'], player_trajectory['y_loc'])

    @staticmethod
    def rotate_coordinates_around_center_court(moments_df):
        moments_df.loc[:,'x_loc'] = 47.0 - (moments_df.loc[:,'x_loc'] - 47.0)
        moments_df.loc[:,'y_loc'] = 50.0 - moments_df.loc[:,'y_loc']

        return moments_df

    @staticmethod
    def get_offset_into_game(period, game_clock):
        offset = game_clock
        if (period <= 4):
            offset += (period - 1) * 12
        else:
            offset += 48 + (period - 1) * 5

        return math.floor(offset)

    @staticmethod
    def get_pass_duration(moments, event_passes, target_candidate):
        # Loop through the event passes and find the one corresponding to the candidate, returning the delta between the receive and pass moments 
        for event_pass in event_passes:
            if(moments.iloc[11*event_pass['pass_moment']]['shot_clock'] == target_candidate['shot_clock']):
                return event_pass['receive_moment'] - event_pass['pass_moment']

        # If this fails, just return NaN
        return np.NaN

    @staticmethod
    def get_pass_start_end(moments, event_passes, target_candidate):
        # Loop through the event passes and find the one corresponding to the candidate, returning the delta between the receive and pass moments 
        for event_pass in event_passes:
            if(moments.iloc[11*event_pass['pass_moment']]['shot_clock'] == target_candidate['shot_clock']):
                return event_pass['receive_moment'], event_pass['pass_moment']

        # If this fails, just return NaN
        return np.NaN