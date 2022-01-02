# by protago90
from abc import abstractmethod
from typing import List, Optional, Sequence
import math
import random


class BoardAPI():

    @abstractmethod
    def get_state(self) -> List[List[str]]:
        pass    

    @abstractmethod
    def get_winner(self) -> Optional[str]:
        pass

    @abstractmethod
    def process_move(self, sign: str, pos: int) -> None:
        pass
    
    @abstractmethod
    def undo_move(self) -> None:
        pass

    @abstractmethod
    def get_open_poss(self) -> list:
        pass
    
    @abstractmethod
    def get_debuts_pos(self) -> int:
        pass

    @abstractmethod
    def is_open(self) -> bool:
        pass


class TicTacToe(BoardAPI):
    EMPTY = '⠀' 

    def __init__(self, empty: str=EMPTY) -> None:
        self._empty:  str = empty
        self._board:  List[str] = [self._empty for _ in range(9)]
        self._record: List[int] = []
        self._winner: Optional[str] = None


    def _get_rows(self, desc: bool=False) -> List[List[str]]:
        rows = [self._board[i*3 : i*3+3] for i in range(3)]
        return rows[::-1] if desc else rows

    def get_state(self, desc: bool=True) -> List[List[str]]:
        return self._get_rows(desc=desc)

    def get_winner(self) -> Optional[str]:
        return self._winner

    @staticmethod
    def _is_win_line(vec: Sequence[str]) -> bool:
        return len(set(vec)) == 1

    def _is_win_state(self, pos: int) -> bool:
        i = math.floor(pos/3)
        if self._is_win_line(self._get_rows()[i]):
            return True
        i = pos % 3
        if self._is_win_line([self._board[i+j] for j in (0, 3, 6)]):
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
        poss = self.get_open_poss()
        if len(poss) == 9:
           return 8  # random.choice([0, 2, 6, 8])
        if len(poss) == 8:
           return 4 if 4 in poss else random.choice([2, 6])
        # TODO: implement TicTacToe'a openning book for whole gameplay depth
        return random.choice(poss)
    
    def is_open(self) -> bool:
        return not self._winner and any(self.get_open_poss())
