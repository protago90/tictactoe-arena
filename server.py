import server as st

from tictactoe import XOBoard, PlayerF
from tictactoe.main import run_gameplay


st.set_page_config(
    page_title=" TicTacToe",
    page_icon="👾",
    layout="centered")


session = st.session_state

def app_play():

    if "board" not in st.session_state:
        session.board = XOBoard()
        session.o_plyr = PlayerF.set('random', 'X')
        session.x_plyr = PlayerF.set('random', 'O')

        session.plyr = session.x_plyr
        session.plyr_n = session.o_plyr

    st.write(f'GAMEPLAY "X" {session.x_plyr.ID} vs. {session.x_plyr.ID} "O"')

    # Define callbacks to handle button clicks.
    def handle_click(i, j):
        pos = session.plyr.make_move(session.board)
        session.board.process_move(session.plyr.sign, pos)
        session.plyr, session.plyr = session.plyr_n, session.plyr


    for i, row in enumerate(st.session_state.board.get_state(desc=False)):
        cols = st.columns([.1,.1,.1,.7])
        for j, field in enumerate(row):
            cols[j].button(
                field,
                key=f"{i}-{j}",
                on_click=handle_click,
                args=(i, j),
            )

    st.write(session.plyr.sign)

    if session.board.is_open():
        st.success(f"Congrats! {session.board.get_winner()} won the game! 🎈")


def app_about():
    with open('README.md') as f:
        md = f.read()
    st.write(md)

def app_tournament():
    st.write("tournament to-be")


# Pages as key-value pairs
PAGES = {
    "About":     app_about,
    "PLAYGROUND": app_play,
    "TOURNAMENT": app_tournament
}

st.sidebar.title('Menu:')

selection = st.sidebar.radio("", list(PAGES.keys()))

page = PAGES[selection]

page()


# if __name__ == "__main__":
#     show()