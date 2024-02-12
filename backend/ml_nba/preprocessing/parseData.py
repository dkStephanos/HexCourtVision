from ml_nba.preprocessing.utilities.FeatureUtil import FeatureUtil
from ml_nba.preprocessing.utilities.DataLoader import DataLoader
from ml_nba.preprocessing.utilities.ConstantsUtil import ConstantsUtil
from ml_nba.preprocessing.utilities.PlayerMvmtProcessor import PlayerMvmtProcessor
from ml_nba.preprocessing.utilities.AnnotationProcessor import AnnotationProcessor
from ml_nba.preprocessing.utilities.EventsProcessor import EventsProcessor


def parse_data():
    # Collect the raw game data and the event data for the game_id
    game = "20151228SACGSW"
    game_df, annotation_df = DataLoader.load_game_and_annotation_df_game_key(game)

    # Extract team and player data from game_df
    teams_data = DataLoader.get_teams_data(game_df)
    players_data = PlayerMvmtProcessor.get_players_data(game_df)
    players_dict = PlayerMvmtProcessor.get_players_dict(game_df)

    # Trim event data, and add an columns for the ID and team in possesion 
    annotation_df = AnnotationProcessor.trim_annotation_rows(annotation_df, ConstantsUtil.games[game]['bad_events'])
    annotation_df = FeatureUtil.determine_possession(annotation_df, teams_data)
    annotation_df = AnnotationProcessor.generate_event_ids(annotation_df)
    annotation_df = AnnotationProcessor.trim_annotation_cols(annotation_df)

    # Merge the coordinate and event dataframes
    combined_event_df = AnnotationProcessor.combine_game_and_annotation_events(game_df, annotation_df)

    # Get direction for each play and remove moments occurring on the other half of the court
    combined_event_df = FeatureUtil.determine_directionality(combined_event_df)
    combined_event_df = EventsProcessor.trim_moments_by_directionality(combined_event_df)

    # combined_event_df.to_csv("static/backend/test/events.csv")
    print(combined_event_df)
    sample_event = DataLoader.load_combined_event_by_num(combined_event_df, 427)
    moments_df = EventsProcessor.get_moments_from_event(sample_event)

    # moments_df.to_csv("static/backend/test/test.csv")
    if len(moments_df) > 0:
        event_passes = FeatureUtil.get_passes_for_event(moments_df, sample_event["possession"], players_data)
        dribble_handoff_candidates = FeatureUtil.get_dribble_handoff_candidates(
            combined_event_df, moments_df, event_passes, ConstantsUtil.games[game]['moment_range'], players_dict)

        # get ball movements for event and graph them
        ball_df = moments_df[moments_df.player_id == -1]

    print(ball_df)