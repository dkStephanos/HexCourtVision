from django.db import transaction
from ml_nba.models import Game, Event, Moment, Candidate, Team, Player
from ml_nba.preprocessing.utilities.DataLoader import DataLoader
from ml_nba.preprocessing.utilities.DatabaseUtil import DatabaseUtil
from ml_nba.preprocessing.utilities.EventsProcessor import EventsProcessor


def persist_processed_game(game_id: str, overwrite: bool = False):
    """
    Processes and persists all relevant data for a single NBA game into the database.

    This function takes a game key, loads raw and processed data files associated with that game,
    processes the data to extract game, team, player, event, moment, and candidate information,
    and updates or creates corresponding records in the database. Uses django transactions to
    ensure atomic operations and rollback any changes if we run into an exception during persistence.

    Parameters:
    - game_id (str): A unique identifier for the game being processed.
    - overwrite (bool): Indicates whether to overwrite previous game data. Defaults to False.
                        NOTE: An exception is thrown if False and game data found

    Steps involved:
    1. Load data files for the game, its events, combined event data, and candidate data.
    2. Process the raw data files to extract structured data for game, teams, and players.
    3. Update or create records for the home and visitor teams, and the game itself.
    4. Bulk update or create player records to minimize database hits.
    5. Collect event and moment data based on processed combined event data and candidate data.
    6. Create event records and associated moment records in bulk, again to improve efficiency.
    7. Process and create candidate records for the game.
    8. Utilize Django's transaction.atomic to ensure data integrity and efficient bulk operations.

    """
    if DatabaseUtil.check_game_exists(game_id):
        if not overwrite:
            raise Exception(f"Cannot persist requested game_id: {game_id}. Game already present and overwrite set to False.")
        else:
            print('Overwrite set to True. Dropping previous entries...')
            with transaction.atomic():
                # Fetch related Event instances
                game = Game.objects.get(game_id=game_id)
                related_events = Event.objects.filter(game=game)
                
                # Delete related Moment/Candidate instances
                Moment.objects.filter(event__in=related_events).delete()
                Candidate.objects.filter(event__in=related_events).delete()
                
                # Now, you can delete the Event instances
                related_events.delete()
    
    print("Loading data files...")
    game_df = DataLoader.load_raw_game(game_id)
    annotation_df = DataLoader.load_game_events(game_id)
    combined_event_df = DataLoader.load_processed_game(game_id)
    candidate_df = DataLoader.load_game_candidates(game_id)

    print("Processing Data Files...")
    game_data = DataLoader.get_game_data(game_df, annotation_df)
    teams_data = DataLoader.get_teams_data(game_df)
    players_data = DataLoader.get_players_data(game_df)

    print("Creating or Updating Game/Team/Player models...")
    with transaction.atomic():
        home_team, _ = Team.objects.update_or_create(**teams_data["home_team"])
        visitor_team, _ = Team.objects.update_or_create(**teams_data["away_team"])
        game, _ = Game.objects.update_or_create(
            game_id=game_data["game_id"],
            defaults={
                **game_data,
                "home_team": home_team,
                "visitor_team": visitor_team,
            },
        )

        DatabaseUtil.bulk_update_or_create(
            Player,
            players_data,
            "player_id",
        )

    print("Collecting and Creating Event and Moment Models...")
    event_instances = []
    moment_instances = []
    for _, event_row in combined_event_df.iterrows():
        event_data = event_row.to_dict()
        if (event_data['EVENT_ID'] in set(candidate_df['event_id'])):
            # Map incoming event data to Event model fields
            event_kwargs = {
                'event_id': event_data['EVENT_ID'],
                'game': game,
                'possession_team': Team.objects.get(team_id=int(event_data['POSSESSION'])),
                'player_1': Player.objects.filter(player_id=event_data['PLAYER1_ID']).first(),
                'player_2': Player.objects.filter(player_id=event_data['PLAYER2_ID']).first(),
                'player_3': Player.objects.filter(player_id=event_data['PLAYER3_ID']).first(),
                'event_num': event_data['EVENT_ID'].split("-")[1],
                'event_msg_type': event_data['EVENTMSGTYPE'],
                'event_action_type': event_data['EVENTMSGACTIONTYPE'],
                'period': event_data['PERIOD'],
                'period_time': event_data['PCTIMESTRING'],
                'home_desc': event_data.get('HOMEDESCRIPTION', ''),
                'visitor_desc': event_data.get('VISITORDESCRIPTION', ''),
                'score': event_data.get('SCORE', '0 - 0'),
                'directionality': event_data.get('DIRECTION')
            }
            event = Event(**event_kwargs)
            event_instances.append(event)

            # Prepare Moment instances for bulk creation
            for _, moment_row in EventsProcessor.get_moments_from_event(event_data).iterrows():
                moment_data = moment_row.to_dict()
                # Adjust moment_data to correctly reference related instances
                adjusted_moment_data = {
                    'team': Team.objects.filter(team_id=moment_data.get('team_id')).first(),
                    'player': Player.objects.filter(player_id=moment_data.get('player_id')).first(),
                    'event': event,  # Directly use the event instance created/updated above
                    'x_loc': moment_data['x_loc'],
                    'y_loc': moment_data['y_loc'],
                    'radius': moment_data.get('radius', None),  # Provide a default if necessary
                    'index': moment_data['index'],
                    'game_clock': moment_data['game_clock'],
                    'shot_clock': moment_data['shot_clock'],
                }
                
                # Append a new Moment instance to the list for bulk creation
                moment_instances.append(Moment(**adjusted_moment_data))
    
    print("Performing bulk inserts of generated models...")     
    with transaction.atomic():
        if event_instances:
            Event.objects.bulk_create(event_instances)
        if moment_instances:
            Moment.objects.bulk_create(moment_instances)

    print("Creating/Inserting Candidate Models...")
    candidate_instances = []
    for _, candidate_row in candidate_df.iterrows():
        candidate_data = candidate_row.to_dict()
        
        # Prepare the kwargs for creating/updating the Candidate instance, mapping incoming data keys to model fields
        candidate_kwargs = {
            'candidate_id': candidate_data['candidate_id'],
            'event': Event.objects.get(event_id=candidate_data['event_id']),
            'classification_type': candidate_data['classification_type'],
            'manual_label': candidate_data['manual_label'],
            'period': candidate_data['period'],
            'game_clock': candidate_data['game_clock'],
            'shot_clock': candidate_data['shot_clock'],
            'player_a': Player.objects.filter(player_id=candidate_data['player_a']).first() if 'player_a' in candidate_data else None,
            'player_a_name': candidate_data.get('player_a_name', ''),
            'player_b': Player.objects.filter(player_id=candidate_data['player_b']).first() if 'player_b' in candidate_data else None,
            'player_b_name': candidate_data.get('player_b_name', ''),
            'notes': candidate_data.get('notes', '')
        }
        
        candidate_instances.append(Candidate(**candidate_kwargs))

    with transaction.atomic():
        if candidate_instances:
            Candidate.objects.bulk_create(candidate_instances)

    print("Finished processing game.")
