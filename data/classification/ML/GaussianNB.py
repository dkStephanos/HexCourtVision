from sklearn import preprocessing, naive_bayes
from sklearn.metrics import classification_report, confusion_matrix

class GaussianNB:
    def __init__(self,):
        self.clf = naive_bayes.GaussianNB()
        self.min_max_scaler = preprocessing.MinMaxScaler()

    def get_model(self):
        return self.clf

    def fit_and_predict(self, X_train, X_test, y_train):      
        X_train = self.min_max_scaler.fit_transform(X_train)
        X_test = self.min_max_scaler.fit_transform(X_test)
        
        self.clf.fit(X_train, y_train)
        self.predictions = self.clf.predict(X_test)

    def get_confusion_matrix(self, y_test):
        return confusion_matrix(y_test, self.predictions)

    def get_classification_report(self, y_test):
        return classification_report(y_test, self.predictions)