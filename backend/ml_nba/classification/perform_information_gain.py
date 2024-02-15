import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_classif

from ml_nba.models import CandidateFeatureVector
from ml_nba.classification.utilities.EncodingUtil import EncodingUtil
from ml_nba.classification.utilities.ConstantsUtil import ConstantsUtil

def perform_information_gain(iterations: int = 10):
    """
    Computes and visualizes the feature importances using mutual information gain over a specified number of iterations.

    This function fetches candidate data, preprocesses features using encoding utilities, computes feature importances using
    mutual information gain for each feature across the specified number of iterations, and aggregates the importances to determine
    the mean importance for each feature. It then plots these mean importances in a horizontal bar chart.

    Args:
        iterations (int, optional): The number of iterations to compute mutual information gain. Defaults to 10.

    Returns:
        Tuple[pd.Series, matplotlib.figure.Figure]: A tuple containing a pandas Series of the mean importances for each feature
        and a matplotlib figure object of the plotted mean importances. The pandas Series is indexed by the feature names.

    The function leverages the CandidateFeatureVector model to fetch candidate data, and utilizes custom encoding utilities
    to preprocess the features before computing the mutual information gain. This is particularly useful for evaluating the
    relevance of each feature in the dataset in relation to the target variable 'classification'.
    """
    # Fetch candidates and create DataFrame
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates).set_index('id')

    # Separate features and target variable
    y = candidates_df['classification']
    X = candidates_df.drop(columns=['candidate_id', 'classification'])

    # Preprocess features
    X_encoded = EncodingUtil.basic_label_encode_cols(X, ConstantsUtil.BASIC_ENCODE_COLS)
    X_encoded_sorted = EncodingUtil.sort_position_cols_and_encode(X_encoded, ConstantsUtil.STRING_TUPLE_ENCODE_COLS)

    # Initialize a list to hold the importances from each iteration
    feat_importances = []

    # Compute feature importances in each iteration
    for i in range(iterations):
        importances = mutual_info_classif(X_encoded_sorted.values, y)
        feat_importances.append(importances)

    # Aggregate the importances over all iterations
    feature_importance_df = pd.DataFrame(feat_importances, columns=X_encoded_sorted.columns)
    importance_means = feature_importance_df.mean()

    # Plot the mean importances
    fig, ax = plt.subplots()
    importance_means.plot(kind='barh', ax=ax)

    return importance_means, fig