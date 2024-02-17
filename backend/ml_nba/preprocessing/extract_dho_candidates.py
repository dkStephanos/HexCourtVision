import sys
import pandas as pd
from ml_nba.preprocessing.utilities.FeatureUtil import FeatureUtil
from ml_nba.preprocessing.utilities.DataLoader import DataLoader
from ml_nba.preprocessing.utilities.ConstantsUtil import ConstantsUtil
from ml_nba.preprocessing.utilities.EventsProcessor import EventsProcessor
from ml_nba.preprocessing.utilities.PlayerMvmtProcessor import PlayerMvmtProcessor


all_results = "All Results:\n\n"

def extract_dho_candidates(game_key: str, moment_range: int = None):
    print(f"\n\n------------------------------\n\nStarting {game_key}")
    
    # Collect processed game and event data
    game_df = DataLoader.load_processed_game(game_key)
    raw_df = DataLoader.load_raw_game(game_key)
    
    if moment_range is None:
        moment_range = ConstantsUtil.games[game_key]['moment_range']
    
    print(f"Loaded game")

    players_data = DataLoader.get_players_data(raw_df)
    players_dict = DataLoader.get_players_dict(raw_df)
    print("Extracted team/player data")

    all_candidates = []
    successful = 0
    failed = 0
    pass_detected = 0
    hand_off_detected = 0

    print("Starting Candidate Extraction\n")
    for index, event in game_df.iterrows():
        try:
            moments_df = EventsProcessor.get_moments_from_event(event)
            if len(moments_df) > 0:
                event_passes = FeatureUtil.get_passes_for_event(moments_df, event["POSSESSION"], players_data)
                if len(event_passes) > 0:
                    pass_detected += 1
                dribble_handoff_candidates = FeatureUtil.get_dribble_handoff_candidates(
                    game_df, moments_df, event_passes, moment_range, players_dict)
                if len(dribble_handoff_candidates) > 0:
                    all_candidates += dribble_handoff_candidates
                    hand_off_detected += 1
            else:
                print("No moments for event: " + str(event['EVENTNUM']))
            successful += 1
        except:
            print("Issue at index: " + str(event['EVENTNUM']), sys.exc_info())
            failed += 1

    final_candidates = EventsProcessor.remove_duplicate_candidates(all_candidates)

    result = (
        f"\n\n------------------------------\n\nStats for {game_key}\n" +
        f"\nNumber of candidates parsed: {str(len(final_candidates))}" +
        f"\nSuccessful events: {str(successful)} \nFailed events: {str(failed)}" +
        f"\nPercent Successful: {str(round(successful / (failed + successful), 2) * 100)}%" +
        f"\nEvents w/ pass detected: " + str(pass_detected) + "\nEvents w/ hand-off detected: " + str(hand_off_detected) +
        f"\nPercent w/ candidate: {str(round(hand_off_detected / (failed + successful), 2) * 100)}%"
    )
    all_results += result
    print(result)

    candidate_df = pd.DataFrame(final_candidates)
    candidate_df.to_csv(f'static/backend/test/candidates-{game_key}.csv')
    print("Saving to csv...\n")

    print(all_results)
