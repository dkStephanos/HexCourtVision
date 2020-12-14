from matplotlib.pyplot import annotate
import numpy as np
import pandas as pd
from .DataUtil import DataUtil
from scipy.spatial.distance import euclidean

class FeatureUtil:

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
    def average_speed(event_df, player):
        # get the number of seconds for the play
        seconds = event_df.game_clock.max() - event_df.game_clock.min()
        # feet per second
        player_fps = FeatureUtil.travel_dist(player) / seconds
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
    # Function to find the distance between players at each moment
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
    def distance_between_ball_and_players(moments_df, player_ids):
        group = moments_df[moments_df.player_id.isin(player_ids)].groupby("player_id")[["x_loc", "y_loc"]]
        ball_distances = group.apply(FeatureUtil.distance_between_players, moments_df[moments_df.player_id==-1][["x_loc", "y_loc"]])
        
        return ball_distances

    @staticmethod
    def possession_at_moment(moment_df):
        distances = []

        for player in moment_df[5][1:]:
            distances.append([euclidean([moment_df[5][0][3], moment_df[5][0][4]], [player[3], player[4]]), player[0]])

        return min(distances, key=lambda x: x[0])[1]


    @staticmethod
    def distance_between_player_and_other_players(player_id, player_loc, event_df):
        group = event_df[event_df.player_id!=player_id].groupby("player_id")[["x_loc", "y_loc"]]

        return group.apply(FeatureUtil.distance_between_players, player_b=(player_loc))

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
                pass_moment = ball_handler_df.iloc[i - 1]['moment']
            elif (not pd.isna(passer) and not pd.isna(ball_handler_df.iloc[i]['player_id'])) and passer == ball_handler_df.iloc[i]['player_id'] and pass_moment != 0:
                pass_moment = 0
            elif not pd.isna(passer) and (not pd.isna(ball_handler_df.iloc[i]['player_id']) and ball_handler_df.iloc[i]['player_id'] != passer):
                receiver = ball_handler_df.iloc[i]['player_id']
                receive_moment = ball_handler_df.iloc[i]['moment']
                pass_moment = ball_handler_df.iloc[i - 1]['moment'] if not pd.isna(ball_handler_df.iloc[i-1]['player_id']) else pass_moment
                passes.append({'passer': passer, 'pass_moment': pass_moment, 'receiver': receiver, 'receive_moment': receive_moment}) if len(passes) == 0 or passes[-1]['passer'] != passer else ""
                passer = pd.NA
                receiver = pd.NA
                pass_moment = 0
        
        return passes

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
            moment_nums.append(int(moments_df.iloc[index * 11]['moment']))
        
        ball_handler_df['moment'] = moment_nums

        # We also need to check the ball radius to make sure we aren't counting shot attempts 
        for i in range(0, len(ball_handler_df)):
            if moments_df.iloc[i*11]['radius'] >= 10.0:
                ball_handler_df.iat[i, 0] = pd.NA

        #ball_handler_df.to_csv("static/data/test/ball_handler.csv")
        return ball_handler_df

    @staticmethod
    def get_passess_for_event(moments_df, possession, players_data):
        # Get the player ids for the team in possession, we wan't to exclude defensive players
        player_ids = DataUtil.get_possession_team_player_ids(possession, players_data)

        ball_handler_df = FeatureUtil.get_ball_handler_for_event(moments_df, player_ids)    

        # Next, step through each moment and find the passes
        passes = FeatureUtil.convert_ball_handler_to_passes(ball_handler_df)
        
        return passes

    # Takes in a list of basic pass objects (passer, pass_moment, receiver, receive_moment) and calculates features for passes
    @staticmethod
    def get_pass_features(moments_df, event_passes):
        for event_pass in event_passes:
            player_pass_data = moments_df.loc[(moments_df['moment'] == event_pass['pass_moment']) & (moments_df['player_id'] == event_pass['passer'])]
            ball_pass_data = moments_df.loc[(moments_df['moment'] == event_pass['pass_moment']) & (moments_df['player_id'] == -1)]
            player_receive_data = moments_df.loc[(moments_df['moment'] == event_pass['receive_moment']) & (moments_df['player_id'] == event_pass['receiver'])]
            ball_receive_data = moments_df.loc[(moments_df['moment'] == event_pass['receive_moment']) & (moments_df['player_id'] == -1)]     
            print(player_pass_data)
            print(player_receive_data)
            print(ball_pass_data)
            print(ball_receive_data)
        return event_passes

    # Takes list of event_passes, and filters out dribble_hand_off candidates based on pass/receive moments within provided moment_range
    @staticmethod
    def get_dribble_handoff_candidates(combined_event_df, moments_df, event_passes, moment_range, players_dict):
        candidates = []
        for event_pass in event_passes:
            if (event_pass['pass_moment'] + moment_range >= event_pass['receive_moment']):
                moment = moments_df.loc[(moments_df['moment'] == event_pass['pass_moment']) & (moments_df['player_id'] == event_pass['passer'])]
                event_id = moment['event_id'].values[0]
                event = combined_event_df.loc[(combined_event_df['event_id'] == event_id)]
                if len(candidates) == 0 or candidates[-1]['shot_clock'] - moment['shot_clock'].values[0] > .2:
                    candidates.append({
                        'event_id': event_id,
                         'classification_type': 'dribble-hand-off',
                         'classification': pd.NA,
                         'period': event['PERIOD'].values[0],
                         'game_clock': DataUtil.convert_game_clock_to_timestamp(moment['game_clock']),
                         'shot_clock': moment['shot_clock'].values[0],
                         'screener': players_dict[event_pass['passer']],
                         'cutter': players_dict[event_pass['receiver']]})
        return candidates