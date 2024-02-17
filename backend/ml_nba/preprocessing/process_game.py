from ml_nba.preprocessing.utilities.FeatureUtil import FeatureUtil
from ml_nba.preprocessing.utilities.DataLoader import DataLoader
from ml_nba.preprocessing.utilities.ConstantsUtil import ConstantsUtil
from ml_nba.preprocessing.utilities.AnnotationProcessor import AnnotationProcessor
from ml_nba.preprocessing.utilities.EventsProcessor import EventsProcessor


def process_game(game_id: str, save_results=True, save_dir=ConstantsUtil.CLEAN_DATA_PATH):
    # Collect the raw game data and the event data for the game_id
    game_df, annotation_df = DataLoader.load_game_and_annotation_df_game_key(game_id)
    
    # Get our notes, manual indicators for bad events, frame rate, etc.
    game_notes = ConstantsUtil.games[game_id]

    # Extract team and player data from game_df
    teams_data = DataLoader.get_teams_data(game_df)

    # Trim event data to possesions ending in a make, miss, turnover, or foul, stripping corrupted events
    annotation_df = AnnotationProcessor.trim_annotation_rows(annotation_df, game_notes['bad_events'])
    
    # Generate unique ids for each event, and determine which team has possesion for the event
    annotation_df = AnnotationProcessor.generate_event_ids(annotation_df)
    annotation_df = FeatureUtil.determine_possession(annotation_df, teams_data)
    
    # Finally, remove additional annotation columns AFTER determining possesion as those cols are used for interpolation
    annotation_df = AnnotationProcessor.trim_annotation_cols(annotation_df)

    # Merge the coordinate and event dataframes
    combined_event_df = AnnotationProcessor.combine_game_and_annotation_events(game_df, annotation_df)
    
    # Get direction for each play and remove moments occurring on the other half of the court (requires event data)
    combined_event_df = FeatureUtil.determine_directionality(combined_event_df)
    combined_event_df = EventsProcessor.trim_moments_by_directionality(combined_event_df)
    
    # Sort result
    combined_event_df = AnnotationProcessor.organize_columns(combined_event_df)
    
    # Save if directed
    if save_results:
        combined_event_df.to_csv(f"{save_dir}/{game_id}.csv")

    return combined_event_df