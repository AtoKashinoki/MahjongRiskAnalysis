"""
Test that training model.
"""

import os
from numpy import load, array

from MahjongRiskAnalysis.machine_learning_model.decision_tree_classifier.training import DecisionTreeClassifier


os.chdir(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


TARGET_YEARS = tuple(map(str, range(2025, 2026)))


DIST = os.path.join("..", "tenhou_data")


if __name__ == '__main__':
    test_results = []

    for i in range(1, 3+1):

        TEST_DATAS = os.path.join(DIST, "test_datas", f"model{i}")
        MODEL_DATA = os.path.join(DIST, "models", f"model{i}", "decision_tree_classifier.joblib")

        list_idx = list()
        list_x_test = list()
        list_y_test = list()
        for dirname in map(lambda x: os.path.join(TEST_DATAS, x), TARGET_YEARS):
            listdir = os.listdir(dirname)
            length = len(listdir)
            for idx, filename in enumerate(listdir):
                progress = idx + 1
                print(f"loading {filename}. {progress * 100 / length:.3f}%[{progress}/{length}]")
                datas = load(os.path.join(dirname, filename))
                for data in datas:
                    list_idx.append((idx, data[0]))
                    list_x_test.append(data[1:-1])
                    list_y_test.append(data[-1])
                    continue
                print(f"Success to load data from {filename}")
                continue
            continue
        idx_test, X_test, y_test= array(list_idx), array(list_x_test), array(list_y_test)

        model = DecisionTreeClassifier.load(MODEL_DATA)
        model_results = model.model.predict_proba(X_test)

        results = []
        pre_game_idx, pre_result_idx = -1, -1
        for idx, (game_idx, result_idx) in enumerate(list_idx):
            if not (pre_game_idx == game_idx and pre_result_idx == result_idx):
                pre_game_idx = game_idx
                pre_result_idx = result_idx
                results.append([])
                ...
            results[-1].append([model_results[idx], y_test[idx]])
            continue

        prediction_results = []
        for result in results:

            answer = result[0]

            result.sort(key=lambda x: x[0][1], reverse=True)
            prediction_result = None
            for idx in range(len(result)):
                data = result.pop(0)
                if data[1] == answer[1]:
                    prediction_result = idx + sum(
                        data_[0][1] == answer[0][1] and not data_[1] == answer[1]
                        for data_ in result
                    )
                    break
                continue
            prediction_results.append((answer, int(prediction_result)))
            continue

        prediction_graph = {}
        for prediction in prediction_results:
            if prediction[1] not in prediction_graph:
                prediction_graph[prediction[1]] = 0
                ...
            prediction_graph[prediction[1]] += 1
            continue
        prediction_graph = dict(sorted(
            prediction_graph.items(),
            key=lambda x: x[0],
        ))
        test_results.append(prediction_graph)
        continue

    for test_result in test_results:
        print(test_result)
        print({
            idx: num*100 / sum(test_result.values())
            for idx, num in enumerate(test_result.values())
        })
        continue
    ...
