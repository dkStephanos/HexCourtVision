from sklearn import svm

class SVM:
    def __init__(self,kernel):
        self.clf = svm.SVC(kernel=kernel)

    def get_model(self):
        return self.clf
