from sklearn import svm, preprocessing
from sklearn.metrics import classification_report, confusion_matrix
from .SklearnClf import SklearnClf

class SVM(SklearnClf):
    def __init__(self, C, kernel="poly"):
        super().__init__()
        self.clf = svm.SVC(C=C, kernel=kernel)