from sklearn import preprocessing
from keras.models import Sequential
from keras.layers import Dense

class KerasNN:
    def __init__(self,):
        self.min_max_scaler = preprocessing.MinMaxScaler()
        self.model = Sequential()
        self.model.add(Dense(12, input_dim=50, activation='relu'))
        self.model.add(Dense(8, activation='relu'))
        self.model.add(Dense(1, activation='sigmoid'))
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    def get_model(self):
        return self.model

    def fit_model(self, X, y):      
        X = self.min_max_scaler.fit_transform(X)
        self.X = X
        self.y = y
        
        self.model.fit(X, y, epochs=150, batch_size=10)

    def get_classification_report(self):
        return self.model.evaluate(self.X, self.y)