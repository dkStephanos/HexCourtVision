class ConstantsUtil:
    BASIC_ENCODE_COLS = ['cutter_archetype',
                         'screener_archetype']
                         
    STRING_TUPLE_ENCODE_COLS = ['cutter_loc_on_pass',
                                'screener_loc_on_pass',
                                'ball_loc_on_pass',
                                'cutter_loc_on_start_approach',
                                'screener_loc_on_start_approach',
                                'ball_loc_on_start_approach',
                                'cutter_loc_on_end_execution',
                                'screener_loc_on_end_execution',
                                'ball_loc_on_end_execution',
                                'cutter_loc_on_screen',
                                'screener_loc_on_screen',
                                'ball_loc_on_screen',]

    FEATURES_IGNORED_BY_INFORMATION_GAIN = ['ball_loc_on_end_execution',
                                            'ball_radius_loc_on_end_execution',
                                            'cutter_dist_traveled_execution',
                                            'players_dist_on_end_execution',
                                            'screener_avg_speed_approach',
                                            'ball_avg_speed_execution',
                                            'intercept_of_cutter_trajectory_approach',
                                            'slope_of_cutter_trajectory_execution',
                                            'slope_of_screener_trajectory_approach',
                                            'intercept_of_screener_trajectory_approach',
                                            'slope_of_screener_trajectory_execution',
                                            'intercept_of_screener_trajectory_execution',
                                            'slope_of_ball_trajectory_approach',
                                            'intercept_of_ball_trajectory_approach']