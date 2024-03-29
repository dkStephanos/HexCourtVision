from django.db import transaction
from ml_nba.models import Game, Event, Moment, Candidate, Team, Player
from ml_nba.preprocessing.utilities.DataLoader import DataLoader
from ml_nba.preprocessing.utilities.DatabaseUtil import DatabaseUtil


def persist_processed_game(game_id: str, overwrite: bool = True):
    """
    Processes and persists all relevant data for a single NBA game into the database.

    This function takes a game key, loads raw and processed data files associated with that game,
    processes the data to extract game, team, player, event, moment, and candidate information,
    and updates or creates corresponding records in the database. Uses django transactions to
    ensure atomic operations and rollback any changes if we run into an exception during persistence.

    Parameters:
    - game_id (str): A unique identifier for the game being processed.

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
    
    
    print("Loading data files")
    game_df = DataLoader.load_raw_game(game_id)
    annotation_df = DataLoader.load_game_events(game_id)
    combined_event_df = DataLoader.load_processed_game(game_id)
    candidate_df = DataLoader.load_game_candidates(game_id)

    print("Processing Data Files")
    game_data = DataLoader.get_game_data(game_df, annotation_df)
    teams_data = DataLoader.get_teams_data(game_df)
    players_data = DataLoader.get_players_data(game_df)
    print(teams_data, players_data)
    print("Creating or Updating Game/Team/Player models")
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
            ["team_id", "last_name", "first_name", "jersey_number", "position"],
        )

    print("Collecting and Creating Event and Moment Data")
    events, moments = DataLoader.collect_events_and_moments(
        combined_event_df, candidate_df
    )

    with transaction.atomic():
        for event_data in events:
            event, _ = Event.objects.get_or_create(**event_data)

            # Assume moments_data is structured for bulk creation
            Moment.objects.bulk_create(
                [
                    Moment(**moment_data, event=event)
                    for moment_data in moments[event_data["event_id"]]
                ]
            )

    print("Creating Candidate Models")
    with transaction.atomic():
        for candidate_data in candidate_df.itertuples(index=False):
            Candidate.objects.get_or_create(**dict(candidate_data))

    print("Finished processing game")
