
import pandas as pd
import matplotlib.pyplot as plt
import math, sys, os, traceback
from django.forms.models import model_to_dict

from data.preprocessing.utilities.DataUtil import DataUtil
from data.preprocessing.utilities.FeatureUtil import FeatureUtil
from data.preprocessing.utilities.GraphUtil import GraphUtil

from data.models import Game
from data.models import Player
from data.models import Event
from data.models import Moment
from data.models import Candidate
from data.models import CandidateFeatureVector

pd.set_option('mode.chained_assignment', None)

def generate_feature_vector(target_event, target_candidate):
    # Collects moments for single candidate
    moments = pd.DataFrame(list(Moment.objects.filter(event_id=target_candidate['event_id']).values()))

    # Collects players for single candidate
    screener = Player.objects.values().get(player_id=target_candidate['player_a_id'])
    cutter = Player.objects.values().get(player_id=target_candidate['player_b_id'])

    # Collects passes for event
    event_passes = FeatureUtil.get_passess_for_event(moments, Event.objects.values().get(event_id=target_candidate['event_id'])['possesion_team_id'], list(Player.objects.values()))

    # Trim the moments data around the pass
    game_clock = DataUtil.convert_timestamp_to_game_clock(target_candidate['game_clock'])
    trimmed_moments = moments[(moments.game_clock > game_clock - 2) & (moments.game_clock < game_clock + 2)]

    # If the data occurs past half-court (x > 47), rotate the points about the center of the court so features appear consistent 
    if(trimmed_moments.iloc[math.ceil(len(trimmed_moments)/2)]['x_loc'] > 47.0):
        trimmed_moments = FeatureUtil.rotate_coordinates_around_center_court(trimmed_moments)

    # Pull out other moment subsects for features
    approach_moments = trimmed_moments[trimmed_moments.game_clock < game_clock]
    execution_moments = trimmed_moments[trimmed_moments.game_clock > game_clock]
    pass_moment = trimmed_moments.iloc[math.ceil(len(trimmed_moments)/2):math.ceil(len(trimmed_moments)/2) + 11]
    start_moment = approach_moments.iloc[0:11]
    end_moment = execution_moments.iloc[len(execution_moments) - 12:len(execution_moments) - 1]

    # Gets screen moment
    screener_pos_data = DataUtil.get_player_position_data(trimmed_moments, screener['player_id'])
    filtered_moments = trimmed_moments.loc[(trimmed_moments.player_id.isin([screener['player_id'], cutter['player_id']]))]
    distance_from_screener = FeatureUtil.distance_between_player_and_other_players(screener['player_id'], screener_pos_data, filtered_moments)
    min_dist_from_screen = min(distance_from_screener[0])
    screen_moment = trimmed_moments.loc[trimmed_moments['index'] == int(min_dist_from_screen[1])]

    # Isolate cutter, screener and ball from trimmed_moments
    cutter_df = trimmed_moments[trimmed_moments['player_id'] == cutter['player_id']][['x_loc', 'y_loc']]
    screener_df = trimmed_moments[trimmed_moments['player_id'] == screener['player_id']][['x_loc', 'y_loc']]
    ball_df = trimmed_moments[trimmed_moments['player_id'].isna()][['x_loc', 'y_loc']]
    
    # Collect linregress stats for cutter, screener, ball
    cutter_df_approach = approach_moments[approach_moments['player_id'] == cutter['player_id']][['x_loc', 'y_loc']]
    screener_df_approach = approach_moments[approach_moments['player_id'] == screener['player_id']][['x_loc', 'y_loc']]
    ball_df_approach = approach_moments[approach_moments['player_id'].isna()][['x_loc', 'y_loc']]
    cutter_linregress_stats_approach = FeatureUtil.get_lingress_results_for_player_trajectory(cutter_df_approach)
    screener_linregress_stats_approach = FeatureUtil.get_lingress_results_for_player_trajectory(screener_df_approach)
    ball_linregress_stats_approach = FeatureUtil.get_lingress_results_for_player_trajectory(ball_df_approach)
    cutter_df_execution = execution_moments[execution_moments['player_id'] == cutter['player_id']][['x_loc', 'y_loc']]
    screener_df_execution = execution_moments[execution_moments['player_id'] == screener['player_id']][['x_loc', 'y_loc']]
    ball_df_execution = execution_moments[execution_moments['player_id'].isna()][['x_loc', 'y_loc']]
    cutter_linregress_stats_execution = FeatureUtil.get_lingress_results_for_player_trajectory(cutter_df_execution)
    screener_linregress_stats_execution = FeatureUtil.get_lingress_results_for_player_trajectory(screener_df_execution)
    ball_linregress_stats_execution = FeatureUtil.get_lingress_results_for_player_trajectory(ball_df_execution)

    # Offset y_loc data to work with hexbin
    screener_hex_df = screener_df.copy(deep=True)
    cutter_hex_df = cutter_df.copy(deep=True)
    ball_hex_df = ball_df.copy(deep=True)
    screener_hex_df['y_loc'] = screener_hex_df['y_loc'] - 50.0
    cutter_hex_df['y_loc'] = cutter_hex_df['y_loc'] - 50.0
    ball_hex_df['y_loc'] = ball_hex_df['y_loc'] - 50.0
    ax = GraphUtil.draw_court()	
    screener_hexbin = ax.hexbin(x=screener_hex_df['x_loc'], y=screener_hex_df['y_loc'], cmap=plt.cm.Greens, mincnt=1, gridsize=50, extent=(0,94,-50,0))
    cutter_hexbin = ax.hexbin(x=cutter_hex_df['x_loc'], y=cutter_hex_df['y_loc'], cmap=plt.cm.Blues, mincnt=1, gridsize=50, extent=(0,94,-50,0))
    ball_hexbin = ax.hexbin(x=ball_hex_df['x_loc'], y=ball_hex_df['y_loc'], cmap=plt.cm.Reds, mincnt=1, gridsize=50, extent=(0,94,-50,0))

    # Create the feature vector
    feature_vector = {
        # Classification
        'classification': target_candidate['manual_label'],
        'candidate_id': target_candidate['candidate_id'],

        # Player Data
        'cutter_archetype': cutter['position'],
        'screener_archetype': screener['position'],

        # Location Data
        'cutter_loc_on_pass': FeatureUtil.convert_coordinate_to_hexbin_vertex(
            pass_moment.loc[pass_moment['player_id'] == cutter['player_id']]['x_loc'].values[0],
            pass_moment.loc[pass_moment['player_id'] == cutter['player_id']]['y_loc'].values[0],
            cutter_hexbin._offsets),
        'screener_loc_on_pass': FeatureUtil.convert_coordinate_to_hexbin_vertex(
            pass_moment.loc[pass_moment['player_id'] == screener['player_id']]['x_loc'].values[0],
            pass_moment.loc[pass_moment['player_id'] == screener['player_id']]['y_loc'].values[0],
            screener_hexbin._offsets),
        'ball_loc_on_pass': FeatureUtil.convert_coordinate_to_hexbin_vertex(
            pass_moment.loc[pass_moment['player_id'].isna()]['x_loc'].item(),
            pass_moment.loc[pass_moment['player_id'].isna()]['y_loc'].item(),
            ball_hexbin._offsets),
        'ball_radius_on_pass': pass_moment.loc[pass_moment['player_id'].isna()]['radius'].item(),
        'cutter_loc_on_start_approach': FeatureUtil.convert_coordinate_to_hexbin_vertex(
            start_moment.loc[start_moment['player_id'] == cutter['player_id']]['x_loc'].values[0],
            start_moment.loc[start_moment['player_id'] == cutter['player_id']]['y_loc'].values[0],
            cutter_hexbin._offsets),
        'screener_loc_on_start_approach': FeatureUtil.convert_coordinate_to_hexbin_vertex(
            start_moment.loc[start_moment['player_id'] == screener['player_id']]['x_loc'].values[0],
            start_moment.loc[start_moment['player_id'] == screener['player_id']]['y_loc'].values[0],
            screener_hexbin._offsets),
        'ball_loc_on_start_approach': FeatureUtil.convert_coordinate_to_hexbin_vertex(
            start_moment.loc[start_moment['player_id'].isna()]['x_loc'].item(),
            start_moment.loc[start_moment['player_id'].isna()]['y_loc'].item(),
            ball_hexbin._offsets),
        'ball_radius_loc_on_start_approach': start_moment[start_moment['player_id'].isna()]['radius'].item(),
        'cutter_loc_on_end_execution': FeatureUtil.convert_coordinate_to_hexbin_vertex(
            end_moment.loc[end_moment['player_id'] == cutter['player_id']]['x_loc'].values[0],
            end_moment.loc[end_moment['player_id'] == cutter['player_id']]['y_loc'].values[0],
            cutter_hexbin._offsets),
        'screener_loc_on_end_execution': FeatureUtil.convert_coordinate_to_hexbin_vertex(
            end_moment.loc[end_moment['player_id'] == screener['player_id']]['x_loc'].values[0],
            end_moment.loc[end_moment['player_id'] == screener['player_id']]['y_loc'].values[0],
            screener_hexbin._offsets),
        'ball_loc_on_end_execution': FeatureUtil.convert_coordinate_to_hexbin_vertex(
            end_moment.loc[end_moment['player_id'].isna()]['x_loc'].item(),
            end_moment.loc[end_moment['player_id'].isna()]['y_loc'].item(),
            ball_hexbin._offsets),
        'ball_radius_loc_on_end_execution': end_moment[end_moment['player_id'].isna()]['radius'].item(),
        'cutter_loc_on_screen': FeatureUtil.convert_coordinate_to_hexbin_vertex(
            screen_moment.loc[screen_moment['player_id'] == cutter['player_id']]['x_loc'].values[0],
            screen_moment.loc[screen_moment['player_id'] == cutter['player_id']]['y_loc'].values[0],
            cutter_hexbin._offsets),
        'screener_loc_on_screen': FeatureUtil.convert_coordinate_to_hexbin_vertex(
            screen_moment.loc[screen_moment['player_id'] == screener['player_id']]['x_loc'].values[0],
            screen_moment.loc[screen_moment['player_id'] == screener['player_id']]['y_loc'].values[0],
            screener_hexbin._offsets),
        'ball_loc_on_screen': FeatureUtil.convert_coordinate_to_hexbin_vertex(
            screen_moment.loc[screen_moment['player_id'].isna()]['x_loc'].item(),
            screen_moment.loc[screen_moment['player_id'].isna()]['y_loc'].item(),
            ball_hexbin._offsets),
        'ball_radius_on_screen': screen_moment.loc[screen_moment['player_id'].isna()]['radius'].item(),

        # Travel Distance Data
        'cutter_dist_traveled_approach': FeatureUtil.travel_dist(approach_moments[approach_moments['player_id'] == cutter['player_id']]),
        'cutter_dist_traveled_execution': FeatureUtil.travel_dist(execution_moments[execution_moments['player_id'] == cutter['player_id']]),
        'screener_dist_traveled_approach': FeatureUtil.travel_dist(approach_moments[approach_moments['player_id'] == screener['player_id']]),
        'screener_dist_traveled_execution': FeatureUtil.travel_dist(execution_moments[execution_moments['player_id'] == screener['player_id']]),
        'ball_dist_traveled_approach': FeatureUtil.travel_dist(approach_moments[approach_moments['player_id'].isna()]),
        'ball_dist_traveled_execution': FeatureUtil.travel_dist(execution_moments[execution_moments['player_id'].isna()]),

        # Relative Distance Data
        'players_dist_on_pass': FeatureUtil.distance_between_players_at_moment(
            [pass_moment.loc[pass_moment['player_id'] == cutter['player_id']]['x_loc'].values[0], pass_moment.loc[pass_moment['player_id'] == cutter['player_id']]['y_loc'].values[0]],
            [pass_moment.loc[pass_moment['player_id'] == screener['player_id']]['x_loc'].values[0], pass_moment.loc[pass_moment['player_id'] == screener['player_id']]['y_loc'].values[0]]),
        'cutter_dist_from_ball_on_pass': FeatureUtil.distance_between_players_at_moment(
            [pass_moment.loc[pass_moment['player_id'] == cutter['player_id']]['x_loc'].values[0], pass_moment.loc[pass_moment['player_id'] == cutter['player_id']]['y_loc'].values[0]],
            [pass_moment.loc[pass_moment['player_id'].isna()]['x_loc'].values[0], pass_moment.loc[pass_moment['player_id'].isna()]['y_loc'].values[0]]),
        'screener_dist_from_ball_on_pass': FeatureUtil.distance_between_players_at_moment(
            [pass_moment.loc[pass_moment['player_id'] == screener['player_id']]['x_loc'].values[0], pass_moment.loc[pass_moment['player_id'] == screener['player_id']]['y_loc'].values[0]],
            [pass_moment.loc[pass_moment['player_id'].isna()]['x_loc'].values[0], pass_moment.loc[pass_moment['player_id'].isna()]['y_loc'].values[0]]),

        'players_dist_on_screen': FeatureUtil.distance_between_players_at_moment(
            [screen_moment.loc[screen_moment['player_id'] == cutter['player_id']]['x_loc'].values[0], screen_moment.loc[screen_moment['player_id'] == cutter['player_id']]['y_loc'].values[0]],
            [screen_moment.loc[screen_moment['player_id'] == screener['player_id']]['x_loc'].values[0], screen_moment.loc[screen_moment['player_id'] == screener['player_id']]['y_loc'].values[0]]),
        'cutter_dist_from_ball_on_screen': FeatureUtil.distance_between_players_at_moment(
            [screen_moment.loc[screen_moment['player_id'] == cutter['player_id']]['x_loc'].values[0], screen_moment.loc[screen_moment['player_id'] == cutter['player_id']]['y_loc'].values[0]],
            [screen_moment.loc[screen_moment['player_id'].isna()]['x_loc'].values[0], screen_moment.loc[screen_moment['player_id'].isna()]['y_loc'].values[0]]),
        'screener_dist_from_ball_on_screen': FeatureUtil.distance_between_players_at_moment(
            [screen_moment.loc[screen_moment['player_id'] == screener['player_id']]['x_loc'].values[0], screen_moment.loc[screen_moment['player_id'] == screener['player_id']]['y_loc'].values[0]],
            [screen_moment.loc[screen_moment['player_id'].isna()]['x_loc'].values[0], screen_moment.loc[screen_moment['player_id'].isna()]['y_loc'].values[0]]),
        
        'players_dist_on_start_approach': FeatureUtil.distance_between_players_at_moment(
            [start_moment.loc[start_moment['player_id'] == cutter['player_id']]['x_loc'].values[0], start_moment.loc[start_moment['player_id'] == cutter['player_id']]['y_loc'].values[0]],
            [start_moment.loc[start_moment['player_id'] == screener['player_id']]['x_loc'].values[0], start_moment.loc[start_moment['player_id'] == screener['player_id']]['y_loc'].values[0]]),
        'cutter_dist_from_ball_on_approach': FeatureUtil.distance_between_players_at_moment(
            [start_moment.loc[start_moment['player_id'] == cutter['player_id']]['x_loc'].values[0], start_moment.loc[start_moment['player_id'] == cutter['player_id']]['y_loc'].values[0]],
            [start_moment.loc[start_moment['player_id'].isna()]['x_loc'].values[0], start_moment.loc[start_moment['player_id'].isna()]['y_loc'].values[0]]),
        'screener_dist_from_ball_on_approach': FeatureUtil.distance_between_players_at_moment(
            [start_moment.loc[start_moment['player_id'] == screener['player_id']]['x_loc'].values[0], start_moment.loc[start_moment['player_id'] == screener['player_id']]['y_loc'].values[0]],
            [start_moment.loc[start_moment['player_id'].isna()]['x_loc'].values[0], start_moment.loc[start_moment['player_id'].isna()]['y_loc'].values[0]]),
        
        'players_dist_on_end_execution': FeatureUtil.distance_between_players_at_moment(
            [end_moment.loc[end_moment['player_id'] == cutter['player_id']]['x_loc'].values[0], end_moment.loc[end_moment['player_id'] == cutter['player_id']]['y_loc'].values[0]],
            [end_moment.loc[end_moment['player_id'] == screener['player_id']]['x_loc'].values[0], end_moment.loc[end_moment['player_id'] == screener['player_id']]['y_loc'].values[0]]),
        'cutter_dist_from_ball_on_execution': FeatureUtil.distance_between_players_at_moment(
            [end_moment.loc[end_moment['player_id'] == cutter['player_id']]['x_loc'].values[0], end_moment.loc[end_moment['player_id'] == cutter['player_id']]['y_loc'].values[0]],
            [end_moment.loc[end_moment['player_id'].isna()]['x_loc'].values[0], end_moment.loc[end_moment['player_id'].isna()]['y_loc'].values[0]]),
        'screener_dist_from_ball_on_execution': FeatureUtil.distance_between_players_at_moment(
            [end_moment.loc[end_moment['player_id'] == screener['player_id']]['x_loc'].values[0], end_moment.loc[end_moment['player_id'] == screener['player_id']]['y_loc'].values[0]],
            [end_moment.loc[end_moment['player_id'].isna()]['x_loc'].values[0], end_moment.loc[end_moment['player_id'].isna()]['y_loc'].values[0]]),

        # Speed/Acceleration Data
        'cutter_avg_speed_approach': FeatureUtil.average_speed(approach_moments, cutter['player_id']),
        'cutter_avg_speed_execution': FeatureUtil.average_speed(execution_moments, cutter['player_id']),
        'screener_avg_speed_approach': FeatureUtil.average_speed(approach_moments, screener['player_id']),
        'screener_avg_speed_execution': FeatureUtil.average_speed(execution_moments, screener['player_id']),
        'ball_avg_speed_approach': FeatureUtil.average_speed(approach_moments, None),
        'ball_avg_speed_execution': FeatureUtil.average_speed(execution_moments, None),

        # Linear Regression Data
        'slope_of_cutter_trajectory_approach': cutter_linregress_stats_approach[0],
        'intercept_of_cutter_trajectory_approach': cutter_linregress_stats_approach[1],
        'slope_of_cutter_trajectory_execution': cutter_linregress_stats_execution[0],
        'intercept_of_cutter_trajectory_execution': cutter_linregress_stats_execution[1],
        'slope_of_screener_trajectory_approach': screener_linregress_stats_approach[0],
        'intercept_of_screener_trajectory_approach': screener_linregress_stats_approach[1],
        'slope_of_screener_trajectory_execution': screener_linregress_stats_execution[0],
        'intercept_of_screener_trajectory_execution': screener_linregress_stats_execution[1],
        'slope_of_ball_trajectory_approach': ball_linregress_stats_approach[0],
        'intercept_of_ball_trajectory_approach': ball_linregress_stats_approach[1],
        'slope_of_ball_trajectory_execution': ball_linregress_stats_execution[0],
        'intercept_of_ball_trajectory_execution': ball_linregress_stats_execution[1],

        # Play Data
        'offset_into_play': math.floor(pass_moment.iloc[0]['shot_clock'] / 6),
        'pass_duration': FeatureUtil.get_pass_duration(moments, event_passes, target_candidate),
        'num_players_past_half_court': FeatureUtil.num_players_past_halfcourt(pass_moment),
        'is_inbounds_pass': FeatureUtil.check_for_inbound_pass(moments, event_passes[0])
    }

    print("\n\n------------------------------ Feature Vector ---------------------------\n")
    print(feature_vector)
    print(f"\n Num Features: {len(feature_vector.keys())-2}")

    return feature_vector

def run():
    num_failed_candidates = 0
    num_successful_candidates = 0
    issue_candidates = []
    for game in Game.objects.all():
        events = Event.objects.filter(game=game)
        for event in events:
            target_event = model_to_dict(event)
            next_candidates = Candidate.objects.filter(event=event).values()
            for target_candidate in next_candidates:
                has_vector = CandidateFeatureVector.objects.filter(candidate=target_candidate).exists()
                if not has_vector:
                    try:
                        vector = generate_feature_vector(target_event, target_candidate)
                        CandidateFeatureVector.objects.update_or_create(**vector)
                        num_successful_candidates += 1
                    except Exception as e:
                        print(f"Issue at candidate: {target_candidate['candidate_id']}")
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname)
                        print(traceback.print_tb(exc_tb))
                        issue_candidates.append(target_candidate)
                        num_failed_candidates += 1

        output = f"Total successful candidates: {num_successful_candidates}\nTotal failed candidates: {num_failed_candidates}" 
        print(output)
        text_file = open("static/data/test/feature_gen_results_round2.txt", "w")
        text_file.write(output)
        text_file.close()
    