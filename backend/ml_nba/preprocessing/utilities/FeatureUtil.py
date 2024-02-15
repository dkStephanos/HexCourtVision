import math
import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean
from scipy.stats import linregress
from .AnnotationProcessor import AnnotationProcessor
from .EventsProcessor import EventsProcessor
from .DataLoader import DataLoader
from .PlayerMvmtProcessor import PlayerMvmtProcessor


class FeatureUtil:
    """
    Utility class for various feature extraction and analysis functions related to basketball events.

    This class provides methods for determining possession and directionality of events, as well as
    calculating travel distances, player speed, and other basketball-related features.
    """

    @staticmethod
    def determine_possession(annotation_df, teams_data):
        """
        Determine possession for each event in the annotation DataFrame.

        Args:
            annotation_df (pd.DataFrame): DataFrame containing event annotations.
            teams_data (list): List of team data dictionaries.

        Returns:
            pd.DataFrame: DataFrame with a new 'possession' column indicating possession for each event.
        """
        # Static mappings for event types to possession identifiers
        possession_map = {
            1: "PLAYER1_TEAM_ID",
            2: "PLAYER1_TEAM_ID",
            "Turnover: Shot Clock": "PLAYER1_ID",  # This seems off, might need adjustment
            "T.Foul": "PLAYER1_TEAM_ID",
            5: "PLAYER1_TEAM_ID",
            6: "PLAYER2_TEAM_ID",
        }

        # Define a separate handling for dynamic possession determination
        def determine_event_possession(row):
            event_type = row["EVENTMSGTYPE"]
            # Handle dynamic cases first
            if event_type == "Def. 3 Sec":
                return teams_data[1]["team_id"] if row["PLAYER1_TEAM_ID"] == teams_data[0]["team_id"] else teams_data[0]["team_id"]
            
            # Then handle static mappings
            if event_type in possession_map:
                # Directly return the mapped value if it's a static mapping
                return row[possession_map[event_type]]
            
            # For descriptions that require lookup in the possession map
            event_desc = str(row["HOMEDESCRIPTION"]) if event_type in [1, 2] else str(row["VISITORDESCRIPTION"])
            return row.get(possession_map.get(event_desc, "PLAYER1_TEAM_ID"), np.NaN)  # Adjusted to handle default case

        annotation_df["possession"] = annotation_df.apply(determine_event_possession, axis=1)

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
                for moment in row["moments"]:
                    if (moment[2] <= event_time + 1) and (moment[2] >= event_time - 1):
                        last_event = row
                        last_moment = moment
                        reached_end_of_play = True
                        break
                if reached_end_of_play:
                    break

        # Once we have found it, check the x_loc of the ball to determine basket
        team_basket["team"] = last_event["possession"]
        if last_moment[5][0][2] >= 47.0:
            team_basket["direction"] = "RIGHT"
        else:
            team_basket["direction"] = "LEFT"
        other_direction = "RIGHT" if team_basket["direction"] == "LEFT" else "LEFT"

        # Next, set up the conditions and values for directionality, direction flips after the second period
        conditions = [
            (combined_event_df["possession"] == team_basket["team"])
            & (combined_event_df["PERIOD"] < 3),
            (combined_event_df["possession"] != team_basket["team"])
            & (combined_event_df["PERIOD"] < 3),
            (combined_event_df["possession"] == team_basket["team"])
            & (combined_event_df["PERIOD"] >= 3),
            (combined_event_df["possession"] != team_basket["team"])
            & (combined_event_df["PERIOD"] >= 3),
        ]
        values = [
            team_basket["direction"],
            other_direction,
            other_direction,
            team_basket["direction"],
        ]

        # Finally, map the direction onto each event and return the combined event dataframe
        combined_event_df["direction"] = np.select(conditions, values)

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
        Calculate the distance between players and the ball for each player in the specified list.

        Args:
            moments_df (pd.DataFrame): DataFrame containing moment data.
            player_ids (list): List of player IDs.

        Returns:
            pd.Series: Series containing distances between players and the ball for each player.
        """
        group = moments_df[moments_df.player_id.isin(player_ids)].groupby("player_id")[
            ["x_loc", "y_loc"]
        ]
        ball_distances = group.apply(
            lambda x: [euclidean(x.iloc[i], x.iloc[-1]) for i in range(len(x))]
        )

        return ball_distances

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
    def convert_ball_handler_to_passes(ball_handler_df):
        """
        Convert ball handler DataFrame into a list of passes with passer, receiver, and pass moments.

        Args:
            ball_handler_df (pd.DataFrame): DataFrame representing ball handler moments.

        Returns:
            list: List of pass dictionaries with passer, receiver, and pass moments.
        """
        passes = []
        passer = pd.NA
        pass_moment = 0
        receiver = pd.NA
        receive_moment = 0

        for i in range(len(ball_handler_df)):
            if pd.isna(passer) and not pd.isna(ball_handler_df.iloc[i]["player_id"]):
                passer = ball_handler_df.iloc[i]["player_id"]
            elif (
                not pd.isna(passer)
                and pass_moment == 0
                and pd.isna(ball_handler_df.iloc[i]["player_id"])
            ):
                pass_moment = ball_handler_df.iloc[i - 1]["index"]
            elif (
                not pd.isna(passer)
                and not pd.isna(ball_handler_df.iloc[i]["player_id"])
                and passer == ball_handler_df.iloc[i]["player_id"]
                and pass_moment != 0
            ):
                pass_moment = 0
            elif (
                not pd.isna(passer)
                and not pd.isna(ball_handler_df.iloc[i]["player_id"])
                and ball_handler_df.iloc[i]["player_id"] != passer
            ):
                receiver = ball_handler_df.iloc[i]["player_id"]
                receive_moment = ball_handler_df.iloc[i]["index"]
                pass_moment = (
                    ball_handler_df.iloc[i - 1]["index"]
                    if not pd.isna(ball_handler_df.iloc[i - 1]["player_id"])
                    else pass_moment
                )
                if (
                    len(passes) == 0
                    or passes[-1]["passer"] != passer
                    or pass_moment > passes[-1]["pass_moment"] + 10
                ):
                    passes.append(
                        {
                            "passer": passer,
                            "pass_moment": pass_moment,
                            "receiver": receiver,
                            "receive_moment": receive_moment,
                        }
                    )
                passer = pd.NA
                receiver = pd.NA
                pass_moment = 0

        return passes

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
        Check if a pass is an inbound pass based on the start location of the ball.

        Args:
            moments_df (pd.DataFrame): DataFrame representing player locations and ball position at moments.
            event_pass (dict): Pass event containing pass and receive moments.

        Returns:
            bool: True if the pass is an inbound pass, False otherwise.
        """
        start_loc = moments_df.loc[(moments_df['index'] == event_pass['pass_moment']) & (moments_df['player_id'] == -1)]
        
        return (((((start_loc['x_loc'] >= 0.0) & (start_loc['x_loc'] <= 5.0)) | ((start_loc['x_loc'] >= 89.0) & (start_loc['x_loc'] <= 94.0))) & ((start_loc['y_loc'] >= 17.0) & (start_loc['y_loc'] <= 33.0))).all())


    @staticmethod
    def get_ball_handler_for_event(moments_df, player_ids):
        """
        Extract ball handler moments and their respective players.

        Args:
            moments_df (pd.DataFrame): DataFrame representing player locations and ball position at moments.
            player_ids (list): List of player IDs to consider for ball handling.

        Returns:
            pd.DataFrame: DataFrame containing ball handler moments and player IDs.
        """
        ball_distances = FeatureUtil.distance_between_ball_and_players(moments_df, player_ids)
        ball_dist_df = EventsProcessor.convert_labeled_series_to_df('player_id', 'ball_distances', ball_distances)
        ball_handler_df = AnnotationProcessor.get_labeled_mins_from_df(ball_dist_df, "dist_from_ball")
        ball_handler_df.loc[ball_handler_df['dist_from_ball'] > 3.3, 'player_id'] = pd.NA
        
        moment_nums = [int(moments_df.iloc[i * 11]['index']) for i in range(len(ball_handler_df))]
        ball_handler_df['index'] = moment_nums

        for i in range(len(ball_handler_df)):
            if moments_df.iloc[i * 11]['radius'] >= 10.0:
                ball_handler_df.iat[i, 0] = pd.NA

        return ball_handler_df

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
        group = moment_df[moment_df.player_id != player_id].groupby("player_id")[["x_loc", "y_loc", "index"]]
        
        return group.apply(FeatureUtil.distance_between_players_with_moment, player_b=(moment_df[moment_df.player_id == player_id][["x_loc", "y_loc"]]))

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
        player_ids = PlayerMvmtProcessor.get_possession_team_player_ids(possession, players_data)
        ball_handler_df = FeatureUtil.get_ball_handler_for_event(moments_df, player_ids)
        passes = FeatureUtil.convert_ball_handler_to_passes(ball_handler_df)

        return passes

    @staticmethod
    def get_dribble_handoff_candidates(combined_event_df, moments_df, event_passes, moment_range, players_dict, offset=0):
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
        candidate_count = 0

        for event_pass in event_passes:
            if not FeatureUtil.check_for_paint_pass(moments_df, event_pass) and not FeatureUtil.check_for_inbound_pass(moments_df, event_pass) and event_pass['pass_moment'] + moment_range >= event_pass['receive_moment']:
                moment = moments_df.loc[(moments_df['index'] == event_pass['pass_moment']) & (moments_df['player_id'] == event_pass['passer'])]
                event_id = moment['event_id'].values[0]

                if offset > 0:
                    event_id = f"{event_id.split('-')[0]}-{int(event_id.split('-')[0]) + offset}"

                event = combined_event_df.loc[(combined_event_df['event_id'] == event_id)]
                candidate_count += 1

                candidates.append({
                    'candidate_id': f"{event_id}-{candidate_count}",
                    'event_id': event_id,
                    'classification_type': 'dribble-hand-off',
                    'manual_label': pd.NA,
                    'period': event['PERIOD'].values[0],
                    'game_clock': DataLoader.convert_game_clock_to_timestamp(moment['game_clock']),
                    'shot_clock': moment['shot_clock'].values[0],
                    'player_a': event_pass['passer'],
                    'player_a_name': players_dict[event_pass['passer']][0],
                    'player_b': event_pass['receiver'],
                    'player_b_name': players_dict[event_pass['receiver']][0]
                })

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
            temp_distance = abs(abs(x_loc) - abs(vertex[0])) + abs(abs(y_loc) - abs(vertex[1]))
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
        return linregress(player_trajectory['x_loc'], player_trajectory['y_loc'])

    @staticmethod
    def rotate_coordinates_around_center_court(moments_df):
        """
        Rotate player and ball coordinates around the center court.

        Args:
            moments_df (pd.DataFrame): DataFrame representing player locations and ball position at moments.

        Returns:
            pd.DataFrame: DataFrame with rotated coordinates.
        """
        moments_df.loc[:, 'x_loc'] = 47.0 - (moments_df.loc[:, 'x_loc'] - 47.0)
        moments_df.loc[:, 'y_loc'] = 50.0 - moments_df.loc[:, 'y_loc']

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
            if moments.iloc[11 * event_pass['pass_moment']]['shot_clock'] == target_candidate['shot_clock']:
                return event_pass['receive_moment'] - event_pass['pass_moment']

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
            if moments.iloc[11 * event_pass['pass_moment']]['shot_clock'] == target_candidate['shot_clock']:
                return event_pass['pass_moment'], event_pass['receive_moment']

        return np.NaN, np.NaN
