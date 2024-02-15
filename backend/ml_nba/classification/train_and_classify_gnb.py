import pandas as pd
from ml_nba.classification.utilities.EncodingUtil import EncodingUtil
from ml_nba.classification.utilities.ConstantsUtil import ConstantsUtil
from ml_nba.classification.models.GaussianNB import GaussianNB
from ml_nba.models import CandidateFeatureVector

def run_gaussian_nb_analysis():
    """
    Fetches candidate data, preprocesses it, trains a Gaussian Naive Bayes model, and evaluates it.
    
    Returns:
        A dictionary containing evaluation metrics and figures for the model.
    """
    # Fetch and preprocess candidate data
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates).set_index('id').drop(columns=['candidate_id'])
    candidates_df = EncodingUtil.encode_columns(candidates_df, ConstantsUtil.COLS_TO_ENCODE)

    # Initialize the GaussianNB model
    gnb = GaussianNB()
    gnb.set_data(candidates_df, 'classification')

    # Split data and train the model
    X_train, X_test, y_train, y_test = gnb.split_test_data(0.3, True)
    gnb.fit_and_predict(X_train, X_test, y_train)

    # Evaluate the model
    roc_curve_fig = gnb.get_roc_curve(X_train, X_test, y_train, y_test)
    confusion_matrix = gnb.get_confusion_matrix(y_test)
    classification_report = gnb.get_classification_report(y_test)
    learning_curve_fig = gnb.get_learning_curve()
    avg_metrics = gnb.get_avg_metrics_for_n_iterations(10, 0.3, True)

    # Package results
    results = {
        "confusion_matrix": confusion_matrix,
        "classification_report": classification_report,
        "roc_curve_fig": roc_curve_fig,
        "learning_curve_fig": learning_curve_fig,
        "average_metrics_over_n_iterations": avg_metrics
    }

    return results
