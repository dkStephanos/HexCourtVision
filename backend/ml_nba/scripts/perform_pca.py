from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot  as plt
import numpy as np

from backend.classification.utilities.EncodingUtil import EncodingUtil
from backend.classification.utilities.ConstantsUtil import ConstantsUtil
from backend.classification.ML.DecisionTree import DecisionTree

from backend.ml_nba.models import CandidateFeatureVector\

def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates)
    candidates_df.set_index('id', inplace=True)
    candidates_df.drop(columns=['candidate_id', 'classification'], inplace=True)

    candidates_df = EncodingUtil.basic_label_encode_cols(candidates_df, ConstantsUtil.BASIC_ENCODE_COLS)
    candidates_df = EncodingUtil.sort_position_cols_and_encode(candidates_df, ConstantsUtil.STRING_TUPLE_ENCODE_COLS)

    pca = PCA(.9)
    pca.fit(candidates_df)
    print(pca.components_)