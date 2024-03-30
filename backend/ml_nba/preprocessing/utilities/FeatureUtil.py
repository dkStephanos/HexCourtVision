import math
import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean
from scipy.stats import linregress
from .DataLoader import DataLoader
from .PlayerMvmtProcessor import PlayerMvmtProcessor


class FeatureUtil:
    """
    Utility class for various feature extraction and analysis functions related to basketball events.

    This class provides methods for determining possession and directionality of events, as well as
    calculating travel distances, player speed, and other basketball-related features.
    """

    @staticmethod
    def determine_possession_from_eventmsg(annotation_df, players_data):
        """
        Revised method to determine possession for each event in the annotation DataFrame,
        addressing edge cases and refining logic based on basketball rules.

        Args:
            annotation_df (pd.DataFrame): DataFrame containing event annotations.
            players_data (list): List of dictionaries with player and team data.

        Returns:
            pd.DataFrame: Updated DataFrame with a new 'possession' column indicating
                        the team in possession for each event.
        """
        # Convert the list of player data dictionaries into a player_id to team_id mapping
        player_to_team_map = {player['player_id']: player['team_id'] for player in players_data}
        # Extract unique team IDs for handling cases where opposite team's ID is needed
        unique_team_ids = set(player['team_id'] for player in players_data)

        def determine_event_possession(row):
            # Default assumption for possession based on PLAYER1_TEAM_ID
            possession_key = 'PLAYER1_TEAM_ID'

            event_type = row['EVENTMSGTYPE']
            # Adjust logic based on event type
            if event_type in [1, 2]:  # Possession typically remains with PLAYER1's team
                possession_key = 'PLAYER1_TEAM_ID'
            elif event_type == 5:  # Handling all turnovers
                # Check if PLAYER1_ID corresponds to a team ID, which indicates a team turnover
                if row['PLAYER1_ID'] in unique_team_ids:
                    # This signifies the team that has committed the turnover
                    return row['PLAYER1_ID']
                else:
                    possession_key = 'PLAYER1_TEAM_ID'  # Handle individual turnovers normally
            elif event_type == 6:
                # If it's a type of foul, decide based on specific rules or descriptions
                # For defensive fouls or where PLAYER2_ID is zero, special handling might be needed
                if row['PLAYER2_ID'] == 0:
                    # Here, we might need to determine possession based on the context of the foul
                    # E.g., for a defensive 3 seconds violation, switch possession to the other team
                    # This might need customization based on your data and rules
                    if "Def. 3 Sec" in (str(row["VISITORDESCRIPTION"]) + str(row["HOMEDESCRIPTION"])).replace('nan', ''):
                        # Determine the team that's not committing the foul
                        non_fouling_team_id = next((id for id in unique_team_ids if id != row['PLAYER1_TEAM_ID']), 'Unknown')
                        return non_fouling_team_id
                    # Add additional foul-specific conditions here
                else:
                    # For other types of fouls, use PLAYER2_TEAM_ID when available
                    possession_key = 'PLAYER2_TEAM_ID'

            # Final check for possession, either directly or via player-team mapping
            if pd.isna(row.get(possession_key)):
                player_id_key = 'PLAYER1_ID' if possession_key == 'PLAYER1_TEAM_ID' else 'PLAYER2_ID'
                player_id = row.get(player_id_key)
                return player_to_team_map.get(player_id, 'Unknown')  # Default to 'Unknown' if mapping fails
            else:
                return row.get(possession_key)
        # Apply the custom logic to each event in the DataFrame
        annotation_df['POSSESSION'] = annotation_df.apply(determine_event_possession, axis=1).astype(int)

        return annotation_df


    @staticmethod
    def determine_directionality(combined_event_df):
        """
        Determine directionality for events in the combined event DataFrame.

        Args:
            combined_event_df (pd.DataFrame): DataFrame containing combined event data.

        Returns:
            pd.DataFrame: DataFrame with a new 'direction' column indicating directionality for each event.
        """
        reached_end_of_play = False
        last_moment = []
        last_event = []
        team_basket = {"team": -1, "direction": ""}

        # Loop through the events, looking for a made field goal in the first half
        for index, row in combined_event_df.iterrows():
            if row["EVENTMSGTYPE"] == 1 and row["PERIOD"] < 3:
                event_time = DataLoader.convert_timestamp_to_game_clock(
                    row["PCTIMESTRING"]
                )
                # we want to find the end of the play, so we can determine which basket was scored on
                for moment in row["MOMENTS"]:
                    if (moment[2] <= event_time + 1) and (moment[2] >= event_time - 1):
                        last_event = row
                        last_moment = moment
                        reached_end_of_play = True
                        break
                if reached_end_of_play:
                    break

        # Once we have found it, check the x_loc of the ball to determine basket
        team_basket["team"] = last_event["POSSESSION"]
        if last_moment[5][0][2] >= 47.0:
            team_basket["DIRECTION"] = "RIGHT"
        else:
            team_basket["DIRECTION"] = "LEFT"
        other_direction = "RIGHT" if team_basket["DIRECTION"] == "LEFT" else "LEFT"

        # Next, set up the conditions and values for directionality, direction flips after the second period
        conditions = [
            (combined_event_df["POSSESSION"] == team_basket["team"])
            & (combined_event_df["PERIOD"] < 3),
            (combined_event_df["POSSESSION"] != team_basket["team"])
            & (combined_event_df["PERIOD"] < 3),
            (combined_event_df["POSSESSION"] == team_basket["team"])
            & (combined_event_df["PERIOD"] >= 3),
            (combined_event_df["POSSESSION"] != team_basket["team"])
            & (combined_event_df["PERIOD"] >= 3),
        ]
        values = [
            team_basket["DIRECTION"],
            other_direction,
            other_direction,
            team_basket["DIRECTION"],
        ]

        # Finally, map the direction onto each event and return the combined event dataframe
        combined_event_df["DIRECTION"] = np.select(conditions, values)

        return combined_event_df

    @staticmethod
    def travel_dist(player):
        """
        Calculate the total distance traveled by a player based on their movement coordinates.

        Args:
            player (pd.DataFrame): DataFrame containing player location coordinates (x_loc, y_loc).

        Returns:
            float: Total distance traveled by the player.
        """
        player_locations = player[["x_loc", "y_loc"]]
        diff = np.diff(player_locations, axis=0)
        dist = np.sqrt((diff**2).sum(axis=1))

        return dist.sum()

    @staticmethod
    def travel_dist_all(event_df):
        """
        Calculate the total distance traveled by all players in an event DataFrame.

        Args:
            event_df (pd.DataFrame): Event DataFrame containing player location coordinates.

        Returns:
            pd.Series: Series containing total distance traveled by each player.
        """
        player_travel_dist = event_df.groupby("player_id")[["x_loc", "y_loc"]].apply(
            lambda x: np.sqrt(((np.diff(x, axis=0) ** 2).sum(axis=1)).sum())
        )

        return player_travel_dist

    @staticmethod
    def average_speed(event_df, player_id=None):
        """
        Calculate the average speed of a player or all players in an event DataFrame.

        Args:
            event_df (pd.DataFrame): Event DataFrame containing player location coordinates.
            player_id (int or None): Player ID for individual speed calculation, or None for all players.

        Returns:
            float or pd.Series: Average speed in miles per hour for the specified player or all players.
        """
        seconds = event_df.game_clock.max() - event_df.game_clock.min()
        if player_id is None:
            player_fps = (
                np.sqrt(
                    (
                        (
                            np.diff(
                                event_df[event_df["player_id"].isna()][
                                    ["x_loc", "y_loc"]
                                ],
                                axis=0,
                            )
                            ** 2
                        ).sum(axis=1)
                    ).sum()
                )
                / seconds
            )
        else:
            player_fps = (
                np.sqrt(
                    (
                        (
                            np.diff(
                                event_df[event_df["player_id"] == player_id][
                                    ["x_loc", "y_loc"]
                                ],
                                axis=0,
                            )
                            ** 2
                        ).sum(axis=1)
                    ).sum()
                )
                / seconds
            )
        player_mph = 0.681818 * player_fps

        return player_mph

    @staticmethod
    def average_speed_all(event_df):
        """
        Calculate the average speed of all players in an event DataFrame.

        Args:
            event_df (pd.DataFrame): Event DataFrame containing player location coordinates.

        Returns:
            pd.Series: Series containing average speed in miles per hour for each player.
        """
        seconds = event_df.game_clock.max() - event_df.game_clock.min()
        player_speeds = (
            event_df.groupby("player_id")[["x_loc", "y_loc"]].apply(
                lambda x: np.sqrt(((np.diff(x, axis=0) ** 2).sum(axis=1)).sum())
            )
            / seconds
        ) * 0.681818

        return player_speeds

    @staticmethod
    def distance_between_players_at_moment(player_a, player_b):
        """
        Calculate the Euclidean distance between two players at a given moment.

        Args:
            player_a (pd.Series): DataFrame row representing player A's location at a moment.
            player_b (pd.Series): DataFrame row representing player B's location at the same moment.

        Returns:
            float: Euclidean distance between player A and player B at the moment.
        """
        return euclidean(player_a[["x_loc", "y_loc"]], player_b[["x_loc", "y_loc"]])

    @staticmethod
    def distance_between_players(player_a, player_b):
        """
        Calculate the Euclidean distance between two players at each moment.

        Args:
            player_a (pd.DataFrame): DataFrame containing player A's location coordinates.
            player_b (pd.DataFrame): DataFrame containing player B's location coordinates.

        Returns:
            list: List of distances between player A and player B at each moment.
        """
        player_range = min(len(player_a), len(player_b))

        return [
            euclidean(
                player_a.iloc[i][["x_loc", "y_loc"]],
                player_b.iloc[i][["x_loc", "y_loc"]],
            )
            for i in range(player_range)
        ]

    @staticmethod
    def distance_between_players_with_moment(player_a, player_b):
        """
        Calculate the Euclidean distance between two players at each moment, including moment numbers.

        Args:
            player_a (pd.DataFrame): DataFrame containing player A's location coordinates and moment numbers.
            player_b (pd.DataFrame): DataFrame containing player B's location coordinates and moment numbers.

        Returns:
            list: List of tuples (distance, moment#) between player A and player B at each moment.
        """
        player_range = min(len(player_a), len(player_b))

        return [
            (euclidean(player_a.iloc[i][:1], player_b.iloc[i][:1]), player_a.iloc[i][2])
            for i in range(player_range)
        ]

    @staticmethod
    def distance_between_ball_and_players(moments_df, player_ids):
        """
        Calculate distances between players and the ball for each relevant player per tick in a basketball game.

        This function merges player and ball position data to compute distances

        Args:
            moments_df (pd.DataFrame): DataFrame containing moment data for players and the ball.
            player_ids (List[int]): List of player IDs to include in the distance calculations.

        Returns:
            pd.DataFrame: A DataFrame with columns ['index', 'player_id', 'dist_from_ball', 'radius'],
                        where each row represents a game moment, detailing the player's ID, their distance from the ball, and the ball's radius at that moment.
        """
        # Filter to include only relevant player IDs and the ball
        relevant_df = moments_df[moments_df["player_id"].isin(player_ids + [-1])]

        # Separate ball positions
        ball_positions_df = relevant_df[relevant_df["player_id"] == -1][
            ["index", "player_id", "x_loc", "y_loc", "radius"]
        ]

        # Remove the ball positions from the relevant_df
        players_df = relevant_df[relevant_df["player_id"] != -1][
            ["index", "player_id", "x_loc", "y_loc"]
        ]

        # Merge player and ball positions on their common index --> this will allow us to vectorize the calculation
        merged_df = players_df.merge(
            ball_positions_df, on="index", suffixes=("_player", "_ball")
        )

        # Calculate distances using numpy's norm function across rows (axis=1)
        merged_df["dist_from_ball"] = np.linalg.norm(
            merged_df[["x_loc_player", "y_loc_ball"]].values
            - merged_df[["x_loc_ball", "y_loc_player"]].values,
            axis=1,
        )

        # Prepare the final DataFrame to return
        result_df = merged_df.rename(columns={"player_id_player": "player_id"})[
            ["index", "player_id", "dist_from_ball", "radius"]
        ].reset_index(drop=True)

        return result_df

    @staticmethod
    def distance_between_player_and_other_players(player_id, player_loc, event_df):
        """
        Calculate the distance between a player and all other players at each moment.

        Args:
            player_id (int): Player ID for the reference player.
            player_loc (pd.Series): DataFrame row representing the reference player's location.
            event_df (pd.DataFrame): Event DataFrame containing player location coordinates.

        Returns:
            pd.Series: Series containing distances between the reference player and other players at each moment.
        """
        group = event_df[event_df.player_id != player_id].groupby("player_id")[
            ["x_loc", "y_loc", "index"]
        ]

        return group.apply(
            lambda x: [
                (
                    euclidean(
                        player_loc[["x_loc", "y_loc"]], x.iloc[i][["x_loc", "y_loc"]]
                    ),
                    x.iloc[i][2],
                )
                for i in range(len(x))
            ]
        )

    @staticmethod
    def distance_between_player_and_defensive_players(
        player_id, defending_ids, moments_df
    ):
        """
        Calculate the distance between a player and defensive players at each moment.

        Args:
            player_id (int): Player ID for the reference player.
            defending_ids (list): List of defensive player IDs.
            moments_df (pd.DataFrame): DataFrame containing moment data.

        Returns:
            pd.Series: Series containing distances between the reference player and defensive players at each moment.
        """
        group = moments_df[moments_df.player_id.isin(defending_ids)].groupby(
            "player_id"
        )[["x_loc", "y_loc"]]

        return group.apply(
            lambda x: [
                (
                    euclidean(
                        player_id[["x_loc", "y_loc"]], x.iloc[i][["x_loc", "y_loc"]]
                    ),
                    x.iloc[i][2],
                )
                for i in range(len(x))
            ]
        )

    @staticmethod
    def num_players_past_halfcourt(moment_df):
        """
        Calculate the number of players on the side of the court with the ball at a given moment.

        Args:
            moment_df (pd.DataFrame): DataFrame representing player locations and ball position at a moment.

        Returns:
            int: Number of players on the same side of the court as the ball.
        """
        ball_loc = moment_df.iloc[0]["x_loc"]
        count = 0

        if ball_loc > 47.0:
            count = sum(moment_df["x_loc"] > 47.0)
        else:
            count = sum(moment_df["x_loc"] < 47.0)

        return count

    @staticmethod
    def possession_at_moment(moment_df):
        """
        Determine the player possessing the ball at a given moment.

        Args:
            moment_df (pd.DataFrame): DataFrame representing player locations and ball position at a moment.

        Returns:
            int: Player ID possessing the ball at the moment.
        """
        distances = []

        for player in moment_df.iloc[1:]:
            distances.append(
                [
                    euclidean(
                        [moment_df.iloc[0]["x_loc"], moment_df.iloc[0]["y_loc"]],
                        [player["x_loc"], player["y_loc"]],
                    ),
                    player["player_id"],
                ]
            )

        return min(distances, key=lambda x: x[0])[1]

    @staticmethod
    def convert_ball_handler_to_passes(
        ball_handler_df: pd.DataFrame, fill_limit: int = 2
    ) -> pd.DataFrame:
        """
        Converts ball handling information into a DataFrame of passing events between players.

        This method processes a DataFrame containing tick-by-tick information on which player is handling the ball. It identifies changes in possession by detecting transitions from one player to another and addresses data gaps representing the ball in transit. The function applies smoothing parameters to mitigate noise and accurately delineate passing events. Each event captures the passer and receiver's IDs along with the ticks at which the pass was initiated and completed.

        Args:
            ball_handler_df (pd.DataFrame): DataFrame with columns 'tick' and 'player_id', indicating the ball's handler at each moment.
            fill_limit (int, optional): The maximum number of consecutive NA values to fill, bridging short gaps where the ball is considered in transit, defaulting to 2.

        Returns:
            pd.DataFrame: A DataFrame containing columns 'passer', 'receiver', 'pass_moment', and 'receive_moment', detailing each identified passing event.
        """
        # Generate shifted versions for comparison
        shifted_forward = ball_handler_df['player_id'].shift(1)
        shifted_backward = ball_handler_df['player_id'].shift(-1)

        # Detect new possession (NA to ID or ID change)
        ball_handler_df['new_possession'] = (
            (ball_handler_df['player_id'].notna() & shifted_forward.isna()) |  # From NA to ID
            (ball_handler_df['player_id'] != shifted_forward) & ball_handler_df['player_id'].notna()  # From ID to different ID
        )

        # Detect end of possession (ID to NA or ID change)
        ball_handler_df['end_possession'] = (
            (ball_handler_df['player_id'].notna() & shifted_backward.isna()) |  # From ID to NA
            (ball_handler_df['player_id'] != shifted_backward) & ball_handler_df['player_id'].notna()  # From ID to different ID
        )     

        # Apply fill limit to account for small changes where src data may flicker or fail
        ball_handler_df['player_id'] = ball_handler_df['player_id'].ffill(limit=fill_limit).bfill(limit=fill_limit)

        # Filter events where there is a change to a new player
        start_possessions = ball_handler_df[ball_handler_df['new_possession']]
        end_possessions = ball_handler_df[ball_handler_df['end_possession']]

        # Ensure the start and end possessions dataframes have same length
        if len(start_possessions) > len(end_possessions):
            # Add a fake end for the last possession if necessary
            last_possession = start_possessions.iloc[-1:].copy()
            last_possession['end_possession'] = True
            last_possession['index'] = len(ball_handler_df) - 1  # assuming 'index' is your DataFrame index
            end_possessions = pd.concat([end_possessions, last_possession], ignore_index=True)

        # Construct the passes data
        passes_data = {
            'passer': start_possessions['player_id'].values[:-1],  # exclude the last as there's no subsequent receiver
            'pass_moment': end_possessions.index.values[:-1],  # moments when possession ends
            'receiver': start_possessions['player_id'].values[1:],  # subsequent player receiving the ball
            'receive_moment': start_possessions.index.values[1:]  # moments when new possession starts
        }

        # Convert to DataFrame
        passes_df = pd.DataFrame(passes_data)

        # Remove instances where passer and receiver are the same (due to noise or data error)
        passes_df = passes_df[passes_df['passer'] != passes_df['receiver']]

        return passes_df


    @staticmethod
    def check_for_paint_pass(moments_df, event_pass):
        """
        Check if a pass occurs in the paint area based on start and end locations of the ball.

        Args:
            moments_df (pd.DataFrame): DataFrame representing player locations and ball position at moments.
            event_pass (dict): Pass event containing pass and receive moments.

        Returns:
            bool: True if the pass occurs in the paint area, False otherwise.
        """
        start_loc = moments_df.loc[
            (moments_df["index"] == event_pass["pass_moment"])
            & (moments_df["player_id"] == -1)
        ]
        end_loc = moments_df.loc[
            (moments_df["index"] == event_pass["receive_moment"])
            & (moments_df["player_id"] == -1)
        ]

        return (
            (
                ((start_loc["x_loc"] >= 0.0) & (start_loc["x_loc"] <= 19.0))
                | ((start_loc["x_loc"] >= 71.0) & (start_loc["x_loc"] <= 90.0))
            )
            & ((start_loc["y_loc"] >= 17.0) & (start_loc["y_loc"] <= 33.0))
        ).all() or (
            (
                ((end_loc["x_loc"] >= 0.0) & (end_loc["x_loc"] <= 19.0))
                | ((end_loc["x_loc"] >= 71.0) & (end_loc["x_loc"] <= 90.0))
            )
            & ((end_loc["y_loc"] >= 17.0) & (end_loc["y_loc"] <= 33.0))
        ).all()

    @staticmethod
    def check_for_inbound_pass(moments_df, event_pass):
        """
        Check if a pass is an inbound pass based on the start location of the passer/ball.

        Args:
            moments_df (pd.DataFrame): DataFrame representing player locations and ball position at moments.
            event_pass (dict): Pass event containing pass and receive moments.

        Returns:
            bool: True if the pass is an inbound pass, False otherwise.
        """
        # Extract the locations for the ball at the moment of the pass
        start_loc_ball = moments_df.loc[
            (moments_df["index"] == event_pass["pass_moment"])
            & (moments_df["player_id"] == -1)
        ]

        # Extract the locations for the passer at the moment of the pass
        start_loc_passer = moments_df.loc[
            (moments_df["index"] == event_pass["pass_moment"])
            & (moments_df["player_id"] == event_pass["passer"])
        ]

        # Check baseline inbound conditions for both the ball and the passer
        is_baseline_inbound_ball = (
            (start_loc_ball["x_loc"] <= 0.0) | (start_loc_ball["x_loc"] >= 94.0)
        ) & (start_loc_ball["y_loc"].between(0.0, 50.0))  # Anywhere between the sidelines

        is_baseline_inbound_passer = (
            (start_loc_passer["x_loc"] <= 0.0) | (start_loc_passer["x_loc"] >= 94.0)
        ) & (start_loc_passer["y_loc"].between(0.0, 50.0))  # Anywhere between the sidelines

        # Check sideline inbound conditions for both the ball and the passer
        is_sideline_inbound_ball = (
            (start_loc_ball["y_loc"] <= 0.0) | (start_loc_ball["y_loc"] >= 50.0)
        ) & (start_loc_ball["x_loc"].between(0.0, 94.0))  # Anywhere along the length

        is_sideline_inbound_passer = (
            (start_loc_passer["y_loc"] <= 0.0) | (start_loc_passer["y_loc"] >= 50.0)
        ) & (start_loc_passer["x_loc"].between(0.0, 94.0))  # Anywhere along the length

        # Return True if either inbound condition is met for both the ball and the passer
        return (is_baseline_inbound_ball.any() | is_sideline_inbound_ball.any()) & (is_baseline_inbound_passer.any() | is_sideline_inbound_passer.any())


    @staticmethod
    def get_ball_handler_for_event(
        moments_df: pd.DataFrame,
        player_ids: list,
        ball_distance_heuristic: float = 3.0,
        ball_radius_heuristic: float = 9.0,
    ):
        """
        Extracts and analyzes ball handler moments based on proximity and ball radius.

        This function computes the nearest player to the ball at each recorded moment within a basketball game, considering specified player IDs. It then evaluates whether a shot or pass has occurred by examining if the ball's radius exceeds a set heuristic value, indicating a potential release of the ball.

        Args:
            moments_df (pd.DataFrame): Data on player locations and ball positions.
            player_ids (List[int]): IDs of players to evaluate as potential ball handlers.

        Returns:
            pd.DataFrame: Information on moments where each player is handling the ball, excluding moments likely associated with shots or passes.
        """
        ball_distances = FeatureUtil.distance_between_ball_and_players(
            moments_df, player_ids
        )

        # Find the closest player for each tick/index
        closest_players = ball_distances.loc[
            ball_distances.groupby("index")["dist_from_ball"].idxmin()
        ].drop(columns=["index"])

        # Ensure player_id column is of type nullable int
        closest_players['player_id'] = closest_players['player_id'].astype('Int64')

        # Null out possesion if ball distance or height heuristic is exceeded
        closest_players.loc[
            closest_players["dist_from_ball"] > ball_distance_heuristic, "player_id"
        ] = pd.NA
        closest_players.loc[
            closest_players["radius"] > ball_radius_heuristic, "player_id"
        ] = pd.NA

        # Drop radius, reset index, and return ball_handler_df
        return closest_players.drop(columns=["radius"]).reset_index(drop=True)

    @staticmethod
    def get_defender_for_player(moment_df, player_id, defensive_team_ids):
        """
        Determine the closest defender to a player.

        Args:
            moment_df (pd.DataFrame): DataFrame representing player locations and ball position at moments.
            player_id (int): ID of the player for whom to find the closest defender.
            defensive_team_ids (list): List of defensive team IDs.

        Returns:
            pd.DataFrame: DataFrame containing the closest defender moments and their distances.
        """
        group = moment_df[moment_df.player_id != player_id].groupby("player_id")[
            ["x_loc", "y_loc", "index"]
        ]

        return group.apply(
            FeatureUtil.distance_between_players_with_moment,
            player_b=(moment_df[moment_df.player_id == player_id][["x_loc", "y_loc"]]),
        )

    @staticmethod
    def get_passes_for_event(moments_df, possession, players_data):
        """
        Extract passes made during an event.

        Args:
            moments_df (pd.DataFrame): DataFrame representing player locations and ball position at moments.
            possession (int): Team possessing the ball during the event.
            players_data (list): List of player data.

        Returns:
            list: List of pass dictionaries with passer, receiver, and pass moments.
        """
        player_ids = PlayerMvmtProcessor.get_possession_team_player_ids(
            possession, players_data
        )
        ball_handler_df = FeatureUtil.get_ball_handler_for_event(moments_df, player_ids)
        passes = FeatureUtil.convert_ball_handler_to_passes(ball_handler_df)

        return passes

    @staticmethod
    def get_dribble_handoff_candidates(
        event, moments_df, event_passes, moment_range, players_dict, offset=0
    ):
        """
        Extract potential dribble handoff candidates from event passes.

        Args:
            combined_event_df (pd.DataFrame): DataFrame containing combined event data.
            moments_df (pd.DataFrame): DataFrame representing player locations and ball position at moments.
            event_passes (list): List of pass events.
            moment_range (int): Maximum time duration for a pass to be considered a dribble handoff.
            players_dict (dict): Dictionary containing player information.
            offset (int, optional): Offset for adjusting event IDs. Defaults to 0.

        Returns:
            list: List of dribble handoff candidate dictionaries.
        """
        candidates = []
        event_id = event["EVENT_ID"]
        candidate_count = 0

        # Iterate through DataFrame rows
        for index, event_pass in event_passes.iterrows():
            if (
                not FeatureUtil.check_for_paint_pass(moments_df, event_pass)
                and not FeatureUtil.check_for_inbound_pass(moments_df, event_pass)
                and event_pass["pass_moment"] + moment_range
                >= event_pass["receive_moment"]
            ):

                moment = moments_df.loc[
                    moments_df["index"] == event_pass["pass_moment"]
                ]

                if offset > 0:
                    event_id = f"{event_pass['event_id'].split('-')[0]}-{int(event_pass['event_id'].split('-')[1]) + offset}"

                candidate_count += 1
                candidates.append(
                    {
                        "candidate_id": f"{event_id}-{candidate_count}",
                        "event_id": event_id,
                        "classification_type": "dribble-hand-off",
                        "manual_label": pd.NA,
                        "period": moment["period"].iloc[0],
                        "game_clock": DataLoader.convert_game_clock_to_timestamp(
                            moment["game_clock"].iloc[0]
                        ),
                        "shot_clock": moment["shot_clock"].iloc[0],
                        "player_a": event_pass["passer"],
                        "player_a_name": players_dict[event_pass["passer"]][0],
                        "player_b": event_pass["receiver"],
                        "player_b_name": players_dict[event_pass["receiver"]][0],
                    }
                )

        return candidates

    @staticmethod
    def convert_coordinate_to_hexbin_vertex(x_loc, y_loc, vertices):
        """
        Convert coordinates to the nearest hexbin vertex.

        Args:
            x_loc (float): X-coordinate.
            y_loc (float): Y-coordinate.
            vertices (list): List of hexbin vertices.

        Returns:
            str: Hexbin vertex coordinates as a string.
        """
        min_distance = 10000
        temp_distance = 0
        closest_vertex = -1

        for vertex in vertices:
            temp_distance = abs(abs(x_loc) - abs(vertex[0])) + abs(
                abs(y_loc) - abs(vertex[1])
            )
            if temp_distance < min_distance:
                min_distance = temp_distance
                closest_vertex = vertex

        return f"({closest_vertex[0]},{closest_vertex[1]})"

    @staticmethod
    def get_lingress_results_for_player_trajectory(player_trajectory):
        """
        Calculate linear regression results for player trajectory.

        Args:
            player_trajectory (pd.DataFrame): DataFrame representing player trajectory data.

        Returns:
            scipy.stats.linregress result object: Linear regression results.
        """
        return linregress(player_trajectory["x_loc"], player_trajectory["y_loc"])

    @staticmethod
    def rotate_coordinates_around_center_court(moments_df):
        """
        Rotate player and ball coordinates around the center court.

        Args:
            moments_df (pd.DataFrame): DataFrame representing player locations and ball position at moments.

        Returns:
            pd.DataFrame: DataFrame with rotated coordinates.
        """
        moments_df.loc[:, "x_loc"] = 47.0 - (moments_df.loc[:, "x_loc"] - 47.0)
        moments_df.loc[:, "y_loc"] = 50.0 - moments_df.loc[:, "y_loc"]

        return moments_df

    @staticmethod
    def get_offset_into_game(period, game_clock):
        """
        Calculate the offset time into the game based on period and game clock.

        Args:
            period (int): Current game period.
            game_clock (float): Current game clock time.

        Returns:
            int: Offset time into the game.
        """
        offset = game_clock

        if period <= 4:
            offset += (period - 1) * 12
        else:
            offset += 48 + (period - 1) * 5

        return math.floor(offset)

    @staticmethod
    def get_pass_duration(moments, event_passes, target_candidate):
        """
        Calculate the duration of a pass event.

        Args:
            moments (pd.DataFrame): DataFrame representing player locations and ball position at moments.
            event_passes (list): List of pass events.
            target_candidate (dict): Target candidate for which to calculate the pass duration.

        Returns:
            int or float: Duration of the pass event.
        """
        for event_pass in event_passes:
            if (
                moments.iloc[11 * event_pass["pass_moment"]]["shot_clock"]
                == target_candidate["shot_clock"]
            ):
                return event_pass["receive_moment"] - event_pass["pass_moment"]

        return np.NaN

    @staticmethod
    def get_pass_start_end(moments, event_passes, target_candidate):
        """
        Get the start and end moments of a pass event.

        Args:
            moments (pd.DataFrame): DataFrame representing player locations and ball position at moments.
            event_passes (list): List of pass events.
            target_candidate (dict): Target candidate for which to find the pass start and end moments.

        Returns:
            Tuple[int, int]: Start and end moments of the pass event.
        """
        for event_pass in event_passes:
            if (
                moments.iloc[11 * event_pass["pass_moment"]]["shot_clock"]
                == target_candidate["shot_clock"]
            ):
                return event_pass["pass_moment"], event_pass["receive_moment"]

        return np.NaN, np.NaN
