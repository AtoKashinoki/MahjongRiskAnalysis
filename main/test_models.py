"""
Test that training model.
"""

import os
from numpy import load, array

from MahjongRiskAnalysis.machine_learning_model.decision_tree_classifier.training import DecisionTreeClassifier


""" Configs """

TEST_DATA_YEARS = tuple(map(str, range(2025, 2026)))

TARGET_MODELS = range(1, 3+1)
TARGET_DEPTHS = range(1, 30+1)

DIST = os.path.join("..", "tenhou_data")


""" Process """


def main():

    os.chdir(os.path.join(os.path.dirname(__file__), ".."))

    """ Test models """

    test_results = {}
    for target_model in TARGET_MODELS:

        # get test datas
        test_data_path = os.path.join(DIST, "test_datas", f"model{target_model}")

        list_idx = list()
        list_x_test = list()
        list_y_test = list()
        for dirname in map(lambda x: os.path.join(test_data_path, x), TEST_DATA_YEARS):
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
        idx_test, X_test, y_test = array(list_idx), array(list_x_test), array(list_y_test)

        # test models
        for depth in TARGET_DEPTHS:

            # test
            model_path = os.path.join(DIST, "models", f"model{target_model}", f"decision_tree_classifier_depth{depth}.joblib")

            model = DecisionTreeClassifier.load(model_path)
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

            # arrange result
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

            # create prediction graph
            prediction_graph = {f"e{key}": 0 for key in range(14)}
            for prediction in prediction_results:
                key = f"e{prediction[1]}"
                if prediction[1] > 13:
                    prediction_graph["e13"] += 1
                    continue
                prediction_graph[key] += 1
                continue
            prediction_graph = dict(sorted(
                prediction_graph.items(),
                key=lambda x: int(x[0][1:]),
            ))
            test_results[(target_model, depth)] = prediction_graph

            continue

        continue

    """ Output results """

    score_board = [1000] + [500 for _ in range(2)] + list(range(10)[::-1]) + [-1000 for _ in range(14)]
    test_results = {
        key: (test_result, sum([r * s for r, s in zip(test_result.values(), score_board)]))
        for key, test_result in test_results.items()
    }
    test_results = dict(sorted(test_results.items(), key=lambda x: x[1][1], reverse=True))
    format_prediction_graph = ", ".join([f"{i}:" + "{" + f"e{i}" + ": >5}" for i in range(14)])
    print("-" * 40)
    print("Test score ranking of models")
    print("rank / attr / score / prediction errors {prediction error: occurrences}")
    for target_model, (attr, (test_result, score)) in enumerate(test_results.items()):
        print(
            f"{target_model + 1: >2}",
            "model{} depth:{: >2}".format(*attr),
            f"{score: >8}",
            format_prediction_graph.format(**test_result),
            sep=" / "
        )
        continue
    print("-" * 40)

    return


""" Main """


if __name__ == '__main__':
    main()
    ...
