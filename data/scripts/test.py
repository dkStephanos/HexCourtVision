import pandas as pd

from data.classification.utilities.EncodingUtil import EncodingUtil
from data.classification.utilities.DataUtil import DataUtil
from data.classification.utilities.ConstantsUtil import ConstantsUtil
from data.classification.ML.SVM import SVM

from data.models import CandidateFeatureVector
from data.models import Candidate
from data.models import Player
from data.models import Team

def run():
    candidates = CandidateFeatureVector.objects.all().values()
    filtered_candidates = []
    for candidate in candidates:
        player_id = Candidate.objects.values().get(candidate_id=candidate['candidate_id'])['player_a_id']
        team_id = Player.objects.values().get(player_id=player_id)['team_id']
        if Team.objects.values().get(team_id=team_id)['abreviation'] == 'GSW':
            filtered_candidates.append(candidate)

    print("Success: ", len(candidates), len(filtered_candidates))

    candidates_df = DataUtil.get_candidates_df(filtered_candidates)

    svm = SVM(C=.75, kernel='poly')
    svm.set_data(candidates_df, 'classification')
    X_train, X_test, y_train, y_test = svm.split_test_data(.3, True)
        
    #svm.get_roc_curve(X_train, X_test, y_train, y_test)

    svm.fit_and_predict(X_train, X_test, y_train)
    print(svm.get_classification_report(y_test))

    #svm.get_learning_curve()
    #  Not working correctly... svm.get_validation_curve()

    metrics = svm.get_avg_metrics_for_n_iterations(10, .3, True)
    print(metrics)