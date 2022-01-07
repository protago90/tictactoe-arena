# by protago90
from tictactoe import HumanUI, PlayerAPI, PlayerFcty, recap_game_stats, XOBoard

from argparse import ArgumentParser, Namespace
from typing import Optional, Tuple, Iterable
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
TOURNAMENT = 'TOURNAMENT'
PLAYGROUND = 'PLAYGROUND'
BOARD = '\033[36m{:>17} | {} | {}\033[0m'
GAME = '•‌ "X" \033[1m{}\033[0m -vs- \033[1m{}\033[0m "O".'
STAT = '•‌ Stats: "{}" {} -{}:{}:{}- {} "{}".'
RULE = '•‌ (intefere with game board via numeric keybord.)'
POS  = '•‌ Pick position 1-9: '
PLYR = '•‌ "{}" moves:'
PBAR = '•‌ Games'
WIN  = '•‌ Player "{}" wins the game!\033[91m END∎\n'
END  = '•‌ The game is over with draw.\033[91m END∎\n'
XSIGN = 'X'
OSIGN = 'O'
LF = '\n'
NAP = 1.25


def parse_args() -> Namespace:
    p = ArgumentParser()
    plyrs = PlayerFcty.get_plyrs_id()
    p.add_argument('-x', '--x_player', type=str, default='debuts', required=False, metavar='', choices=plyrs,
                   help=f'"X" player: {plyrs}.')
    p.add_argument('-o', '--o_player', type=str, default='debuts', required=False, metavar='', choices=plyrs,
                   help=f'"O" player: {plyrs}.')
    p.add_argument('-n', '--n_games', type=int, default=0, required=False, metavar='',
                   help='N games in tournament.')
    p.add_argument('-d', '--debug', action='store_true', required=False, 
                   help='Show search bot rationale.')   
    args = p.parse_args()
    if args.n_games > 0:
        if any(_id == HumanUI.ID for _id in (args.x_player, args.o_player)):
            p.error('Human participant is not valid in tournament mode.')
    return args


def show_intro(info: str, x_plyr: PlayerAPI, o_plyr: PlayerAPI) -> None:
    x, o = x_plyr.ID, o_plyr.ID
    msg = [INTRO.format(info), GAME.format(x, o)]
    if any(_id == HumanUI.ID for _id in (x, o)): 
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
    if n > 0 and 'trange' in globals().keys(): 
        return trange(n, desc=msg, leave=True)  # tqdm's external module
    return range(max(n, 1))

def get_human_move() -> int:
    return int(input(POS)) - 1  # internal TicTacToe's board representation is 0-8 array
