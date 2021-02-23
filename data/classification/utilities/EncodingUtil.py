from sklearn import preprocessing
from ast import literal_eval as make_tuple

class EncodingUtil:
    @staticmethod
    def basic_label_encode_cols(df, cols):
        le = preprocessing.LabelEncoder()
        for col in cols:
            df[col] = le.fit_transform(df[col])

        return df
