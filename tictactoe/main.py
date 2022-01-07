# by protago90
from tictactoe.player import DebutsBot, HumanUI, MinMaxBot, PlayerAPI, RandomBot, SearchBot

from collections import Counter
from typing import Callable, List, Optional, Tuple


class PlayerFcty():
    # TODO: rethink pattern: factory's attributes names are hardcoded with encapsulated classes 'ID' attributes values
    human = HumanUI
    minmax = MinMaxBot
    random = RandomBot
    search = SearchBot
    debuts = DebutsBot

    @classmethod
    def set(cls, name: str, sign: str, nap: Optional[float]=None, human_api: Optional[Callable]=None) -> PlayerAPI:
        plyr = getattr(cls, name)
        if plyr.ID == HumanUI.ID:
            return plyr(sign=sign, human_api=human_api)
        return plyr(sign=sign, nap=nap)

    @classmethod
    def get_plyrs_id(cls) -> List[str]:
        return [attr.ID for name, attr in cls.__dict__.items() 
                if not name.startswith('__') and callable(attr)]


def recap_game_stats(rec: List[Optional[str]], x_plyr: PlayerAPI, o_plyr: PlayerAPI) -> Tuple[Optional[str], Tuple[int,int,int]]:
    cum = Counter([win for win in rec])
    x, draw, o = (
        cum.get(sign, 0) for sign in (x_plyr.sign, None, o_plyr.sign))
    win = None if x == o else (x_plyr.sign if x > o else o_plyr.sign) 
    return (win, (x, draw, o))
