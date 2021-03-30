import pandas as pd

from data.classification.utilities.EncodingUtil import EncodingUtil
from data.classification.utilities.DataUtil import DataUtil
from data.classification.utilities.ConstantsUtil import ConstantsUtil
from data.classification.ML.NeuralNetwork import NeuralNetwork

from data.models import CandidateFeatureVector
from data.models import Candidate

def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = DataUtil.get_candidates_df(candidates)

    #NeuralNetwork.classify(candidates_df, .05, (512,256,128,64,32,16), 'relu', 'adam', .2, 'classification')
    #NeuralNetwork.plot_roc_curve(candidates_df, .05, (512,256,128,64,32,16), 'relu', 'adam', .2, 'classification')
    NeuralNetwork.plot_loss_val_curve(candidates_df, .05, (512,256,128,64,32,16), 'relu', 'adam', .2, 'classification')

    #results = NeuralNetwork.testNIterations(candidates_df, 1, (256,128,64,32,16), 'relu', 'adam', .2, 'classification', 1000)
    #print(results)