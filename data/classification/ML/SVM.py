from sklearn import svm
from .SklearnClf import SklearnClf

class SVM(SklearnClf):
    def __init__(self, C, kernel="poly"):
        super().__init__(name="SVM")
        self.clf = svm.SVC(C=C, kernel=kernel,probability=True)

    PARAMS_TO_OPTIMIZE = {
        'test_size': {
            'init': .2,
            'type': 'float',
            'range': (.1, .3)
        },
        'is_fixed': {
            'init': True,
            'type': 'bool',
            'range': [True, False]
        },
        'C': {
            'init': 1.0,
            'type': 'float',
            'range': (.0001,1000.0)
        },
        'kernel': {
            'init': 2,
            'type': 'enum',
            'range': ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']
        },
        'degree': {
            'init': 3,
            'type': 'int',
            'range': (2,5)
        },
        'gamma': {
            'init': 0,
            'type': 'enum',
            'range': ['scale', 'auto']
        },
        'shrinking': {
            'init': True,
            'type': 'bool',
            'range': [True, False]
        },
        'probability': {
            'init': True,
            'type': 'bool',
            'range': [True, False]
        }
    }