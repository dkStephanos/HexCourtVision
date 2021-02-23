import pandas as pd

from data.classification.utilities.EncodingUtil import EncodingUtil

from data.models import CandidateFeatureVector


def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates)
    candidates_df.set_index('id', inplace=True)
    candidates_df.drop(columns=['candidate_id'], inplace=True)

    candidates_df = EncodingUtil.basic_label_encode_cols(candidates_df, ['cutter_archetype', 'screener_archetype'])
    candidates_df = EncodingUtil.sort_position_cols_and_encode(candidates_df, [ 'cutter_loc_on_pass',
                                                                                'screener_loc_on_pass',
                                                                                'ball_loc_on_pass',
                                                                                'ball_radius_on_pass',
                                                                                'cutter_loc_on_start_approach',
                                                                                'screener_loc_on_start_approach',
                                                                                'ball_loc_on_start_approach',
                                                                                'ball_radius_loc_on_start_approach',
                                                                                'cutter_loc_on_end_execution',
                                                                                'screener_loc_on_end_execution',
                                                                                'ball_loc_on_end_execution',
                                                                                'ball_radius_loc_on_end_execution',
                                                                                'cutter_loc_on_screen',
                                                                                'screener_loc_on_screen',
                                                                                'ball_loc_on_screen',
                                                                                'ball_radius_on_screen'])

    print(candidates_df.iloc[0])