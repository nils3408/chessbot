from AllFigures.figur import Figur
from AllFigures.moves import (
    get_valid_moves_knight,
    get_valid_moves_king,
    get_valid_moves_bishop,
    get_valid_moves_rook,
    get_valid_moves_queen,
    get_valid_moves_pawn
)
from typing import Tuple, List



class Knight(Figur):
    def __init__(self, owner: str, id: int, position: Tuple[int, int]):
        super().__init__(owner, position, id, "N")


    def get_valid_moves(self, game, player_color, all_pieces, movelist) -> List[Tuple[int, int]]:
        return get_valid_moves_knight(self, game,self.position, all_pieces, player_color, movelist)


    

class King(Figur):
    def __init__(self, owner: str, id: int, position: Tuple[int, int]):
        super().__init__(owner, position, id,"K")
        self.castleQueenside = True
        self.castleKingside = True



    def canCastleQueenside(self) -> bool:
        return self.castleQueenside

    def canCastleKingside(self) -> bool:
        return self.castleKingside


    def set_canCastleKingside(self):
        # will never allowed to castle Kingside anymore
        self.castleKingside = False

    def set_canCastleQueenside(self):
        #will never be allowed to caslte Queendside anymore
        self.castleQueenside = False


    def get_valid_moves(self, game, player_color, all_pieces, movelist) -> List[Tuple[int, int]]:
        return get_valid_moves_king(self, game,self.position, player_color, all_pieces, player_color, movelist)




class Bishop(Figur):
    def __init__(self, owner: str, id: int, position: Tuple[int, int]):
        super().__init__(owner, position, id, "B")


    def get_valid_moves(self, game, player_color, all_pieces, movelist) -> List[Tuple[int, int]]:
        return get_valid_moves_bishop (self, game,self.position, all_pieces, player_color, movelist)



class Rook(Figur):
    def __init__(self, owner: str, id: int, position: Tuple[int, int]):
        super().__init__(owner, position, id, "R")


    def get_valid_moves(self, game, player_color, all_pieces, movelist) -> List[Tuple[int, int]]:
        return get_valid_moves_rook(self, game,self.position, all_pieces, player_color, movelist)
    



class Queen(Figur):
    def __init__(self, owner: str, id: int, position: Tuple[int, int]):
        super().__init__(owner, position, id ,"Q")
        self.type= "Q"

        
    def get_valid_moves(self, game, player_color, all_pieces, movelist) -> List[Tuple[int, int]]:
        return get_valid_moves_queen(self, game, self.position, all_pieces, player_color, movelist)
    



class Pawn(Figur):
    def __init__(self, owner: str, id: int, position: Tuple[int, int]):
        super().__init__(owner, position, id, "P")


    def get_valid_moves(self, game, player_color, all_pieces, movelist) -> List[Tuple[int, int]]:
        return get_valid_moves_pawn(self, game, self.position, player_color, all_pieces, movelist)
