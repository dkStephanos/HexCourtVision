# Import necessary modules from the ml_nba preprocessing utilities package
from ml_nba.preprocessing.utilities.FeatureUtil import FeatureUtil
from ml_nba.preprocessing.utilities.DataLoader import DataLoader
from ml_nba.preprocessing.utilities.ConstantsUtil import ConstantsUtil
from ml_nba.preprocessing.utilities.AnnotationProcessor import AnnotationProcessor
from ml_nba.preprocessing.utilities.EventsProcessor import EventsProcessor


def process_game(
    game_key: str, save_results=True, save_dir=ConstantsUtil.CLEAN_DATA_PATH
):
    """
    Processes a single NBA game's raw data to prepare it for machine learning analysis.

    Parameters:
    - game_key (str): The unique identifier for the game to be processed.
    - save_results (bool): Flag indicating whether to save the processed data to a file. Defaults to True.
    - save_dir (str): The directory path where the processed data files will be saved. Defaults to the CLEAN_DATA_PATH defined in ConstantsUtil.

    Returns:
    - DataFrame: A pandas DataFrame containing the processed game and event data, ready for ML analysis.
    """

    # Load the raw game data and associated event annotations for the specified game_key
    game_df, annotation_df = DataLoader.load_game_and_annotation_df_game_key(game_key)

    # Retrieve game-specific notes, including manual indicators of bad events and frame rate information
    game_notes = ConstantsUtil.games[game_key]

    # Extract team and player metadata from the raw game data
    teams_data = DataLoader.get_teams_data(game_df)

    # Filter out corrupted events from the annotation data based on manual indicators and retain only relevant possessions
    annotation_df = AnnotationProcessor.trim_annotation_rows(
        annotation_df, game_notes["bad_events"]
    )

    # Assign unique IDs to each event and identify the possessing team for each event
    annotation_df = AnnotationProcessor.generate_event_ids(annotation_df)
    annotation_df = FeatureUtil.determine_possession(annotation_df, teams_data)

    # Remove extraneous annotation columns after possession determination, as these columns are used for interim calculations
    annotation_df = AnnotationProcessor.trim_annotation_cols(annotation_df)

    # Combine the coordinate data (from game_df) with event data (from annotation_df) into a single DataFrame
    combined_event_df = AnnotationProcessor.combine_game_and_annotation_events(
        game_df, annotation_df
    )

    # Determine the direction of play for each event and filter out moments occurring outside the relevant half of the court
    combined_event_df = FeatureUtil.determine_directionality(combined_event_df)
    combined_event_df = EventsProcessor.trim_moments_by_directionality(
        combined_event_df
    )

    # Organize columns in the combined DataFrame in a logical order for analysis
    combined_event_df = AnnotationProcessor.organize_columns(combined_event_df)

    # If saving results is enabled, write the processed data to a CSV file in the specified directory
    if save_results:
        combined_event_df.to_csv(f"{save_dir}/{game_id}.csv")

    # Return the processed DataFrame
    return combined_event_df
