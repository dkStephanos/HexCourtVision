import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from data.classification.utilities.EncodingUtil import EncodingUtil
from data.classification.utilities.ConstantsUtil import ConstantsUtil
from data.classification.ML.KerasNN import KerasNN

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

    knn = KerasNN()
    knn.fit_model(X,y)
    #print(knn.get_classification_report())

    knn.plot_roc_curve()