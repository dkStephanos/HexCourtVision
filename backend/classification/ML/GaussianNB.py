from sklearn import naive_bayes
from .SklearnClf import SklearnClf

class GaussianNB(SklearnClf):
    def __init__(self,):
        super().__init__(name="GaussianNB")
        self.clf = naive_bayes.GaussianNB()