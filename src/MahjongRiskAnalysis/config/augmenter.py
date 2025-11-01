"""
Configs that augment game log.
"""
from selectors import SelectSelector
# typing


from typing import (
    List, Union, Tuple
)


# libs


from TenhouAPI.util.config import ConfigBase
from TenhouAPI.config.game_log_tag import DisplayGameLogTag as LogTag
from TenhouAPI.game_log.parse import TagParser

from ..augment.mahjong_log_augmenter_skeleton import MahjongLogAugmenter


""" Augmenter configs
"""


class AugmenterConfig(ConfigBase):
    """
    Configs that augment game log.
    """

    player_num = 4

    tile_kind_num = 9 * (3 if player_num == 4 else 2) + 7
    tile_num = tile_kind_num * 4
    red_doras = tuple((i*9+4)*4 for i in range(3))

    game_attributes = (
        "oya", "display_doras", "reach", "hands", "discard_tiles", "disclosed_tile_nums"
    )

    OUT_OF_LOG_RANGE = "Out of log range"

    @classmethod
    def is_dora(
            cls,
            tile_id: int,
            display_doras: Tuple[int, ...],
    ) -> bool:
        """
        Check if a tile is dora.
        :param tile_id: Tile id that discard.
        :param display_doras: Tile ids of displayed doras.
        :return: Discard tile is dora.
        """
        display_dora_kinds = tuple(map(
            lambda dora_tile_id: dora_tile_id//4,
            display_doras
        ))
        dora_kinds = tuple(map(
            lambda d_dora_k:
                d_dora_k - 8 if d_dora_k%9 == 8 else
                d_dora_k - 3 if d_dora_k == 30 else
                d_dora_k - 2 if d_dora_k == 33 else
                d_dora_k + 1,
            display_dora_kinds
        ))
        return tile_id//4 in dora_kinds or tile_id in cls.red_doras

    @staticmethod
    def is_suji(
            tile_id: int,
            reach_player_discard_tiles: Tuple[int, ...]
    ) -> bool:
        """
        Check if a tile is suji.
        :param tile_id: Tile id that discard.
        :param reach_player_discard_tiles: Discard tiles of reach player.
        :return: Discard tile is suji.
        """
        suji_of_discard_tile = tuple(tile_id + d for d in (-3, 3))
        return 0 != sum(
            tile_id in reach_player_discard_tiles
            for tile_id in suji_of_discard_tile
        )

    @classmethod
    def generate_training_data(
            cls,
            self_player_id: int,
            reach_player_id: int,
            augmenter: MahjongLogAugmenter,
    ) -> str:
        """"""
        """ init training data """

        training_data: List[Union[List[int], int]] = [[], 0]

        """ Explanatory variables """

        # disclosed
        disclosed_tile_nums = list(augmenter.disclosed_tile_nums)

        for tile_id in augmenter.hands[self_player_id]:
            disclosed_tile_nums[tile_id//4] += 1
            continue

        call_tiles = [
            tile_kind_id
            for call_tiles in augmenter.calls[self_player_id]
            for tile_kind_id in call_tiles
        ]
        for tile_kind_id in call_tiles:
            disclosed_tile_nums[tile_kind_id] -= 1
            continue

        for idx in range(len(disclosed_tile_nums)):
            if not disclosed_tile_nums[idx] >= 5: continue
            print(
                "over: ",
                idx,
                disclosed_tile_nums[idx],
                augmenter.calls[self_player_id],
                tuple(map(lambda x: x//4, augmenter.hands[self_player_id]))
            )
            exit()

        training_data[0] += disclosed_tile_nums

        # discard of reach player
        discard_nums = [0 for _ in range(cls.tile_kind_num)]
        for tile_id in augmenter.discard_tiles[reach_player_id]:
            discard_nums[tile_id//4] += 1
            continue
        training_data[0] += discard_nums

        # tile that discard self
        discard_tile = augmenter.discard_tiles[self_player_id][-1]
        discard_tile_vec = [
            0 if not id_ == discard_tile else 1
            for id_ in range(cls.tile_num)
        ]
        training_data[0] += discard_tile_vec

        # discard tile is dora
        training_data[0] += [
            1 if cls.is_dora(discard_tile, augmenter.display_doras) else 0
        ]

        # discard tile is suji
        training_data[0] += [
            1 if cls.is_suji(discard_tile, augmenter.discard_tiles[reach_player_id]) else 0
        ]

        """ Response variable """

        next_tag: TagParser = augmenter.game_log[augmenter.log_index + 1]
        if next_tag == LogTag.AGARI and int(next_tag.attrs["who"]) == reach_player_id:
            training_data[1] = 1
            ...

        """ Return training data """

        return str(training_data) + "\n"

    @classmethod
    def generate_training_datas(
            cls,
            self_player_id: int,
            augmenter: MahjongLogAugmenter,
    ) -> str:
        """
        Generate training data ini augmenter.
        :param self_player_id: id of discard player
        :param augmenter: MahjongRiskAnalysis.augment.game_log.MahjongLogAugmenter
        :return: String of training data
        """

        """ generate training data """

        result = ""
        for player_id, reach in enumerate(augmenter.reach):

            if not reach: continue
            if player_id == self_player_id: continue

            result += cls.generate_training_data(
                self_player_id=self_player_id,
                reach_player_id=player_id,
                augmenter=augmenter,
            )

            continue

        return result

    ...
