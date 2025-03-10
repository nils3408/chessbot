# moves.py
#get legal moves for all peaces

from AllFigures.figures import *
from AllFigures.deleteMoves import *
from AllGameParts.helpers import *



def King_is_not_in_check_right_now(MyBoard, MyKing:Figur, all_figures, playerColor, movelist) -> bool:
    #checks if the King is in check right now
    return (King_is_not_in_check_on_a_special_field(MyBoard, MyKing, all_figures, MyKing.position, playerColor, movelist))

def King_is_not_in_check_on_a_special_field(MyBoard, MyKing:Figur, all_figures, field:Tuple[int, int], playerColor, movelist) -> bool:
    #moving_piece= the King itself
    #move= field (King moves to this field)
    whitePieces, blackPieces = sortPieces_by_color(all_figures)
    oponents_pieces= whitePieces if MyKing.color=="black" else blackPieces
    return not(ownKing_would_be_in_check(MyBoard, MyKing, MyKing, field, oponents_pieces, playerColor, movelist))



def field_is_available(MyBoard, field:Tuple[int, int], MyKing:Figur, all_figures, playerColor, movelist):
    #is empty and no pieces from the oponent scopes on in (piece would be in check)
    #needed for castling, becaue king can not castle when the relevant fields contain figur(es) or the king would move throug a check
    if piece_is_on_this_tile(MyBoard, field) == False:
        if King_is_not_in_check_on_a_special_field(MyBoard, MyKing, all_figures, field, playerColor, movelist):
            return True

    return False



def get_Kingside_direction(playercolor, Kings_position:Tuple[int,int]):
    # direction of kingside and queenside depends on playercolor due do initialization of Figures
    #when King.position.x <=3 -> go to left, else right
    #only works when the King that belongs to Kings_position is on startingfield
    x,y = Kings_position
    return (-1 if x<=3 else 1)


def there_is_connected_rook_that_has_not_moved(MyBoard, tile:Tuple[int,int])->bool:
    #check if on tile is to the King connected Rook who has not moved
     #relevant for King- and Queendside castling
    x,y= tile
    if isinstance (MyBoard[x][y], Figur):
        if (MyBoard[x][y].type == "R" and MyBoard[x][y].hasMoved() == False):
            return True

    return False



def add_new_move( ownFigur,MyBoard, moves:list, position:Tuple[int, int], direction:Tuple[int, int]) -> List[Tuple[int, int]]:
    # first value of direction defines movement on x-scale ,second value of direction defines movement on y-scale
    # move along the line with recursion, until it is not more possible
        # it is not more possible if (x,y) are out of bord or you collapse with an other peace
            # if it is your piece: you can not go on this fild
            # if it is  oponents' piece: you can go on this fild (take the piece) but not any further

    x,y = position
    dx, dy = direction
    x1,y1 = x+dx, y+dy # new position after move

    if( (x1< 0) or (x1>7) or (y1<0) or (y1>7)):
        return moves

    element=  piece_is_on_this_tile(MyBoard, (x1,y1),)
    if element == False: #tile is empty
        moves.append((x1,y1))
        return add_new_move(ownFigur, MyBoard, moves, (x1,y1), direction)

    else: # tile is not empty
        if(is_oponents_piece(ownFigur, element)):
            moves.append((x1,y1))
        return moves




def get_valid_moves_bishop(self, MyBoard, position: Tuple[int, int], all_pieces, playerColor, movelist) -> List[Tuple[int, int]]:
    x, y = position
    moves = []

    moves += add_new_move (self, MyBoard, moves, position, (1, 1))
    moves += add_new_move (self, MyBoard, moves, position, (1, -1))
    moves += add_new_move (self, MyBoard, moves, position, (-1, 1))
    moves += add_new_move (self, MyBoard, moves, position, (-1, -1))

    moves= delete_impossible_moves(MyBoard,self, moves, all_pieces, playerColor, movelist)
    return moves


def get_valid_moves_rook(self, MyBoard, position: Tuple[int, int], all_pieces, playerColor,movelist) -> List[Tuple[int, int]]:
    x, y = position
    moves = []

    moves += add_new_move (self, MyBoard, moves, position, (1, 0))  # right
    moves += add_new_move (self, MyBoard, moves, position, (0, -1))  # down
    moves += add_new_move (self, MyBoard, moves, position, (-1, 0))  # left
    moves += add_new_move (self, MyBoard, moves, position, (0, 1))  # up

    moves = delete_impossible_moves(MyBoard,self, moves, all_pieces, playerColor, movelist)
    return moves


