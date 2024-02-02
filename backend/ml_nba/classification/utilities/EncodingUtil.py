# File: my_library/utils/encoding_util.py

from sklearn import preprocessing
from ast import literal_eval as make_tuple

class EncodingUtil:

    @staticmethod
    def basic_label_encode_cols(df, cols):
        """
        Encode specified columns using basic label encoding.

        Args:
            df (pandas.DataFrame): The DataFrame to be encoded.
            cols (list): List of column names to be encoded.

        Returns:
            pandas.DataFrame: The DataFrame with specified columns label encoded.
        """
        df_copy = df.copy()
        le = preprocessing.LabelEncoder()
        for col in cols:
            df_copy[col] = le.fit_transform(df[col])

        return df_copy

    @staticmethod
    def sort_position_cols_and_encode(df, cols):
        """
        Sort specified columns by a 'sort_val' column and encode them using label encoding.

        Args:
            df (pandas.DataFrame): The DataFrame to be sorted and encoded.
            cols (list): List of column names to be sorted and encoded.

        Returns:
            pandas.DataFrame: The DataFrame with specified columns sorted and label encoded.
        """
        df_copy = df.copy()
        le = preprocessing.LabelEncoder()

        for col in cols:
            try:
                # Construct the sort_val col from the position
                df_copy['sort_val'] = df_copy[col].apply(lambda x: make_tuple(x))
                df_copy = df_copy.sort_values('sort_val').drop('sort_val', 1)
                df_copy[col] = le.fit_transform(df_copy[col])
            except Exception as e:
                print(f"Issue encoding the following col: {col}")
                print(e)

        return df_copy.sort_values('id')
