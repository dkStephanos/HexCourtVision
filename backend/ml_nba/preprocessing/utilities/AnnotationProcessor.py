import pandas as pd
import numpy as np
class AnnotationProcessor:
    """
    A utility class for processing annotation data.
    """

    @staticmethod
    def trim_annotation_rows(annotation_df, bad_events=[]):
        """
        Trim annotation rows based on specified conditions.

        Args:
            annotation_df (pd.DataFrame): DataFrame containing annotation data.
            bad_events (list): List of event numbers to be removed.

        Returns:
            pd.DataFrame: Trimmed DataFrame with specified rows removed.
        """
        # Extract only make, miss, turnover, and foul events
        annotation_df = annotation_df.loc[annotation_df["EVENTMSGTYPE"].isin([1, 2, 5, 6])]

        # Trim out specific event types
        annotation_df = AnnotationProcessor._trim_specific_events(annotation_df)

        # Remove events with specified event numbers
        if len(bad_events) > 0:
            annotation_df = annotation_df[~annotation_df["EVENTNUM"].isin(bad_events)]

        return annotation_df

    @staticmethod
    def trim_annotation_cols(annotation_df):
        """
        Trim unnecessary columns from the annotation DataFrame.

        Args:
            annotation_df (pd.DataFrame): DataFrame containing annotation data.

        Returns:
            pd.DataFrame: DataFrame with unnecessary columns removed.
        """
        # Remove specified columns
        columns_to_remove = [
            "WCTIMESTRING",
            "NEUTRALDESCRIPTION",
            "SCOREMARGIN",
            "PERSON1TYPE",
            "PLAYER1_NAME",
            "PLAYER1_TEAM_ID",
            "PLAYER1_TEAM_CITY",
            "PLAYER1_TEAM_NICKNAME",
            "PLAYER1_TEAM_ABBREVIATION",
            "PERSON2TYPE",
            "PLAYER2_NAME",
            "PLAYER2_TEAM_ID",
            "PLAYER2_TEAM_CITY",
            "PLAYER2_TEAM_NICKNAME",
            "PLAYER2_TEAM_ABBREVIATION",
            "PERSON3TYPE",
            "PLAYER3_NAME",
            "PLAYER3_TEAM_ID",
            "PLAYER3_TEAM_CITY",
            "PLAYER3_TEAM_NICKNAME",
            "PLAYER3_TEAM_ABBREVIATION",
        ]
        annotation_df.drop(columns=columns_to_remove, axis=1, inplace=True)

        return annotation_df

    @staticmethod
    def generate_event_ids(annotation_df):
        """
        Generate unique event IDs based on game and event numbers.

        Args:
            annotation_df (pd.DataFrame): DataFrame containing annotation data.

        Returns:
            pd.DataFrame: DataFrame with an additional 'event_id' column.
        """
        event_ids = []

        for index, row in annotation_df.iterrows():
            event_ids.append(f'{row["GAME_ID"]}-{row["EVENTNUM"]:03}')

        annotation_df["event_id"] = event_ids

        return annotation_df

    @staticmethod
    def combine_game_and_annotation_events(game_df, annotation_df):
        """
        Combine game and annotation events based on event numbers.

        Args:
            game_df (pd.DataFrame): Game DataFrame.
            annotation_df (pd.DataFrame): Annotation DataFrame.

        Returns:
            pd.DataFrame: Combined DataFrame.
        """
        moments = []
        
        for event in game_df['events']:
            if np.any(annotation_df['EVENTNUM'] == int(event['eventId'])):
                moments.append({'EVENTNUM': int(event['eventId']), 'moments': event['moments']})

        moments_df = pd.DataFrame(moments)

        return annotation_df.merge(moments_df, how="inner").set_index('EVENTNUM')
    
    @staticmethod
    def organize_columns(game_df):
        # Define the new column order with a logical grouping
        new_order = [
            'GAME_ID', 'EVENTNUM', 'event_id',  # Game Identifiers and Metadata
            'EVENTMSGTYPE', 'EVENTMSGACTIONTYPE',  # Event Details
            'PERIOD', 'PCTIMESTRING',  # Temporal Information
            'HOMEDESCRIPTION', 'VISITORDESCRIPTION',  # Event Descriptions
            'possession', 'direction', 'SCORE',  # Game State Information
            'PLAYER1_ID', 'PLAYER2_ID', 'PLAYER3_ID',  # Player Information
            'moments'  # Raw Data
        ]
        
        # Reorder the DataFrame according to the new column order
        df_reorganized = game_df[new_order]
        
        return df_reorganized

    @staticmethod
    def _trim_specific_events(annotation_df):
        """
        Trim specific event types and descriptions from the annotation DataFrame.

        Args:
            annotation_df (pd.DataFrame): DataFrame containing annotation data.

        Returns:
            pd.DataFrame: DataFrame with specific events removed.
        """
        # Trim offensive foul events
        annotation_df = annotation_df[~annotation_df["HOMEDESCRIPTION"].str.contains("Offensive Charge", na=False)]
        annotation_df = annotation_df[~annotation_df["VISITORDESCRIPTION"].str.contains("Offensive Charge", na=False)]
        annotation_df = annotation_df[~annotation_df["HOMEDESCRIPTION"].str.contains("OFF.FOUL", na=False)]
        annotation_df = annotation_df[~annotation_df["VISITORDESCRIPTION"].str.contains("OFF.FOUL", na=False)]

        # Trim technical, loose ball, and personal take fouls
        annotation_df = annotation_df[~annotation_df["HOMEDESCRIPTION"].str.contains("T.FOUL", na=False)]
        annotation_df = annotation_df[~annotation_df["VISITORDESCRIPTION"].str.contains("T.FOUL", na=False)]
        annotation_df = annotation_df[~annotation_df["HOMEDESCRIPTION"].str.contains("L.B.FOUL", na=False)]
        annotation_df = annotation_df[~annotation_df["VISITORDESCRIPTION"].str.contains("L.B.FOUL", na=False)]

        return annotation_df
