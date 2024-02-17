import pandas as pd
import numpy as np
class PlayerMvmtProcessor:
    @staticmethod
    def get_players_df(game_event):
        """
        Get players' DataFrame from a game event.

        Args:
            game_event (dict): Game event data.

        Returns:
            pd.DataFrame: Players' DataFrame.
        """
        home = game_event["home"]
        visitor = game_event["visitor"]
        players_dict = {}

        for player in home["players"]:
            players_dict[player['playerid']] = [home["teamid"], player["firstname"], player["lastname"],
                                                 player["jersey"], player["position"]]
        for player in visitor["players"]:
            players_dict[player['playerid']] = [visitor["teamid"], player["firstname"], player["lastname"],
                                                 player["jersey"], player["position"]]

        players_df = pd.DataFrame.from_dict(players_dict, orient='index',
                                            columns=['team_id', 'first_name', 'last_name', 'jersey_number', 'position'])
        players_df.reset_index(inplace=True)

        return players_df.rename(columns={'index': 'player_id'})


    @staticmethod
    def get_player_data(event_df, player_id):
        """
        Get player data from an event DataFrame.

        Args:
            event_df (pd.DataFrame): Event DataFrame.
            player_id (int): Player ID.

        Returns:
            pd.DataFrame: Player data for the specified player ID.
        """
        return event_df[event_df.player_id == player_id]

    @staticmethod
    def get_player_position_data(event_df, player_id):
        """
        Get player position data from an event DataFrame.

        Args:
            event_df (pd.DataFrame): Event DataFrame.
            player_id (int): Player ID.

        Returns:
            pd.DataFrame: Player position data for the specified player ID.
        """
        return event_df[event_df.player_id == player_id][["x_loc", "y_loc"]]

    @staticmethod
    def get_all_player_position_data(event_df):
        """
        Get all player position data from an event DataFrame.

        Args:
            event_df (pd.DataFrame): Event DataFrame.

        Returns:
            pd.GroupBy: Grouped DataFrame containing player position data.
        """
        group = event_df.groupby("player_id")[["x_loc", "y_loc"]]

        return group

    @staticmethod
    def get_possession_team_player_ids(possession, players_data):
        """
        Get player IDs for a specific team possession.

        Args:
            possession (int): Team possession ID.
            players_data (list): List of player data dictionaries.

        Returns:
            list: List of player IDs for the specified team possession.
        """
        player_ids = []

        for player in players_data:
            if player['team_id'] == possession:
                player_ids.append(player['player_id'])

        return player_ids
