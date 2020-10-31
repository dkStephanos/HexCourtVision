# Collection of methods to preprocess data, instantiate db entries, select candidates, train models, classify cases, etc.

import pandas as pd;
from preprocessing.utilities.DataUtil import DataUtil
from preprocessing.utilities.FeatureUtil import FeatureUtil
from preprocessing.utilities.GraphUtil import GraphUtil

def process_game(game_path, event_path):
    game_df = DataUtil.load_game_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\game_raw_data\12.11.2015.GSW.at.BOS\0021500336.json")
    annotation_df = DataUtil.load_annotation_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\event_annotations\events-20151211GSWBOS.csv")

    print("GameDF Shape: ")
    print(game_df.shape)
    print("AnnotationDF Shape: ")
    print(annotation_df.shape)

process_game("testing","testing")