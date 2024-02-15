import pandas as pd
from ml_nba.classification.utilities.EncodingUtil import EncodingUtil
from ml_nba.classification.utilities.DataUtil import DataUtil
from ml_nba.classification.utilities.ConstantsUtil import ConstantsUtil
from ml_nba.classification.models.KerasNN import KerasNN

from ml_nba.models import CandidateFeatureVector

def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates = DataUtil.remove_fake_candidates(candidates)    
    candidates_df = pd.DataFrame(candidates)
    candidates_df.set_index('id', inplace=True)
    candidates_df.drop(columns=['candidate_id'], inplace=True)

    candidates_df = EncodingUtil.encode_columns(candidates_df, ConstantsUtil.COLS_TO_ENCODE)
    candidates_df.drop(columns=ConstantsUtil.FEATURES_IGNORED_BY_INFORMATION_GAIN, inplace=True)

    X = candidates_df.drop(columns=['classification'])
    y = candidates_df['classification']

    knn = KerasNN(input_dim=len(X.columns))
    X_train, X_test, y_train, y_test = knn.fit_model(X,y,120,.3,.2)
    knn.plot_training_validation()
    knn.plot_roc_curve()
    print(knn.get_classification_report(X_test, y_test))
    knn.get_accuracy_stats(X_test, y_test)

    results = knn.test_n_iterations(X,y,120,.3,.2,10)
    print(results)
