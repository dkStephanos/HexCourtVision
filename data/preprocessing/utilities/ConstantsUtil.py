class ConstantsUtil:
    
    HEADERS = ["team_id", "player_id", "x_loc", "y_loc", 	
           "radius", "moment", "game_clock", "shot_clock", "event_id"]

    COLOR_DICT = {
        1610612737: "#E13A3E",
        1610612738: "#008348",
        1610612751: "#061922",
        1610612766: "#1D1160",
        1610612741: "#CE1141",
        1610612739: "#860038",
        1610612742: "#007DC5",
        1610612743: "#4D90CD",
        1610612765: "#006BB6",
        1610612744: "#FDB927",
        1610612745: "#CE1141",
        1610612754: "#00275D",
        1610612746: "#ED174C",
        1610612747: "#552582",
        1610612763: "#0F586C",
        1610612748: "#98002E",
        1610612749: "#00471B",
        1610612750: "#005083",
        1610612740: "#002B5C",
        1610612752: "#006BB6",
        1610612760: "#007DC3",
        1610612753: "#007DC5",
        1610612755: "#006BB6",
        1610612756: "#1D1160",
        1610612757: "#E03A3E",
        1610612758: "#724C9F",
        1610612759: "#BAC3C9",
        1610612761: "#CE1141",
        1610612762: "#00471B",
        1610612764: "#002B5C",
    }

    games = {
        "20151029MEMIND": {
            'raw_data': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/10.29.2015.MEM.at.IND/0021500018.json",
            'events': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151029MEMIND.csv",
            'bad_events': [],
            'moment_range': 8
        },
        "20151106MIAIND": {
            'raw_data': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/11.06.2015.MIA.at.IND/0021500080.json",
            'events': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151106MIAIND.csv",
            'bad_events': [],
            'moment_range': 8,
        },
        "20151106MILNYK": {
            'raw_data': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/11.06.2015.MIL.at.NYK/0021500079.json",
            'events': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151106MILNYK.csv",
            'bad_events': [110],
            'moment_range': 8,
        },
        "20151106PHICLE": {
            'raw_data': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/11.06.2015.PHI.at.CLE/0021500078.json",
            'events': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151106PHICLE.csv",
            'bad_events': [],
            'moment_range': 8,
        },
        "20151110DALNOP": {
            'raw_data': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/11.10.2015.DAL.at.NOP/0021500112.json",
            'events': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151110DALNOP.csv",
            'bad_events': [],
            'moment_range': 8,
        },
        "20151110LALMIA": {
            'raw_data': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/11.10.2015.LAL.at.MIA/0021500108.json",
            'events': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151110LALMIA.csv",
            'bad_events': [],
            'moment_range': 8,
        },
        "20151110LALMIA": {
            'raw_data': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/11.10.2015.LAL.at.MIA/0021500108.json",
            'events': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-.csv",
            'bad_events': [],
            'moment_range': 8,
        },

        "20151211GSWBOS": {
            'raw_data': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.11.2015.GSW.at.BOS/0021500336.json",
            'events': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151211GSWBOS.csv",
            'bad_events': [],
            'moment_range': 7,
        },
        "20151225LACLAL": {
            'raw_data': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.25.2015.LAC.at.LAL/0021500440.json",
            'events': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151225LACLAL.csv",
            'bad_events': [212, 294, 296, 386],
            'moment_range': 8,
        },
        "20151231PHXOKC": {
            'raw_data': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.31.2015.PHX.at.OKC/0021500488.json",
            'events': r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151231PHXOKC.csv",
            'bad_events': [],
            'moment_range': 8,
        },
    }