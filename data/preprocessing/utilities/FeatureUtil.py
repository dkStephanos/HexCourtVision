import numpy as np
import pandas as pd
from .DataUtil import DataUtil
from scipy.spatial.distance import euclidean

class FeatureUtil:

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
        return [euclidean(player_a.iloc[i], player_b.iloc[i])
                for i in range(player_range)]

    @staticmethod
    def distance_between_ball_and_players(event_df, player_ids):
        group = event_df[event_df.player_id.isin(player_ids)].groupby("player_id")[["x_loc", "y_loc"]]

        return group.apply(FeatureUtil.distance_between_players, event_df[event_df.player_id==-1][["x_loc", "y_loc"]])

    @staticmethod
    def distance_between_player_and_other_players(player_id, player_loc, event_df):
        group = event_df[event_df.player_id!=player_id].groupby("player_id")[["x_loc", "y_loc"]]

        return group.apply(FeatureUtil.distance_between_players, player_b=(player_loc))

    @staticmethod
    def get_passess_for_event(moments_df, possession, players_data):
        # Get the player ids for the team in possession, we wan't to exclude defensive players
        player_ids = DataUtil.get_possession_team_player_ids(possession, players_data)

        # First, calculate the distances between players and the ball, and get a min dist data frame
        ball_distances = FeatureUtil.distance_between_ball_and_players(moments_df, player_ids)
        ball_dist_df = DataUtil.convert_labled_series_to_df('player_id', 'ball_distances', ball_distances)
        min_dist_df = DataUtil.get_labled_mins_from_df(ball_dist_df, 'dist_from_ball')

        # Get the player ids for the team in possession, we wan't to exclude defensive players
        #player_ids = DataUtil.get_possession_team_player_ids(possession, players_data)
        #min_dist_df.loc[~min_dist_df['player_id'].isin(player_ids), 'player_id'] = pd.NA
        
        # Also eliminate any moment where no player was within 3 feet of the ball
        min_dist_df.loc[min_dist_df['dist_from_ball'] > 3.3, 'player_id'] = pd.NA

        # We also need to check the ball radius to make sure we aren't counting shot attempts 
        for i in range(0, len(min_dist_df)):
            if moments_df.iloc[i*11]['radius'] >= 10.0:
                min_dist_df.iat[i, 0] = pd.NA

        # Next, step through each moment and find the passes
        passes = []
        passer = pd.NA
        pass_moment = 0
        receiver = pd.NA
        receive_moment = 0
        for i in range(0, len(min_dist_df)):
            if pd.isna(passer) and not pd.isna(min_dist_df.iloc[i]['player_id']):
                passer = min_dist_df.iloc[i]['player_id']
            elif (not pd.isna(passer) and pass_moment == 0) and pd.isna(min_dist_df.iloc[i]['player_id']):
                pass_moment = i - 1
            elif not pd.isna(passer) and (not pd.isna(min_dist_df.iloc[i]['player_id']) and min_dist_df.iloc[i]['player_id'] != passer):
                receiver = min_dist_df.iloc[i]['player_id']
                receive_moment = i
                passes.append({'passer': passer, 'pass_moment': pass_moment, 'receiver': receiver, 'receive_moment': receive_moment})
                passer = pd.NA
                receiver = pd.NA
                pass_moment = 0

        print(passes)
        min_dist_df.to_csv('static/data/test/ball_handler.csv')
        
        return min_dist_df