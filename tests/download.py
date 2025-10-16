

import os
from TenhouAPI.util import download


TARGET = "2024"


DIST = os.path.join("..", "Tenhou")
ID_DIST = os.path.join(DIST, "game_ids")
LOG_DIST = os.path.join(DIST, "game_logs")
GZ_FILES = os.path.join(DIST, "gz", TARGET)

if __name__ == '__main__':

    game_id_dist = download.GameID(ID_DIST)

    all_ids = game_id_dist.extract_game_ids_from_directory(GZ_FILES)

    game_log_dist = download.GameLog(LOG_DIST)

    for ids in all_ids.values():
        for id_ in ids:
            game_log_dist.run_all_processes(id_, 0.1)
            continue
        continue

    ...
