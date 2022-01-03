# by protago90
from tictactoe.board import BoardAPI

from abc import abstractmethod
from typing import Callable, List, Optional, Tuple
import random
import time


class PlayerAPI():
    SIGNS = ('X', 'O')  # TicTacToe's hardcoded signatures 
    NAP = 0
    ID = 'None'

    def __init__(self, sign: str) -> None:
        if sign not in self.__class__.SIGNS:
            raise ValueError(f'One of {self.__class__.SIGNS} player signs must be set.')
        self.sign = sign

    @abstractmethod
    def make_move(self, board: BoardAPI) -> int:
        pass


class HumanUI(PlayerAPI):
    ID = 'Human'

    def __init__(self, sign: str, human_api: Callable) -> None:
        super().__init__(sign)
        self._get_move_from_human_ui = human_api

    def make_move(self, board: BoardAPI) -> int:
        while True:
            try:
                pos = self._get_move_from_human_ui()  # external human resp injection
                if pos in board.get_open_poss():
                    return pos
            except ValueError: pass


class BotAPI(PlayerAPI):

    def __init__(self, sign: str, nap: Optional[float]=None) -> None:
        super().__init__(sign)
        self.nap = nap if nap else self.__class__.NAP
    
    def make_move(self, board: BoardAPI) -> int:
        time.sleep(self.nap)
        # dirty hack: below deterministic pick of first move reduce bot's inference time
        if len(board.get_open_poss()) == 9:
           return board.get_debuts_pos()
        return self._get_move(board)
    
    @abstractmethod
    def _get_move(self, board: BoardAPI) -> int:
        pass

    def _get_rival(self, sign: str) -> str:
        signs = self.__class__.SIGNS
        return signs[1] if sign == signs[0] else signs[0]


class RandomBot(BotAPI):
    ID = 'Random'

    def __init__(self, sign: str, nap: Optional[float]=None) -> None:
        super().__init__(sign, nap)
    
    def _get_move(self, board: BoardAPI) -> int:
        return random.choice(board.get_open_poss())


class DebutsBot(BotAPI):
    ID = 'Debuts'

    def __init__(self, sign: str, nap: Optional[float]=None) -> None:
        super().__init__(sign, nap)

    def _get_move(self, board: BoardAPI) -> int:
        poss = board.get_open_poss()
        for pos in poss:
            for sign in (self.sign, self._get_rival(self.sign)):
                board.process_move(sign, pos)  # search for wining then blocking pos
                if not board.is_open():
                    board.undo_move()
                    return pos
                board.undo_move()
        return board.get_debuts_pos()


class SearchBotAPI(BotAPI):

    def __init__(self, sign: str, nap: Optional[float]=None) -> None:
        super().__init__(sign, nap)

    def _get_move(self, board: BoardAPI) -> int:
        rec = []
        for pos in board.get_open_poss():
            board.process_move(self.sign, pos)
            scr = self._eval_game_branch_with_rule(board, self.sign, 1)
            board.undo_move()
            rec.append((pos, scr))
        the_pos = self._eval_top_heuristic(rec)
        return the_pos

    def _eval_game_branch_with_rule(self, board: BoardAPI, sign: str, i: int) -> float:
        fin = self._eval_final_state(board, sign, i)
        if fin is not None:
            return fin
        sign = self._get_rival(sign)
        scrs = []
        i += 1
        for pos in board.get_open_poss():
            board.process_move(sign, pos)
            scrs.append(
                self._eval_game_branch_with_rule(board, sign, i))
            board.undo_move()
        return self._eval_heuristic(sign, scrs)

    @abstractmethod
    def _eval_final_state(self, board: BoardAPI, sign: str, i: int) -> Optional[float]:
        pass

    @abstractmethod
    def _eval_heuristic(self, sign: str, scrs: List[float]) -> float:
        pass

    @abstractmethod
    def _eval_top_heuristic(self, pos_score_pairs: List[Tuple[int, float]]) -> int:
        pass


class MinMaxBot(SearchBotAPI):
    ID = 'Minmax'

    def __init__(self, sign: str, nap: Optional[float]=None) -> None:
        super().__init__(sign, nap)

    def _eval_final_state(self, board: BoardAPI, sign: str, i: int) -> Optional[float]:
        if not board.is_open():
            if board.get_winner():
                return 1 if self.sign == sign else -1
            return 0
        return None

    def _eval_heuristic(self, sign: str, scrs: List[float]) -> float:
        return max(scrs) if self.sign == sign else min(scrs)

    def _eval_top_heuristic(self, pos_scr_pairs: List[Tuple[int, float]]) -> int:
        return sorted(
            pos_scr_pairs, key=lambda xy: (xy[1], random.random()), reverse=True
        )[0][0]


class SearchBot(SearchBotAPI):
    ID = 'Search'
    def __init__(self, sign: str, nap: Optional[float]=None) -> None:
        super().__init__(sign, nap)

    def _eval_final_state(self, board: BoardAPI, sign: str, i: int) -> Optional[float]:
        wt = (1/i**4)  # game tree depth depended factor
        if not board.is_open():
            if board.get_winner():
                return 1 * wt if self.sign == sign else -1 * wt
            return 0
        return None

    def _eval_heuristic(self, sign: str, scrs: List[float]) -> float:
        return sum(scrs)

    def _eval_top_heuristic(self, pos_scr_pairs: List[Tuple[int, float]]) -> int:
        return sorted(
            pos_scr_pairs, key=lambda xy: (xy[1], random.random()), reverse=True
        )[0][0]
