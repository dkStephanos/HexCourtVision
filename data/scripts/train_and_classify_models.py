import pandas as pd
from sklearn.model_selection import train_test_split

from data.classification.utilities.EncodingUtil import EncodingUtil
from data.classification.ML.SVM import SVM

from data.models import CandidateFeatureVector


def run():
    candidates = CandidateFeatureVector.objects.all().values()
    candidates_df = pd.DataFrame(candidates)
    candidates_df.set_index('id', inplace=True)
    candidates_df.drop(columns=['candidate_id'], inplace=True)

    candidates_df = EncodingUtil.basic_label_encode_cols(candidates_df, ['cutter_archetype', 'screener_archetype'])
    candidates_df = EncodingUtil.sort_position_cols_and_encode(candidates_df, [ 'cutter_loc_on_pass',
                                                                                'screener_loc_on_pass',
                                                                                'ball_loc_on_pass',
                                                                                'ball_radius_on_pass',
                                                                                'cutter_loc_on_start_approach',
                                                                                'screener_loc_on_start_approach',
                                                                                'ball_loc_on_start_approach',
                                                                                'ball_radius_loc_on_start_approach',
                                                                                'cutter_loc_on_end_execution',
                                                                                'screener_loc_on_end_execution',
                                                                                'ball_loc_on_end_execution',
                                                                                'ball_radius_loc_on_end_execution',
                                                                                'cutter_loc_on_screen',
                                                                                'screener_loc_on_screen',
                                                                                'ball_loc_on_screen',
                                                                                'ball_radius_on_screen'])

    X = candidates_df.drop(columns=['classification'])
    y = candidates_df['classification']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    svm = SVM(C=.8, kernel='poly')
    svm.fit_and_predict(X_train, X_test, y_train)
    print(svm.get_confusion_matrix(y_test))
    print(svm.get_classification_report(y_test))
