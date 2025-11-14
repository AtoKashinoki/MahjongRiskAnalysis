"""
Test that training model.
"""

import os
from numpy import load, array

from MahjongRiskAnalysis.machine_learning_model.decision_tree_classifier.training import DecisionTreeClassifier


TARGET_YEARS = tuple(map(str, range(2024, 2025)))


DIST = os.path.join("..", "tenhou_data")
TRAINING_DATAS = os.path.join(DIST, "training_datas")
MODEL_DATA = os.path.join(DIST, "models", "decision_tree_classifier.joblib")


if __name__ == '__main__':
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
            print(f"success to load data from {filename}")
            continue
        continue
    X_train, y_train = array(list_x_train), array(list_y_train)
    print(X_train.shape, y_train.shape)

    model = DecisionTreeClassifier()
    model.fit(X_train[:-1], y_train[:-1])
    model.save(MODEL_DATA)

    model = DecisionTreeClassifier.load(MODEL_DATA)
    result = model.model.predict_proba(X_train[-1:])[0][1]
    print(f"{result=}, ans={y_train[-1:]}")
    ...
