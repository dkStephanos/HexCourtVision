from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
import pandas as pd

class EncodingUtil:
    @staticmethod
    def encode_columns(df, columns, encoding_type='label'):
        """
        Encode specified columns in the DataFrame according to the specified encoding type.
        Supports 'label', 'onehot', and 'ordinal' encoding.

        Args:
            df (pandas.DataFrame): The DataFrame to be encoded.
            columns (list): List of column names to be encoded.
            encoding_type (str): Type of encoding to apply. Options include 'label', 'onehot', and 'ordinal'.

        Returns:
            pandas.DataFrame: The DataFrame with specified columns encoded. For 'onehot' encoding, returns
            original DataFrame with new one-hot encoded columns added.
        """
        df_copy = df.copy()

        if encoding_type == 'label':
            encoder = LabelEncoder()
            for col in columns:
                df_copy[col] = encoder.fit_transform(df_copy[col])

        elif encoding_type == 'onehot':
            encoder = OneHotEncoder(sparse=False, drop='first')
            encoded_cols = encoder.fit_transform(df_copy[columns])
            encoded_col_names = encoder.get_feature_names_out(columns)
            df_encoded = pd.DataFrame(encoded_cols, columns=encoded_col_names, index=df_copy.index)
            df_copy = pd.concat([df_copy.drop(columns, axis=1), df_encoded], axis=1)

        elif encoding_type == 'ordinal':
            encoder = OrdinalEncoder()
            df_copy[columns] = encoder.fit_transform(df_copy[columns])

        else:
            raise ValueError(f"Unsupported encoding type: {encoding_type}")

        return df_copy
