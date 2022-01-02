# by protago90
from board import BoardAPI

from abc import abstractmethod


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