def get_valid_moves_queen(self, MyBoard, position: Tuple[int, int], all_pieces, playerColor, movelist) -> List[Tuple[int, int]]:
    return (get_valid_moves_rook(self, MyBoard, position, all_pieces, playerColor, movelist)
           + get_valid_moves_bishop(self, MyBoard, position, all_pieces, playerColor, movelist))



def get_valid_moves_knight(self, MyBoard, position: Tuple[int, int], all_pieces, playerColor, movelist) -> List[Tuple[int, int]]:
    x, y = position
    moves = [
        (x + 2, y + 1), (x + 2, y - 1),
        (x - 2, y + 1), (x - 2, y - 1),
        (x + 1, y + 2), (x + 1, y - 2),
        (x - 1, y + 2), (x - 1, y - 2)
    ]

    # return and already ignores moves where (x or y) ar out of board
    moves2= []
    for e in moves:
        x,y = e
        if x<=7 and x>=0 and y>=0 and y<=7:
            element = piece_is_on_this_tile(MyBoard, (x,y))

            if(element == False):
                moves2.append((x,y))
            else:
                if(is_oponents_piece(self, element)):
                    moves2.append((x,y))

    moves2= delete_impossible_moves(MyBoard,self, moves2, all_pieces, playerColor, movelist)
    return moves2




def get_valid_moves_king(self, MyBoard, position: Tuple[int, int], player_color, all_pieces, playerColor, movelist) -> List[Tuple[int, int]]:
    x, y = position
    moves = []

    #add normal moves
    for i in range (-1,2):
        for j in range(-1,2):
            if 0 <= x + i <= 7 and 0 <= y + j <= 7:
                element = piece_is_on_this_tile(MyBoard, (x+i, y+j))
                if(element == False):
                    moves.append((x+i, y+j))
                else:
                    if(is_oponents_piece(self, element)):
                        moves.append((x+i, y+j))


    #add castling moves
    if King_is_not_in_check_right_now(MyBoard, self, all_pieces, playerColor, movelist):

      if (self.hasMoved()== False):
        Kingside_direction=get_Kingside_direction(player_color, self.getPosition())
        Queenside_direction= Kingside_direction*-1

        #kingside
        if field_is_available(MyBoard, (x+1*Kingside_direction,y), self, all_pieces,playerColor,movelist):
            if field_is_available(MyBoard, (x+2*Kingside_direction, y), self, all_pieces, playerColor, movelist):
                        if there_is_connected_rook_that_has_not_moved(MyBoard, (x+3*Kingside_direction,y)):
                            moves.append((x+2*Kingside_direction,y))

        #Queenside
        if field_is_available(MyBoard, (x+1*Queenside_direction,y), self, all_pieces, playerColor, movelist):
            if field_is_available(MyBoard, (x+2*Queenside_direction,y), self, all_pieces, playerColor, movelist):
                if there_is_connected_rook_that_has_not_moved(MyBoard, (x+4*Queenside_direction,y)):
                    moves.append((x+2*Queenside_direction,y))

    moves= delete_impossible_moves(MyBoard, self, moves, all_pieces, playerColor, movelist)
    return moves




def get_valid_moves_pawn(self, MyBoard, position: Tuple[int, int], player_color, all_pieces, movelist) -> List[Tuple[int, int]]:
    x, y = position
    moves = []
    direction = (-1 if (self.color == player_color) else 1)

    #normak moves
    for i in range (1, 2 if self.hasMoved() else 3):
        if(piece_is_on_this_tile(MyBoard,(x,y+direction*i)) == False):
            moves.append((x,y+direction*i))
        else:
            break


    # normal capturing moves
    if( 0<= x+1 <=7 and 0<= y+direction*1 <=7): # tile exists
        element= piece_is_on_this_tile(MyBoard, (x+1, y+direction*1))
        if(element != False):
           if(is_oponents_piece(self, element)):
               moves.append((x+1, y+direction*1))

    if( 0<= x-1 <=7 and 0<= y+direction*1 <=7): # tile exists
        element= piece_is_on_this_tile(MyBoard, (x-1, y+direction*1))
        if(element != False):
            if(is_oponents_piece(self, element)):
                moves.append((x-1, y+direction*1))


    #en passent
    if is_enPassent_move(MyBoard, (x+1, y+direction), player_color, self, movelist):
        moves.append((x+1, y+direction))
    if is_enPassent_move(MyBoard, (x-1, y+direction), player_color, self, movelist):
        moves.append((x-1, y+direction))

    moves= delete_impossible_moves(MyBoard, self, moves, all_pieces, player_color, movelist)
    return moves



