# scripts/process_game.py

import pandas as pd
import easygui
import sys

from data.preprocessing.utilities.DataUtil import DataUtil
from data.preprocessing.utilities.FeatureUtil import FeatureUtil
from data.preprocessing.utilities.ConstantsUtil import ConstantsUtil

from data.models import Game
from data.models import Team
from data.models import Player
from data.models import Event
from data.models import Moment
from data.models import Candidate

def run():
    # Load game with GUI
    game_path = easygui.fileopenbox(default="C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/", title="Select a game file")
    game_df = DataUtil.load_game_df(game_path)

    easygui.msgbox("Next select corresponding annotation file")
    annotation_path = easygui.fileopenbox(default="C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/", title="Select an annotation file")
    annotation_df = DataUtil.load_annotation_df(annotation_path)
    print("Loading data files")
    #game_df = DataUtil.load_game_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\game_raw_data\12.11.2015.GSW.at.BOS\0021500336.json")
    #annotation_df = DataUtil.load_annotation_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\event_annotations\events-20151211GSWBOS.csv")

    print("Processing Data Files")
    game_data = DataUtil.get_game_data(game_df, annotation_df)
    teams = DataUtil.get_teams_data(game_df)
    players = DataUtil.get_players_data(game_df)

    print("Creating Game/Team/Player models")
    home_team = Team.objects.get_or_create(**teams[0])
    visitor_team = Team.objects.get_or_create(**teams[1])
    game = Game.objects.get_or_create(
        game_id=game_data["game_id"], 
        game_date=game_data["game_date"], 
        home_team=home_team[0], 
        visitor_team=visitor_team[0], 
        final_score=game_data["final_score"])

    for player in players:
        Player.objects.get_or_create(**player)

    print("Finding Candidates")
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
    all_events = []
    all_moments = []
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
                    all_events.append(event)
                    all_moments.append(moments_df)
                    hand_off_detected += 1
            else:
                print("No moments for event: " + str(event['EVENTNUM']))
            succesful += 1
        except:
            print("Issue at index: " + str(event['EVENTNUM']), sys.exc_info())
            failed += 1

    final_candidates = DataUtil.remove_duplicate_candidates(all_candidates)
    candidate_df = pd.DataFrame(final_candidates) 

    result = (
        f"\n\n------------------------------\n\nStats for {game}\n" +
        f"\nNumber of candidates parsed: {str(len(final_candidates))}" + 
        f"\nSuccessful events: {str(succesful)} \nFailed events: {str(failed)}" + 
        f"\nPercent Successful: {str(round(succesful/(failed + succesful), 2)*100)}%" +
        f"\nEvents w/ pass detected: " + str(pass_detected) + "\nEvents w/ hand-off detected: " + str(hand_off_detected) +
        f"\nPercent w/ candidate: {str(round(hand_off_detected/(failed + succesful), 2)*100)}%"
    )
    print(result)

    print("\nCreating Event/Moment/Candidate models")
    for candidate in all_candidates:
        Candidate.objects.get_or_create(**candidate)
    for event in all_events:
        Event.objects.get_or_create({
            'event_id': event['event_id'],
            'game_id': event['GAME_ID'],
            'possesion_team': event['possession'],
            'player_1': event['PLAYER1_ID'],
            'player_3': event['PLAYER2_ID'],
            'player_2': event['PLAYER3_ID'],
            'event_num': event['EVENTNUM'],
            'event_msg_type': event['EVENTMSGTYPE'],
            'event_action_type': event['EVENTMSGACTIONTYPE'],
            'period': event['PERIOD'],
            'period_time': event['PCTIMESTRING'],
            'home_desc': event['HOMEDESCRIPTION'],
            'visitor_desc': event['VISITORDESCRIPTION'],
            'score': event['SCORE'],
            'directionality': event['direction']
            })
    for moment in all_moments:
        Moment.objects.get_or_create(**moment)
    print("Finished processing game")