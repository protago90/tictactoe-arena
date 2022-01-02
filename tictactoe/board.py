from abc import abstractmethod
from typing import List, Optional


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
