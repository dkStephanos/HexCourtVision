# scripts/process_game.py

import pandas as pd;

from data.preprocessing.utilities.DataUtil import DataUtil
from data.preprocessing.utilities.FeatureUtil import FeatureUtil
from data.preprocessing.utilities.GraphUtil import GraphUtil

from data.models import Game
from data.models import Team

def run():
    game_df = DataUtil.load_game_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\game_raw_data\12.11.2015.GSW.at.BOS\0021500336.json")
    annotation_df = DataUtil.load_annotation_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\event_annotations\events-20151211GSWBOS.csv")

    game_data = DataUtil.get_game_data(game_df, annotation_df)
    teams = DataUtil.get_teams_data(game_df)
    Team.objects.create(**teams[0])
    Team.objects.create(**teams[1])
    print(game_data)
    print(teams[0])
    print(teams[1])
    #game = Game(**game_data)