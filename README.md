# TicTacToe Ring

##### i.e. simple tictactoe game sandbox for crash testing ai-bots designs

<p align="center"> <img width="550" src="misc/demo.gif" alt="tictactoe"> </p> &nbsp;

The purpose of what's above, despite fun, was to facilitate the testing of bots prototypes performance -by benchmarking them with [searchable](https://en.wikipedia.org/wiki/Game_theory) algorithms. The following have been accomplished:
 - [x] `playground` / `tournament` modes providing respectively touch'n'feel / at-scale-simulated gameplay;
 - [x] referential bots implementations i.e.: `minmax`, `debuts`, `random`, `search` (and `human`xd);
 - [ ] from-scratch AI-based bots prototypes (waiting for a dose of spare time...)
 - [x] transparent API exposed to interfere with: [BoardAPI](https://github.com/protago90/tictactoe-ring/blob/main/tictactoe/board.py#L8) and [PlayerAPI](https://github.com/protago90/tictactoe-ring/blob/main/tictactoe/player.py#L10);
 - [x] twofold UI, via: shell CLI (see `demo.gif`) or clickable web GUI (once hosted [here](https://share.streamlit.io/protago90/tictactoe-ring/main/streamgui.py) <img width="9.5" src="misc/link.png">).

<p align="center"> <a href="https://share.streamlit.io/protago90/tictactoe-ring/main/streamgui.py"> <img width="150" src="misc/gui.png" alt="streamlit"> </a></p> &nbsp;

[TicTacToe](https://en.wikipedia.org/wiki/Tic-tac-toe) is deterministic zero-sum game with `19683` possible states and `255168` gameplayes. See complete map of game tree depth depiceted by [XKCD](https://xkcd.com/832/) <img width="9" src="misc/link.png">. 


##### #QUICKTOUR:
```
# for CLI --script howto:
# (optional) python3.8 -m pip install tqdm==4.51.0
python3.8 -m tictactoe -o human -x minmax
python3.8 -m tictactoe -o search -x minmax -n 10  # tournament

# for GUI --server deploy & run:
python3.8 -m venv .env && source .env/bin/activate && python3.8 -m pip install -r requirements.txt
streamlit run streamgui.py

# for GUI --server deploy & run with docker:
sudo docker build -t streamgui .
sudo docker run -p 8501:8501 streamgui
```