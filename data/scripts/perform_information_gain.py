from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot  as plt

from data.classification.utilities.EncodingUtil import EncodingUtil
from data.classification.utilities.ConstantsUtil import ConstantsUtil

from data.models import CandidateFeatureVector\

def run():
    feat_importances = []
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates)
    candidates_df.set_index('id', inplace=True)
    for i in range(0,10):
        y = candidates_df['classification']
        X = candidates_df.copy()
        X.drop(columns=['candidate_id', 'classification'], inplace=True)

        X = EncodingUtil.basic_label_encode_cols(X, ConstantsUtil.BASIC_ENCODE_COLS)
        X = EncodingUtil.sort_position_cols_and_encode(X, ConstantsUtil.STRING_TUPLE_ENCODE_COLS)


        importances = mutual_info_classif(X.values, y)
        feat_importances.append(pd.Series(importances, X.columns))
    
    feature_df = pd.DataFrame(feat_importances)
    importance_means = feature_df.mean()
    
    importance_means.plot(kind='barh')
    plt.show()
    print(importance_means)
    