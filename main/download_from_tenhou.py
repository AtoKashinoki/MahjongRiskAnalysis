

import os
from urllib.error import HTTPError

from TenhouAPI.game_id import GameIdDirectory
from TenhouAPI.game_log import GameLogDirectory


""" Configs """


YEAR = 2025
MONTH = 12
DIST = os.path.join("..", "tenhou_data")


""" Process """


def main():

    os.chdir(os.path.join(os.path.dirname(__file__), ".."))

    """ Game ids """

    # select directory of game ids
    ids_dir = GameIdDirectory(os.path.join(DIST, "game_ids", str(YEAR)))

    # download game ids from tenhou
    filelist = []
    for day in range(1, 31 + 1):
        try:
            filelist += [
                ids_dir.download_and_install(
                    YEAR, MONTH, day, hour, sleep_time=0.1
                )
                for hour in range(24)
            ]
        except HTTPError as e:
            print(e)
            ...
        continue

    # get game ids
    ids = []
    for filename in filelist:
        ids += ids_dir.extract_game_ids_from_file(filename)
        continue

    """ Game logs """

    # select directory of game logs
    log_dir = GameLogDirectory(os.path.join(DIST, "game_logs", str(YEAR)))

    # download game logs
    ids_len = len(ids)
    for idx, id_ in enumerate(ids):
        log_dir.download_and_install(id_, sleep_time=0.1)
        progress = idx + 1
        print(f"Progress: {progress * 100 / ids_len:.2f}%[{progress}/{ids_len}]")
        continue

    return

""" Main """


if __name__ == '__main__':
    main()
    ...
