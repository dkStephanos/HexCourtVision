import pandas as pd
from ml_nba.preprocessing.utilities.FeatureUtil import FeatureUtil
from ml_nba.preprocessing.utilities.DataLoader import DataLoader
from ml_nba.preprocessing.utilities.ConstantsUtil import ConstantsUtil
from ml_nba.preprocessing.utilities.EventsProcessor import EventsProcessor


def extract_dho_candidates(game_key: str, moment_range: int = None):
    print(f"\n\n------------------------------\n\nStarting {game_key}")

    # Collect processed game and event data
    game_df = DataLoader.load_processed_game(game_key)
    raw_df = DataLoader.load_raw_game(game_key)

    # Not all recordings seem to be at the same frequency, moment_range helps scale this
    # NOTE: defaults to 8 ticks of the clock as the maximum window for the action to occur
    if moment_range is None:
        if game_key in ConstantsUtil.games:
            moment_range = ConstantsUtil.games[game_key]["moment_range"]
        else:
            moment_range = 8

    print(f"Loaded game")

    players_data = DataLoader.get_players_data(raw_df)
    players_dict = DataLoader.get_players_dict(raw_df)
    print("Extracted team/player data")

    all_candidates = []
    pass_detected = 0
    hand_off_detected = 0
    all_results = "All Results:\n\n"

    print("Starting Candidate Extraction\n")
    for index, event in game_df.iterrows():
        moments_df = EventsProcessor.get_moments_from_event(event)

        if not moments_df.empty:
            event_passes = FeatureUtil.get_passes_for_event(
                moments_df, event["POSSESSION"], players_data
            )

            if len(event_passes) > 0:
                pass_detected += 1
                
                dribble_handoff_candidates = FeatureUtil.get_dribble_handoff_candidates(
                    event, moments_df, event_passes, moment_range, players_dict
                )
                if dribble_handoff_candidates:
                    all_candidates.extend(dribble_handoff_candidates)  # Assuming this is a list
                    hand_off_detected += 1
                    print(f"Discovered {len(dribble_handoff_candidates)} dho candidates for event: {index}!")
                else:
                    print(f"No handoffs detected amoung {len(event_passes)} passes for event: {index}")
            else:
                print(f"No event_passes for event: {index}")
        else:
            print(f"No moments for event: {index}")

    final_candidates = EventsProcessor.remove_duplicate_candidates(all_candidates)

    result = (
        f"\n\n------------------------------\n\nStats for {game_key}\n"
        + f"\nNumber of candidates parsed: {str(len(final_candidates))}"
        + f"\nEvents w/ pass detected: "
        + str(pass_detected)
        + "\nEvents w/ hand-off detected: "
        + str(hand_off_detected)
        + f"\nPercent w/ candidate: {str(round(hand_off_detected / (len(game_df)), 2) * 100)}%"
    )
    all_results += result
    print(result)

    candidate_df = pd.DataFrame(final_candidates)
    candidate_df.to_csv(f"{ConstantsUtil.CANDIDATES_PATH}/candidates-{game_key}.csv")
    print("Saving to csv...\n")

    print(all_results)
