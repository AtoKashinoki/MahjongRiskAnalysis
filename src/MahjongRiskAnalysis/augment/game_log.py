"""
Tools that augment game log of tenhou.
"""
import os
# typing


from typing import (
    Tuple, List, Set, Union, Dict, Any, Optional, Callable, Iterator
)


# libs


from TenhouAPI.game_log.parse import GameLogParser, TagParser, parse_m_attribute
from TenhouAPI.config.game_log_tag import DisplayGameLogTag as LogTag
from TenhouAPI.config.game_log_tag import DisplayCalls as Calls

from .mahjong_log_augmenter_skeleton import MahjongLogAugmenter as Augmenter
from ..config.augmenter import AugmenterConfig


""" Augment game log
"""


""" mahjong processes """


class MahjongLogAugmenter(Augmenter):
    """
    Augment game log class.
    """

    """ augmenter config """

    __augmenter_config: Union[AugmenterConfig, type[AugmenterConfig]] =\
        AugmenterConfig

    @property
    def augmenter_config(self) -> AugmenterConfig: return self.__augmenter_config

    """ Initializer """

    def __init__(
            self,
            game_log_parser: GameLogParser,
            augmenter_config: AugmenterConfig = AugmenterConfig()
    ) -> None:
        """
        Initialize mahjong attributes.
        :param game_log_parser: Game log parser.
        :param augmenter_config: Augmenter config.
        """

        self.__game_log_parser = game_log_parser
        self.__game_log = [
            tag
            for game_log in game_log_parser.game_logs
            for tag in game_log
        ]

        self.__augmenter_config = augmenter_config

        self.__log_index = -1
        return

    """ Game log parser """

    __game_log_parser: GameLogParser
    @property
    def game_log_parser(self) -> GameLogParser: return self.__game_log_parser

    """ Game attributes """

    __oya: int
    @property
    def oya(self) -> int: return self.__oya

    __display_doras: List[int]
    @property
    def display_doras(self) -> Tuple[int, ...]: return tuple(self.__display_doras)

    def add_dora(self, tile_id: int) -> None:
        """
        Add new dora.
        :param tile_id: Tile id of the dora.
        :return: None
        """
        self.__display_doras.append(tile_id)
        return

    __reach: List[bool]
    @property
    def reach(self) -> Tuple[bool, ...]: return tuple(self.__reach)

    def on_reach(self, player_id: int) -> None:
        """
        Up flag of reach.
        :param player_id: Player id of the player.
        :return: None
        """
        self.__reach[player_id] = True
        return

    """ Hands """

    __hands: List[Set[int]]
    @property
    def hands(self) -> Tuple[Set[int], ...]: return tuple(self.__hands)

    def get_hand(self, player_id: int) -> Set[int]:
        """
        Return hand that you select.
        :param player_id: Player id to get.
        :return: Player hand.
        """
        return self.__hands[player_id]

    __calls: List[List[Tuple[int, ...]]]
    @property
    def calls(self) -> Tuple[Tuple[Tuple[int, ...], ...], ...]: return tuple(map(tuple, self.__calls))

    """ Discard tile """

    __discard_tiles: List[List[int]]
    @property
    def discard_tiles(self) -> Tuple[Tuple[int, ...], ...]:
        return tuple(map(tuple, self.__discard_tiles))

    def get_discard_tile(self, player_id: int) -> Tuple[int, ...]:
        """
        Return discard tile that you select.
        :param player_id: Player id to get.
        :return: Player discard tile.
        """
        return tuple(self.__discard_tiles[player_id])

    """ Disclosed """

    __disclosed_tile_nums: List[int]
    @property
    def disclosed_tile_nums(self) -> Tuple[int, ...]: return tuple(self.__disclosed_tile_nums)

    """ get attrs """

    def get_all_attrs(self) -> Dict[str, Any]:
        """
        Return all attributes of game.
        :return: Attributes of game.
        """
        return {
            key: getattr(self, key)
            for key in self.__augmenter_config.game_attributes
        }

    """ Tag processes """

    def __init_tag(
            self,
            init_tag: TagParser,
    ) -> None:
        """
        Processes of init tag.
        :param init_tag: Tag parser of init tag.
        :return: None
        """
        """ get attrs """
        attrs = init_tag.attrs

        """ assign attributes """
        # oya id
        self.__oya = int(int(attrs["oya"]))

        # dora
        self.__display_doras = [int(attrs["seed"].split(",")[-1])]

        # reach
        self.__reach = [False for _ in range(self.__augmenter_config.player_num)]

        # hand
        self.__hands = [
            set([int(id_txt) for id_txt in attrs[f"hai{idx}"].split(",") if not id_txt == ""])
            for idx in range(self.__augmenter_config.player_num)
        ]
        self.__calls = [[] for _ in range(self.__augmenter_config.player_num)]

        # discard
        self.__discard_tiles = [[] for _ in range(self.__augmenter_config.player_num)]

        # disclose
        self.__disclosed_tile_nums = [
            0 for _ in range(self.__augmenter_config.tile_kind_num)
        ]
        self.__disclosed_tile_nums[self.__display_doras[-1] // 4] += 1
        return None

    def __draw_tag(
            self,
            draw_tag: TagParser,
    ) -> None:
        """
        Processes of draw tag.
        :param draw_tag: Tag parser of draw tag.
        :return: None
        """

        # search player id
        player_id = 0
        for player_id, key in enumerate(LogTag.DRAWS):
            if not draw_tag == key: continue
            break

        # add tile
        self.__hands[player_id].add(int(draw_tag.attrs["id"]))

        return

    def __discard_tag(
            self,
            discard_tag: TagParser,
    ) -> str:
        """
        Processes of discard tag.
        :param discard_tag:
        :return: String of training data.
        """

        # search player id
        player_id = 0
        for player_id, key in enumerate(LogTag.DISCARDS):
            if not discard_tag == key: continue
            break

        # remove tile from hand
        target_id = int(discard_tag.attrs["id"])
        self.__hands[player_id].remove(target_id)

        # discard tile
        self.__discard_tiles[player_id].append(target_id)
        self.__disclosed_tile_nums[target_id//4] += 1

        return self.__augmenter_config.__class__.generate_training_datas(player_id, self)

    def __reach_tag(
            self,
            reach_tag: TagParser,
    ) -> None:
        """
        Processes of reach tag.
        :param reach_tag: Tag parser of reach tag.
        :return: None
        """
        if not int(reach_tag.attrs["step"]) == 2: return
        self.on_reach(int(reach_tag.attrs["who"]))
        return

    def __naki_of_kakan(
            self,
            naki_tag: TagParser,
            parsed_m: Dict[str, Union[int, str, Dict[str, Union[int, Tuple[int, ...]]]]],
            call_player_id: int,
    ) -> None:
        """
        Processes naki tag of kakan.
        :param naki_tag: Tag parser of naki tag.
        :param parsed_m: Parsed m attribute.
        :param call_player_id: Player id to call.
        :return: None
        """

        # add tile in calls
        details = parsed_m["details"]
        self.__calls[call_player_id].append(tuple(map(int, details["tiles"])))

        # add disclosed tiles
        self.__disclosed_tile_nums[int(details["tiles"][0])] += 1

        return

    def __naki_of_kan(
            self,
            naki_tag: TagParser,
            parsed_m: Dict[str, Union[int, str, Dict[str, Union[int, Tuple[int, ...]]]]],
            call_player_id: int,
    ) -> None:
        """
        Processes naki tag of kan.
        :param naki_tag: Tag parser of naki tag.
        :param parsed_m: Parsed m attribute.
        :param call_player_id: Player id to call.
        :return: None
        """

        """ check kan type"""

        # Get pre discard or draw tag
        pre_tag = self.__game_log[self.__log_index-1]
        if pre_tag == LogTag.REACH:
            pre_tag = self.__game_log[self.__log_index-2]
            ...

        # minkan process
        if pre_tag in LogTag.DISCARDS:
            self.__naki_of_other(naki_tag, parsed_m, call_player_id)
            return

        """ annkann process """

        # add tile in calls
        tiles = parsed_m["details"]["tiles"]
        self.__calls[call_player_id].append(tiles)

        # add disclosed tiles
        for tile_kind_id in tiles:
            self.__disclosed_tile_nums[tile_kind_id] += 1
            continue

        return

    def __naki_of_other(
            self,
            naki_tag: TagParser,
            parsed_m: Dict[str, Union[int, str, Dict[str, Union[int, Tuple[int, ...]]]]],
            call_player_id: int,
    ) -> None:
        """
        Processes naki tag of other call.
        :param naki_tag: Tag parser of naki tag.
        :param parsed_m: Parsed m attribute.
        :param call_player_id: Player id to call.
        :return: None
        """

        # get pre discard tag
        pre_discard_tag = None
        for i in range(1, 4):
            if pre_discard_tag in LogTag.DISCARDS: break
            pre_discard_tag = self.__game_log[self.__log_index - i]
            continue

        # add called tile in hand
        self.__hands[call_player_id].add(
            int(pre_discard_tag.attrs["id"])
        )

        # add tile in calls
        details = parsed_m["details"]
        tiles = details["tiles"]
        self.__calls[call_player_id].append(tiles)

        # generate open tiles
        called_idx = details["called_idx"]
        new_disclosed_tiles = tuple(
            int(tile_kind_id)
            for idx, tile_kind_id in enumerate(tiles)
            if not idx == called_idx
        )

        # add disclosed tiles
        for tile_kind_id in new_disclosed_tiles:
            self.__disclosed_tile_nums[tile_kind_id] += 1
            continue

        return

    def __naki_tag(
            self,
            naki_tag: TagParser,
    ) -> None:
        """
        Processes of naki tag.
        :param naki_tag: Tag parser of naki tag.
        :return: None
        """


        # get calling player
        call_player_id = int(naki_tag.attrs["who"])

        # parse m attribute
        result = parse_m_attribute(int(naki_tag.attrs["m"]))

        # call processes
        call_type = result["type"]
        if call_type == Calls.KAKAN:
            self.__naki_of_kakan(naki_tag, result, call_player_id)
            return
        if call_type == Calls.KAN:
            self.__naki_of_kan(naki_tag, result, call_player_id)
            return

        self.__naki_of_other(naki_tag, result, call_player_id)
        return

    def __open_dora(
            self,
            open_dora_tag: TagParser,
    ) -> None:
        """
        Processes of open dora.
        :param open_dora_tag: Tag parser of open dora.
        :return: None
        """
        self.__display_doras.append(int(open_dora_tag.attrs["hai"]))
        return

    """ Proceed game """

    __game_log: List[TagParser]
    @property
    def game_log(self) -> Tuple[TagParser, ...]: return tuple(self.__game_log)

    __log_index: int
    @property
    def log_index(self) -> int: return self.__log_index

    __PROCEED_METHODS: Dict[str, Callable[[TagParser], Optional[str]]] = dict(zip(
        [
            LogTag.DRAWS, LogTag.DISCARDS, LogTag.NAKI,
            LogTag.REACH, LogTag.INIT, LogTag.OPEN_DORA
        ],
        [
            __draw_tag, __discard_tag, __naki_tag,
            __reach_tag, __init_tag, __open_dora,
        ]
    ))

    def __proceed_game_process(self) -> Optional[str]:
        """
        Proceed game from game log.
        :return: String of training data or TagParser.
        """

        """ Proceed tag index """

        self.__log_index += 1
        if not self.__log_index < len(self.__game_log):
            return self.__augmenter_config.OUT_OF_LOG_RANGE

        """ Get tag """

        tag = self.__game_log[self.__log_index]

        """ Processing each tags """

        for key, method in self.__PROCEED_METHODS.items():
            if str(tag) not in key: continue
            return method(self, tag)

        return None

    def proceed_game(self) -> str:
        """
        Proceed game from game log.
        :return: String of training data.
        """
        result = self.__proceed_game_process()

        if not isinstance(result, str):
            return self.proceed_game()

        return result

    def __next__(self):
        """
        Proceed game from game log.
        :return: String of training data.
        """
        return self.proceed_game()

    """ iterator process """

    def __iter__(self) -> Iterator[TagParser]:
        return iter(self.__game_log)

    def __len__(self) -> int:
        return sum([
            1
            for tag in self.__game_log
            if tag in LogTag.DISCARDS
        ])

    ...


""" augment file """


def augment_and_save_game_log(
        game_log_file_path: str,
        save_file_path: str,
        parser: type[GameLogParser] = GameLogParser,
        augmenter: type[MahjongLogAugmenter] = MahjongLogAugmenter,
) -> str:
    """
    Augment game log and save it to file.
    :param game_log_file_path: Game log file path.
    :param save_file_path: Save file path.
    :param parser: File of game log parser.
    :param augmenter: Augmenter class.
    :return: Save file path.
    """

    """ Parse file """

    parsed_file = parser(game_log_file_path)

    """ Augment game log and generate training data """

    augmenter = augmenter(parsed_file)

    training_data_string = ""
    for _ in range(len(augmenter)):
        training_data_string += next(augmenter)
        continue

    """ save training data """

    # check directory
    dirname = os.path.dirname(save_file_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        ...

    # save
    with open(save_file_path, "w") as f:
        f.write(training_data_string)
        ...

    return save_file_path
