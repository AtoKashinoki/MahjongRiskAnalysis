
# libs
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import joblib
import os


""" Configs """


TARGET_MODEL = 3
TARGET_DEPTH = 19

MODEL_NAME_FORMAT = "decision_tree_classifier_depth{depth}.joblib"
DIST = os.path.join("..", "tenhou_data")


""" Functools """


def generate_tile_names():
    man = [f"{i}Man" for i in range(1, 10)]
    pin = [f"{i}Pin" for i in range(1, 10)]
    sou = [f"{i}Sou" for i in range(1, 10)]
    ji = ["Ton", "Nan", "Sha", "Pei", "Haku", "Hatsu", "Chun"]
    return man + pin + sou + ji


def save_decision_tree_visualization(model_path, output_file_name):

    try:
        clf = joblib.load(model_path)
        tile_names = generate_tile_names()
        features = []

        # 1. モデル1: 公開牌(34), リーチ者打牌(34), 宣言牌(34), 自身打牌(34), ドラ(1)
        features.extend([f"Public_{t}" for t in tile_names])
        features.extend([f"R_Discard_{t}" for t in tile_names])
        features.extend([f"R_Decl_{t}" for t in tile_names])
        features.extend([f"Self_Discard_{t}" for t in tile_names])
        features.append("Is_Dora")  # [cite: 1]

        # 2. モデル2: 種類別個数(4*3), スジ(1), 現物(1)
        types = ["Man", "Pin", "Sou", "Ji"]
        features.extend([f"Public_Type_{t}" for t in types])
        features.extend([f"R_Discard_Type_{t}" for t in types])
        features.extend([f"Self_Discard_Type_{t}" for t in types])
        features.extend(["Is_Suji", "Is_Genbutsu"])  # [cite: 2]

        # 3. モデル3: 壁情報(27)
        # 数牌1-9の3種(27次元)に対応
        suu_pai = [f"{i}{t}" for t in ["Man", "Pin", "Sou"] for i in range(1, 10)]
        features.extend([f"Wall_{s}" for s in suu_pai])  # [cite: 3]

        plt.figure(figsize=(30, 15))
        plot_tree(clf,
                  feature_names=features,
                  class_names=["Safe", "Danger"],
                  filled=True,
                  rounded=True,
                  fontsize=7)

        plt.title(f"Decision Tree Analysis: {output_file_name}")
        plt.savefig(f"{output_file_name}.png", bbox_inches='tight', dpi=300)
        plt.close()

        print(f"REPORT: Visualization with tile names saved as '{output_file_name}.png'.")

    except Exception as e:
        print(f"WARNING: Process failed. Error: {e}")
        ...

    return


""" Main """


if __name__ == '__main__':
    save_decision_tree_visualization(
        os.path.join(DIST, "models", f"model{TARGET_MODEL}", MODEL_NAME_FORMAT.format(depth=TARGET_DEPTH)),
        MODEL_NAME_FORMAT.format(depth=TARGET_DEPTH)
    )
    ...
