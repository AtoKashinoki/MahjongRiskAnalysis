"""
Test code that contains of augmented file.
"""


import os

from numpy import load


os.chdir(os.path.join(os.path.dirname(__file__), "..", ".."))


TARGET_YEARS = tuple(map(str, range(2024, 2025)))


DIST = os.path.join("..", "tenhou_data")
TRAINING_DATAS = os.path.join(DIST, "test_datas")

model_id = 1


if __name__ == '__main__':

    for dirname in map(lambda x: os.path.join(TRAINING_DATAS, f"model{model_id}", x), TARGET_YEARS):
        listdir = os.listdir(dirname)
        for filename in listdir:
            result = load(os.path.join(dirname, filename))
            if len(list(result)) == 0: continue
            print(list(result))
            print(len(list(result)))
            exit()
        continue

    ...
