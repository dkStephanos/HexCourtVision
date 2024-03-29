import os
import ast
import glob
import easygui
import pandas as pd
import numpy as np
from .ConstantsUtil import ConstantsUtil


class DataLoader:
    """
    A utility class for loading and converting data.
    """

    @classmethod
    def load_game_and_annotation_df_gui(cls):
        # Note: Game files are located within folders named after the game date and teams, e.g., "01.01.2016.DAL.at.MIA"
        # The actual game file is a JSON named after the game_id inside the respective folder.

        # Load game file with GUI
        game_path = easygui.fileopenbox(
            default=ConstantsUtil.RAW_DATA_PATH,
            title="Select a game folder and then the game file",
        )

        if game_path is None:
            raise Exception("No game file selected.")

        # Load annotation file with GUI
        easygui.msgbox("Next select the corresponding annotation file")
        annotation_path = easygui.fileopenbox(
            default=ConstantsUtil.EVENT_ANNOTATIONS_PATH,
            title="Select an annotation file",
        )

        if annotation_path is None:
            raise Exception("No annotation file selected.")

        # Load DataFrames
        game_df = pd.read_json(game_path)  # Adjusted to read JSON
        annotation_df = pd.read_csv(
            annotation_path, index_col=0
        )  # Prefix 'events-' is considered in file selection, not in loading

        return game_df, annotation_df

    @classmethod
    def load_raw_game(cls, game_key):
        # Derive game folder name from game key
        # This might require custom logic to convert game_key to folder name format, e.g., "YYYYMMDDAAAHHH" to "MM.DD.YYYY.AAA.at.HHH"
        game_folder_name = cls.convert_game_key_to_folder_name(
            game_key
        )  # Placeholder for actual conversion logic

        game_folder_path = os.path.join(ConstantsUtil.RAW_DATA_PATH, game_folder_name)
        game_file_path = glob.glob(os.path.join(game_folder_path, "*.json"))[
            0
        ]  # Assuming single JSON file per folder

        return pd.read_json(game_file_path)

    @classmethod
    def load_game_events(cls, game_key):
        # Construct annotation file path
        annotation_file_name = f"events-{game_key}.csv"  # Assuming the game_key can directly derive the file name
        annotation_path = os.path.join(
            ConstantsUtil.EVENT_ANNOTATIONS_PATH, annotation_file_name
        )

        return pd.read_csv(annotation_path, index_col=0)

    @classmethod
    def load_processed_game(cls, game_id):
        # Ingest data
        df = pd.read_csv(f"{ConstantsUtil.CLEAN_DATA_PATH}/{game_id}.csv", index_col=0)

        # Parse the tracking data
        df["MOMENTS"] = df["MOMENTS"].apply(cls._eval_nested_list)

        return df

    @classmethod
    def _eval_nested_list(cls, row):
        try:
            # Convert the string representation of the list into an actual list
            return ast.literal_eval(row)
        except ValueError as e:
            # Handle cases where conversion fails
            print(f"Error converting row: {e}")
            return None

    @staticmethod
    def convert_game_key_to_folder_name(game_key):
        # Placeholder for conversion logic
        # Convert "YYYYMMDDAAAHHH" to expected folder name format, e.g., "MM.DD.YYYY.AAA.at.HHH"
        # Example: "20160101DALMIA" -> "01.01.2016.DAL.at.MIA"
        # This is a simplified example and may need adjustment based on actual key structure and naming conventions
        date = game_key[:8]
        away_team = game_key[8:11]
        home_team = game_key[11:14]
        formatted_date = f"{date[4:6]}.{date[6:8]}.{date[:4]}"
        folder_name = f"{formatted_date}.{away_team}.at.{home_team}"

        return folder_name

    @staticmethod
    def convert_game_clock_to_timestamp(game_clock: float) -> str:
        """
        Convert game clock time from seconds to MM:SS format.

        Args:
            game_clock (float): The game clock time in seconds.

        Returns:
            str: The game clock time in MM:SS format.
        """
        minutes = int(game_clock) // 60
        seconds = int(game_clock) % 60
        
        return f"{minutes:02}:{seconds:02}"

    @staticmethod
    def convert_timestamp_to_game_clock(timestamp: str) -> int:
        """
        Convert a timestamp from MM:SS format to game clock time in seconds.

        Args:
            timestamp (str): The timestamp in MM:SS format.

        Returns:
            int: The game clock time in seconds.
        """
        minutes, seconds = map(int, timestamp.split(":"))
        
        return minutes * 60 + seconds

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
            dict: A dict of dictionaries containing team data.
        """
        return {
            "home_team": {
                "team_id": game_df.iloc[0]["events"]["home"]["teamid"],
                "name": game_df.iloc[0]["events"]["home"]["name"],
                "abbreviation": game_df.iloc[0]["events"]["home"]["abbreviation"],
                "color": ConstantsUtil.COLOR_DICT[
                    game_df.iloc[0]["events"]["home"]["teamid"]
                ],
            },
            "away_team": {
                "team_id": game_df.iloc[0]["events"]["visitor"]["teamid"],
                "name": game_df.iloc[0]["events"]["visitor"]["name"],
                "abbreviation": game_df.iloc[0]["events"]["visitor"]["abbreviation"],
                "color": ConstantsUtil.COLOR_DICT[
                    game_df.iloc[0]["events"]["visitor"]["teamid"]
                ],
            },
        }

    @staticmethod
    def get_players_data(event_df):
        """
        Get players' data from a game DataFrame.

        Args:
            event_df (pd.DataFrame): Game DataFrame.

        Returns:
            list: List of player data dictionaries.
        """
        return [
            {
                "player_id": player["playerid"],
                "team_id": event_df["events"][0][team]["teamid"],
                "first_name": player["firstname"],
                "last_name": player["lastname"],
                "jersey_number": player.get("jersey", 99),
                "position": player["position"],
            }
            for team in ["home", "visitor"]
            for player in event_df["events"][0][team]["players"]
        ]

    @staticmethod
    def get_players_dict(event_df):
        """
        Get players' dictionary from a game DataFrame.

        Args:
            event_df (pd.DataFrame): Game DataFrame.

        Returns:
            dict: Dictionary containing player names and jersey numbers.
        """
        home_players = event_df["events"][0]["home"]["players"]
        visitor_players = event_df["events"][0]["visitor"]["players"]
        players_dict = {
            player["playerid"]: [
                player["firstname"] + " " + player["lastname"],
                player.get("jersey"),
            ]
            for player in home_players + visitor_players
        }
        players_dict[-1] = ["ball", np.nan]

        return players_dict
