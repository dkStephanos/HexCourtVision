import pandas as pd

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
            # Add other columns to be removed here
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
        Combine game events with annotation data based on event numbers.

        Args:
            game_df (pd.DataFrame): DataFrame containing game events.
            annotation_df (pd.DataFrame): DataFrame containing annotation data.

        Returns:
            pd.DataFrame: Merged DataFrame with game and annotation events.
        """
        merged_events = []

        for event in game_df['events']:
            event_num = int(event['eventId'])
            if event_num in annotation_df["EVENTNUM"].values:
                moments = event['moments']
                merged_events.append({"EVENTNUM": event_num, "moments": moments})

        moments_df = pd.DataFrame(merged_events)

        return annotation_df.merge(moments_df, how="inner")

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
