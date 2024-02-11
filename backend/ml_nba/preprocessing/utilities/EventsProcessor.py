import pandas as pd
import numpy as np
from .ConstantsUtil import ConstantsUtil

class EventsProcessor:
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

        return annotation_df.merge(moments_df, how="inner")

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
        temp_df = pd.DataFrame({label_name: series_to_convert.index, series_name: series_to_convert.values})
        return pd.DataFrame(temp_df[series_name].tolist(), index=temp_df[label_name])

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
            if event['direction'] == "RIGHT":
                event['moments'][:] = [x for x in event['moments'] if x[5][0][2] > 45.0]
            else:
                event['moments'][:] = [x for x in event['moments'] if x[5][0][2] < 45.0]

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
        moments = event_df["moments"]
        player_moments = []
        last_game_clock = 720
        last_shot_clock = 24
        reached_end_of_play = False

        while not reached_end_of_play:
            for moment in moments:
                if moment[3] is None:
                    moment[3] = 0.0
                if moment[3] > last_shot_clock and moment[2] < EventsProcessor.convert_timestamp_to_game_clock(event_df['PCTIMESTRING']):
                    reached_end_of_play = True
                else:
                    last_shot_clock = moment[3]
                    last_game_clock = moment[2]
                    for player in moment[5]:
                        player_copy = player.copy()
                        player_copy.extend((moments.index(moment), moment[2], moment[3], event_df["event_id"]))
                        player_moments.append(player_copy)
            reached_end_of_play = True

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
            if not game_df['events'][index - 1]['moments'] is None:
                moments_copy = game_df['events'][index - 1]['moments'].copy()
                game_df['events'][index]['moments'] = game_df['events'][index]['moments'] + moments_copy

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