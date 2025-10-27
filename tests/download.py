

import os
from TenhouAPI.game_id import GameIdDirectory
from TenhouAPI.game_log import GameLogDirectory


TARGET = "2024"

DIST = os.path.join("..", "tenhou_data")


if __name__ == '__main__':

    ids_dir = GameIdDirectory(os.path.join(DIST, "game_ids", TARGET))

    ids = []
    for filename in ids_dir.listdir():
        ids += ids_dir.extract_game_ids_from_file(filename)
        continue

    log_dir = GameLogDirectory(os.path.join(DIST, "logs", TARGET))

    for id_ in ids:
        log_dir.download_and_install(id_, sleep_time=0.1)
        continue

    ...
