import pandas as pd

from data.classification.utilities.EncodingUtil import EncodingUtil
from data.classification.utilities.ConstantsUtil import ConstantsUtil
from data.classification.ML.SVM import SVM

from data.models import CandidateFeatureVector


def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates)
    candidates_df.set_index('id', inplace=True)
    candidates_df.drop(columns=['candidate_id'], inplace=True)

    candidates_df = EncodingUtil.basic_label_encode_cols(candidates_df, ConstantsUtil.BASIC_ENCODE_COLS)
    candidates_df = EncodingUtil.sort_position_cols_and_encode(candidates_df, ConstantsUtil.STRING_TUPLE_ENCODE_COLS)
    #candidates_df.drop(columns=ConstantsUtil.FEATURES_IGNORED_BY_INFORMATION_GAIN, inplace=True)

    svm = SVM(C=.75, kernel='poly')
    svm.set_data(candidates_df, 'classification')
    X_train, X_test, y_train, y_test = svm.split_test_data(.3, True)
        
    svm.get_roc_curve(X_train, X_test, y_train, y_test)

    svm.fit_and_predict(X_train, X_test, y_train)
    print(svm.get_classification_report(y_test))

    #svm.get_learning_curve()
    #svm.get_validation_curve()

    metrics = svm.get_avg_metrics_for_n_iterations(10, .3, True)
    print(metrics)
    '''
    Genetic optimization stuff -- needs work
    optimized_configuration = svm.run_genetic_optimization_on_model(svm.PARAMS_TO_OPTIMIZE, num_generations=20,pop_size=10,display_rate=2)
    optimized_features = svm.run_genetic_optimization_on_features(num_generations=20,pop_size=10,display_rate=2)

    text_file = open("static/data/test/genetic_algorithm_test.txt", "w")
    text_file.write(f'Ideal configuration found:\n{optimized_configuration}\n\nIdeal Feature Set found:\n{optimized_features}')
    text_file.close()
    '''

    