STATIC_PATH = "/app/backend/static/ml_nba"

class ConstantsUtil:
        
    HEADERS = ["team_id", "player_id", "x_loc", "y_loc", 	
           "radius", "index", "game_clock", "shot_clock", "event_id"]

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
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/10.29.2015.MEM.at.IND/0021500018.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151029MEMIND.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151106MIAIND": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/11.06.2015.MIA.at.IND/0021500080.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151106MIAIND.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151106MILNYK": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/11.06.2015.MIL.at.NYK/0021500079.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151106MILNYK.csv",
            'bad_events': [110],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151106PHICLE": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/11.06.2015.PHI.at.CLE/0021500078.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151106PHICLE.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151110DALNOP": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/11.10.2015.DAL.at.NOP/0021500112.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151110DALNOP.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151110LALMIA": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/11.10.2015.LAL.at.MIA/0021500108.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151110LALMIA.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151211GSWBOS": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.11.2015.GSW.at.BOS/0021500336.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151211GSWBOS.csv",
            'bad_events': [],
            'moment_range': 7,
            'event_offset': 0,
        },
        "20151225LACLAL": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.25.2015.LAC.at.LAL/0021500440.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151225LACLAL.csv",
            'bad_events': [212, 294, 296, 386],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151225NOPMIA": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.25.2015.NOP.at.MIA/0021500436.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151225NOPMIA.csv",
            'bad_events': [427],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151228ATLIND": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.28.2015.ATL.at.IND/0021500459.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151228ATLIND.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151228CLEPHX": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.28.2015.CLE.at.PHX/0021500466.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151228CLEPHX.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151228LALCHA": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.28.2015.LAL.at.CHA/0021500458.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151228LALCHA.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151228PHIUTA": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.28.2015.PHI.at.UTA/0021500467.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151228PHIUTA.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151228SACGSW": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.28.2015.SAC.at.GSW/0021500468.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151228SACGSW.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151228TORCHI": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.28.2015.TOR.at.CHI/0021500463.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151228TORCHI.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151229ATLHOU": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.29.2015.ATL.at.HOU/0021500470.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151229ATLHOU.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151229CLEDEN": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.29.2015.CLE.at.DEN/0021500473.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151229CLEDEN.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151230DENPOR": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.30.2015.DEN.at.POR/0021500482.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151230DENPOR.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151230GSWDAL": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.30.2015.GSW.at.DAL/0021500480.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151230GSWDAL.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151230BKLORL": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.30.2015.BKN.at.ORL/0021500475.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151230BKLORL.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151230LALBOS": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.30.2015.LAL.at.BOS/0021500476.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151230LALBOS.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151230PHXSAS": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.30.2015.PHX.at.SAS/0021500481.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151230PHXSAS.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151230WASTOR": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.30.2015.WAS.at.TOR/0021500477.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151230WASTOR.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151231LACNOP": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.31.2015.LAC.at.NOP/0021500487.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151231LACNOP.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20151231PHXOKC": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/12.31.2015.PHX.at.OKC/0021500488.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20151231PHXOKC.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160102BKLBOS": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.02.2016.BKN.at.BOS/0021500495.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160102BKLBOS.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160102HOUSAS": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.02.2016.HOU.at.SAS/0021500502.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160102HOUSAS.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160113ATLCHA": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.13.2016.ATL.at.CHA/0021500577.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160113ATLCHA.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160113MIALAC": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.13.2016.MIA.at.LAC/0021500586.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160113MIALAC.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160113NOPSAC": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.13.2016.NOP.at.SAC/0021500585.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160113NOPSAC.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160113NYKBKL": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.13.2016.NYK.at.BKN/0021500579.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160113NYKBKL.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160113UTAPOR": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.13.2016.UTA.at.POR/0021500584.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160113UTAPOR.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160115ATLMIL": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.15.2016.ATL.at.MIL/0021500599.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160115ATLMIL.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160115CHANOP": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.15.2016.CHA.at.NOP/0021500598.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160115CHANOP.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160115DALCHI": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.15.2016.DAL.at.CHI/0021500597.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160115DALCHI.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160115MIADEN": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.15.2016.MIA.at.DEN/0021500600.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160115MIADEN.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160115MINOKC": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.15.2016.MIN.at.OKC/0021500594.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160115MINOKC.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160115WASIND": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.15.2016.WAS.at.IND/0021500593.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160115WASIND.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160118ORLATL": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.18.2016.ORL.at.ATL/0021500620.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160118ORLATL.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160118PHINYK": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.18.2016.PHI.at.NYK/0021500615.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160118PHINYK.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160120CHAOKC": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.20.2016.CHA.at.OKC/0021500636.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160120CHAOKC.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160120MIAWAS": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.20.2016.MIA.at.WAS/0021500630.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160120MIAWAS.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160121DETNOP": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.21.2016.DET.at.NOP/0021500641.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160121DETNOP.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160122CHIBOS": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.22.2016.CHI.at.BOS/0021500646.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160122CHIBOS.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160122LACNYK": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.22.2016.LAC.at.NYK/0021500648.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160122LACNYK.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160122MIATOR": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.22.2016.MIA.at.TOR/0021500649.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160122MIATOR.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160122MILHOU": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.22.2016.MIL.at.HOU/0021500650.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160122MILHOU.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160123ATLPHX": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.23.2016.ATL.at.PHX/0021500660.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160123ATLPHX.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160123CHICLE": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.23.2016.CHI.at.CLE/0021500659.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160123CHICLE.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160123DETDEN": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.23.2016.DET.at.DEN/0021500661.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160123DETDEN.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160123INDSAC": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.23.2016.IND.at.SAC/0021500663.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160123INDSAC.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },
        "20160123LALPOR": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.23.2016.LAL.at.POR/0021500662.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160123LALPOR.csv",
            'bad_events': [23],
            'moment_range': 8,
            'event_offset': 1,
        },
        "20160123NYKCHA": {
            'raw_data': fr"{STATIC_PATH}/game_raw_data_round2/01.23.2016.NYK.at.CHA/0021500655.json",
            'events': fr"{STATIC_PATH}/event_annotations_round2/events-20160123NYKCHA.csv",
            'bad_events': [],
            'moment_range': 8,
            'event_offset': 0,
        },

    }