class ConstantsUtil:
    STATIC_PATH = "/app/static/ml_nba"
    RAW_DATA_PATH = STATIC_PATH + "/2016.NBA.Raw.SportVU.Game.Logs"
    CLEAN_DATA_PATH = STATIC_PATH + "/processed_games"
    EVENT_ANNOTATIONS_PATH = STATIC_PATH + "/event_annotations"

    HEADERS = [
        "team_id",
        "player_id",
        "x_loc",
        "y_loc",
        "radius",
        "index",
        "game_clock",
        "shot_clock",
        "event_id",
    ]

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
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151106MIAIND": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151106MILNYK": {
            "bad_events": [110],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151106PHICLE": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151110DALNOP": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151110LALMIA": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151211GSWBOS": {
            "bad_events": [],
            "moment_range": 7,
            "event_offset": 0,
        },
        "20151225LACLAL": {
            "bad_events": [212, 294, 296, 386],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151225NOPMIA": {
            "bad_events": [427],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151228ATLIND": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151228CLEPHX": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151228LALCHA": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151228PHIUTA": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151228SACGSW": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151228TORCHI": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151229ATLHOU": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151229CLEDEN": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151230DENPOR": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151230GSWDAL": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151230BKLORL": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151230LALBOS": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151230PHXSAS": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151230WASTOR": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151231LACNOP": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20151231PHXOKC": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160102BKLBOS": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160102HOUSAS": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160113ATLCHA": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160113MIALAC": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160113NOPSAC": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160113NYKBKL": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160113UTAPOR": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160115ATLMIL": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160115CHANOP": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160115DALCHI": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160115MIADEN": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160115MINOKC": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160115WASIND": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160118ORLATL": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160118PHINYK": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160120CHAOKC": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160120MIAWAS": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160121DETNOP": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160122CHIBOS": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160122LACNYK": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160122MIATOR": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160122MILHOU": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160123ATLPHX": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160123CHICLE": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160123DETDEN": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160123INDSAC": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
        "20160123LALPOR": {
            "bad_events": [23],
            "moment_range": 8,
            "event_offset": 1,
        },
        "20160123NYKCHA": {
            "bad_events": [],
            "moment_range": 8,
            "event_offset": 0,
        },
    }
