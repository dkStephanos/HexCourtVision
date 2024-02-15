import pandas as pd

from ml_nba.classification.utilities.EncodingUtil import EncodingUtil
from ml_nba.classification.utilities.ConstantsUtil import ConstantsUtil
from ml_nba.classification.ML.GaussianNB import GaussianNB

from ml_nba.models import CandidateFeatureVector


def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates)
    candidates_df.set_index('id', inplace=True)
    candidates_df.drop(columns=['candidate_id'], inplace=True)

    candidates_df = EncodingUtil.encode_columns(candidates_df, ConstantsUtil.COLS_TO_ENCODE)

    gnb = GaussianNB()
    gnb.set_data(candidates_df, 'classification')
    X_train, X_test, y_train, y_test = gnb.split_test_data(.3, True)

    gnb.get_roc_curve(X_train, X_test, y_train, y_test)

    gnb.fit_and_predict(X_train, X_test, y_train)
    print(gnb.get_confusion_matrix(y_test))
    print(gnb.get_classification_report(y_test))

    gnb.get_learning_curve()

    print(gnb.get_avg_metrics_for_n_iterations(10, .3, True))