# TicTacToe Ring

##### i.e. my tictactoe tournament arena for crash testing ai-bot designs

<p align="center"> <img width="500" src="src/demo.gif" alt="tictactoe"> </p> &nbsp;
 
The purpose of all-of-this, despite pure fun, is to easy process of validation behind-the-curtain algorithms for *searchable* games. To achieve this the following assumptions have been born:
 - referencial agents implementations i.e.: `Minmax`, `Debuts`, `Random`, `Custom` (and `Human` UI);
 - transparent API exposed to overwrite and interfere with: [BoardAPI](https://github.com/protago90/tictactoe-ring/blob/main/tictactoe/board.py#L8) and [PlayerAPI](https://github.com/protago90/tictactoe-ring/blob/main/tictactoe/player.py#L10);
 - `playground` / `tournament` modes providing respectively touch'n'feel / at-scale sandboxes;
 - twofold user interface, via: shell client (see: demo) or clickable web app (see: TODO).
