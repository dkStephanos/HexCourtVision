import os, sys, traceback
from django.db import transaction
from ml_nba.models import Game, Event, Candidate, CandidateFeatureVector
from ml_nba.preprocessing.utilities.FeatureUtil import FeatureUtil


def generate_dho_feature_vectors(game_key):
    game = Game.objects.get(game_id=game_key)
    events = Event.objects.filter(game=game)
    
    num_failed_candidates = 0
    num_successful_candidates = 0
    issue_candidates = []
    with transaction.atomic():
        for event in events:
            candidates = Candidate.objects.filter(event=event).values()
            for target_candidate in candidates:
                try:
                    print(f'Generating vector for candidate: {target_candidate["candidate_id"]}')
                    vector = FeatureUtil.generate_dribble_handoff_feature_vector(target_candidate)
                except Exception as e:
                    print(f"Issue at candidate: {target_candidate['candidate_id']}")
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname)
                    print(traceback.print_tb(exc_tb))
                    issue_candidates.append(target_candidate)
                    num_failed_candidates += 1
                    continue
                CandidateFeatureVector.objects.update_or_create(**vector)
                num_successful_candidates += 1

    print(f"Total successful candidates: {num_successful_candidates}\nTotal failed candidates: {num_failed_candidates}")