"""
Initialize skeleton that augment mahjong log
"""


# typing


from typing import (
    Union, List, Tuple, Set, Dict, Any, Callable, Optional
)


# libs


from abc import ABC, abstractmethod

from TenhouAPI.util.config import ConfigBase
from TenhouAPI.game_log.parse import GameLogParser, TagParser


""" 
"""


class MahjongLogAugmenter(ABC):
    """
    Augment game log class.
    """

    """ augmenter config """

    __augmenter_config: Union[ConfigBase, type[ConfigBase]]

    @property
    @abstractmethod
    def augmenter_config(self) -> ConfigBase: ...

    """ Initializer """

    @abstractmethod
    def __init__(
            self,
            game_log_parser: GameLogParser,
            augmenter_config: ConfigBase = ...,
    ) -> None:
        """
        Initialize mahjong attributes.
        :param game_log_parser: Game log parser.
        :param augmenter_config: Augmenter config.
        """
        return

    """ Game log parser """

    __game_log_parser: GameLogParser
    @property
    @abstractmethod
    def game_log_parser(self) -> GameLogParser: ...

    """ Game attributes """

    __oya: int
    @property
    @abstractmethod
    def oya(self) -> int: ...

    __display_doras: List[int]
    @property
    @abstractmethod
    def display_doras(self) -> Tuple[int, ...]: ...

    @abstractmethod
    def add_dora(self, tile_id: int) -> None:
        """
        Add new dora.
        :param tile_id: Tile id of the dora.
        :return: None
        """
        return

    __reach: List[bool]
    @property
    @abstractmethod
    def reach(self) -> Tuple[bool, ...]: ...

    @abstractmethod
    def on_reach(self, player_id: int) -> None:
        """
        Up flag of reach.
        :param player_id: Player id of the player.
        :return: None
        """
        return

    """ Hands """

    __hands: List[Set[int]]
    @property
    @abstractmethod
    def hands(self) -> Tuple[Set[int], ...]: ...

    @abstractmethod
    def get_hand(self, player_id: int) -> Set[int]:
        """
        Return hand that you select.
        :param player_id: Player id to get.
        :return: Player hand.
        """
        ...

    __calls: List[List[Tuple[int, ...]]]
    @property
    @abstractmethod
    def calls(self) -> Tuple[Tuple[Tuple[int, ...], ...], ...]: return tuple(map(tuple, self.__calls))

    """ Discard tile """

    __discard_tiles: List[List[int]]
    @property
    @abstractmethod
    def discard_tiles(self) -> Tuple[Tuple[int, ...], ...]: ...

    @abstractmethod
    def get_discard_tile(self, player_id: int) -> Tuple[int, ...]:
        """
        Return discard tile that you select.
        :param player_id: Player id to get.
        :return: Player discard tile.
        """
        ...

    """ Disclosed """

    __disclosed_tile_nums: List[int]
    @property
    @abstractmethod
    def disclosed_tile_nums(self) -> Tuple[int, ...]: ...

    """ get attrs """

    @abstractmethod
    def get_all_attrs(self) -> Dict[str, Any]:
        """
        Return all attributes of game.
        :return: Attributes of game.
        """
        ...

    """ Tag processes """

    @abstractmethod
    def __init_tag(
            self,
            init_tag: TagParser,
    ) -> None:
        """
        Processes of init tag.
        :param init_tag: Tag parser of init tag.
        :return: None
        """
        return

    @abstractmethod
    def __draw_tag(
            self,
            draw_tag: TagParser,
    ) -> None:
        """
        Processes of draw tag.
        :param draw_tag: Tag parser of draw tag.
        :return: None
        """
        return

    @abstractmethod
    def __discard_tag(
            self,
            discard_tag: TagParser,
    ) -> str:
        """
        Processes of discard tag.
        :param discard_tag:
        :return: String of training data.
        """
        ...

    @abstractmethod
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
        return

    @abstractmethod
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
        return

    @abstractmethod
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

    @abstractmethod
    def __naki_tag(
            self,
            naki_tag: TagParser,
    ) -> None:
        """
        Processes of naki tag.
        :param naki_tag: Tag parser of naki tag.
        :return: None
        """
        return

    @abstractmethod
    def __open_dora(
            self,
            open_dora_tag: TagParser,
    ) -> None:
        """
        Processes of open dora.
        :param open_dora_tag: Tag parser of open dora.
        :return: None
        """
        return

    """ Proceed game """

    __game_log: List[TagParser]
    @property
    @abstractmethod
    def game_log(self) -> Tuple[TagParser, ...]: ...

    __log_index: int
    @property
    @abstractmethod
    def log_index(self) -> int: ...

    __PROCEED_METHODS: Dict[str, Callable[[TagParser], Optional[str]]]

    @abstractmethod
    def __proceed_game_process(self) -> Optional[str]:
        """
        Proceed game from game log.
        :return: String of training data or TagParser.
        """
        ...

    @abstractmethod
    def proceed_game(self) -> str:
        """
        Proceed game from game log.
        :return: String of training data.
        """
        ...

    ...
