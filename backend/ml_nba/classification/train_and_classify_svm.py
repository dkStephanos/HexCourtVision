from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from ml_nba.classification.models.SVM import SVM
from ml_nba.classification.utilities.EncodingUtil import EncodingUtil
from ml_nba.classification.utilities.ConstantsUtil import ConstantsUtil
from ml_nba.classification.utilities.DataUtil import DataUtil
from ml_nba.models import CandidateFeatureVector

def train_and_evaluate_svm(C=0.75, kernel='poly', test_size=0.3, shuffle=True, n_iterations=None):
    """
    Train and evaluate an SVM classifier on the dataset obtained from CandidateFeatureVector objects, 
    including necessary preprocessing steps such as encoding categorical variables.
    
    Args:
        C (float): Regularization parameter. The strength of the regularization is inversely proportional to C.
        kernel (str): Specifies the kernel type to be used in the algorithm.
        test_size (float): The proportion of the dataset to include in the test split.
        shuffle (bool): Whether or not to shuffle the data before splitting.
        n_iterations (int, optional): The number of iterations for averaging metrics. If provided, the function returns averaged metrics over n iterations.
        
    Returns:
        dict: A dictionary containing the model's classification report and optionally averaged metrics over n iterations.
    """
    # Fetch candidates and create DataFrame using a utility function for consistency
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = DataUtil.get_candidates_df(candidates)
    
    # Encode categorical columns if DataUtil.get_candidates_df hasn't already done so
    candidates_df = EncodingUtil.encode_columns(candidates_df, ConstantsUtil.COLS_TO_ENCODE)

    # Assuming DataUtil.get_candidates_df already handles setting index and encoding
    X = candidates_df.drop(columns=['classification'])
    y = candidates_df['classification']
    
    # Splitting dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=shuffle)
    
    # Training SVM
    svm_model = SVM(C=C, kernel=kernel)  # Adjust based on your SVM wrapper's implementation
    svm_model.fit(X_train, y_train)
    
    # Predicting and Evaluating
    y_pred = svm_model.predict(X_test)
    classification_rep = classification_report(y_test, y_pred, output_dict=True)
    
    results = {
        "classification_report": classification_rep,
        # Include ROC curve data, learning curve data, validation curve data as needed
    }
    
    # Optionally calculate and return average metrics over n_iterations
    if n_iterations:
        # Assume svm_model.get_avg_metrics_for_n_iterations is implemented
        avg_metrics = svm_model.get_avg_metrics_for_n_iterations(n_iterations, test_size, shuffle)
        results['avg_metrics'] = avg_metrics
    
    return results