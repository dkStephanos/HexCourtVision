import json
import pandas as pd
from .ConstantsUtil import ConstantsUtil
from .DataLoader import DataLoader

class EventsProcessor:
    @staticmethod
    def convert_labeled_series_to_df(label_name, series_name, series_to_convert):
        """
        Convert a labeled series to a DataFrame.

        Args:
            label_name (str): Name for the label column.
            series_name (str): Name for the series column.
            series_to_convert (pd.Series): Labeled series.

        Returns:
            pd.DataFrame: DataFrame with label and series columns.
        """
        # Initialize an empty list to hold the data
        data = []

        # Iterate over the series, assuming series_to_convert.index contains labels
        # and series_to_convert.values contains 1D arrays
        for label, values in series_to_convert.items():
            for value in values:  # Assuming 'values' is an iterable; adjust as needed
                data.append({label_name: label, series_name: value})

        # Convert the list of dictionaries to a DataFrame
        temp_df = pd.DataFrame(data)
        return temp_df

    @staticmethod
    def get_labeled_mins_from_df(dataframe, min_value_label):
        """
        Get labeled mins from a DataFrame.

        Args:
            dataframe (pd.DataFrame): Input DataFrame.
            min_value_label (str): Label for the minimum value column.

        Returns:
            pd.DataFrame: DataFrame with index and minimum value columns.
        """
        return pd.concat([dataframe.idxmin(), dataframe.min()], axis=1, keys=[dataframe.index.name, min_value_label])

    @staticmethod
    def trim_moments_by_directionality(combined_event_df):
        """
        Trim moments in a combined event DataFrame by directionality.

        Args:
            combined_event_df (pd.DataFrame): Combined event DataFrame.

        Returns:
            pd.DataFrame: Trimmed DataFrame.
        """
        for index, event in combined_event_df.iterrows():
            if event['DIRECTION'] == "RIGHT":
                event['MOMENTS'][:] = [x for x in event['MOMENTS'] if x[5][0][2] > 45.0]
            else:
                event['MOMENTS'][:] = [x for x in event['MOMENTS'] if x[5][0][2] < 45.0]

        return combined_event_df
    
    @staticmethod
    def get_moments_from_event(event_df):
        """
        Extract moments data from an event DataFrame.

        Args:
            event_df (pd.DataFrame): Event DataFrame.

        Returns:
            pd.DataFrame: Moments DataFrame.
        """
        player_moments = []
        last_shot_clock = 24
        game_clock_at_start = DataLoader.convert_timestamp_to_game_clock(event_df['PCTIMESTRING'])

        for moment in event_df["MOMENTS"]:
            # Normalize None shot clock to 0.0
            shot_clock = 0.0 if moment[3] is None else moment[3]

            # Update shot clock only if it's valid and we're not at the end of the play
            if shot_clock <= last_shot_clock or moment[2] >= game_clock_at_start:
                last_shot_clock = shot_clock
                last_game_clock = moment[2]

                for player in moment[5]:
                    player_copy = player.copy()
                    moment_index = event_df["MOMENTS"].index(moment)
                    player_copy.extend((moment_index, last_game_clock, last_shot_clock, event_df["PERIOD"], event_df["EVENT_ID"]))
                    player_moments.append(player_copy)

        return pd.DataFrame(player_moments, columns=ConstantsUtil.HEADERS)

    @staticmethod
    def extend_event_moments(game_df):
        """
        Extend moments of events in the game DataFrame.

        Args:
            game_df (pd.DataFrame): Game DataFrame.

        Returns:
            pd.DataFrame: Game DataFrame with extended moments.
        """
        for index in range(1, len(game_df['events'])):
            if not game_df['events'][index - 1]['MOMENTS'] is None:
                moments_copy = game_df['events'][index - 1]['MOMENTS'].copy()
                game_df['events'][index]['MOMENTS'] = game_df['events'][index]['MOMENTS'] + moments_copy

        return game_df

    @staticmethod
    def remove_duplicate_candidates(all_candidates):
        """
        Remove duplicate candidates from a list of candidates.

        Args:
            all_candidates (list): List of candidate dictionaries.

        Returns:
            list: List of unique candidates.
        """
        final_candidates = []
        offset_length = 5
        duplicate = False

        for index in range(0, len(all_candidates)):
            if index + offset_length >= len(all_candidates):
                final_candidates.append(all_candidates[index])
            else:
                for offset in range(1, offset_length):
                    if (
                        all_candidates[index]['period'] == all_candidates[index + offset]['period']
                        and all_candidates[index]['game_clock'] == all_candidates[index + offset]['game_clock']
                        and all_candidates[index]['shot_clock'] == all_candidates[index + offset]['shot_clock']
                    ):
                        duplicate = True
                        break
                if not duplicate:
                    final_candidates.append(all_candidates[index])
                duplicate = False

        return final_candidates
