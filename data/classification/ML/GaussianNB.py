from sklearn import preprocessing, naive_bayes
from sklearn.metrics import classification_report, confusion_matrix
from .SklearnClf import SklearnClf

class GaussianNB(SklearnClf):
    def __init__(self,):
        super().__init__()
        self.clf = naive_bayes.GaussianNB()