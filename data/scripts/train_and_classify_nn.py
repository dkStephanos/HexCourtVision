import pandas as pd

from data.classification.utilities.EncodingUtil import EncodingUtil
from data.classification.utilities.ConstantsUtil import ConstantsUtil
from data.classification.ML.NeuralNetwork import NeuralNetwork

from data.models import CandidateFeatureVector


def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates)
    candidates_df.set_index('id', inplace=True)
    candidates_df.drop(columns=['candidate_id'], inplace=True)

    candidates_df = EncodingUtil.basic_label_encode_cols(candidates_df, ConstantsUtil.BASIC_ENCODE_COLS)
    candidates_df = EncodingUtil.sort_position_cols_and_encode(candidates_df, ConstantsUtil.STRING_TUPLE_ENCODE_COLS)

    NeuralNetwork.classify(candidates_df, .05, (512,256,128,64,32,16), 'relu', 'adam', .2, 'classification')
    NeuralNetwork.plot_roc_curve(candidates_df, .05, (512,256,128,64,32,16), 'relu', 'adam', .2, 'classification')
    NeuralNetwork.plot_loss_val_curve(candidates_df, .05, (512,256,128,64,32,16), 'relu', 'adam', .2, 'classification')

    #NeuralNetwork.testNIterations(candidates_df, .05, (512,256,128,64,32,16), 'relu', 'adam', .2, 'classification', 10)