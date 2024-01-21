import pandas as pd	
import numpy as np	
import sys

import matplotlib.pyplot as plt	
import seaborn as sns	

from utilities.FeatureUtil import FeatureUtil
from utilities.DataUtil import DataUtil
from utilities.ConstantsUtil import ConstantsUtil

processed_games = [
    "20151029MEMIND", # 81 candidates
    "20151106MIAIND", # 45 candidates
    #"20151106MILNYK", # 101 candidates
    "20151106PHICLE", # 44 candidates
    #"20151110DALNOP", # 98 candidates
    #"20151110LALMIA", # 124 candidates
    #"20151211GSWBOS", # 157 candidates
    #"20151225LACLAL", # 112 candidates
    #"20151225NOPMIA", # 151 candidates
    "20151228ATLIND", # 46 candidates
    "20151228CLEPHX", # 27 candidates
    "20151228LALCHA", # 102 candidates
    "20151228PHIUTA", # 21 candidates
    #"20151228SACGSW", # 120 candidates
    "20151228ATLIND", # 46 candidates
    "20151228TORCHI", # 53 candidates
    "20151229ATLHOU", # 33 candidates
    "20151229CLEDEN", # 48 candidates
    "20151230BKLORL", # 49 candidates
    #"20151230LALBOS", # 155 candidates
    "20151230PHXSAS", # 46 candidates
    "20151230WASTOR", # 93 candidates
    "20151230DENPOR", # 87 candidates
    "20151230GSWDAL", # 44 candidates
    #"20151231PHXOKC", # 107 candidates
    "20151231LACNOP", # 36 candidates
    #"20160102BKLBOS", # 148 candidates  
    "20160102HOUSAS", # 29 candidates
    "20160113ATLCHA", # 68 candidates
    "20160113MIALAC", # 123 candidates  
    "20160113NOPSAC", # 30 candidates
    "20160113NYKBKL", # 32 candidates
    "20160113UTAPOR", # 55 candidates  
    "20160115ATLMIL", # 50 candidates
    "20160115CHANOP", # 46 candidates
    #"20160115DALCHI", # 133 candidates
    "20160115MIADEN", # 34 candidates
    #"20160115MINOKC", # 117 candidates
    "20160115WASIND", # 47 candidates
    "20160118ORLATL", # 50 candidates
    #"20160118PHINYK", # 126 candidates
    "20160120CHAOKC", # 87 candidates
    #"20160120MIAWAS", # 103 candidates
    "20160121DETNOP", # 29 candidates
    "20160122CHIBOS", # 84 candidates
    "20160122LACNYK", # 58 candidates
    "20160122MILHOU", # 13 candidates
    "20160122MIATOR", # 30 candidates
    "20160123ATLPHX", # 46 candidates
    "20160123CHICLE", # FAILED
    "20160123DETDEN", # 52 candidates
    "20160123INDSAC", # 31 candidates
    #"20160123LALPOR", # 122 candidates
    "20160123NYKCHA", # 41 candidates
 ]

all_results = "All Results:\n\n"

for game in ConstantsUtil.games:
    if not game in processed_games:
        print(f"\n\n------------------------------\n\nStarting {game}")
        game_df = DataUtil.load_game_df(ConstantsUtil.games[game]['raw_data'])
        annotation_df = DataUtil.load_annotation_df(ConstantsUtil.games[game]['events'])  
        print(f"Loaded game")

        teams_data = DataUtil.get_teams_data(game_df)
        players_data = DataUtil.get_players_data(game_df)
        players_dict = DataUtil.get_players_dict(game_df)
        print("Extracted team/player data")

        print("Extracting events...")
        annotation_df = DataUtil.trim_annotation_rows(annotation_df, ConstantsUtil.games[game]['bad_events'])
        annotation_df = FeatureUtil.determine_possession(annotation_df, teams_data)
        annotation_df = DataUtil.generate_event_ids(annotation_df)
        annotation_df = DataUtil.trim_annotation_cols(annotation_df)
        combined_event_df = DataUtil.combine_game_and_annotation_events(game_df, annotation_df)
        # Get direction for each play, and remove moments occuring on the other half of the court
        combined_event_df = FeatureUtil.determine_directionality(combined_event_df)
        combined_event_df = DataUtil.trim_moments_by_directionality(combined_event_df)
        print("Processed and combined events")

        all_candidates = []
        succesful = 0
        failed = 0
        pass_detected = 0
        hand_off_detected = 0

        print("Starting Candidate Extraction\n")
        for index, event in combined_event_df.iterrows():
            try:
                moments_df = DataUtil.get_moments_from_event(event)
                if len(moments_df) > 0:
                    event_passes = FeatureUtil.get_passess_for_event(moments_df, event["possession"], players_data)
                    if len(event_passes) > 0:
                        pass_detected += 1
                    dribble_handoff_candidates = FeatureUtil.get_dribble_handoff_candidates(combined_event_df, moments_df, event_passes, ConstantsUtil.games[game]['moment_range'], players_dict)
                    if len(dribble_handoff_candidates) > 0:
                        all_candidates += dribble_handoff_candidates
                        hand_off_detected += 1
                else:
                    print("No moments for event: " + str(event['EVENTNUM']))
                succesful += 1
            except:
                print("Issue at index: " + str(event['EVENTNUM']), sys.exc_info())
                failed += 1

        final_candidates = DataUtil.remove_duplicate_candidates(all_candidates)
        
        result = (
            f"\n\n------------------------------\n\nStats for {game}\n" +
            f"\nNumber of candidates parsed: {str(len(final_candidates))}" + 
            f"\nSuccessful events: {str(succesful)} \nFailed events: {str(failed)}" + 
            f"\nPercent Successful: {str(round(succesful/(failed + succesful), 2)*100)}%" +
            f"\nEvents w/ pass detected: " + str(pass_detected) + "\nEvents w/ hand-off detected: " + str(hand_off_detected) +
            f"\nPercent w/ candidate: {str(round(hand_off_detected/(failed + succesful), 2)*100)}%"
        )
        all_results += result 
        print(result)


        candidate_df = pd.DataFrame(final_candidates)
        candidate_df.to_csv(f'static/backend/test/candidates-{game}.csv')
        print("Saving to csv...\n")

print("Writing all results to txt...")
text_file = open("static/backend/notes/all_results.txt", "w")
n = text_file.write(all_results)
text_file.close()
