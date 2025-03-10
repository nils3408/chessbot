from AllFigures.figures import *
from AllFigures.figur import *
from AllGameParts.helpers import *
from typing import List
import copy


def delete_impossible_moves(MyBoard, piece:Figur, moves:List, all_pieces, playerColor, movelist):
    # beginning point of all Figures
    # get a List of moves and delete the ones, that would create a situation where the one King is in Check

    ownKing = get_own_King (all_pieces, piece.color)
    oponents_pieces= []
    for e in all_pieces:
        if e.color != piece.color:
            oponents_pieces.append(e)

    moves2= copy.deepcopy(moves)
    for move in moves:
        if ownKing_would_be_in_check(MyBoard,ownKing, piece,move, oponents_pieces, playerColor, movelist):
            moves2.remove(move)

        piece.resetVirtualPosition()
    return moves2


def ownKing_would_be_in_check(originalBoard, ownKing, MyPiece:Figur, move, oponents_pieces, playerColor, movelist):
        #MyPiece is the piece that can make the move
        # look whether opposite pieces could take the King on the newBoard

        newBoard= get_new_Board(originalBoard, MyPiece, move)
        capturedFigur =False

        # normal capturingMove
        if(would_be_caputuring_move(originalBoard, move, MyPiece.color)):
            x,y= move
            capturedFigur = originalBoard[x][y]

        #enPassent
        if (would_be_EnPassent_capturing_move(originalBoard, move, playerColor, MyPiece, movelist)):
            x,y= move
            direction_the_pawn_moves= (-1 if (MyPiece.color == playerColor) else 1)
            capturedFigur= originalBoard[x] [y-direction_the_pawn_moves]


        MyPiece.setVirtualPosition(move)
        types=["R","N","K","P","B", "Q"]
        functions=(Rook_Check, Knight_Check, King_Check, Pawn_Check, Bishop_Check, Queen_Check)

        for piece in oponents_pieces:
            if(piece != capturedFigur):

                # get the right function connected to piece.type
                for i in range(0,len(types)):
                    if(piece.type == types[i]):
                        if(functions[i](newBoard, ownKing, piece, playerColor))==True:
                            # the piece could take the KIng on the newBoard
                            return True


        return False



#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
def King_Check(newBoard, ownKing, piece, playerColor):
    # piece is the King from the oponent
    x1,y1 = piece.position
    x2,y2= ownKing.virtualPositon


    #check if Kings are next to each other
    if (abs(x1-x2) <=1) and (abs(y1-y2)<=1):
                return True

    return False



def Pawn_Check(newBoard, ownKing, piece:Figur, playerColor):
    #piece is pawn from oponent -> get Color with piece.color
    #playerColor= Color of the player ->Import to get move-direction of paws
    #pawns: (move up with movingColour = playerColor), else move down

    x1,y1 = piece.position
    x2,y2= ownKing.virtualPositon
    direction = (-1 if (piece.color == playerColor) else 1)

    if(abs(x2-x1)==1 and  y2== y1+direction):
        return True

    return False



def Knight_Check(newBoard, ownKing, piece, playerColor):
    #piece is a Knight from the opponent
    x1,y1 = piece.position
    x2,y2= ownKing.virtualPositon

    KnightMoves = [(x1 + 2, y1 + 1), (x1 + 2, y1 - 1), (x1 - 2, y1 + 1), (x1 - 2, y1 - 1), (x1 + 1, y1 + 2),
                   (x1 + 1, y1 - 2),(x1 - 1, y1 + 2), (x1 - 1, y1 - 2)]

    for e in KnightMoves:
        x3,y3 = e
        if 0<=x3<=7 and 0<=y3<=7: #check if legalField

            #check Knight could captureKing <-> moving to Kings position
            if x3==x2 and y3==y2:
                return True

    return False



def Queen_Check(newBoard, ownKing, piece:Figur, playerColor):
    #piece is a queen from the opponent
    a= Rook_Check(newBoard,  ownKing, piece, playerColor)
    b= Bishop_Check(newBoard,ownKing, piece, playerColor)
    return (a or b)



