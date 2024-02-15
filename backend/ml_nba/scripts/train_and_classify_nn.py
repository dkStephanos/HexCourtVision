import pandas as pd

from ml_nba.classification.utilities.EncodingUtil import EncodingUtil
from ml_nba.classification.utilities.DataUtil import DataUtil
from ml_nba.classification.utilities.ConstantsUtil import ConstantsUtil
from ml_nba.classification.models.NeuralNetwork import NeuralNetwork

from ml_nba.models import CandidateFeatureVector
from ml_nba.models import Candidate

def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = DataUtil.get_candidates_df(candidates)

    #NeuralNetwork.classify(candidates_df, .05, (512,256,128,64,32,16), 'relu', 'adam', .2, 'classification')
    NeuralNetwork.plot_roc_curve(candidates_df, .85, (512,256,128,64,32,16), 'relu', 'adam', .2, 'classification')
    NeuralNetwork.plot_loss_val_curve(candidates_df, .85, (512,256,128,64,32,16), 'relu', 'adam', .2, 'classification')

    results = NeuralNetwork.testNIterations(candidates_df, .85, (256,128,64,32,16), 'relu', 'adam', .2, 'classification', 1000)
    print(results)