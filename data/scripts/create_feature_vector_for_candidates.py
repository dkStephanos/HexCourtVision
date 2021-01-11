
import pandas as pd
import easygui
import sys

from utilities.DataUtil import DataUtil
from utilities.FeatureUtil import FeatureUtil
from utilities.ConstantsUtil import ConstantsUtil

from ..models import Game


print(Game.objects.all()[0])