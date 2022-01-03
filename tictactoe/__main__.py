#!/usr/bin/python
# by protago90
from game import Player, run_gameplay, run_tournament
from player import PlayerAPI, HumanUI

from typing import Optional, Tuple, Iterable
import argparse
try: 
    from tqdm import trange # type: ignore # install is optional
except: pass


INTRO = '''\033[91m
Welcome in:\033[1m
 _____ _     _____         _____          
|_   _(_) __|_   _|_ _  __|_   _|__   ___ 
  | | | |/ __|| |/ _` |/ __|| |/ _ \ / _ \\
  | | | | (__ | | (_| | (__ | | (_) |  __/
  |_| |_|\___||_|\__,_|\___||_|\___/ \___|\033[0m\033[91m {}!\033[0m
'''
BOARD = '\033[36m{:>17} | {} | {}\033[0m'
GAME = '•‌ "X" \033[1m{}\033[0m -vs- \033[1m{}\033[0m "O".'
STAT = '•‌ Stats: "{}" {} -{}:{}:{}- {} "{}".'
RULE = '•‌ (intefere with game board via numeric keybord.)'
POS  = '•‌ Pick position 1-9: '
PLYR = '•‌ "{}" moves:'
BAR  = '•‌ Games'
WIN  = '•‌ Player "{}" wins the game!\033[91m END∎\n'
END  = '•‌ The game is over with draw.\033[91m END∎\n'
LF = '\n'
NAP = 1.25


def parse_args():
    p = argparse.ArgumentParser()
    plyrs = Player.list()
    p.add_argument('-x', '--x_player', type=str, default='custom', required=False, metavar='', choices=plyrs,
                   help=f'"X" player: {plyrs}.')
    p.add_argument('-o', '--o_player', type=str, default='custom', required=False, metavar='', choices=plyrs,
                   help=f'"O" player: {plyrs}.')
    p.add_argument('-n', '--n_games', type=int, default=0, required=False, metavar='',
                   help='N games in tournament.')
    p.add_argument('-d', '--debug', action='store_true', required=False, 
                   help='Show search bot rationale.')   
    args = p.parse_args()
    if args.n_games > 0:
        if any(idx == HumanUI.ID.lower() for idx in (args.x_player, args.o_player)):
            p.error('Human participant is not valid in tournament mode.')
    return args


def show_intro(info: str, x_plyr: PlayerAPI, o_plyr: PlayerAPI) -> None:
    x, o = x_plyr.ID, o_plyr.ID
    msg = [INTRO.format(info), GAME.format(x, o)]
    if any(idx == HumanUI.ID for idx in (x, o)): 
        msg.append(RULE)
        for a, b, c in [list(range(i*3+1, i*3+4)) for i in range(3)][::-1]:
            msg.append(BOARD.format(a, b, c))
    print(*msg, sep=LF)

def show_end(sign: Optional[str]) -> None:
    msg = WIN.format(sign) if sign else END
    print(msg)

def show_stats(x_plyr: PlayerAPI, o_plyr: PlayerAPI, stats: Tuple[int,int,int]) -> None:
    msg = STAT.format(x_plyr.sign, x_plyr.ID, *stats, o_plyr.ID, o_plyr.sign)
    print(msg)

def show_board(board: list, sign: str) -> None:
    msg = [PLYR.format(sign)]
    for a, b, c in board: 
        msg.append(BOARD.format(a, b, c))
    print(*msg, sep=LF)


def set_progress_bar(msg: str, n: int) -> Iterable:
    if 'trange' in globals().keys(): 
        return trange(n, desc=msg, leave=True)  # tqdm's external module
    return range(n)

def get_human_move() -> int:
    return int(input(POS)) - 1  # internal TicTacToe's board representation is 0-8 array


if __name__ == '__main__':
    args = parse_args()
    x_mode = (args.x_player, 'X')
    o_mode = (args.o_player, 'O')
    n = abs(args.n_games)

    if n == 0:
        x_plyr = Player.set(*x_mode, nap=NAP, human_api=get_human_move)
        o_plyr = Player.set(*o_mode, nap=NAP, human_api=get_human_move)
        show_intro('GAMEPLAY', x_plyr, o_plyr)
        win = run_gameplay(x_plyr, o_plyr, show_api=show_board)
        show_end(win)

    else:
        x_plyr = Player.set(*x_mode)
        o_plyr = Player.set(*o_mode)
        show_intro('TOURNAMENT', x_plyr, o_plyr)
        win, stats = run_tournament(x_plyr, o_plyr, progress_api=set_progress_bar(BAR, n))
        show_stats(x_plyr, o_plyr, stats)
        show_end(win)
