import pandas as pd
from sklearn.decomposition import PCA

from ml_nba.classification.utilities.EncodingUtil import EncodingUtil
from ml_nba.classification.utilities.ConstantsUtil import ConstantsUtil
from ml_nba.models import CandidateFeatureVector

def perform_pca(n_components: float = .9):
    # TODO: allow for subset selection of candidates
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates)
    
    candidates_df.set_index('id', inplace=True)
    candidates_df.drop(columns=['candidate_id', 'classification'], inplace=True)

    candidates_df = EncodingUtil.basic_label_encode_cols(candidates_df, ConstantsUtil.BASIC_ENCODE_COLS)
    candidates_df = EncodingUtil.sort_position_cols_and_encode(candidates_df, ConstantsUtil.STRING_TUPLE_ENCODE_COLS)

    pca = PCA(n_components=n_components)
    pca.fit(candidates_df)
    
    return pca.components_