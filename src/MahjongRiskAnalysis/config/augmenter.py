"""
Configs that augment game log.
"""

# typing


from typing import (
    List, Tuple, Optional
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

    @classmethod
    def is_suji(
            cls,
            tile_id: int,
            reach_player_discard_tiles: List[int]
    ) -> bool:
        """
        Check if a tile is suji.
        :param tile_id: Tile id that discard.
        :param reach_player_discard_tiles: Discard tiles of reach player.
        :return: Discard tile is suji.
        """
        suji_of_discard_tile = tuple(tile_id//4 + d for d in (-3, 3))
        return 0 != sum(
            reach_player_discard_tiles[tile] > 0
            for tile in suji_of_discard_tile
            if 0 <= tile < len(reach_player_discard_tiles)
        )

    @classmethod
    def is_genbutu(
            cls,
            tile_id: int,
            reach_player_discard_tiles: List[int]
    ) -> bool:
        """
        Check if a tile is genbutu.
        :param tile_id: Tile id that discard.
        :param reach_player_discard_tiles: Discard tiles of reach player.
        :return: Discard tile is genbutu.
        """
        return reach_player_discard_tiles[tile_id // 4] != 0

    @classmethod
    def generate_disclosed_data(
            cls,
            self_player_id: int,
            augmenter: MahjongLogAugmenter,
    ) -> List[int]:
        """
        Generate training data of disclosed.
        :param self_player_id: Target player id that generate training data.
        :param augmenter: Mahjong log augmenter.
        :return: Generated training data of disclosed.
        """

        disclosed_tile_nums = list(augmenter.disclosed_tile_nums)

        for tile_id in augmenter.hands[self_player_id]:
            disclosed_tile_nums[tile_id // 4] += 1
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
                tuple(map(lambda x: x // 4, augmenter.hands[self_player_id]))
            )
            exit()

        return disclosed_tile_nums

    @classmethod
    def generate_discard_data(
            cls,
            target_player_id: int,
            augmenter: MahjongLogAugmenter,
    ) -> List[int]:
        """
        Generate training data that target player discard.
        :param target_player_id: Target player id that generate training data.
        :param augmenter: Mahjong log augmenter.
        :return: Generated training data of discard.
        """

        discard_nums = [0 for _ in range(cls.tile_kind_num)]
        for tile_id in augmenter.discard_tiles[target_player_id]:
            discard_nums[tile_id//4] += 1
            continue

        return discard_nums

    @classmethod
    def generate_called_reach(
            cls,
            reach_player_id: int,
            augmenter: MahjongLogAugmenter,
    ) -> List[int]:
        """
        Generate training data that reach plyer discard tile calling reach.
        :param reach_player_id: Target player id that generate training data.
        :param augmenter: Mahjong log augmenter.
        :return: Generated training data of calling reach.
        """
        reach_tile_kind_id = augmenter.reach[reach_player_id] // 4
        calling_reach_tile_vec = [
            1 if idx == reach_tile_kind_id else 0
            for idx in range(cls.tile_kind_num)
        ]
        if not sum(calling_reach_tile_vec) == 1: exit()
        return calling_reach_tile_vec

    @classmethod
    def generate_discard_now(
            cls,
            self_player_id: int,
            augmenter: MahjongLogAugmenter,
    ) -> Tuple[List[int], int]:
        """
        Generate training data that target player discard now.
        :param self_player_id: Target player id that generate training data.
        :param augmenter: Mahjong log augmenter.
        :return: Generated training data of discard now and discard tile id.
        """

        discard_tile = augmenter.discard_tiles[self_player_id][-1]
        discard_tile_vec = [
            0 if not id_ == discard_tile//4 else 1
            for id_ in range(cls.tile_kind_num)
        ]
        if sum(discard_tile_vec) == 0: exit()

        return discard_tile_vec, discard_tile

    @classmethod
    def generate_is_dora(
            cls,
            target_tile: int,
            augmenter: MahjongLogAugmenter,
    ) -> List[int]:
        """
        Generate training data that target tile is dora.
        :param target_tile: Tile id to check.
        :param augmenter: Mahjong log augmenter.
        :return: Generated training data that target tile is dora.
        """
        return [
            1 if cls.is_dora(target_tile, augmenter.display_doras) else 0
        ]

    @classmethod
    def generate_is_suji(
            cls,
            target_tile: int,
            reach_player_discards: List[int],
    ) -> List[int]:
        """
        Generate training data that target tile is suji.
        :param target_tile: Tile id to check.
        :param reach_player_discards: Reach player discard tiles.
        :return: Generated training data that target tile is suji.
        """
        return [
            1 if cls.is_suji(target_tile, reach_player_discards) else 0
        ]

    @classmethod
    def generate_is_genbutu(
            cls,
            target_tile: int,
            reach_player_discards: List[int],
    ) -> List[int]:
        """
        Generate training data that target tile is genbutu.
        :param target_tile: Tile id to check.
        :param reach_player_discards: Reach player discard tiles.
        :return: Generated training data that target tile is genbutu.
        """
        return [
            1 if cls.is_genbutu(target_tile, reach_player_discards) else 0
        ]

    @classmethod
    def generate_tile_types(
            cls,
            target_tile_nums: List[int],
    ) -> List[int]:
        """
        Generate training data that target tile is type.
        :param target_tile_nums: Tile numbers to check.
        :return: Generated training data that target tile is type.
        """
        result = [0, 0, 0, 0]
        for tile_id, num in enumerate(target_tile_nums):
            result[tile_id//9] += num
            continue
        return result

    @classmethod
    def generate_kabe(
            cls,
            disclosed_tile_nums: List[int],
    ) -> List[int]:
        """
        Generate training data that kabe vec.
        :param disclosed_tile_nums: Tile numbers to discard.
        :return: Generated training data that target tile is kabe.
        """
        return [
            0 if not disclosed_tile_num == 4 else 1
            for tile_id, disclosed_tile_num in enumerate(disclosed_tile_nums)
            if tile_id < 27
        ]

    @classmethod
    def generate_model1_training_data(
            cls,
            self_player_id: int,
            reach_player_id: int,
            augmenter: MahjongLogAugmenter,
    ) -> Tuple[List[int], int]:
        """
        Generate training data of model1.
        :param self_player_id: Target player id that generate training data.
        :param reach_player_id: Reach player id that generate training data.
        :param augmenter: Mahjong log augmenter.
        :return: Generated training data of model1 and discard tile id.
        """

        # init training data
        training_data = []

        # disclosed
        training_data += cls.generate_disclosed_data(
            self_player_id,
            augmenter,
        )

        # discard of reach player
        training_data += cls.generate_discard_data(
            reach_player_id,
            augmenter,
        )

        # discard tile of called reach
        training_data += cls.generate_called_reach(
            reach_player_id,
            augmenter,
        )

        # tile that discard self
        discard_now_training, discard_tile = cls.generate_discard_now(
            self_player_id,
            augmenter,
        )
        training_data += discard_now_training

        # discard tile is dora
        training_data += cls.generate_is_dora(discard_tile, augmenter)

        return training_data, discard_tile

    @classmethod
    def generate_model2_training_data(
            cls,
            self_player_id: int,
            reach_player_id: int,
            augmenter: MahjongLogAugmenter,
    ) -> List[int]:
        """
        Generate training data of model2.
        :param self_player_id: Target player id that generate training data.
        :param reach_player_id: Reach player id that generate training data.
        :param augmenter: Mahjong log augmenter.
        :return: Generated training data of model2.
        """

        # init training data
        training_data = []

        # disclosed
        disclosed_tile_nums = cls.generate_disclosed_data(
            self_player_id,
            augmenter,
        )
        training_data += disclosed_tile_nums
        training_data += cls.generate_tile_types(disclosed_tile_nums)

        # discard of reach player
        reach_player_discards = cls.generate_discard_data(
            reach_player_id,
            augmenter,
        )
        training_data += reach_player_discards
        training_data += cls.generate_tile_types(reach_player_discards)

        # discard tile of called reach
        training_data += cls.generate_called_reach(
            reach_player_id,
            augmenter,
        )

        # tile that discard self
        discard_now_training, discard_tile = cls.generate_discard_now(
            self_player_id,
            augmenter,
        )
        training_data += discard_now_training
        training_data += cls.generate_tile_types(discard_now_training)

        # discard tile is dora
        training_data += cls.generate_is_dora(discard_tile, augmenter)

        # discard tile is suji
        training_data += cls.generate_is_suji(discard_tile, reach_player_discards)

        # discard tile is genbutu
        training_data += cls.generate_is_genbutu(discard_tile, reach_player_discards)

        return training_data

    @classmethod
    def generate_model3_training_data(
            cls,
            self_player_id: int,
            reach_player_id: int,
            augmenter: MahjongLogAugmenter,
    ) -> List[int]:
        """
        Generate training data of model3.
        :param self_player_id: Target player id that generate training data.
        :param reach_player_id: Reach player id that generate training data.
        :param augmenter: Mahjong log augmenter.
        :return: Generated training data of model3.
        """

        # init training data
        training_data = []

        # disclosed
        disclosed_tile_nums = cls.generate_disclosed_data(
            self_player_id,
            augmenter,
        )
        training_data += disclosed_tile_nums
        training_data += cls.generate_tile_types(disclosed_tile_nums)

        # discard of reach player
        reach_player_discards = cls.generate_discard_data(
            reach_player_id,
            augmenter,
        )
        training_data += reach_player_discards
        training_data += cls.generate_tile_types(reach_player_discards)

        # discard tile of called reach
        training_data += cls.generate_called_reach(
            reach_player_id,
            augmenter,
        )

        # tile that discard self
        discard_now_training, discard_tile = cls.generate_discard_now(
            self_player_id,
            augmenter,
        )
        training_data += discard_now_training
        training_data += cls.generate_tile_types(discard_now_training)

        # discard tile is dora
        training_data += cls.generate_is_dora(discard_tile, augmenter)

        # discard tile is suji
        training_data += cls.generate_is_suji(discard_tile, reach_player_discards)

        # discard tile is genbutu
        training_data += cls.generate_is_genbutu(discard_tile, reach_player_discards)

        # kabe
        training_data += cls.generate_kabe(disclosed_tile_nums)

        return training_data


    @classmethod
    def generate_training_data(
            cls,
            self_player_id: int,
            reach_player_id: int,
            augmenter: MahjongLogAugmenter,
    ) -> Tuple[int, ...]:
        """
        Generate training data.
        :param self_player_id: Target player id that generate training data.
        :param reach_player_id: Player id that reach player.
        :param augmenter: MahjongLogAugmenter.
        :return: Generated training data.
        """

        """ Select training data generator """

        # TODO: Select function that training data of model
        generate_training_data = cls.generate_model3_training_data(
            self_player_id,
            reach_player_id,
            augmenter,
        )
        
        """ Explanatory variables """

        # base training data
        training_data = generate_training_data(
            self_player_id,
            reach_player_id,
            augmenter,
        )

        """ Response variable """

        next_tag: TagParser = augmenter.game_log[augmenter.log_index + 1]
        training_data += [
            1
            if (
                    next_tag == LogTag.AGARI and
                    int(next_tag.attrs["who"]) == reach_player_id
            ) else
            0
        ]

        """ Return training data """
        return tuple(training_data)

    @classmethod
    def generate_training_datas(
            cls,
            self_player_id: int,
            augmenter: MahjongLogAugmenter,
    ) -> Optional[Tuple[Tuple[int, ...], ...]]:
        """
        Generate training data ini augmenter.
        :param self_player_id: id of discard player
        :param augmenter: MahjongRiskAnalysis.augment.game_log.MahjongLogAugmenter
        :return: String of training data
        """

        """ generate training data """

        result: List[Tuple[int, ...]] = []
        for player_id, reach_tile_id in enumerate(augmenter.reach):

            if not isinstance(reach_tile_id, int): continue
            if player_id == self_player_id: continue

            datas = cls.generate_training_data(
                self_player_id=self_player_id,
                reach_player_id=player_id,
                augmenter=augmenter,
            )
            result.append(datas)
            continue

        if len(result) == 0:
            return None

        return tuple(result)

    ...
