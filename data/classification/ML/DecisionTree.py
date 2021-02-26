from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.metrics import classification_report, confusion_matrix
from .SklearnClf import SklearnClf

class DecisionTree(SklearnClf):
    def __init__(self,criterion):
        super().__init__()
        self.clf = DecisionTreeClassifier(criterion=criterion)