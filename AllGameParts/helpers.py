#functions that get used more than in one file
# write them here in order to prevent circuar import statements when using
from AllFigures.figur import *



def isPawn(piece) -> bool:
    try:
        return (piece.type=="P")
    except:
        return False

def getKing(figures):
    #gets a List of Black or white figures and returnes the reference on the King

    for figur in figures:
        if figur.type =="K":
            return figur
    return None


def piece_is_on_this_tile(MyBoard, position:Tuple[int, int]):
    # returns false if there is no piece on th given tile,
    # otherwiese it reutrns the pice
    x,y = position
    return MyBoard[x][y]



def pawn_moved_two_fields_on_last_move(element:Figur, movelist, posx)-> bool:
    #posx = the posiiton of element on the x scale
    #important to prevenet the following error
            #white pawn has a blackPawn (element) on the left                                           -> no enpassent
            #           has a blackPawn (element) on the right that moved 2 fields infront on last move -> en passent
    #without checking xpos of element whitePawn could en-passent in both directions in this case

    if len(movelist) ==0:
        return False

    figur_type, oldPosition, newPosition, new_figur_type= movelist[-1]
    if figur_type=="P" and abs(oldPosition[1]- newPosition[1]) == 2 and oldPosition[0] == posx:
        return True
    else:
        return False



def is_enPassent_move(Board, move:Tuple[int, int], playerColor, movingPiece:Figur, movelist) -> bool:
    x,y=move
    if x<0 or x>7:
        return False
    if movingPiece.type != "P":
        return False

    direction_the_pawn_moves = (-1 if (movingPiece.color == playerColor) else 1)
    element= piece_is_on_this_tile (Board, (x ,y-direction_the_pawn_moves))

    if is_oponents_piece (movingPiece, element) and isPawn (element):
        if pawn_moved_two_fields_on_last_move(element, movelist, x):
            return True

    return False



def is_oponents_piece(ownFigur, otherFigur,) -> bool:
    try:
        return (ownFigur.color != otherFigur.color)
    except:
        return False


def sortPieces_by_color(all_pieces):
    #sort pieces by there color and return them
    white_pieces=[]
    black_pieces=[]
    # have to regenerate this list every time because all_figures changes during the Game
    for e in all_pieces:
        if e.color=="white":
            white_pieces.append(e)
        else:
            black_pieces.append(e)

    return (white_pieces,black_pieces)


def printBoard(board):
        for row in board:
            txt = " | ".join(str(e.type) if e else "-" for e in row)
            print(txt)


def transpose_board(board):
    # in our version rows and colums are changed based from what the user can see
    # and the intern implementation of array
    #solution: transpose the board and return the transposed version
    # we know we have 8x8 fields, each row/colum has 8 fields
    #return just references: changes of B will also change original ARRAY!!!!!!!!

    B = [[False] * 8 for _ in range(8)]
    for i in range(8):
        for j in range(8):
            B[i][j] = board[j][i]
    return B



def get_Kingside_direction(playercolor, Kings_position:Tuple[int,int]):
    # direction of kingside and queenside depends on playercolor due do initialization of Figures
    #when King.position.x <=3 -> go to left, else right
    #only works when the King that belongs to Kings_position is on startingfield
    x,y = Kings_position
    return (-1 if x<=3 else 1)


def is_there_connected_rook_that_has_not_moved(MyBoard, tile:Tuple[int,int])-> bool:
    #checks if one tile is a rook that has not moved
    x,y=tile
    if isinstance (MyBoard[x][y], Figur):
        if (MyBoard[x][y].type == "R" and MyBoard[x][y].hasMoved() == False):
            return True

    return False




def get_theoretical_castling_rights(MyBoard, all_figures, player_color) -> Tuple[Tuple[bool, bool], Tuple[bool, bool]]:
    # check if white/ black can castle based on the fact
    # whether the kings or the corresponding rooks have already moved
    #return value example for
    #       white can castle both sides, black no side       ((True, True), (False, False))
    #       both sites can castle kingside and not queenside ((True,False), (True, False))

    whites_rights=  get_theoretical_castling_rights_helper(MyBoard, all_figures, "white", player_color)
    black_rights=   get_theoretical_castling_rights_helper(MyBoard, all_figures, "black", player_color)
    return (whites_rights, black_rights)



def get_theoretical_castling_rights_helper(MyBoard, all_figures, color, playercolor) -> Tuple[bool, bool]:
    #return value = (kingside, queenside)
    #make sure color= {white, black}
    white_pieces, black_pieces= sortPieces_by_color(all_figures)
    pieces= white_pieces if color== "white" else black_pieces
    king= getKing(pieces)

    if isinstance(king, Figur)== False:
        raise  Exception ("Figur should be a king but is not, \n  "
                          "message occurs in get_theoretical_castling_rights_white")#

    if king.hasAlreadyMoved:
        return (False, False)

    kingside_direction=  get_Kingside_direction(playercolor, king.position)
    queenside_direction= kingside_direction* -1

    bool_kingside=  is_there_connected_rook_that_has_not_moved(MyBoard, (king.position[0] + 3 * kingside_direction,  king.position[1]))
    bool_queenside= is_there_connected_rook_that_has_not_moved(MyBoard, (king.position[0] + 4 * queenside_direction, king.position[1]))
    return bool_kingside, bool_queenside

