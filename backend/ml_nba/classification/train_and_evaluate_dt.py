import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from ml_nba.classification.models.DecisionTree import DecisionTree
from ml_nba.classification.utilities.EncodingUtil import EncodingUtil
from ml_nba.classification.utilities.ConstantsUtil import ConstantsUtil
from ml_nba.models import CandidateFeatureVector


def train_and_evaluate_decision_tree(criterion="entropy", test_size=0.3, shuffle=True, n_iterations=None):
    """
    Train and evaluate a decision tree classifier on the dataset obtained from CandidateFeatureVector objects.
    
    Args:
        criterion (str): The function to measure the quality of a split. Supported criteria are "gini" for the Gini impurity and "entropy" for the information gain.
        test_size (float): The proportion of the dataset to include in the test split.
        shuffle (bool): Whether or not to shuffle the data before splitting.
        n_iterations (int, optional): The number of iterations for averaging metrics. If provided, the function returns averaged metrics over n iterations.
        
    Returns:
        dict: A dictionary containing the model's confusion matrix, classification report, and optionally averaged metrics over n iterations.
    """
    # Fetch candidates and create DataFrame
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates).set_index('id')
    candidates_df.drop(columns=['candidate_id'], inplace=True)

    # Encoding categorical columns
    # Assuming EncodingUtil and ConstantsUtil are defined and applicable
    candidates_df = EncodingUtil.encode_columns(candidates_df, ConstantsUtil.COLS_TO_ENCODE)

    # Separating features and target
    X = candidates_df.drop(columns=['classification'])
    y = candidates_df['classification']
    
    # Splitting dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=shuffle)
    
    # Training Decision Tree
    dt_classifier = DecisionTree(criterion=criterion)
    dt_classifier.fit(X_train, y_train)
    
    # Predicting and Evaluating
    y_pred = dt_classifier.predict(X_test)
    results = {
        "confusion_matrix": confusion_matrix(y_test, y_pred),
        "classification_report": classification_report(y_test, y_pred, output_dict=True),
        
    }
    
    # Optionally calculate and return average metrics over n_iterations
    if n_iterations:
        # Assume svm_model.get_avg_metrics_for_n_iterations is implemented
        avg_metrics = dt_classifier.get_avg_metrics_for_n_iterations(n_iterations, test_size, shuffle)
        results['avg_metrics'] = avg_metrics
    
    return results
