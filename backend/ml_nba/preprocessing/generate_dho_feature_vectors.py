import sys, os, traceback
from ml_nba.models import Game, Event, Candidate, CandidateFeatureVector
from ml_nba.preprocessing.utilities.FeatureUtil import FeatureUtil


def generate_dho_feature_vectors(game_key):
    num_failed_candidates = 0
    num_successful_candidates = 0
    issue_candidates = []
    game = Game.objects.get(game_id=game_key)
    events = Event.objects.filter(game=game)
    for event in events:
        next_candidates = Candidate.objects.filter(event=event).values()
        for target_candidate in next_candidates:
            has_vector = CandidateFeatureVector.objects.filter(candidate=target_candidate).exists()
            if not has_vector:
                try:
                    vector = FeatureUtil.generate_dribble_handoff_feature_vector(target_candidate)
                    CandidateFeatureVector.objects.update_or_create(**vector)
                    num_successful_candidates += 1
                except Exception as e:
                    print(f"Issue at candidate: {target_candidate['candidate_id']}")
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname)
                    print(traceback.print_tb(exc_tb))
                    issue_candidates.append(target_candidate)
                    num_failed_candidates += 1

    output = f"Total successful candidates: {num_successful_candidates}\nTotal failed candidates: {num_failed_candidates}" 
    print(output)
    