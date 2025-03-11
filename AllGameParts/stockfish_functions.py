# bridge between stockfish and our version
# from AllFigures.figur import *
from AllGameParts.helpers import*


def format_castling_rights(rights: Tuple[Tuple[bool, bool], Tuple[bool, bool]]) -> str:
    # rights = ((w_kingside, w_queenside), (b_kingside, b_queenside))

    txt = ""
    if rights[0][0]:  # Weiß kurze Rochade
        txt += "K"
    if rights[0][1]:  # Weiß lange Rochade
        txt += "Q"
    if rights[1][0]:  # Schwarz kurze Rochade
        txt += "k"
    if rights[1][1]:  # Schwarz lange Rochade
        txt += "q"

    return txt if txt else "-"  # Falls keine Rochade möglich ist, gib "-" zurück



def convert_to_fen_when_own_player_is_white(board) ->str:
    #board[0 bis 7][0] = schwarze Figuren von links nach rechts -> board[3][0]=Queen
    # -> start [0][0]
    # rows and col are transposed in our version compared on intern handling of 2 dim-arrays
    # -> transpose it, so you can iterarte as usal
        #[0][0] bis [0][7] black pieces on row 8
        #[7][0] bis [7][7]

    transposed_board= transpose_board(board)
    rows=[]
    for y in transposed_board:
        empty_fields_counter, txt =0, ""
        for figure in y:
            if figure == False:
                empty_fields_counter+=1
            else:
                txt= txt+ str(empty_fields_counter) if empty_fields_counter >0 else txt
                empty_fields_counter=0

                symbol= figure.type.upper() if figure.color =="white" else figure.type.lower()
                txt+= symbol

        txt = txt + str(empty_fields_counter) if empty_fields_counter > 0 else txt
        empty_fields_counter=0
        rows.append(txt)

    fen_string = "/".join(rows)
    return fen_string



def convert_to_fen_when_own_player_is_black(board)-> str:
    #board[0 bis 7] [0] ist weiße Figuren, board[3][0]= white King
    # -> start [7][7] bis [0][7]
    # rows and col are transposed in our version based on intern handling
    # -> transpose it, so you can iterarte as usal
        # black figures from [7][7] t0 [7][0]  (starting position) rnbqkbnr
        #white figures from [7] [0] to [0] [0] (starting position) RNBQKBNR

    transposed_board= transpose_board(board)
    rows=[]
    for y in transposed_board[::-1]:
        empty_fields_counter, txt = 0, ""
        for figure in y[::-1]:
            if figure == False:
                empty_fields_counter+=1
            else:
                txt= txt+ str(empty_fields_counter) if empty_fields_counter >0 else txt
                empty_fields_counter=0

                symbol= figure.type.upper() if figure.color =="white" else figure.type.lower()
                txt+= symbol

        txt = txt + str(empty_fields_counter) if empty_fields_counter > 0 else txt
        empty_fields_counter = 0
        rows.append(txt)

    fen_string = "/".join(rows)
    return fen_string



def get_fen_of_position(board, player_color):
    if player_color=="white":
        fen_position= convert_to_fen_when_own_player_is_white(board)
    else:
        fen_position= convert_to_fen_when_own_player_is_black(board)

    return fen_position




#---------- -----this function gets called first from the bot -------------------------

def convert_to_fen(MyBoard, all_figures, color_to_move, player_color):
#convert our board to a FEN so the engine can use it
# fen notes:
#   white has uppercase letters and black lowercase
#   in the fen notation you start on the row 8 and go down to row one
#   beginning fen:   rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR


    if color_to_move not in ("white", "black"):
        raise Exception("Ungültige Farbe")
    color_symbol_to_move = "w" if color_to_move=="white" else "b"

    fen_string= get_fen_of_position(MyBoard, player_color)
    #color_symbol_to_move= color_symbol_to_move
    castling_rights= format_castling_rights(get_theoretical_castling_rights(MyBoard, all_figures, player_color))
    #todo
    en_passant_target = "-"  # Kein En-Passant-Ziel vorhanden
    halfmove_clock = "0"  # Halbzüge seit dem letzten Schlagzug oder Bauernzug
    fullmove_number = "1"  # Aktuelle Zugnummer

    return f"{fen_string} {color_symbol_to_move} {castling_rights} {en_passant_target} {halfmove_clock} {fullmove_number}"



#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#return direction:
# stockfish_data -> our data
def get_field_from_stockfish_noation_white(x,y)->Tuple[int, int]:
    #playercolor = white

    row= ["a","b","c","d","e","f","g","h"]
    for i in range(8):
        if row[i]==x:
            return (i,8-int(y)) # fields go  from 0-7 not from 1-8

    raise Exception("Fehler in get_field_from_stockfish_white  ---- x= " +str(x)+ " y= "+y)



def get_field_from_stockfish_notation_black(x,y)->Tuple[int, int]:
    #player_color = black

    y=int(y) #sites are changed as well: row 4 (d) from white is row 5 (=9-4) for black

    row=["h","g","f","e","d","c","b","a"]
    for i in range(8):
        if row[i]==x:
            return (i, int(y)-1) #fileds go from 0-7 instead of 1-8

    raise Exception ("Fehler in get_field_from_stockfish_black  ---- x= " +str(x)+ " y= "+str(y))


def get_field_from_stockfish_notation(x,y, player_color)-> Tuple[int, int]:
    #player_color is the color of the player, not the engine
    #this is relevant because based on player_color figures have different starting position and their pawns move in
    # opposite directions
    #example a1:
        # player_color = white: board[0][0]
        # player_color = black: board[7][7]

    if player_color=="white":
        return get_field_from_stockfish_noation_white(x,y)
    elif player_color=="black":
        return get_field_from_stockfish_notation_black(x,y)
    else:
        raise Exception (" Error in get_field_from_stockfish_notation due to player_color error---------  "
                         "player_color= "+str(player_color))



def convert_move(move, board, player_color):
    #stockfish returns move in the following: <oldfield><newfield> , f.e e2e4 # e2e1b
    # howvever we need to return the following: (piece, new_field= Tuple[int, int])

    #normally move is 4 chars long
    #only exeption: it is a promotion move: fith char to descripe with Piece pawn should be promoted to

    if len(move)!=4 and len(move) != 5:
        raise Exception ("stockfish move is not 4 chars long")


    new_field= get_field_from_stockfish_notation(move[2],move[3], player_color)
    old_field= get_field_from_stockfish_notation(move[0], move[1], player_color)
    x,y=old_field
    piece=board[x][y]

    newPieceType="Q" if len(move)==4 else move[4].upper()

    return (piece, new_field, newPieceType)

    


