import pandas as pd
import statistics as stats
from sklearn import metrics
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

class NeuralNetwork:
    @staticmethod
    def classify(dataFrame, alphaToUse, hiddenLayerSize, activationToUse, solverToUse, test_size, target_col, isFixed=False, printResults=True):

        X_train, X_test, y_train, y_test = NeuralNetwork.splitTestData(dataFrame, test_size, target_col, isFixed)      #Split the data
        scaler=StandardScaler()
        scaler.fit(X_train)
        X_train=scaler.transform(X_train)
        X_test=scaler.transform(X_test)

        mlp = MLPClassifier(activation=activationToUse, hidden_layer_sizes = hiddenLayerSize, solver=solverToUse, alpha=alphaToUse, learning_rate_init=.03, early_stopping=True, max_iter=1000) #Generate the Learning infrastructure

        mlp_model = mlp.fit(X_train, y_train)                                                           #generate model from training data
        mlp_predictions = mlp_model.predict(X_test)                                                     #Make predictions
        accuracy = mlp_model.score(X_test, y_test)                                                      #Model Accuracy

        if(printResults):
            NeuralNetwork.printStats(alphaToUse, solverToUse, hiddenLayerSize, activationToUse, test_size, isFixed, y_test, mlp_predictions)

        return [metrics.accuracy_score(y_test, mlp_predictions)*100,metrics.precision_score(y_test, mlp_predictions, average='weighted')*100,metrics.recall_score(y_test, mlp_predictions, average='weighted')*100], metrics.confusion_matrix(y_test, mlp_predictions)        #only works with sgd

    @staticmethod
    def plot_roc_curve(dataFrame, alphaToUse, hiddenLayerSize, activationToUse, solverToUse, test_size, target_col, isFixed=False):

        X_train, X_test, y_train, y_test = NeuralNetwork.splitTestData(dataFrame, test_size, target_col, isFixed)      #Split the data
        scaler=StandardScaler()
        scaler.fit(X_train)
        X_train=scaler.transform(X_train)
        X_test=scaler.transform(X_test)

        mlp = MLPClassifier(activation=activationToUse, hidden_layer_sizes = hiddenLayerSize, solver=solverToUse, alpha=alphaToUse, early_stopping=True, max_iter=1000) #Generate the Learning infrastructure

        mlp.fit(X_train, y_train)
        # calculate the fpr and tpr for all thresholds of the classification
        probs = mlp.predict_proba(X_test)
        preds = probs[:,1]
        fpr, tpr, threshold = metrics.roc_curve(y_test, preds)
        roc_auc = metrics.auc(fpr, tpr)

        # method I: plt
        plt.style.use('seaborn')
        plt.title(f'Receiver Operating Characteristic for MLP')
        plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
        plt.legend(loc = 'lower right')
        plt.plot([0, 1], [0, 1],'r--')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        plt.show() 

    @staticmethod
    def plot_loss_val_curve(dataFrame, alphaToUse, hiddenLayerSize, activationToUse, solverToUse, test_size, target_col, isFixed=False):

        X_train, X_test, y_train, y_test = NeuralNetwork.splitTestData(dataFrame, test_size, target_col, isFixed)      #Split the data
        scaler=StandardScaler()
        scaler.fit(X_train)
        X_train=scaler.transform(X_train)
        X_test=scaler.transform(X_test)

        mlp = MLPClassifier(activation=activationToUse, hidden_layer_sizes = hiddenLayerSize, solver=solverToUse, alpha=alphaToUse, learning_rate_init=.025, early_stopping=True, max_iter=1000) #Generate the Learning infrastructure

        mlp.fit(X_train, y_train)
        mlp.score(X_train,y_train)

        plt.style.use('seaborn')
        plt.title(f'Learning Curve for MLP')
        plt.plot(mlp.loss_curve_, label='Loss')
        plt.plot(mlp.validation_scores_, label='Validation Accuracy')
        plt.ylabel('Score')
        plt.xlabel('Epochs')
        plt.legend(loc = 'upper right')
        plt.show()

    @staticmethod
    def splitTestData(dataFrame, test_size, target_col, isFixed=False):
        X = dataFrame.drop(columns=[target_col])
        Y = dataFrame[target_col]
        if(isFixed):    #Use the same seed when generating test and training sets
            X_train, X_test, y_train, y_test = train_test_split(X, Y, shuffle = True, random_state = 42, test_size = test_size)
        else:           #Use a completely random set of test and training data
            X_train, X_test, y_train, y_test = train_test_split(X, Y, shuffle = True, test_size = test_size)

        return X_train, X_test, y_train, y_test

    #Finds the accuracy values given a number of classification tests
    @staticmethod
    def testNIterations(dataFrame, alphaToUse, hiddenLayerSize, activationToUse, solverToUse, test_size, target_col, nIterations):
        accuracyResults = []
        matrixTotals = {'tn': 0, 'fp': 0, 'fn': 0, 'tp': 0,}
        for test in range(0, nIterations):
            accuracy, confusion_matrix = NeuralNetwork.classify(dataFrame, alphaToUse, hiddenLayerSize, activationToUse, solverToUse, test_size, target_col, False, True)
            accuracyResults.append(accuracy)
            matrixTotals['tn'] += confusion_matrix[0][0]
            matrixTotals['fp'] += confusion_matrix[0][1]
            matrixTotals['fn'] += confusion_matrix[1][0]
            matrixTotals['tp'] += confusion_matrix[1][1]

        for total in matrixTotals:
            matrixTotals[total] = matrixTotals[total] / nIterations
            
        accuracyResults = pd.DataFrame(accuracyResults)
        
        return accuracyResults.mean(), matrixTotals

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
    def printStats(Alpha, solverToUse, hiddenLayerSize, activation, test_size, isFixed, y_test, mlp_predictions):
        print("\t The results for for NN with settings: ")
        print("\t Solver: "+solverToUse)
        print("\t Activation: "+activation)
        print("\t Alpha: "+str(Alpha))
        print("\t Hidden Layer Dimensions: "+str(hiddenLayerSize))
        print("\t Fixed seed: "+str(isFixed))
        print("\t Test Set Percentage: "+str(test_size))
        print("\n\t are as follows: ")

        report_lr = metrics.precision_recall_fscore_support(y_test, mlp_predictions, average='micro')
        print ("\n     precision = %0.2f, recall = %0.2f, F1 = %0.2f, accuracy = %0.2f\n" % \
           (report_lr[0], report_lr[1], report_lr[2], metrics.accuracy_score(y_test, mlp_predictions)))

        print("\n    Accuracy: ",metrics.accuracy_score(y_test, mlp_predictions))
        print("\n    Precision: ",metrics.precision_score(y_test, mlp_predictions, average='weighted'))
        print("\n    Recall:",metrics.recall_score(y_test, mlp_predictions, average='weighted'))

        print("\n\n  Confusion Matrix: ")
        print(confusion_matrix(y_test, mlp_predictions))