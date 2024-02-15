import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler,
    RobustScaler,
    Normalizer,
    PowerTransformer,
    QuantileTransformer,
    FunctionTransformer,
)
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    f1_score,
    roc_curve,
    auc,
)
from sklearn.model_selection import train_test_split, learning_curve, validation_curve
from .GeneticOptimizer import GeneticOptimizer


class SklearnClf:
    scaler_options = {
        "standard": StandardScaler,
        "minmax": MinMaxScaler,
        "robust": RobustScaler,
        "normalizer": Normalizer,
        "power": PowerTransformer,
        "quantile": QuantileTransformer,
        "log": lambda: FunctionTransformer(
            func=np.log1p, validate=True
        ),  # Handling positive skewness; +1 to accommodate zero values.
    }

    def __init__(self, name, scaler_option='standard'):
        """
        Initialize the SklearnClf with a given classifier.

        Args:
        - classifier: The sklearn-like classifier to be used.
        - name (str):
        Name of the classifier, used for visualization and reporting.
        """
        self.name = name
        self.set_scaler_type(scaler_option)

    def get_model(self):
        return self.clf

    def set_data(self, df, target_col):
        """
        Set the data for training and testing the model.

        Args:
        - df (pd.DataFrame): The dataframe containing the features and target column.
        - target_col (str): The name of the target column.
        """
        self.X = df.drop(columns=[target_col])
        self.y = df[target_col]
        
    def set_scaler_type(self, scaler_option):
        """
        Set the scaler type from the available options.

        Args:
        - scaler_option (str): Key of the scaler to use.
        """
        if scaler_option not in self.scaler_options:
            raise ValueError(f"Scaler option '{scaler_option}' is not supported. Available options: {list(self.scaler_options.keys())}")
        self.scaler = self.scaler_options[scaler_option]()
        self.scaler_option = scaler_option

    def get_data(self):
        return [self.X, self.y]

    def fit_and_predict(self, X_train, X_test, y_train):
        """
        Fit the model to the training data and predict on the test set.

        Args:
        - X_train (pd.DataFrame): Training feature set.
        - X_test (pd.DataFrame): Test feature set.
        - y_train (pd.Series): Training target variable.
        """
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.clf.fit(X_train_scaled, y_train)
        self.predictions = self.clf.predict(X_test_scaled)

    def split_test_data(self, test_size=0.3, random_state=None):
        """
        Split the data into training and testing sets.

        Args:
        - test_size (float): The proportion of the dataset to include in the test split.
        - random_state (int, optional): Controls the shuffling applied to the data before applying the split.

        Returns:
        Tuple containing split data: X_train, X_test, y_train, y_test.
        """
        return train_test_split(
            self.X, self.y, test_size=test_size, random_state=random_state
        )

    def get_avg_metrics_for_n_iterations(
        self, n_iterations=10, test_size=0.3, random_state=None
    ):
        """
        Compute average metrics over a specified number of iterations.

        Args:
        - n_iterations (int): Number of iterations to average over.
        - test_size (float): Proportion of dataset to include in the test split.
        - random_state (int, optional): Random state for reproducibility.

        Returns:
        Dictionary containing average precision, recall, f1_score, and confusion matrix.
        """
        metrics_summary = {
            "precision": 0,
            "recall": 0,
            "f1_score": 0,
            "confusion_matrix": np.zeros((2, 2)),
        }

        for _ in range(n_iterations):
            X_train, X_test, y_train, y_test = self.split_test_data(
                test_size, random_state
            )
            self.fit_and_predict(X_train, X_test, y_train)
            report = classification_report(y_test, self.predictions, output_dict=True)
            metrics_summary["precision"] += report["weighted avg"]["precision"]
            metrics_summary["recall"] += report["weighted avg"]["recall"]
            metrics_summary["f1_score"] += report["weighted avg"]["f1_score"]
            metrics_summary["confusion_matrix"] += confusion_matrix(
                y_test, self.predictions
            )

        # Average the metrics over the iterations
        for key in metrics_summary:
            if key != "confusion_matrix":
                metrics_summary[key] /= n_iterations
            else:
                metrics_summary[key] = metrics_summary[key].astype(int) // n_iterations

        return metrics_summary

    def run_genetic_optimization_on_model(
        self,
        params_to_optimize,
        num_generations=20,
        pop_size=25,
        mutation_rate=0.85,
        display_rate=1,
        rand_selection=False,
        plot_dir="static/backend/test/",
    ):
        gen_optimizer = GeneticOptimizer(
            params_to_optimize,
            num_generations,
            pop_size,
            mutation_rate,
            display_rate,
            rand_selection,
        )
        gen_optimizer.set_model(self)
        gen_optimizer.run_ga()
        gen_optimizer.plot_ga(plot_dir)

    def run_genetic_optimization_on_features(
        self,
        num_generations=20,
        pop_size=25,
        mutation_rate=0.25,
        display_rate=2,
        rand_selection=False,
        plot_dir="static/backend/test/",
    ):
        gen_optimizer = GeneticOptimizer(
            {}, num_generations, pop_size, mutation_rate, display_rate, rand_selection
        )
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
        """
        Generate a ROC curve for the classifier.

        Args:
            X_train, X_test, y_train, y_test: training and testing sets.

        Returns:
            A matplotlib figure object containing the ROC curve.
        """
        self.clf.fit(X_train, y_train)
        probs = self.clf.predict_proba(X_test)
        preds = probs[:, 1]
        fpr, tpr, threshold = roc_curve(y_test, preds)
        roc_auc = auc(fpr, tpr)

        fig, ax = plt.subplots()
        ax.plot(fpr, tpr, "b", label=f"AUC = {roc_auc:.2f}")
        ax.plot([0, 1], [0, 1], "r--")
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title(f"Receiver Operating Characteristic for {self.name}")
        ax.legend(loc="lower right")

        return fig

    def get_learning_curve(self):
        """
        Generate a learning curve for the classifier.

        Returns:
            A matplotlib figure object containing the learning curve.
        """
        train_sizes, train_scores, validation_scores = learning_curve(
            self.clf,
            self.X,
            self.y,
            train_sizes=np.linspace(0.01, 1.0, 10),
            cv=5,
            shuffle=True,
        )

        train_scores_mean = np.mean(train_scores, axis=1)
        validation_scores_mean = np.mean(validation_scores, axis=1)

        fig, ax = plt.subplots()
        ax.plot(train_sizes, train_scores_mean, "o-", label="Training score")
        ax.plot(
            train_sizes, validation_scores_mean, "o-", label="Cross-validation score"
        )
        ax.set_xlabel("Training examples")
        ax.set_ylabel("Score")
        ax.set_title(f"Learning Curve for {self.name}")
        ax.legend(loc="best")

        return fig

    def get_validation_curve(
        self, param_name="gamma", param_range=np.logspace(-6, -1, 5)
    ):
        """
        Generate a validation curve for the classifier.

        Args:
            param_name (str): Name of the parameter to vary.
            param_range (np.ndarray): The range of parameter values to evaluate.

        Returns:
            A matplotlib figure object containing the validation curve.
        """
        train_scores, test_scores = validation_curve(
            self.clf,
            self.X,
            self.y,
            param_name=param_name,
            param_range=param_range,
            cv=5,
            scoring="accuracy",
            n_jobs=-1,
        )

        train_scores_mean = np.mean(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)

        fig, ax = plt.subplots()
        ax.semilogx(
            param_range, train_scores_mean, label="Training score", color="darkorange"
        )
        ax.fill_between(
            param_range,
            np.min(train_scores, axis=1),
            np.max(train_scores, axis=1),
            alpha=0.2,
            color="darkorange",
            lw=2,
        )
        ax.semilogx(
            param_range, test_scores_mean, label="Cross-validation score", color="navy"
        )
        ax.fill_between(
            param_range,
            np.min(test_scores, axis=1),
            np.max(test_scores, axis=1),
            alpha=0.2,
            color="navy",
            lw=2,
        )
        ax.set_title(f"Validation Curve with {self.name}")
        ax.set_xlabel(param_name)
        ax.set_ylabel("Score")
        ax.legend(loc="best")

        return fig
