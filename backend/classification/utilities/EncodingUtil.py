from sklearn import preprocessing
from ast import literal_eval as make_tuple

class EncodingUtil:
    @staticmethod
    def basic_label_encode_cols(df, cols):
        le = preprocessing.LabelEncoder()
        for col in cols:
            df[col] = le.fit_transform(df[col])

        return df

    @staticmethod
    def sort_position_cols_and_encode(df, cols):
        le = preprocessing.LabelEncoder()

        for col in cols:
            try:
                # Construct the sort_val col from the position
                df['sort_val'] = df[col].apply(lambda x: make_tuple(x))
                df = df.sort_values('sort_val').drop('sort_val', 1)
                df[col] = le.fit_transform(df[col])
            except:
                print("Issue encoding the following col:")
                print(df[col])

        return df.sort_values('id')
