
import pandas as pd
import easygui
import sys

from data.preprocessing.utilities.DataUtil import DataUtil
from data.preprocessing.utilities.FeatureUtil import FeatureUtil
from data.preprocessing.utilities.ConstantsUtil import ConstantsUtil

from data.models import Game
from data.models import Team
from data.models import Player
from data.models import Event
from data.models import Moment
from data.models import Candidate

def run():
    print(Game.objects.all())

    candidates = Candidate.objects.none()
    events = Event.objects.filter(game=Game.objects.all()[0])
    for event in events:
        next_candidates = Candidate.objects.filter(event=event)
        candidates = candidates | next_candidates

    print(candidates.count())
    print(candidates[0])