# by protago90
from tictactoe.player import PlayerAPI, HumanUI, DebutsBot, MinMaxBot, SearchBot, RandomBot

from collections import Counter
from typing import Callable, List, Optional, Sequence, Tuple


class PlayerF():
    human = HumanUI
    minmax = MinMaxBot
    random = RandomBot
    search = SearchBot
    debuts = DebutsBot

    @classmethod
    def set(cls, idx: str, sign: str, nap: Optional[float]=None, human_api: Optional[Callable]=None) -> PlayerAPI:
        plyr = getattr(cls, idx)
        if plyr.ID == HumanUI.ID:
            return plyr(sign=sign, human_api=human_api)
        return plyr(sign=sign, nap=nap)

    @classmethod
    def list(cls) -> List[str]:
        return [attr.ID.lower() for idx, attr in cls.__dict__.items() 
                if not idx.startswith('__') and callable(attr)]


def recap_game_stats(rec: Sequence[str], x_plyr: PlayerAPI, o_plyr: PlayerAPI) -> Tuple[str, Tuple[int,int,int]]:
    cum = Counter([win for win in rec])
    x, draw, o = (
        cum.get(idx, 0) for idx in (x_plyr.sign, None, o_plyr.sign))
    win = None if x == o else (x_plyr.sign if x > o else o_plyr.sign) 
    return (win, (x, draw, o))