def Bishop_Check(newBoard, ownKing, piece:Figur, playerColor):
    #piece is Bishop from oponent
    x1, y1 = piece.position
    x2, y2 = ownKing.virtualPositon

    #4 cases where piece is located compared to King
    #{left up, right up, left down, right down)

    #they are on same row/colum ->False
    if((y1==y2 and x1!=x2) or (x1==x2 and y1!=y2)):
        return False


    if are_on_same_Diagonale(piece, ownKing):
        dx,dy= getBishopDirection(piece, ownKing)
        return all_fields_between_are_empty1(newBoard, piece.position, ownKing.virtualPositon, (dx,dy))

    return False



def Rook_Check(newBoard, ownKing:Figur, piece:Figur, playerColor) -> bool:
   #piece is a Rook from the oponent
    x1,y1 = piece.position
    x2,y2= ownKing.virtualPositon

    direction=(0,0)
    if(x1 == x2):
       direction = (0,1) if y1<y2 else (0,-1)
       return all_fields_between_are_empty1 (newBoard, piece.position, ownKing.virtualPositon,direction)

    elif(y1==y2):
        direction= (1,0) if x1<x2 else (-1,0)
        return all_fields_between_are_empty1 (newBoard, piece.position, ownKing.virtualPositon,direction)

    else:
        return False

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------


def get_own_King(all_pieces, color):
    for e in all_pieces:
        if e.type == "K" and e.color == color:
            return e


def get_new_Board(originalBoard, piece:Figur, move):
    #board that would exist , when the move would be happen
    newBoard = [row[:] for row in originalBoard]
    x,y= piece.position
    x1,y1 = move

    newBoard[x1][y1]= piece
    newBoard[x][y]= False
    return newBoard



def would_be_caputuring_move(Board, move:Tuple[int, int], ownColor):
    x,y =move
    return (Board[x][y] != False and Board[x][y].color != ownColor)


def would_be_EnPassent_capturing_move(Board, move:Tuple[int, int], player_color, piece:Figur, movelist) -> bool:
    #piece= the moving piece
    return  is_enPassent_move(Board, move, player_color, piece,movelist)


def pawn_moved_two_fields_on_last_move(element: Figur, movelist, posx) -> bool:
            #same as in moves.py
            if len (movelist) == 0:
                return False

            figur_type, oldPosition, newPosition = movelist[-1]
            if figur_type == "P" and abs (oldPosition[1] - newPosition[1]) == 2 and oldPosition[0] == posx:
                return True
            else:
                return False

#-----------------------------------------------------------------------------------------------------------------------------------------
def all_fields_between_are_empty1(MyBoard, field1:Tuple[int, int], field2:Tuple[int, int], direction:Tuple[int, int]) -> bool:
    #field1= the field where the other piece(not the King) is standing

    first_field= (field1[0]+direction[0], field1[1]+direction[1])
    return all_fields_between_are_empty2(MyBoard, first_field, field2, direction)



def all_fields_between_are_empty2(MyBoard, field1:Tuple[int,int], field2:Tuple[int, int], direction:Tuple[int, int]) -> bool:

    x1,y1= field1
    x2,y2= field2

    if(x1 == x2 and y1==y2):
        return True

    if MyBoard[x1][y1] !=False:
        return False

    newField1 = x1+direction[0], y1+direction[1]
    return all_fields_between_are_empty2(MyBoard, newField1, field2, direction)


#------------------------------------------------------------------------------------------------------------------------------------
#helper functions for Bishop

def getBishopDirection(piece1:Figur, ownKing) ->Tuple[int, int]:
    x1,y1= piece1.position
    x2,y2= ownKing.virtualPositon

    d11 = 1 if (x2-x1)>0 else -1
    d22 = 1 if (y2-y1)>0 else -1

    return (d11,d22)


def are_on_same_Diagonale(piece1:Figur, ownKing):
    x1,y1 = piece1.position
    x2,y2=ownKing.virtualPositon

    return abs(x2-x1) == abs(y2-y1)




