from ml_nba.classification.utilities.DataUtil import DataUtil
from ml_nba.classification.models.NeuralNetwork import NeuralNetwork
from ml_nba.models import CandidateFeatureVector

def run_neural_network_analysis(
    test_size=0.85,
    layers=(512, 256, 128, 64, 32, 16),
    activation='relu',
    optimizer='adam',
    validation_split=0.2,
    target_col='classification',
    n_iterations=1000
):
    """
    Runs neural network analysis including classification, ROC curve plotting,
    loss and validation curve plotting, and testing over N iterations.

    Args:
    - test_size (float): Proportion of the data to use for testing.
    - layers (tuple): Tuple specifying the number of neurons in each layer.
    - activation (str): Activation function to use.
    - optimizer (str): Optimizer to use.
    - validation_split (float): Proportion of data to use for validation.
    - target_col (str): Name of the target column.
    - n_iterations (int): Number of iterations for testing.

    Returns:
    - dict: A dictionary containing the results from the neural network analysis.
    """
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = DataUtil.get_candidates_df(candidates)

    # Assuming NeuralNetwork class methods are updated to return figures/results instead of showing or printing them directly
    roc_curve_fig = NeuralNetwork.plot_roc_curve(
        candidates_df, test_size, layers, activation, optimizer, validation_split, target_col
    )
    loss_val_curve_fig = NeuralNetwork.plot_loss_val_curve(
        candidates_df, test_size, layers, activation, optimizer, validation_split, target_col
    )
    results = NeuralNetwork.testNIterations(
        candidates_df, test_size, layers, activation, optimizer, validation_split, target_col, n_iterations
    )

    return {
        "roc_curve_fig": roc_curve_fig,
        "loss_val_curve_fig": loss_val_curve_fig,
        "test_iterations_results": results
    }