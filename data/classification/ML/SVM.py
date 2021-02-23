from sklearn import svm

class SVM:
    def create_model(self):
        self.clf = svm.SVC()
