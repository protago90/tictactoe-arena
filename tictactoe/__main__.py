#!/usr/bin/python
# by protago90
from tictactoe import PlayerF, recap_game_stats, XOBoard
from tictactoe.cli import *  # precomposed cli scirpt utils


if __name__ == '__main__':
    args = parse_args()
    mode, p = TOURNAMENT, {}
    if args.n_games == 0: 
        mode, p = PLAYGROUND, {'nap':NAP, 'human_api': get_human_move}
    x_plyr = PlayerF.set(args.x_player, 'X', **p)
    o_plyr = PlayerF.set(args.o_player, 'O', **p)
    
    show_intro(mode, x_plyr, o_plyr)
    rec = []
    for _ in set_progress_bar(BAR, args.n_games):
        board = XOBoard()
        plyr = x_plyr
        plyr_n = o_plyr
        while board.is_open():
            pos = plyr.make_move(board)
            board.process_move(plyr.sign, pos)
            if mode == PLAYGROUND: 
                show_board(board.get_state(), plyr.sign)
            plyr, plyr_n = plyr_n, plyr
        rec.append(board.get_winner())
    win, stats = recap_game_stats(rec, x_plyr, o_plyr)
    if mode == TOURNAMENT: 
        show_stats(x_plyr, o_plyr, stats)
    show_end(win)
