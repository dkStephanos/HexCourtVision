import pandas as pd
from .ConstantsUtil import ConstantsUtil

class DataLoader:
    """
    A utility class for loading and converting data.
    """

    @staticmethod
    def load_game_df(path):
        """
        Load game data from a JSON file.

        Args:
            path (str): The path to the JSON file.

        Returns:
            pd.DataFrame: A DataFrame containing game data.
        """
        game_df = pd.read_json(path)
        return game_df

    @staticmethod
    def convert_game_clock_to_timestamp(game_clock):
        """
        Convert game clock time to timestamp format.

        Args:
            game_clock (float): The game clock time.

        Returns:
            str: The game clock time in timestamp format (e.g., '12:34').
        """
        seconds = int(float(game_clock) / 60)
        milliseconds = int(float(game_clock) % 60)
        return f'{seconds}:{milliseconds}'

    @staticmethod
    def convert_timestamp_to_game_clock(timestamp):
        """
        Convert a timestamp to game clock time.

        Args:
            timestamp (str): The timestamp in the format 'mm:ss'.

        Returns:
            int: The game clock time in seconds.
        """
        time = timestamp.split(':')
        return int(time[0]) * 60 + int(time[1])

    @staticmethod
    def get_game_data(game_df, annotation_df):
        """
        Get game-related data from the game DataFrame.

        Args:
            game_df (pd.DataFrame): DataFrame containing game data.
            annotation_df (pd.DataFrame): DataFrame containing annotation data.

        Returns:
            dict: A dictionary containing game-related information.
        """
        game_dict = {}
        game_dict["game_id"] = game_df.iloc[0]["gameid"]
        game_dict["game_date"] = game_df.iloc[0]["gamedate"]
        game_dict["home_team"] = game_df.iloc[0]["events"]["home"]["teamid"]
        game_dict["visitor_team"] = game_df.iloc[0]["events"]["visitor"]["teamid"]
        game_dict["final_score"] = annotation_df.iloc[-1]["SCORE"]
        return game_dict

    @staticmethod
    def get_teams_data(game_df):
        """
        Get data about home and visitor teams from the game DataFrame.

        Args:
            game_df (pd.DataFrame): DataFrame containing game data.

        Returns:
            list: A list of dictionaries containing team data.
        """
        home_team = {
            "team_id": game_df.iloc[0]["events"]["home"]["teamid"],
            "name": game_df.iloc[0]["events"]["home"]["name"],
            "abbreviation": game_df.iloc[0]["events"]["home"]["abbreviation"],
            "color": ConstantsUtil.COLOR_DICT[game_df.iloc[0]["events"]["home"]["teamid"]]
        }
        visitor_team = {
            "team_id": game_df.iloc[0]["events"]["visitor"]["teamid"],
            "name": game_df.iloc[0]["events"]["visitor"]["name"],
            "abbreviation": game_df.iloc[0]["events"]["visitor"]["abbreviation"],
            "color": ConstantsUtil.COLOR_DICT[game_df.iloc[0]["events"]["visitor"]["teamid"]]
        }
        return [home_team, visitor_team]
