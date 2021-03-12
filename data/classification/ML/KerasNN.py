from sklearn import preprocessing
from sklearn.utils import validation
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import roc_curve,auc

class KerasNN:
    def __init__(self,):
        self.min_max_scaler = preprocessing.MinMaxScaler()
        self.model = Sequential()
        self.model.add(Dense(32, input_dim=50, activation='relu'))
        self.model.add(Dense(16, activation='relu'))
        self.model.add(Dense(8, activation='relu'))
        self.model.add(Dense(1, activation='sigmoid'))
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    def get_model(self):
        return self.model

    def fit_model(self, X, y):      
        X = self.min_max_scaler.fit_transform(X)
        self.X = X
        self.y = y
        self.history = self.model.fit(X, y, epochs=120, batch_size=10, validation_split=.2)

    def get_classification_report(self):
        return self.model.evaluate(self.X, self.y)

    def plot_training_validation(self):
        pd.DataFrame(self.history.history).plot(figsize=(8, 5))
        plt.grid(True)
        plt.gca().set_ylim(0, 1) # set the vertical range to [0-1]
        plt.title("Learning Curves for Keras NN")
        plt.show()

    def plot_roc_curve(self):
        y_val_cat_prob = self.model.predict_proba(self.X)
        fpr , tpr , thresholds = roc_curve( self.y , y_val_cat_prob)

        roc_auc = auc(fpr, tpr)

        # method I: plt
        plt.title(f'Receiver Operating Characteristic for Keras NN')
        plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
        plt.legend(loc = 'lower right')
        plt.plot([0, 1], [0, 1],'r--')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        plt.show() 

        