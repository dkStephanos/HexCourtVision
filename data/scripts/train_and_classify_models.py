import pandas as pd
import matplotlib.pyplot as plt
import math, sys, os, traceback
from django.forms.models import model_to_dict
from pandas.io.parsers import count_empty_vals

from data.preprocessing.utilities.DataUtil import DataUtil
from data.preprocessing.utilities.FeatureUtil import FeatureUtil
from data.preprocessing.utilities.GraphUtil import GraphUtil

from data.models import Game
from data.models import Player
from data.models import Event
from data.models import Moment
from data.models import Candidate
from data.models import CandidateFeatureVector


def run():
    candidates = CandidateFeatureVector.objects.all().values()
    print(len(candidates))
    candidates_df = pd.DataFrame(candidates)
    candidates_df.set_index('id', inplace=True)
    candidates_df.drop(columns=['candidate_id'], inplace=True)
    print(candidates_df)