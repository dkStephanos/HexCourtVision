import pandas as pd
import statistics as stats
from sklearn import metrics
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

class NeuralNetwork:
    @staticmethod
    def classify(dataFrame, alphaToUse, hiddenLayerSize, activationToUse, solverToUse, test_size, target_col, isFixed=False, printResults=True):

        X_train, X_test, Y_train, Y_test = NeuralNetwork.splitTestData(dataFrame, test_size, target_col, isFixed)      #Split the data
        scaler=StandardScaler()
        scaler.fit(X_train)
        X_train=scaler.transform(X_train)
        X_test=scaler.transform(X_test)

        mlp = MLPClassifier(activation=activationToUse, hidden_layer_sizes = hiddenLayerSize, solver=solverToUse, alpha=alphaToUse, early_stopping=True, max_iter=1000) #Generate the Learning infrastructure

        mlp_model = mlp.fit(X_train, Y_train)                                                           #generate model from training data
        mlp_predictions = mlp_model.predict(X_test)                                                     #Make predictions
        accuracy = mlp_model.score(X_test, Y_test)                                                      #Model Accuracy

        if(printResults):
            NeuralNetwork.printStats(alphaToUse, solverToUse, hiddenLayerSize, activationToUse, test_size, isFixed, Y_test, mlp_predictions)

        return [metrics.accuracy_score(Y_test, mlp_predictions)*100,metrics.precision_score(Y_test, mlp_predictions, average='weighted')*100,metrics.recall_score(Y_test, mlp_predictions, average='weighted')*100], mlp.loss_curve_        #only works with sgd

    @staticmethod
    def splitTestData(dataFrame, test_size, target_col, isFixed=False):
        X = dataFrame.drop(columns=[target_col])
        Y = dataFrame[target_col]
        if(isFixed):    #Use the same seed when generating test and training sets
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, shuffle = True, random_state = 42, test_size = test_size)
        else:           #Use a completely random set of test and training data
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, shuffle = True, test_size = test_size)

        return X_train, X_test, Y_train, Y_test

    #Finds the accuracy values given a number of classification tests
    @staticmethod
    def testNIterations(dataFrame, alphaToUse, hiddenLayerSize, activationToUse, solverToUse, test_size, target_col, nIterations):
        accuracyResults = []
        for test in range(0, nIterations):
            accuracy, curve = NeuralNetwork.classify(dataFrame, alphaToUse, hiddenLayerSize, activationToUse, solverToUse, test_size, target_col, False, True)
            accuracyResults.append(accuracy)
            
        accuracyResults = pd.DataFrame(accuracyResults)

        return accuracyResults.mean()

    #find the value 
    def testAlpha(dataFrame, alphaToFind, hiddenLayerSize, activationToUse, solverToUse, test_size, nIterations):
        cAverages = []
        alpha = 0.001
        maxAlpha = int(alphaToFind*1000)
        for sTest in range(0, maxAlpha):
            
            accuracyResults = NeuralNetwork.testNIterations(dataFrame, alpha, hiddenLayerSize, activationToUse, solverToUse, test_size, nIterations)
            cAverages.append(NeuralNetwork.findAverage(accuracyResults))
            alpha += 0.001
        return cAverages

    #Finds the average of a passed array
    @staticmethod
    def findAverage(resultArray):
        numResults = len(resultArray)
        return (float)(stats._sum(resultArray)[1]/numResults)

    @staticmethod
    def printStats(Alpha, solverToUse, hiddenLayerSize, activation, test_size, isFixed, Y_test, mlp_predictions):
        print("\t The results for for NN with settings: ")
        print("\t Solver: "+solverToUse)
        print("\t Activation: "+activation)
        print("\t Alpha: "+str(Alpha))
        print("\t Hidden Layer Dimensions: "+str(hiddenLayerSize))
        print("\t Fixed seed: "+str(isFixed))
        print("\t Test Set Percentage: "+str(test_size))
        print("\n\t are as follows: ")

        report_lr = metrics.precision_recall_fscore_support(Y_test, mlp_predictions, average='micro')
        print ("\n     precision = %0.2f, recall = %0.2f, F1 = %0.2f, accuracy = %0.2f\n" % \
           (report_lr[0], report_lr[1], report_lr[2], metrics.accuracy_score(Y_test, mlp_predictions)))

        print("\n    Accuracy: ",metrics.accuracy_score(Y_test, mlp_predictions))
        print("\n    Precision: ",metrics.precision_score(Y_test, mlp_predictions, average='weighted'))
        print("\n    Recall:",metrics.recall_score(Y_test, mlp_predictions, average='weighted'))

        print("\n\n  Confusion Matrix: ")
        print(confusion_matrix(Y_test, mlp_predictions))