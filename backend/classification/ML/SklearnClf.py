import numpy as np
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
from sklearn import preprocessing, metrics
from sklearn.metrics import confusion_matrix, classification_report, f1_score
from sklearn.model_selection import train_test_split, learning_curve, validation_curve
from .GeneticOptimizer import GeneticOptimizer

class SklearnClf:
    def __init__(self, name):
        self.name = name
        self.min_max_scaler = preprocessing.MinMaxScaler()

    def get_model(self):
        return self.clf

    def set_data(self, df, target_col):
        self.X = df.drop(columns=[target_col])
        self.y = df[target_col]

    def get_data(self):
        return [self.X, self.y]

    def fit_and_predict(self, X_train, X_test, y_train):      
        X_train = self.min_max_scaler.fit_transform(X_train)
        X_test = self.min_max_scaler.fit_transform(X_test)
        
        self.clf.fit(X_train, y_train)
        self.predictions = self.clf.predict(X_test)

    def split_test_data(self, test_size, is_fixed=False):
        if(is_fixed):    #Use the same seed when generating test and training sets
            X_train, X_test, Y_train, Y_test = train_test_split(self.X, self.y, shuffle = True, random_state = 42, test_size = test_size)
        else:           #Use a completely random set of test and training data
            X_train, X_test, Y_train, Y_test = train_test_split(self.X, self.y, shuffle = True, test_size = test_size)

        return X_train, X_test, Y_train, Y_test

    def get_avg_metrics_for_n_iterations(self, n_iterations, test_size, is_fixed=False):
        
        precision = 0
        recall = 0
        f1_score = 0
        support = 0
        confusion_matrix = np.zeros((2,2))

        for i in range(0,n_iterations):
            X_train, X_test, y_train, y_test = self.split_test_data(test_size, is_fixed)
            self.fit_and_predict(X_train, X_test, y_train)
            confusion_matrix += self.get_confusion_matrix(y_test)
            clf_report = self.get_classification_report(y_test).split("\n")[-2].split("      ")
            precision += float(clf_report[1])
            recall += float(clf_report[2])
            f1_score += float(clf_report[3])
            support += float(clf_report[4])

        precision = precision/n_iterations
        recall = recall/n_iterations
        f1_score = f1_score/n_iterations
        support = support/n_iterations
        confusion_matrix = confusion_matrix/n_iterations

        return [round(precision,3), round(recall,3), round(f1_score, 3), round(support, 3), confusion_matrix]

    def run_genetic_optimization_on_model(self,params_to_optimize,num_generations=20,pop_size=25,mutation_rate=0.85,display_rate=1,rand_selection=False,plot_dir='static/data/test/'):
        gen_optimizer = GeneticOptimizer(params_to_optimize,num_generations, pop_size, mutation_rate, display_rate, rand_selection)
        gen_optimizer.set_model(self)
        gen_optimizer.run_ga()
        gen_optimizer.plot_ga(plot_dir)

    def run_genetic_optimization_on_features(self,num_generations=20,pop_size=25,mutation_rate=0.25,display_rate=2,rand_selection=False,plot_dir='static/data/test/'):
        gen_optimizer = GeneticOptimizer({},num_generations, pop_size, mutation_rate, display_rate, rand_selection)
        gen_optimizer.set_model(self)
        gen_optimizer.run_ga_features()
        gen_optimizer.plot_ga(plot_dir)

    def get_confusion_matrix(self, y_test):
        return confusion_matrix(y_test, self.predictions)

    def get_classification_report(self, y_test):
        return classification_report(y_test, self.predictions)

    def get_f1_score(self, y_test):
        return f1_score(y_test, self.predictions)

    def get_roc_curve(self, X_train, X_test, y_train, y_test):
        self.clf.fit(X_train, y_train)
        # calculate the fpr and tpr for all thresholds of the classification
        probs = self.clf.predict_proba(X_test)
        preds = probs[:,1]
        fpr, tpr, threshold = metrics.roc_curve(y_test, preds)
        roc_auc = metrics.auc(fpr, tpr)

        # method I: plt
        plt.style.use('seaborn')
        plt.title(f'Receiver Operating Characteristic for {self.name}')
        plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
        plt.legend(loc = 'lower right')
        plt.plot([0, 1], [0, 1],'r--')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        plt.show() 

    def get_learning_curve(self):
        train_sizes = [.01, .05, .1, .15, .2, .25, .3,]

        train_sizes, train_scores, validation_scores = learning_curve(
            self.clf, self.X, self.y, train_sizes = train_sizes, cv=5,	
            shuffle=True,)

        train_scores_mean = -train_scores.mean(axis = 1)
        validation_scores_mean = -validation_scores.mean(axis = 1)

        print('Mean training scores\n\n', pd.Series(train_scores_mean, index = train_sizes))
        print('\n', '-' * 20) # separator
        print('\nMean validation scores\n\n',pd.Series(validation_scores_mean, index = train_sizes))
        
        plt.style.use('seaborn')
        plt.plot(train_sizes, train_scores_mean, label = 'Training error')
        plt.plot(train_sizes, validation_scores_mean, label = 'Validation error')
        plt.ylabel('MSE', fontsize = 14)
        plt.xlabel('Training set size', fontsize = 14)
        plt.title(f'Learning curves for {self.name} model', fontsize = 18, y = 1.03)
        plt.legend()
        plt.show()

    def get_validation_curve(self, param_name="gamma", param_range=np.logspace(-6, -1, 5)):

        train_scores, test_scores = validation_curve(
            self.clf, self.X, self.y, param_name=param_name, param_range=param_range, verbose=5, n_jobs=-1)
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)

        plt.title(f"Validation Curve with {self.name}")
        plt.xlabel(r"$\gamma$")
        plt.ylabel("Score")
        lw = 2
        plt.semilogx(param_range, train_scores_mean, label="Training score",
                     color="darkorange", lw=lw)
        plt.fill_between(param_range, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.2,
                         color="darkorange", lw=lw)
        plt.semilogx(param_range, test_scores_mean, label="Cross-validation score",
                     color="navy", lw=lw)
        plt.fill_between(param_range, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.2,
                         color="navy", lw=lw)
        plt.legend(loc="best")
        plt.show()