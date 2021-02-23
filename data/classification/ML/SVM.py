from sklearn import svm
from sklearn.metrics import classification_report, confusion_matrix

class SVM:
    def __init__(self,kernel):
        self.clf = svm.SVC(kernel=kernel)

    def get_model(self):
        return self.clf

    def fit_and_predict(self, X_train, X_test, y_train):
        self.clf.fit(X_train, y_train)
        self.predictions = self.clf.predict(X_test)
        