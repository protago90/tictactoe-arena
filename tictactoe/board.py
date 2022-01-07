# by protago90
from abc import abstractmethod
from typing import List, Optional, Sequence
import math
import random


class BoardAPI():
    EMPTY = '⠀'
    SIGNS = ('X', 'O', EMPTY)

    @abstractmethod
    def get_state(self) -> List[List[str]]:
        pass    

    @abstractmethod
    def process_move(self, sign: str, pos: int) -> None:
        pass
    
    @abstractmethod
    def undo_move(self) -> None:
        pass

    @abstractmethod
    def get_open_poss(self) -> List[int]:
        pass
    
    @abstractmethod
    def get_debuts_pos(self) -> int:
        pass

    @abstractmethod
    def get_winner(self) -> Optional[str]:
        pass

    @abstractmethod
    def is_open(self) -> bool:
        pass


class XOBoard(BoardAPI):

    def __init__(self, empty: Optional[str]=None) -> None:
        self._empty: str = empty if empty else self.__class__.EMPTY
        self._board: List[str] = [self._empty for _ in range(9)]
        self._winner: Optional[str] = None
        self._record: List[int] = []

    def get_state(self, desc: bool=True) -> List[List[str]]:
        rows = [self._board[i*3 : i*3+3] for i in range(3)]
        return rows[::-1] if desc else rows

    @staticmethod
    def _is_win_line(vec: Sequence[str]) -> bool:
        return len(set(vec)) == 1

    def _is_win_state(self, pos: int) -> bool:
        irow = math.floor(pos/3)
        if self._is_win_line(self.get_state(desc=False)[irow]):
            return True
        icol = pos % 3
        if self._is_win_line([self._board[i+icol] for i in (0, 3, 6)]):
            return True
        for diag in ((0, 4, 8), (2, 4, 6)):
            if pos in diag:
                if self._is_win_line([self._board[i] for i in diag]):
                    return True
        return False

    def process_move(self, sign: str, pos: int) -> None:
        self._board[pos] = sign
        self._record.append(pos)
        if self._is_win_state(pos): self._winner = sign
    
    def undo_move(self) -> None:
        self._board[self._record.pop()] = self._empty
        self._winner = None

    def get_open_poss(self) -> List[int]:
        return [pos for pos, v in enumerate(self._board) if v == self._empty]

    def get_debuts_pos(self) -> int:
        corn = (0, 2, 6, 8)
        poss = self.get_open_poss()
        if len(poss) == 9:
           return random.choice(corn)
        if len(poss) == 8:
           return 4 if 4 in poss else random.choice([pos for pos in poss if pos in corn])
        # TODO: implement TicTacToe's openning book for whole gameplay depth
        return random.choice(poss)
    
    def get_winner(self) -> Optional[str]:
        return self._winner

    def is_open(self) -> bool:
        return not self._winner and len(self.get_open_poss()) > 0
