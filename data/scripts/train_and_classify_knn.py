import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import check_matplotlib_support
import shap
from keras.datasets import imdb
from IPython.display import HTML,display

from data.classification.utilities.EncodingUtil import EncodingUtil
from data.classification.utilities.ConstantsUtil import ConstantsUtil
from data.classification.ML.KerasNN import KerasNN

from data.models import CandidateFeatureVector


def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates)
    candidates_df.set_index('id', inplace=True)
    candidates_df.drop(columns=['candidate_id'], inplace=True)

    candidates_df = EncodingUtil.basic_label_encode_cols(candidates_df, ConstantsUtil.BASIC_ENCODE_COLS)
    candidates_df = EncodingUtil.sort_position_cols_and_encode(candidates_df, ConstantsUtil.STRING_TUPLE_ENCODE_COLS)
    #candidates_df.drop(columns=ConstantsUtil.FEATURES_IGNORED_BY_INFORMATION_GAIN, inplace=True)

    X = candidates_df.drop(columns=['classification'])
    y = candidates_df['classification']

    knn = KerasNN(input_dim=len(X.columns))
    X_train, X_test, y_train, y_test = knn.fit_model(X,y,20)
    #knn.plot_training_validation()
    print(knn.get_classification_report(X_test, y_test))
    knn.get_accuracy_stats(X_test, y_test)

    #knn.plot_roc_curve()

    '''
    Feature ranking stuff with shap, not sure if it works, can't render stupid html 
    # init the JS visualization code
    shap.initjs()

    # we use the first 100 training examples as our background dataset to integrate over
    explainer = shap.DeepExplainer(knn.get_model(), X_train[:100])

    # explain the first 10 predictions
    # explaining each prediction requires 2 * background dataset size runs
    shap_values = explainer.shap_values(X_test[:10])

    # plot the explanation of the first prediction
    # Note the model is "multi-output" because it is rank-2 but only has one column
    shap.force_plot(explainer.expected_value[0], shap_values[0][0,:], X_test[0])
    '''