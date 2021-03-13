import pandas as pd
from data.classification.utilities.EncodingUtil import EncodingUtil
from data.classification.utilities.ConstantsUtil import ConstantsUtil

class DataUtil:

    @classmethod
    def get_candidates_df(candidates, drop_fakes=True, drop_min_features=False):
        candidates_df = pd.DataFrame(candidates)
        candidates_df.set_index('id', inplace=True)
        candidates_df.drop(columns=['candidate_id'], inplace=True)
        print("Inside get candidates df")
        print(len(candidates_df))
        if drop_fakes:
            candidates_df = candidates_df[~candidates_df.notes.str.contains("FAKE")]

        print(len(candidates_df))

        candidates_df = EncodingUtil.basic_label_encode_cols(candidates_df, ConstantsUtil.BASIC_ENCODE_COLS)
        candidates_df = EncodingUtil.sort_position_cols_and_encode(candidates_df, ConstantsUtil.STRING_TUPLE_ENCODE_COLS)
        if drop_min_features:
            candidates_df.drop(columns=ConstantsUtil.FEATURES_IGNORED_BY_INFORMATION_GAIN, inplace=True)

        return candidates_df