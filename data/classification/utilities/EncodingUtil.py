from sklearn import preprocessing

class EncodingUtil:
    @staticmethod
    def create_model():
        return preprocessing.LabelEncoder()