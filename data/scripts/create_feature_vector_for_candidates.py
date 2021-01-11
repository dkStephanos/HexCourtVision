
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
    # Collects all games -- Add loop later
    print(Game.objects.all())

    # Collects all candidates for a given event -- Add loop later
    candidates = []
    events = Event.objects.filter(game=Game.objects.all()[0])
    for event in events:
        next_candidates = Candidate.objects.filter(event=event).values()
        candidates += list(next_candidates)

    # Collects moments for single candidate -- Add loop later
    target_candidate = candidates[0]
    print(target_candidate)
    print(Player.objects.values().get(player_id=target_candidate['player_a_id']))
    moments = pd.DataFrame(list(Moment.objects.filter(event_id=target_candidate['event_id']).values()))
    print(moments.head())

    # Trim the moments data around the pass

    # Create the feature vector
    feature_vector = {
        'cutter_archetype': Player.objects.get(player_id=target_candidate['player_a_id']).position,
        'screener_archetype': Player.objects.get(player_id=target_candidate['player_b_id']).position,
    }

    print(feature_vector)