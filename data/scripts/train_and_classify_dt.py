import pandas as pd
from sklearn.model_selection import train_test_split

from data.classification.utilities.EncodingUtil import EncodingUtil
from data.classification.utilities.ConstantsUtil import ConstantsUtil
from data.classification.ML.DecisionTree import DecisionTree

from data.models import CandidateFeatureVector


def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates)
    candidates_df.set_index('id', inplace=True)
    candidates_df.drop(columns=['candidate_id'], inplace=True)

    candidates_df = EncodingUtil.basic_label_encode_cols(candidates_df, ConstantsUtil.BASIC_ENCODE_COLS)
    candidates_df = EncodingUtil.sort_position_cols_and_encode(candidates_df, ConstantsUtil.STRING_TUPLE_ENCODE_COLS)

    X = candidates_df.drop(columns=['classification'])
    y = candidates_df['classification']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    dt = DecisionTree(criterion='gini')
    dt.fit_and_predict(X_train, X_test, y_train)
    print(dt.get_confusion_matrix(y_test))
    print(dt.get_classification_report(y_test))
