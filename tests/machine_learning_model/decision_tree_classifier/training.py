"""
Test that training model.
"""

import os
from numpy import load, array

from MahjongRiskAnalysis.machine_learning_model.decision_tree_classifier.training import DecisionTreeClassifier
from MahjongRiskAnalysis.machine_learning_model.decision_tree_classifier.config import ModelConfig


os.chdir(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


TARGET_YEARS = tuple(map(str, range(2024, 2025)))


DIST = os.path.join("..", "tenhou_data")


if __name__ == '__main__':

    for i in range(1, 3+1):

        TRAINING_DATAS = os.path.join(DIST, "training_datas", f"model{i}")

        list_x_train = list()
        list_y_train = list()
        for dirname in map(lambda x: os.path.join(TRAINING_DATAS, x), TARGET_YEARS):
            listdir = os.listdir(dirname)
            length = len(listdir)
            for idx, filename in enumerate(listdir):
                progress = idx+1
                print(f"loading {filename}. {progress*100/length:.3f}%[{progress}/{length}]")
                datas = load(os.path.join(dirname, filename))
                for data in datas:
                    list_x_train.append(data[:-1])
                    list_y_train.append(data[-1])
                    continue
                print(f"Success to load data from {filename}")
                continue
            continue
        X_train, y_train = array(list_x_train), array(list_y_train)

        for new_max_depth in range(1, 31):
            ModelConfig.max_depth = new_max_depth

            MODEL_DATA = os.path.join(
                DIST, "models", f"model{i}", f"decision_tree_classifier_depth{ModelConfig.max_depth}.joblib"
            )
            model = DecisionTreeClassifier()
            model.fit(X_train, y_train)
            model.save(MODEL_DATA)

            model = DecisionTreeClassifier.load(MODEL_DATA)
            result = model.model.predict_proba(X_train[-1:])[0]
            print(f"{result=}, ans={y_train[-1:]}")

            continue

        continue
    ...
