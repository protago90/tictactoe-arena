# TicTacToe Ring

##### i.e. my tictactoe tournament arena for crash testing ai-bot designs

<p align="center"> <img width="550" src="misc/demo.gif" alt="tictactoe"> </p> &nbsp;
 
The purpose of what's above, despite fun, was to facilitate the the process of behind-the-curtain algorithms validation for searchable games —the following have been accomplished:
 - referential bots implementations i.e.: `Minmax`, `Debuts`, `Random`, `Search` (and `Human`^^);
 - `playground` / `tournament` modes providing respectively touch'n'feel / at-scale gameplays;
 - transparent API exposed to interfere with: [BoardAPI](https://github.com/protago90/tictactoe-ring/blob/main/tictactoe/board.py#L8) and [PlayerAPI](https://github.com/protago90/tictactoe-ring/blob/main/tictactoe/player.py#L10);
 - twofold UI, via: shell cli script (see `demo.gif`) or clickable GUI (should be hosted TODO <img width="10" src="misc/link.png">).