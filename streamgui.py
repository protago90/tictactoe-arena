# by protago09
from tictactoe import HumanUI, PlayerFcty, recap_game_stats, XOBoard

from PIL import Image
from typing import Callable, Optional
import streamlit as st


AUTHOR = 'Michal Gruszczyński'
CONTACT = '[contact](https://www.linkedin.com/in/protago90/)'
SOURCE = '[source-code](https://github.com/protago90/tictactoe-ring)'
UNI = '[uni](https://www.math.uni.lodz.pl/)'

PLAYGROUND = 'PLAYGROUND'
TOURNAMENT = 'TOURNAMENT'
XSIGN, XLOGO, HFACE = 'X', '❌', '🙇' 
OSIGN, OLOGO, BFACE = 'O', '⭕', '🤖'
STAT = 'Games statistics "X" -{}:{}:{}- "O".'
WIN  = 'Player "{}" wins the game!'
END  = 'The game is over with draw.'
VERSUS = '{} -vs- {}'
LINE = '---'
LINK = '🔗'
PLAY = '▶︎'
REP  = '↻'
DOT  = '•‌'
NULL = ''

LOGO = 'misc/logo.png'
README = 'README.md'
PLYRS = PlayerFcty.get_plyrs_id()
BOTS = [_id for _id in PLYRS if _id != HumanUI.ID]
BOT = BOTS[-1]
NAP = 0
NGAMES = 10
NMAX = 100
NMIN = 1
GRID = 11
ICOL = 4


def init_session(x_id: str, o_id: str, mode: Optional[str]=None) -> None:
    ses.x_plyr = PlayerFcty.set(x_id, XSIGN, nap=NAP)
    ses.o_plyr = PlayerFcty.set(o_id, OSIGN, nap=NAP)
    ses.plyr, ses.plyr_n = ses.x_plyr, ses.o_plyr
    ses.board = XOBoard()
    ses.mode = mode if mode else PLAYGROUND
    ses.rec = []

def exec_move_processor(pos: Optional[int]=None) -> None:
    if not ses.rec and (pos is not None or ses.plyr.ID != HumanUI.ID):
        if ses.plyr.ID != HumanUI.ID:
            pos = ses.plyr.make_move(ses.board)
        ses.board.process_move(ses.plyr.sign, pos)
        ses.plyr, ses.plyr_n = ses.plyr_n, ses.plyr
        if not ses.board.is_open():
            ses.rec.append(ses.board.get_winner())

def exec_tournament_processor() -> None:
    for i in range(NMIN, ses.n_games+1):
        board = XOBoard()
        plyr = ses.x_plyr
        plyr_n = ses.o_plyr
        while board.is_open():
            pos = plyr.make_move(board)
            board.process_move(plyr.sign, pos)
            plyr, plyr_n = plyr_n, plyr
        ses.rec.append(board.get_winner())
        ses.bar.progress(int(i * round(100/ses.n_games, 2)))


def show_intro() -> None:
    try:
        welcome = Image.open(LOGO)
        st.image(welcome)
    except: print('zonk')

def show_meta() -> None:
    st.sidebar.write('---')
    st.sidebar.write(f'by {AUTHOR}')
    st.sidebar.write(f'{CONTACT} {DOT} {SOURCE} {DOT} {UNI}')

def show_plyrs_modes_ui() -> None:
    plyrs = PLYRS if ses.mode == PLAYGROUND else BOTS
    c = st.columns((.27, 1, .28))
    x = c[0].selectbox(NULL, plyrs, key='X', index=plyrs.index(ses.x_plyr.ID))
    o = c[-1].selectbox(NULL, plyrs, key='O', index=plyrs.index(ses.o_plyr.ID))
    if x != ses.x_plyr.ID or o != ses.o_plyr.ID:
        init_session(x, o, mode=ses.mode)

def show_playground_board_ui(get_hunan_move: Callable) -> None:
    for i, row in enumerate(ses.board.get_state()):
        c = st.columns(GRID)
        if i == 0:
            c[1].button(XLOGO)
            c[-2].button(OLOGO)
        for j, sign in enumerate(row):
            pos = (2-i)*3 + j  # hardoced projection on TicTacToe's board representation
            c[ICOL+j].button(sign, key=f"{i}-{j}", on_click=get_hunan_move, args=(pos,))
    c[ICOL+3].button(REP, on_click=init_session, args=(ses.x_plyr.ID, ses.o_plyr.ID))  

def show_tournament_panel_ui(run_tournament: Callable) -> None:
    c = st.columns(GRID)
    c[1].button(XLOGO)
    c[ICOL+1].button(PLAY, on_click=run_tournament)
    c[-2].button(OLOGO)
    c = st.columns(3)
    ses.n_games = c[1].slider(NULL, NMIN, NMAX, NGAMES)

def show_vs() -> None:
    if ses.mode == TOURNAMENT: 
        ses.bar = st.progress(0)
    st.write(LINE)
    c = st.columns((.99, .28, 1))
    c[1].write(VERSUS.format(
        *(HFACE if _id == HumanUI.ID else BFACE for _id in (ses.x_plyr.ID, ses.o_plyr.ID))))

def show_end() -> None:
    if ses.rec:
        win, stats = recap_game_stats(ses.rec, ses.x_plyr, ses.o_plyr)
        if ses.mode == TOURNAMENT: 
            st.info(STAT.format(*stats))
        if win: st.success(WIN.format(win))
        else: st.info(END)


def show_playground_app() -> None:
    if ses.mode != PLAYGROUND: init_session(HumanUI.ID, BOT, mode=PLAYGROUND)
    show_plyrs_modes_ui()
    exec_move_processor()
    show_playground_board_ui(get_hunan_move=exec_move_processor)
    show_vs()
    show_end()

def show_tournament_app() -> None:
    if ses.mode != TOURNAMENT: init_session(BOT, BOT, mode=TOURNAMENT)
    show_plyrs_modes_ui()
    show_tournament_panel_ui(run_tournament=exec_tournament_processor)
    show_vs()
    show_end()

def show_readme_app() -> None:
    with open(README, 'r') as fh:
        readme = ''.join(fh.readlines()[1:])
    st.markdown(readme, unsafe_allow_html=True)


st.set_page_config(page_title=XSIGN+OSIGN, page_icon=XLOGO, layout='centered')
ses = st.session_state  # streamlit's global session variable

APPS_REPO = {
    PLAYGROUND: show_playground_app,
    TOURNAMENT: show_tournament_app,
    'Readme': show_readme_app
}


if __name__ == "__main__":
    show_intro()
    if 'mode' not in ses: init_session(HumanUI.ID, BOT, mode=PLAYGROUND)  # TODO: rethink session init
    st.sidebar.title('Menu:')
    app_name = st.sidebar.radio(NULL, list(APPS_REPO.keys()))
    show_meta()
    APPS_REPO.get(app_name)()
