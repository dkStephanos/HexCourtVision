import pandas as pd

from data.classification.utilities.EncodingUtil import EncodingUtil
from data.classification.utilities.DataUtil import DataUtil
from data.classification.utilities.ConstantsUtil import ConstantsUtil
from data.classification.ML.NeuralNetwork import NeuralNetwork

from data.models import CandidateFeatureVector
from data.models import Candidate
from data.models import Player
from data.models import Team

def run():
    candidates = CandidateFeatureVector.objects.all().values()
    filtered_candidates = []
    for candidate in candidates:
        player_id = Candidate.objects.values().get(candidate_id=candidate['candidate_id'])['player_a_id']
        team_id = Player.objects.values().get(player_id=player_id)['team_id']
        if Team.objects.values().get(team_id=team_id)['abreviation'] == 'BOS':
            filtered_candidates.append(candidate)

    print("Success: ", len(candidates), len(filtered_candidates))

    candidates_df = DataUtil.get_candidates_df(filtered_candidates)

    #NeuralNetwork.classify(candidates_df, .05, (512,256,128,64,32,16), 'relu', 'adam', .2, 'classification')
    NeuralNetwork.plot_roc_curve(candidates_df, .05, (512,256,128,64,32,16), 'relu', 'adam', .2, 'classification')
    #NeuralNetwork.plot_loss_val_curve(candidates_df, .05, (512,256,128,64,32,16), 'relu', 'adam', .2, 'classification')

    results = NeuralNetwork.testNIterations(candidates_df, .05, (256,128,64,32,16), 'relu', 'adam', .3, 'classification', 10)
    print(results)