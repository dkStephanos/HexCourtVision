from sklearn import preprocessing
from sklearn.utils import validation
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import metrics

class KerasNN:
    def __init__(self,input_dim):
        self.min_max_scaler = preprocessing.MinMaxScaler()
        self.model = Sequential()
        #self.model.add(Dense(24, input_dim=input_dim, activation='relu'))
        self.model.add(Dense(36, input_dim=input_dim, activation='relu'))
        self.model.add(Dense(12, activation='relu'))
        self.model.add(Dense(1, activation='sigmoid'))
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['mse'])

    def get_model(self):
        return self.model

    def split_test_data(self, test_size, is_fixed=False):
        if(is_fixed):    #Use the same seed when generating test and training sets
            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, shuffle = True, random_state = 42, test_size = test_size)
        else:           #Use a completely random set of test and training data
            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, shuffle = True, test_size = test_size)

        return X_train, X_test, y_train, y_test

    def fit_model(self, X, y, epochs, class_weight={0: 1., 1: 3.}):      
        X = self.min_max_scaler.fit_transform(X)
        self.X = X
        self.y = y
        X_train, X_test, y_train, y_test = self.split_test_data(.3)

        self.history = self.model.fit(X_train, y_train, epochs=epochs, batch_size=10, validation_split=.2, class_weight=class_weight)

        return X_train, X_test, y_train, y_test

    def get_classification_report(self, X_test, y_test):
        return self.model.evaluate(X_test, y_test)

    def get_accuracy_stats(self, X_test, y_test):
        predictions = self.model.predict_classes(X_test)[:, 0]

        # accuracy: (tp + tn) / (p + n)
        accuracy = metrics.accuracy_score(y_test, predictions)
        print('Accuracy: %f' % accuracy)
        # precision tp / (tp + fp)
        precision = metrics.precision_score(y_test, predictions)
        print('Precision: %f' % precision)
        # recall: tp / (tp + fn)
        recall = metrics.recall_score(y_test, predictions)
        print('Recall: %f' % recall)
        # f1: 2 tp / (2 tp + fp + fn)
        f1 = metrics.f1_score(y_test, predictions)
        print('F1 score: %f' % f1)

    def plot_training_validation(self):
        pd.DataFrame(self.history.history).plot(figsize=(8, 5))
        plt.style.use('seaborn')
        plt.grid(True)
        plt.gca().set_ylim(0, 1) # set the vertical range to [0-1]
        plt.title("Learning Curves for Keras NN")
        plt.show()

    def plot_roc_curve(self):
        y_val_cat_prob = self.model.predict_proba(self.X)
        fpr , tpr , thresholds = metrics.roc_curve( self.y , y_val_cat_prob)

        roc_auc = metrics.auc(fpr, tpr)

        # method I: plt
        plt.style.use('seaborn')
        plt.title(f'Receiver Operating Characteristic for Keras NN')
        plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
        plt.legend(loc = 'lower right')
        plt.plot([0, 1], [0, 1],'r--')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        plt.show() 

        