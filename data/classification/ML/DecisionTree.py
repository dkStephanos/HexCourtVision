from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from .SklearnClf import SklearnClf

class DecisionTree(SklearnClf):
    def __init__(self,criterion):
        super().__init__(name="DecisionTree")
        self.clf = DecisionTreeClassifier(criterion=criterion)