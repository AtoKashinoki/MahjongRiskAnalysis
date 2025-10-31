"""
Test code that augment processes.
"""


# libs


import os

from MahjongRiskAnalysis.augment.game_log import augment_and_save_game_log


# constants


TARGET_YEARS = tuple(map(str, range(2024, 2025)))


DIST = os.path.join("..", "tenhou_data")
GAME_LOGS = os.path.join(DIST, "game_logs")
TRAINING_DATAS = os.path.join(DIST, "training_datas")


if __name__ == '__main__':
    for year in TARGET_YEARS:
        target_game_logs = os.path.join(GAME_LOGS, year)
        target_training_datas = os.path.join(TRAINING_DATAS, year)

        listdir = [
            filename
            for filename in os.listdir(target_game_logs)
            if filename[4:8] == year
        ]
        listdir_length = len(listdir)

        for idx, filename in enumerate(listdir):
            print(f"Augmenting: {filename}")
            save_file_path = os.path.join(
                target_training_datas,
                filename.replace("log", "training_data")
            )
            if os.path.exists(save_file_path):
                print(f"File {save_file_path} already exists, skipping.")
                continue
            target = os.path.join(target_game_logs, filename)
            augment_and_save_game_log(target, save_file_path)
            print("Augmented log saved to " + save_file_path)
            progress_num = idx+1
            print(f"Progress: {progress_num*100/listdir_length:.2f}%[{progress_num}/{listdir_length}]")
            continue

        continue

    ...
