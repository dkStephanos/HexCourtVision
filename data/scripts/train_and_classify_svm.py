import pandas as pd

from data.classification.utilities.EncodingUtil import EncodingUtil
from data.classification.utilities.ConstantsUtil import ConstantsUtil
from data.classification.ML.SVM import SVM

from data.models import CandidateFeatureVector


def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates)
    candidates_df.set_index('id', inplace=True)
    candidates_df.drop(columns=['candidate_id'], inplace=True)

    candidates_df = EncodingUtil.basic_label_encode_cols(candidates_df, ConstantsUtil.BASIC_ENCODE_COLS)
    candidates_df = EncodingUtil.sort_position_cols_and_encode(candidates_df, ConstantsUtil.STRING_TUPLE_ENCODE_COLS)

    svm = SVM(C=.75, kernel='poly')
    X_train, X_test, y_train, y_test = svm.split_test_data(candidates_df, .3, 'classification', True)
    svm.fit_and_predict(X_train, X_test, y_train)
    print(svm.get_confusion_matrix(y_test))
    print(svm.get_classification_report(y_test))
