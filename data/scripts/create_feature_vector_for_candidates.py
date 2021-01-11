
import pandas as pd
import easygui
import sys

from data.preprocessing.utilities.DataUtil import DataUtil
from data.preprocessing.utilities.FeatureUtil import FeatureUtil
from data.preprocessing.utilities.ConstantsUtil import ConstantsUtil

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

    # Trim the moments data around the pass
    game_clock = DataUtil.convert_timestamp_to_game_clock(target_candidate['game_clock'])
    trimmed_moments = moments[(moments.game_clock > game_clock - 2) & (moments.game_clock < game_clock + 2)]
    approach_moments = trimmed_moments[trimmed_moments.game_clock < game_clock]
    execution_moments = trimmed_moments[trimmed_moments.game_clock > game_clock]
    pass_moment = trimmed_moments[trimmed_moments.game_clock == game_clock]
    start_moment = approach_moments[approach_moments.game_clock == approach_moments.iloc[0].game_clock]
    end_moment = execution_moments[execution_moments.game_clock == execution_moments.iloc[-1].game_clock]

    print(pass_moment)

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

        # Speed/Acceleration Data
        'cutter_avg_speed_approach': FeatureUtil.average_speed(approach_moments, cutter['player_id']),
        'cutter_avg_speed_execution': FeatureUtil.average_speed(execution_moments, cutter['player_id']),
        'screener_avg_speed_approach': FeatureUtil.average_speed(approach_moments, screener['player_id']),
        'screener_avg_speed_execution': FeatureUtil.average_speed(execution_moments, screener['player_id']),
        'ball_avg_speed_approach': FeatureUtil.average_speed(approach_moments, None),
        'ball_avg_speed_execution': FeatureUtil.average_speed(execution_moments, None),

        # Play Data
    }

    print(feature_vector)
    print(len(feature_vector.keys()))
