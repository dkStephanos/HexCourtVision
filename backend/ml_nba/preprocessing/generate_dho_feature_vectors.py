from ml_nba.models import Game, Event, Candidate, CandidateFeatureVector
from ml_nba.preprocessing.utilities.FeatureUtil import FeatureUtil


def generate_dho_feature_vectors(game_key):
    game = Game.objects.get(game_id=game_key)
    events = Event.objects.filter(game=game)
    
    for event in events:
        candidates = Candidate.objects.filter(event=event).values()
        for target_candidate in candidates:
            vector = FeatureUtil.generate_dribble_handoff_feature_vector(target_candidate)
            CandidateFeatureVector.objects.update_or_create(**vector)

