import pandas as pd
from data.classification.utilities.EncodingUtil import EncodingUtil
from data.classification.utilities.ConstantsUtil import ConstantsUtil
from data.models import Candidate

class DataUtil:
    @staticmethod
    def get_candidates_df(candidates, drop_fakes=False, convert_fakes=True, drop_min_features=False):
        if drop_fakes:
            candidates = DataUtil.remove_fake_candidates(candidates)
        elif convert_fakes:
            candidates = DataUtil.convert_fake_candidates(candidates)
        candidates_df = pd.DataFrame(candidates)
        candidates_df.set_index('id', inplace=True)
        candidates_df.drop(columns=['candidate_id'], inplace=True)

        candidates_df = EncodingUtil.basic_label_encode_cols(candidates_df, ConstantsUtil.BASIC_ENCODE_COLS)
        candidates_df = EncodingUtil.sort_position_cols_and_encode(candidates_df, ConstantsUtil.STRING_TUPLE_ENCODE_COLS)
        if drop_min_features:
            candidates_df.drop(columns=ConstantsUtil.FEATURES_IGNORED_BY_INFORMATION_GAIN, inplace=True)

        return candidates_df

    @staticmethod
    def remove_fake_candidates(candidates):
        candidates_without_fakes = []

        for candidate in candidates:
            data = Candidate.objects.values().get(candidate_id=candidate['candidate_id'])
            if 'FAKE' not in data['notes']:
                candidates_without_fakes.append(candidate)

        return candidates_without_fakes

    @staticmethod
    def convert_fake_candidates(candidates):
        for candidate in candidates:
            data = Candidate.objects.values().get(candidate_id=candidate['candidate_id'])
            if 'FAKE' in data['notes']:
                candidate['classification'] = False

        return candidates