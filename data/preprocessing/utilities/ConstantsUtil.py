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
        "20151211GSWBOS": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.11.2015.GSW.at.BOS/0021500336.json",
        "20151225LACLAL": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.25.2015.LAC.at.LAL/0021500440.json",
        "20151230DENPOR": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.30.2015.DEN.at.POR/0021500482.json",
        "20151230GSWDAL": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.30.2015.GSW.at.DAL/0021500480.json",
        "20151231PHXOKC": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/12.31.2015.PHX.at.OKC/0021500488.json",
        "20151106MILNYK": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/11.06.2015.MIL.at.NYK/0021500079.json"
    }

    events = {
        "20151211GSWBOS": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151211GSWBOS.csv",
        "20151225LACLAL": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151225LACLAL.csv",
        "20151230DENPOR": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151230DENPOR.csv",
        "20151230GSWDAL": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151230GSWDAL.csv",
        "20151231PHXOKC": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151231PHXOKC.csv",
        "20151106MILNYK": r"C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/events-20151106MILNYK.csv"
    }
    
    bad_events = {
        "20151211GSWBOS": [],
        "20151225LACLAL": [212, 294, 296, 386],
        "20151230DENPOR": [212, 440, 455],
        "20151230GSWDAL": [],
        "20151231PHXOKC": [],
        "20151106MILNYK": [110],
    }

    moment_ranges = {
        "20151211GSWBOS": 7,
        "20151225LACLAL": 8,
        "20151230DENPOR": 8,
        "20151230GSWDAL": 8,
        "20151231PHXOKC": 8,
        "20151106MILNYK": 8, 
    }
