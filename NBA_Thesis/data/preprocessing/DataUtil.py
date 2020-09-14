import numpy as np
import pandas as pd

class DataUtil:

    HEADERS = ["team_id", "player_id", "x_loc", "y_loc", 	
           "radius", "moment", "game_clock", "shot_clock"]	

    @staticmethod
    def load_game_df(path):
        game_df = pd.read_json(path)
        
        return game_df
