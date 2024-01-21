import pandas as pd

from backend.classification.utilities.EncodingUtil import EncodingUtil
from backend.classification.utilities.DataUtil import DataUtil
from backend.classification.utilities.ConstantsUtil import ConstantsUtil
from backend.classification.ML.NeuralNetwork import NeuralNetwork

from backend.models import CandidateFeatureVector
from backend.models import Candidate

def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = DataUtil.get_candidates_df(candidates)

    #NeuralNetwork.classify(candidates_df, .05, (512,256,128,64,32,16), 'relu', 'adam', .2, 'classification')
    NeuralNetwork.plot_roc_curve(candidates_df, .85, (512,256,128,64,32,16), 'relu', 'adam', .2, 'classification')
    NeuralNetwork.plot_loss_val_curve(candidates_df, .85, (512,256,128,64,32,16), 'relu', 'adam', .2, 'classification')

    results = NeuralNetwork.testNIterations(candidates_df, .85, (256,128,64,32,16), 'relu', 'adam', .2, 'classification', 1000)
    print(results)