
from matplotlib import colors
import pandas as pd
import matplotlib.pyplot as plt
import math

from data.preprocessing.utilities.DataUtil import DataUtil
from data.preprocessing.utilities.FeatureUtil import FeatureUtil
from data.preprocessing.utilities.ConstantsUtil import ConstantsUtil
from data.preprocessing.utilities.GraphUtil import GraphUtil

from data.models import Game
from data.models import Team
from data.models import Player
from data.models import Event
from data.models import Moment
from data.models import Candidate

def run():
    # Collects all games -- Add loop later
    print(Game.objects.all())

    # Collects all candidates for a given event -- Add loop later
    candidates = []
    events = Event.objects.filter(game=Game.objects.all()[0])
    for event in events:
        next_candidates = Candidate.objects.filter(event=event).values()
        candidates += list(next_candidates)

    # Collects moments for single candidate -- Add loop later
    target_candidate = candidates[1]
    print(target_candidate)
    moments = pd.DataFrame(list(Moment.objects.filter(event_id=target_candidate['event_id']).values()))

    # Collects players for single candidate
    screener = Player.objects.values().get(player_id=target_candidate['player_a_id'])
    cutter = Player.objects.values().get(player_id=target_candidate['player_b_id'])
    print(screener)

    # Collects passes for event
    event_passes = FeatureUtil.get_passess_for_event(moments, Event.objects.values().get(event_id=target_candidate['event_id'])['possesion_team_id'], list(Player.objects.values()))
    print(event_passes[0])

    # Trim the moments data around the pass
    game_clock = DataUtil.convert_timestamp_to_game_clock(target_candidate['game_clock'])
    trimmed_moments = moments[(moments.game_clock > game_clock - 2) & (moments.game_clock < game_clock + 2)]
    approach_moments = trimmed_moments[trimmed_moments.game_clock < game_clock]
    execution_moments = trimmed_moments[trimmed_moments.game_clock > game_clock]
    pass_moment = trimmed_moments[trimmed_moments.game_clock == game_clock]
    start_moment = approach_moments[approach_moments.game_clock == approach_moments.iloc[0].game_clock]
    end_moment = execution_moments[execution_moments.game_clock == execution_moments.iloc[-1].game_clock]

    # Get's screen moment
    screener_pos_data = DataUtil.get_player_position_data(trimmed_moments, screener['player_id'])
    filtered_moments = trimmed_moments.loc[(trimmed_moments.player_id.isin([screener['player_id'], cutter['player_id']]))]
    distance_from_screener = FeatureUtil.distance_between_player_and_other_players(screener['player_id'], screener_pos_data, filtered_moments)
    min_dist_from_screen = min(distance_from_screener[0])
    screen_moment = trimmed_moments.loc[trimmed_moments['index'] == int(min_dist_from_screen[1])]


    cutter_df = trimmed_moments[trimmed_moments['player_id'] == cutter['player_id']][['x_loc', 'y_loc']]
    cutter_df['y_loc'] = cutter_df['y_loc'] - 50.0
    screener_df = trimmed_moments[trimmed_moments['player_id'] == screener['player_id']][['x_loc', 'y_loc']]
    screener_df['y_loc'] = screener_df['y_loc'] - 50.0
    
    ax = GraphUtil.draw_court()	
    cutter_hexbin = ax.hexbin(x=cutter_df['x_loc'], y=cutter_df['y_loc'], cmap=plt.cm.winter, mincnt=1, gridsize=50, extent=(0,94,-50,0))
    #ax.hexbin(x=screener_df['x_loc'], y=screener_df['y_loc'], cmap=plt.cm.winter, mincnt=1, gridsize=50, extent=(0,94,-50,0))
    
    print(cutter_hexbin)
    print(vars(cutter_hexbin))
    print(len(cutter_hexbin._offsets))
    print(cutter_hexbin._axes)
    print(cutter_df.loc[:,'x_loc':'y_loc'])
    print(FeatureUtil.convert_coordinate_to_hexbin_vertex(cutter_df.iloc[0]['x_loc'], cutter_df.iloc[0]['y_loc'], cutter_hexbin._offsets))
    #plt.xlim(0,94)	
    #plt.ylim(-50, 0)
    #plt.show()


    # Create the feature vector
    feature_vector = {
        # Player Data
        'cutter_archetype': cutter['position'],
        'screener_archetype': screener['position'],

        # Location Data
        'cutter_x_loc_on_pass': pass_moment.loc[pass_moment['player_id'] == cutter['player_id']]['x_loc'].values[0],
        'cutter_y_loc_on_pass': pass_moment.loc[pass_moment['player_id'] == cutter['player_id']]['y_loc'].values[0],
        'screener_x_loc_on_pass': pass_moment.loc[pass_moment['player_id'] == screener['player_id']]['x_loc'].values[0],
        'screener_y_loc_on_pass': pass_moment.loc[pass_moment['player_id'] == screener['player_id']]['y_loc'].values[0],
        'ball_x_loc_on_pass': pass_moment.loc[pass_moment['player_id'].isna()]['x_loc'].item(),
        'ball_y_loc_on_pass': pass_moment.loc[pass_moment['player_id'].isna()]['y_loc'].item(),
        'ball_radius_on_pass': pass_moment.loc[pass_moment['player_id'].isna()]['radius'].item(),
        'cutter_x_loc_on_start_approach': start_moment[start_moment['player_id'] == cutter['player_id']]['x_loc'].values[0],
        'cutter_y_loc_on_start_approach': start_moment[start_moment['player_id'] == cutter['player_id']]['y_loc'].values[0],
        'screener_x_loc_on_start_approach': start_moment[start_moment['player_id'] == screener['player_id']]['x_loc'].values[0],
        'screener_y_loc_on_start_approach': start_moment[start_moment['player_id'] == screener['player_id']]['y_loc'].values[0],
        'ball_x_loc_on_start_approach': start_moment[start_moment['player_id'].isna()]['x_loc'].item(),
        'ball_y_loc_on_start_approach': start_moment[start_moment['player_id'].isna()]['y_loc'].item(),
        'ball_radius_loc_on_start_approach': start_moment[start_moment['player_id'].isna()]['radius'].item(),
        'cutter_x_loc_on_end_execution': end_moment[end_moment['player_id'] == cutter['player_id']]['x_loc'].values[0],
        'cutter_y_loc_on_end_execution': end_moment[end_moment['player_id'] == cutter['player_id']]['y_loc'].values[0],
        'screener_x_loc_on_end_execution': end_moment[end_moment['player_id'] == screener['player_id']]['x_loc'].values[0],
        'screener_y_loc_on_end_execution': end_moment[end_moment['player_id'] == screener['player_id']]['y_loc'].values[0],
        'ball_x_loc_on_end_execution': end_moment[end_moment['player_id'].isna()]['x_loc'].item(),
        'ball_y_loc_on_end_execution': end_moment[end_moment['player_id'].isna()]['y_loc'].item(),
        'ball_radius_loc_on_end_execution': end_moment[end_moment['player_id'].isna()]['radius'].item(),

        # Travel Distance Data
        'cutter_dist_traveled_approach': FeatureUtil.travel_dist(approach_moments[approach_moments['player_id'] == cutter['player_id']]),
        'cutter_dist_traveled_execution': FeatureUtil.travel_dist(execution_moments[execution_moments['player_id'] == cutter['player_id']]),
        'screener_dist_traveled_approach': FeatureUtil.travel_dist(approach_moments[approach_moments['player_id'] == screener['player_id']]),
        'screener_dist_traveled_execution': FeatureUtil.travel_dist(execution_moments[execution_moments['player_id'] == screener['player_id']]),
        'ball_dist_traveled_approach': FeatureUtil.travel_dist(approach_moments[approach_moments['player_id'].isna()]),
        'ball_dist_traveled_execution': FeatureUtil.travel_dist(execution_moments[execution_moments['player_id'].isna()]),

        # Relative Distance Data

        # Speed/Acceleration Data
        'cutter_avg_speed_approach': FeatureUtil.average_speed(approach_moments, cutter['player_id']),
        'cutter_avg_speed_execution': FeatureUtil.average_speed(execution_moments, cutter['player_id']),
        'screener_avg_speed_approach': FeatureUtil.average_speed(approach_moments, screener['player_id']),
        'screener_avg_speed_execution': FeatureUtil.average_speed(execution_moments, screener['player_id']),
        'ball_avg_speed_approach': FeatureUtil.average_speed(approach_moments, None),
        'ball_avg_speed_execution': FeatureUtil.average_speed(execution_moments, None),

        # Play Data
        'offset_into_play': math.floor(pass_moment.iloc[0]['shot_clock'] / 6),
        'num_players_past_half_court': FeatureUtil.num_players_past_halfcourt(pass_moment),
        'is_inbounds_pass': FeatureUtil.check_for_inbound_pass(moments, event_passes[0])
    }

    print("\n\n------------------------------ Feature Vector ---------------------------\n")
    print(feature_vector)
    print(f"\n Num Features: {len(feature_vector.keys())}")