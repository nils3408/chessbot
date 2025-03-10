from abc import ABC, abstractmethod
from typing import Tuple

class Figur(ABC):

    def __init__(self, color: str, position: Tuple[int, int], id, type):
        self.color = color
        self.position = position
        self.virtualPositon = position
        self.id=id
        self.type=type
        self.hasAlreadyMoved = False



    def getPosition(self) -> Tuple[int, int]:
        return self.position


    def updatePosition(self, newPosition:Tuple[int, int]):
        self.position = newPosition

    def update_HasMoved(self):
        self.hasAlreadyMoved= True


    def hasMoved(self) -> bool:
        return self.hasAlreadyMoved


    def setVirtualPosition(self, newVirtualPosition:Tuple[int, int]):
        self.virtualPositon= newVirtualPosition


    def resetVirtualPosition(self):
        #virtual Positon gets used in deleting moves
        self.virtualPositon= self.position


    @abstractmethod
    def get_valid_moves(self, MyBoard, player_color, all_pieces, movelist):
        #movelist is  list of moves that are already player, we need it en passant check
        pass
