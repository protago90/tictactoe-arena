# TicTacToe Ring

##### i.e. my tictactoe tournament arena for crash testing ai-bot designs

<p align="center"> <img width="500" src="src/demo.gif" alt="tictactoe"> </p> &nbsp;
 
At this time, the project is dedicated to `TicTacToe`, but in the future it is planned to expand to other searchable games. The purpose of all-of-this, despite pure fun, is to easy process of validation behind-the-curtain algorithms. To achieve this the following assumptions have been born:
 - standard agents implementation for reference i.e.: `Minmax`, `Debuts`, `Random`, `Custom` (and `Human` UI);
 - transparent API exposed to overwrite and interfere with: [BoardAPI](https://github.com/protago90/tictactoe-ring/blob/main/tictactoe/board.py#L8) and [PlayerAPI](https://github.com/protago90/tictactoe-ring/blob/main/tictactoe/player.py#L10);
 - `playground` / `tournament` modes providing respectivele touch'n'feel sandbox / automated at-scale tests;
 - twofold user interface, via: shell client (see: demo above) or clickable web app (see: TODO).
