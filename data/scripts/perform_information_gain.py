from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot  as plt

from data.classification.utilities.EncodingUtil import EncodingUtil
from data.classification.utilities.ConstantsUtil import ConstantsUtil

from data.models import CandidateFeatureVector\

def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates)
    candidates_df.set_index('id', inplace=True)
    y = candidates_df['classification']
    X = candidates_df.copy()
    X.drop(columns=['candidate_id', 'classification'], inplace=True)

    X = EncodingUtil.basic_label_encode_cols(X, ConstantsUtil.BASIC_ENCODE_COLS)
    X = EncodingUtil.sort_position_cols_and_encode(X, ConstantsUtil.STRING_TUPLE_ENCODE_COLS)


    importances = mutual_info_classif(X.values, y)
    feat_importances = pd.Series(importances, X.columns)
    feat_importances.plot(kind='barh', color='teal')
    plt.show()