# scripts/process_game.py

import pandas as pd

from backend.preprocessing.utilities.DataUtil import DataUtil
from backend.preprocessing.utilities.FeatureUtil import FeatureUtil
from backend.preprocessing.utilities.ConstantsUtil import ConstantsUtil

from backend.models import Game
from backend.models import Team
from backend.models import Player
from backend.models import Event
from backend.models import Moment
from backend.models import Candidate

all_games = [
    #"20151106MILNYK", # 101 candidates
    #"20151110DALNOP", # 98 candidates
    #"20151110LALMIA", # 124 candidates
    #"20151211GSWBOS", # 157 candidates
    #"20151225LACLAL", # 112 candidates
    #"20151225NOPMIA", # 151 candidates
    #"20151228SACGSW", # 120 candidates
    #"20151230LALBOS", # 155 candidates
    #"20151231PHXOKC", # 107 candidates
    #"20160102BKLBOS", # 148 candidates  
    #"20160115DALCHI", # 133 candidates
    "20160115MINOKC", # 117 candidates
    "20160118PHINYK", # 126 candidates
    "20160120MIAWAS", # 103 candidates
    "20160123LALPOR", # 122 candidates
 ]

def run():    
    for game in all_games:
        print("\n\n-------------------------------------\n\nLoading data files for " + game)
        annotation_df = DataUtil.load_annotation_df(ConstantsUtil.games[game]['events'])
        game_df = DataUtil.load_game_df(ConstantsUtil.games[game]['raw_data'])
        candidate_df = pd.read_csv(f"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/backend/labled_data/candidates-{game}.csv", index_col=0)
        
        print("Processing Data Files")
        game_data = DataUtil.get_game_data(game_df, annotation_df)
        teams_data = DataUtil.get_teams_data(game_df)
        players_data = DataUtil.get_players_data(game_df)

        print("Creating Game/Team/Player models")
        home_team = Team.objects.update_or_create(**teams_data[0])
        visitor_team = Team.objects.update_or_create(**teams_data[1])
        try:
            Game.objects.get(game_id=game_data["game_id"])
        except:
            Game.objects.update_or_create(
                game_id=game_data["game_id"], 
                game_date=game_data["game_date"], 
                home_team=home_team[0], 
                visitor_team=visitor_team[0], 
                final_score=game_data["final_score"])

        for player in players_data:
            try:
                Player.objects.get(player_id=player['player_id'])
            except:
                Player.objects.update_or_create(**player)

        print("Extracting events...")
        annotation_df = DataUtil.trim_annotation_rows(annotation_df, ConstantsUtil.games[game]['bad_events'])
        annotation_df = FeatureUtil.determine_possession(annotation_df, teams_data)
        annotation_df = DataUtil.generate_event_ids(annotation_df)
        annotation_df = DataUtil.trim_annotation_cols(annotation_df)
        combined_event_df = DataUtil.combine_game_and_annotation_events(game_df, annotation_df)
        combined_event_df = FeatureUtil.determine_directionality(combined_event_df)
        combined_event_df = DataUtil.trim_moments_by_directionality(combined_event_df)
        print("Processed and combined events")

        print("Collecting Event and Moment data")
        all_events = []
        all_moments = []
        for index, event in combined_event_df.iterrows():
            if (f"{event['GAME_ID']}-{event['EVENTNUM']:03}" in set(candidate_df['event_id'])):
                all_events.append(event)
                all_moments.append(DataUtil.get_moments_from_event(event))

        print("\nCreating Event models")
        for event in all_events:
            try:
                Event.objects.get(event_id=event['event_id'])
            except:
                try:
                    player_1 = Player.objects.get(player_id=str(int(event['PLAYER2_ID'])))
                except:
                    player_1 = None
                try:
                    player_2 = Player.objects.get(player_id=str(int(event['PLAYER2_ID'])))
                except:
                    player_2 = None
                try:
                    player_3 = Player.objects.get(player_id=str(int(event['PLAYER3_ID'])))
                except:
                    player_3 = None

                Event.objects.create(
                    event_id = event['event_id'],
                    game = Game.objects.get(game_id=event['GAME_ID']),
                    possesion_team = Team.objects.get(team_id=str(int(event['possession']))),
                    player_1 = player_1,
                    player_2 = player_2,
                    player_3 = player_3,
                    event_num = event['EVENTNUM'],
                    event_msg_type = event['EVENTMSGTYPE'],
                    event_action_type = event['EVENTMSGACTIONTYPE'],
                    period = event['PERIOD'],
                    period_time = event['PCTIMESTRING'],
                    home_desc = event['HOMEDESCRIPTION'],
                    visitor_desc = event['VISITORDESCRIPTION'],
                    score = event['SCORE'],
                    directionality = event['direction']
                    )
        print("\nCreating Moment models")
        for moments in all_moments:
            for index, moment in moments.iterrows():
                Moment.objects.get_or_create(
                    team = Team.objects.get(team_id=moment['team_id']) if moment['team_id'] != -1 else None, 
                    player = Player.objects.get(player_id=moment['player_id']) if moment['player_id'] != -1 else None, 
                    event = Event.objects.get(event_id=moment['event_id']), 
                    x_loc = moment['x_loc'], 
                    y_loc = moment['y_loc'], 
                    radius = moment['radius'], 
                    index = moment['moment'], 
                    game_clock = moment['game_clock'],
                    shot_clock = moment['shot_clock'],
                )
        print("\nCreating Candidate models")
        for index, candidate in candidate_df.iterrows():
            try:
                Candidate.objects.get(candidate_id=candidate['candidate_id'])
            except:
                try:
                    Candidate.objects.create(
                        candidate_id = candidate['candidate_id'],
                        event = Event.objects.get(event_id=candidate['event_id']),
                        classification_type = candidate['classification_type'],
                        manual_label = candidate['manual_label'],
                        period = candidate['period'],
                        game_clock = candidate['game_clock'],
                        shot_clock = candidate['shot_clock'],
                        player_a = Player.objects.get(player_id=candidate['player_a']),
                        player_a_name = candidate['player_a_name'],
                        player_b = Player.objects.get(player_id=candidate['player_b']),
                        player_b_name = candidate['player_b_name'],
                        notes = candidate['notes'],
                    )
                except:
                    print(f"\nFailed on candidate {candidate}")
        
        print("Finished processing game")