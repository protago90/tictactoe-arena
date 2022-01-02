# by protago90
from board import BoardAPI, TicTacToe
from player import PlayerAPI, HumanUI, RandomBot, MinMaxBot, CustomBot, DebutsBot

from collections import Counter
from typing import Callable, Iterable, List, Optional, Tuple


class Player():
    human = HumanUI
    minmax = MinMaxBot
    random = RandomBot
    custom = CustomBot
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


def run_game(board: BoardAPI, x_plyr: PlayerAPI, o_plyr: PlayerAPI, show_api: Optional[Callable]=None) -> Optional[str]:
    plyr = x_plyr
    plyr_n = o_plyr
    while board.is_open():
        pos = plyr.make_move(board)
        board.process_move(plyr.sign, pos)
        if show_api:
            show_api(board.get_state(), plyr.sign)
        plyr, plyr_n = plyr_n, plyr
    return board.get_winner()


def run_gameplay(x_plyr: PlayerAPI, o_plyr: PlayerAPI, show_api: Optional[Callable]=None) -> Optional[str]:
    board = TicTacToe()
    return run_game(board, x_plyr, o_plyr, show_api)


def run_tournament(x_plyr: PlayerAPI, o_plyr: PlayerAPI, progress_api: Iterable) -> Tuple[Optional[str], Tuple[int,int,int]]:
    wins= []
    for _ in progress_api:  # range() alike generated iterable
        wins.append(run_gameplay(x_plyr, o_plyr))
    stats = Counter([win for win in wins])
    x, draw, o = (
        stats.get(idx, 0) for idx in (x_plyr.sign, None, o_plyr.sign))
    win = None if x == o else (x_plyr.sign if x > o else o_plyr.sign) 
    return (win, (x, draw, o))
