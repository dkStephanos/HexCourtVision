import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import math, sys, os, traceback
from django.forms.models import model_to_dict

from ml_nba.preprocessing.utilities.DataUtil import DataUtil
from ml_nba.preprocessing.utilities.FeatureUtil import FeatureUtil
from ml_nba.preprocessing.utilities.ConstantsUtil import ConstantsUtil
from ml_nba.preprocessing.utilities.GraphUtil import GraphUtil

from ml_nba.models import Game
from ml_nba.models import Player
from ml_nba.models import Event
from ml_nba.models import Moment
from ml_nba.models import Candidate

def generate_trajectory_image(target_event, target_candidate):
    target_event = model_to_dict(target_event)
    # visiting_team = []
    # home_team = []
    # game_df = DataUtil.load_game_df(ConstantsUtil.games['20151106MILNYK']['raw_data'])
    # for index, event in game_df.iterrows():
    #     if(event['events']['eventId'] == str(int(target_event['event_id'].split('-')[1]))):
    #         for player in event['events']['visitor']['players']:
    #             visiting_team.append(str(player['playerid']))
    #         for player in event['events']['home']['players']:
    #             home_team.append(str(player['playerid']))

    # if target_candidate['player_a_id'] in home_team:
    #     defending_team = visiting_team
    # else:
    #     defending_team = home_team
    
    # Collects moments for single candidate
    moments = pd.DataFrame(list(Moment.objects.filter(event_id=target_candidate['event_id']).values()))

    event_passes = FeatureUtil.get_passess_for_event(moments, Event.objects.values().get(event_id=target_candidate['event_id'])['possession_team_id'], list(Player.objects.values()))
    pass_moment, receive_moment = FeatureUtil.get_pass_start_end(moments, event_passes, target_candidate)

    # Collects players for single candidate
    screener = Player.objects.values().get(player_id=target_candidate['player_a_id'])
    cutter = Player.objects.values().get(player_id=target_candidate['player_b_id'])

    # Collects defenders for screener and cutter
    #screener_defender = FeatureUtil.get_defender_for_player(moments, target_candidate['player_a_id'], defending_team)
    #print(screener_defender)

    # Trim the moments data around the pass
    game_clock = DataUtil.convert_timestamp_to_game_clock(target_candidate['game_clock'])
    trimmed_moments = moments[(moments.game_clock > game_clock - 2) & (moments.game_clock < game_clock + 2)]
    
    # If the data occurs past half-court (x > 47), rotate the points about the center of the court so features appear consistent 
    if(trimmed_moments.iloc[math.ceil(len(trimmed_moments)/2)]['x_loc'] > 47.0):
        trimmed_moments = FeatureUtil.rotate_coordinates_around_center_court(trimmed_moments)

    # Isolate cutter, screener and ball from trimmed_moments
    cutter_df = trimmed_moments[trimmed_moments['player_id'] == cutter['player_id']][['x_loc', 'y_loc']]
    screener_df = trimmed_moments[trimmed_moments['player_id'] == screener['player_id']][['x_loc', 'y_loc']]
    ball_df = trimmed_moments[(trimmed_moments['index'] >= pass_moment - 5) & (trimmed_moments['index'] <= receive_moment + 5)]
    ball_df = ball_df[ball_df['player_id'].isna()][['x_loc', 'y_loc']]

    # Offset location data to work with hexbins
    screener_df['y_loc'] = screener_df['y_loc'] - 50.0
    cutter_df['y_loc'] = cutter_df['y_loc'] - 50.0
    ball_df['y_loc'] = ball_df['y_loc'] - 50.0
    
    # Create the colormaps
    cmapBlues = mpl.cm.summer(np.linspace(0,1,20))
    cmapBlues = mpl.colors.ListedColormap(cmapBlues[0:,:-1])
    cmapGreens = mpl.cm.autumn(np.linspace(0,1,20))
    cmapGreens = mpl.colors.ListedColormap(cmapGreens[0:,:-1])
    cmapReds = mpl.cm.winter(np.linspace(0,1,20))
    cmapReds = mpl.colors.ListedColormap(cmapReds[0:,:-1])

    # Draw the court and the hexbins
    ax = GraphUtil.draw_court()	    
    cutter_hexbin = ax.hexbin(x=cutter_df['x_loc'], y=cutter_df['y_loc'], cmap=cmapGreens, mincnt=1, gridsize=42, extent=(0,94,-50,0))
    screener_hexbin = ax.hexbin(x=screener_df['x_loc'], y=screener_df['y_loc'], cmap=cmapBlues, mincnt=1, gridsize=42, extent=(0,94,-50,0))
    ball_hexbin = ax.hexbin(x=ball_df['x_loc'], y=ball_df['y_loc'], cmap=cmapReds, mincnt=1, gridsize=42, extent=(0,94,-50,0))

    GraphUtil.save_half_court(f"static/backend/hexmaps/{target_candidate['candidate_id']}-hexmap.png")

def run():
    files = os.listdir("static/backend/hexmaps30")
    dont_render = False
    games = Game.objects.all()
    for game in games:
        events = Event.objects.filter(game=game)
        for event in events:
            next_candidates = Candidate.objects.filter(event=event).values()
            for candidate in next_candidates:
                # for file in files:
                #     if candidate['candidate_id'] in file:
                #         dont_render = True
                if (dont_render == False and candidate['manual_label'] == True):
                    print("Generating hexbin trajectory image for candidate: ", candidate['candidate_id'])
                    try:
                        generate_trajectory_image(event, candidate)
                    except Exception as e:
                        print(f"Issue at candidate: {candidate['candidate_id']}:  {str(e)}")
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname)
                        print(traceback.print_tb(exc_tb))
                dont_render = False