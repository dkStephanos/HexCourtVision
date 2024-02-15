import pandas as pd
from ml_nba.classification.utilities.EncodingUtil import EncodingUtil
from ml_nba.classification.utilities.ConstantsUtil import ConstantsUtil
from ml_nba.classification.ML.SVM import SVM

from ml_nba.models import CandidateFeatureVector

from genetic_selection import GeneticSelectionCV

def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates)
    candidates_df.set_index('id', inplace=True)
    candidates_df.drop(columns=['candidate_id'], inplace=True)

    candidates_df = EncodingUtil.encode_columns(candidates_df, ConstantsUtil.COLS_TO_ENCODE)

    svm = SVM(C=.75, kernel='poly')
    X_train, X_test, y_train, y_test = svm.split_test_data(candidates_df, .3, 'classification', True)
    svm.fit_and_predict(X_train, X_test, y_train)
    print(svm.get_confusion_matrix(y_test))
    print(svm.get_classification_report(y_test))

    estimator = svm.get_model()

    selector = GeneticSelectionCV(estimator,
                                  cv=5,
                                  verbose=1,
                                  scoring="accuracy",
                                  max_features=50,
                                  n_population=50,
                                  crossover_proba=0.5,
                                  mutation_proba=0.2,
                                  n_generations=40,
                                  crossover_independent_proba=0.5,
                                  mutation_independent_proba=0.05,
                                  tournament_size=3,
                                  n_gen_no_change=10,
                                  caching=True,
                                  n_jobs=-1)
    X, y = svm.get_data()
    selector = selector.fit(X, y)

    print(selector.support_)