import pandas as pd
from sklearn.decomposition import PCA

from ml_nba.classification.utilities.EncodingUtil import EncodingUtil
from ml_nba.classification.utilities.ConstantsUtil import ConstantsUtil
from ml_nba.models import CandidateFeatureVector

def perform_pca(n_components: float = .9):
    """
    Performs Principal Component Analysis (PCA) on the dataset obtained from CandidateFeatureVector objects.

    This function fetches data for all candidates, preprocesses the features by encoding categorical variables, and
    then applies PCA to reduce the dimensionality of the data based on the specified number of components or explained variance ratio.

    Args:
        n_components (float, optional): Number of components to keep if < 1, indicating the amount of variance
        to be preserved. If >= 1, it specifies the exact number of components to be returned. Defaults to 0.9.

    Returns:
        numpy.ndarray: The principal components extracted from the dataset.

    Note:
        - Future versions will allow for subset selection of candidates.
        - The function currently drops 'candidate_id' and 'classification' columns and assumes they are not relevant for PCA.
    """
    # Fetch candidates and create DataFrame
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates).set_index('id')

    # Drop columns not relevant for PCA and preprocess features
    candidates_df = candidates_df.drop(columns=['candidate_id', 'classification'])
    candidates_df = EncodingUtil.encode_columns(candidates_df, ConstantsUtil.COLS_TO_ENCODE)

    # Apply PCA
    pca = PCA(n_components=n_components)
    pca.fit(candidates_df)
    
    return pca.components_