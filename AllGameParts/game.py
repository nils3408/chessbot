

import AllGameParts.visualBoard as visual
from AllGameParts.initialisation import *
from AllBots.bot import *
from AllBots.bots import *
from AllFigures.deleteMoves import *
from AllGameParts.stockfish_functions import *


class Game:

    def __init__(self, player_color: str):
        py.init ()
        self.player_color = player_color
        self.squareSize = 80

        self.last_selected_piece = None
        self.all_figures = []
        self.selected_tile = None

        self.selected_piece: Optional[Figur] = None
        self.piece_map: Dict[tuple, Figur] = self.create_piece_map ()

        self.board_pos_selected_x: int
        self.board_pos_selected_y: int

        # here is your move_list#
        self.move_list = []  # each element is Triple (figur, oldPosition, newPosition) like (K ,(x1,y1),(x2,y2))
        self.color_to_move = "white"
        # easiest way, find a connection between a rect on the board and the piece, standing on it
        self.game_status=True
        self.nextRound="" #should it got to newGame or Main meny after finishing this game
        
        if player_color == 'white':
            self.all_figures = initialize_figures_white ()
        if player_color == 'black':
            self.all_figures = initialize_figures_black ()


        self.board = [[False, False, False, False, False, False, False, False],
                      [False, False, False, False, False, False, False, False],
                      [False, False, False, False, False, False, False, False],
                      [False, False, False, False, False, False, False, False],
                      [False, False, False, False, False, False, False, False],
                      [False, False, False, False, False, False, False, False],
                      [False, False, False, False, False, False, False, False],
                      [False, False, False, False, False, False, False, False]
                      ]

    # ----------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------
    # all needed functions



    def add_to_movelist(self, pieceType: str, oldPosition, newPosition: Tuple[int, int], newPieceType):
        #when PawnTransformation -> pieceType != newPiecetype
        self.move_list.append ((pieceType, oldPosition, newPosition, newPieceType))

    def getBoard(self):
        return self.board




    def set_color(self, color: int):
        self.player_color = color


    def update_full_board(self):
        for i in range (8):
            for j in range (8):
                self.board[i][j] = False

        for e in self.all_figures:
            x, y = e.position
            self.board[x][y] = e


    def update_color_to_move(self):
        self.color_to_move = "black" if self.color_to_move == "white" else "white"

    def update_clicked_position(self, position: Tuple[int, int]):
        # the (x,y) where the player clicked on the screen
        x, y = position
        if 0 <= x < 8 and 0 <= y < 8:
            self.board_pos_selected_x = x
            self.board_pos_selected_y = y
            return None
        return None


    def mouse_to_board_coords(self, mouse_x: int, mouse_y: int) -> Optional[tuple[int, int]]:
        board_x = mouse_x // self.squareSize
        board_y = mouse_y // self.squareSize
        return ((board_x, board_y))


    def get_piece_at_board_coords(self) -> Optional[Figur]:
        for piece in self.all_figures:
            if piece.position == (self.board_pos_selected_x, self.board_pos_selected_y):
                return piece
        return None

    def get_piece_at_position(self, x: int, y: int) -> Optional[Figur]:
        for piece in self.all_figures:
            if piece.position == (x,y):
                return piece
        return None


    def deselect(self):
        # deselect a selected piece
        self.last_selected_piece = None
        self.selected_piece = None


#-----------------------------------------------------------------------
    def create_piece_map(self) -> Dict[Tuple[int, int], Figur]:
        piece_map = {}
        for piece in self.all_figures:
            piece_map[piece.position] = piece
        return piece_map

    def update_piece_map(self):
        self.piece_map = self.create_piece_map ()

    def get_piece_map(self) -> Dict[tuple, Figur]:
        return self.piece_map

#------------------------------------------------------------------------------------

    def is_capturingMove(self, ownPiece: Figur, newPiece: Optional[Figur]) -> bool:
        if ownPiece is None:
            return False  # Can't be a capturing move if own piece is None
        if newPiece is None:
            return False  # No piece to capture

        return (ownPiece.color != newPiece.color)


    def is_piece_selected(self, piece1:Figur, ):
        #checks if en piece or en empty tile(None) is selected
        return (piece1 != None)


    def is_valid_move(self, piece:Figur, player_color):
        if(piece == None):
            return False

        possible_moves: list = piece.get_valid_moves (self.getBoard(), player_color, self.all_figures, self.move_list)
        if (self.board_pos_selected_x, self.board_pos_selected_y) in possible_moves:
            return True
        else:
            return False


#----------------------------------------------------------------------------------------------------
    def pawn_reaches_end(self, piece:Figur) -> bool:
        #because a pawn can only reach one end of the board (because it can not move back) checking the site of he board
        #is not neccessary
        x,y = piece.position
        return (y==0 or y==7)


    def pawn_make_transition(self, piece:Figur, player_color, newPieceType, GameMode):
        #pawn transforms into {Queen, Rook, Bishop, Knight}
        possible_figures = [
            Rook(piece.color,   piece.id,  piece.position),
            Knight(piece.color, piece.id,  piece.position),
            Bishop(piece.color, piece.id,  piece.position),
            Queen (piece.color, piece.id, piece.position)
        ]

        #if player makes the move: open Meny,
        # if bot makes move: do not open it- promote based on given input
        if player_color == piece.color or GameMode== "2Player":
            new_piece_type= self.choose_new_figur(possible_figures)
            index = self.all_figures.index(piece)
            self.all_figures[index] = new_piece_type(piece.color, piece.id, piece.position)
            return

        else:
            promotion_map = { "R": Rook, "N": Knight, "B": Bishop, "Q": Queen}

            if newPieceType in promotion_map:
                index = self.all_figures.index(piece)
                self.all_figures[index] = promotion_map[newPieceType](piece.color, piece.id, piece.position)
            else:
                raise Exception("Error in make_move at pawn promotion. piece_type does not match possibilities")



    def choose_new_figur(self, possible_figures):
        visual.draw_background_while_pawn_transition ()

        while True:
            buttons = visual.draw_figures_while_pawn_transition(possible_figures)
            if self.mouse_button_gets_cklicked():
                for button_data in buttons:
                    #button_data[0] = the rect, button_data[1] = the figur
                    if button_data[0].collidepoint(visual.get_relative_maus_coords_for_screen2()):
                        return (type (button_data[1]))

#-------------------------------------------------------------------------------------------------------------


    def is_CastlingMove(self, piece:Figur, newPosition:Tuple[int, int]):
        #King moves two or three steps belong the x scale
        if(isinstance(piece, King)):
            x,y = piece.getPosition()
            x1,y1= newPosition
            return (abs(x-x1) >=2)

        return False


    def castlingHelper(self, KingsPosition:Tuple[int, int], player_color):
        #get the Rook belonging to the Castling Move
        #return   (Rook, Rook.newPosition)
        #KigsPositon = Position of the King after Castling
        # After Castling Rook stands on f or d File -> Rook.newPosition.x ∈ {2,5}

        if(player_color== "white"):
            return self.CastlingHelperWhite(KingsPosition)
        if(player_color== "black"):
            return self.CastlingHelperBlack(KingsPosition)


    def CastlingHelperWhite(self, KingsPosition:Tuple):
        x, y = KingsPosition
        if x == 6:
            if (isinstance (self.board[7][y], Rook)):
                return (self.board[7][y], (5, y))

            else:
                print ("Fehler in Castling Helpers. Auf dem Feld sollte ein Rook stehen tut es aber nicht")
                return (None, (None, None))

        elif x == 2:
            if (isinstance (self.board[0][y], Rook)):
                return (self.board[0][y], (3, y))

            else:
                print ("Fehler in Castling Helpers. Auf dem Feld sollte ein Rook stehen tut es aber nicht")
                return (None, (None, None))

        else:
            print ("unerwarter Fehler beim ANklicken des Feldes")
            return (None, (None, None))


    def CastlingHelperBlack(self, KingsPosition:Tuple[int,int]):
        x, y = KingsPosition
        if x == 1:
            if (isinstance (self.board[0][y], Rook)):
                return (self.board[0][y], (2, y))

            else:
                print ("Fehler in Castling Helpers. Auf dem Feld sollte ein Rook stehen tut es aber nicht")
                return (None, (None, None))

        elif x == 5:
            if (isinstance (self.board[7][y], Rook)):
                return (self.board[7][y], (4, y))

            else:
                print ("Fehler in Castling Helpers. Auf dem Feld sollte ein Rook stehen tut es aber nicht")
                return (None, (None, None))

        else:
            print ("unerwarter Fehler beim ANklicken des Feldes")
            return (None, (None, None))

#-------------------------------------------------------------------------------------



    def gameOver(self, all_pieces, movingColor, playerColor):
        return (self.checkCheckmateAndStaleMate(all_pieces, movingColor, playerColor) == "checkmate"
                or self.checkCheckmateAndStaleMate(all_pieces, movingColor, playerColor == "stalemate"))


    def checkCheckmateAndStaleMate(self, all_pieces, movingColor, playerColor) -> str:
        #playerColor = Color of the manuell Player (not the Bot)
        #movingColor = the Color of the player that makes the move
        #   black makes move -> check for white
        # white makes a move -> check for Black

        white_pieces, black_pieces= sortPieces_by_color(all_pieces)
        color_to_check= "black" if  movingColor=="white" else "white"
        pieces_to_check = black_pieces if color_to_check == "black" else white_pieces

        possible_moves=[]
        for piece in pieces_to_check:
            possible_moves.extend(piece.get_valid_moves(self.getBoard(),playerColor , self.all_figures, self.move_list))

        if len(possible_moves)==0:
            #check if Stalemate or Checkmate
            if self.King_is_in_Check(self.board, getKing(pieces_to_check), self.all_figures, playerColor):
                return "checkmate"

            else:
                print(str(color_to_check +" hat keine Züge mehr! Es ist Stalemate"))
                return "stalemate"
        else:
            return "none"




    def King_is_in_Check(self, board, theKing:King, all_figures, player_color) -> bool:
        whitePieces, blackPieces = sortPieces_by_color(all_figures)
        pieces = whitePieces if theKing.color == "black" else blackPieces

        for piece in pieces:
            moves=piece.get_valid_moves(self.board, player_color, all_figures, self.move_list)
            if (theKing.position in moves):
                return True

        return False

#-------------------------------------------------------------------------------------------------------

    def mouse_button_gets_cklicked(self) -> bool:
        for event in py.event.get():
            if event.type== py.MOUSEBUTTONDOWN:
                return True
        return False


    def makeMove(self, moving_piece: Figur, position_to_move: Tuple[int, int], player_color: str, is_capturing_move: bool, all_pieces: List[Figur], GameMode,newPieceType="Q"  ):
        oldPieceType = moving_piece.type

        # Capturing Move
        if is_capturing_move:
            self.all_figures.remove(self.get_piece_at_position(position_to_move[0], position_to_move[1]))

        # When castling move
        if self.is_CastlingMove(moving_piece, position_to_move):
            Rook1, newPosition = self.castlingHelper(position_to_move, player_color)
            Rook1.updatePosition(newPosition)

        # when enpassentCapturingMove
        if is_enPassent_move(self.board, position_to_move, player_color, moving_piece, self.move_list):
            x, y = position_to_move
            direction_the_pawn_moves = (-1 if (moving_piece.color == player_color) else 1)
            capturedFigur= self.board[x][y - direction_the_pawn_moves]
            self.all_figures.remove(capturedFigur)


        # Update Position
        old_position= moving_piece.position
        moving_piece.updatePosition(position_to_move)
        moving_piece.update_HasMoved()
        self.update_full_board()

        # Check for pawn promotion
        if moving_piece.type == "P" and self.pawn_reaches_end(moving_piece):
            self.pawn_make_transition(moving_piece, player_color, newPieceType, GameMode)

        self.add_to_movelist(oldPieceType ,old_position,moving_piece.getPosition(), moving_piece.type)

        #checkmate and stalemate
        sit= self.checkCheckmateAndStaleMate(all_pieces, moving_piece.color, player_color)=="checkmate" or self.checkCheckmateAndStaleMate(all_pieces, moving_piece.color, player_color)=="stalemate"
        if sit:
            self.endGame(self.createMessage(sit, moving_piece.color))

        self.update_color_to_move()
        self.deselect()




#-------------------------------------------------------------------------------------------------------------------------
    def endGame(self, message):
        #when the game is Over, Checkmate or Stalemate
        visual.endGameSurface1(self.all_figures, message)
        while True:
            rects_data= visual.endGameSurface2()
            for rect_data in rects_data:
                #rect_data= (rect, function)
                rect=rect_data[0]
                if rect.collidepoint(py.mouse.get_pos()) and self.mouse_button_gets_cklicked():
                    self.game_status=False
                    self.nextRound= rect_data[1]
                    return rect_data[1]


    def createMessage(self, sit, colour_that_makes_the_move):
        message=""
        if sit=="stalemate":
            message= " Stalemate It is a draw"
        else:
            message= "checkmate "+str(colour_that_makes_the_move)+" wins"
        return message






 #----------------------------------------------------------------------------------------------------------------------
 # ---------------------------------------------------------------------------------------------------------------------
    def run_2_player(self, player_color):
        Gamemode= "2Player"
        visual.draw_complete_display(self.all_figures)
        self.update_full_board ()
        self.game_status=True

        while self.game_status==True:
            for event in py.event.get ():
                if event.type == py.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = py.mouse.get_pos ()

                    self.update_clicked_position ((self.mouse_to_board_coords (mouse_x, mouse_y)))
                    self.last_selected_piece = self.selected_piece
                    self.selected_piece = self.get_piece_at_board_coords ()

                    # there are 2 possibles
                    # cliked positiion, can be a piece or none
                    if self.is_piece_selected(self.selected_piece):

                        if (self.selected_piece == self.last_selected_piece):  # deselect
                            self.deselect()
                            visual.draw_complete_display (self.all_figures)

                        else:
                            # an other piece is selected
                            # 1. it is a capturing move, 2. selecting a new piece
                            if(self.is_valid_move(self.last_selected_piece, player_color) and self.color_to_move == self.last_selected_piece.color):
                                self.makeMove(self.last_selected_piece, (self.board_pos_selected_x, self.board_pos_selected_y),player_color, True, self.all_figures, Gamemode)
                                self.update_full_board()
                                visual.draw_complete_display(self.all_figures)

                            else:
                                # new piece was selected
                                if self.selected_piece.color == self.color_to_move:
                                    visual.draw_complete_display(self.all_figures)
                                    visual.mark_accessible_fields(self.selected_piece.get_valid_moves(self.getBoard(), player_color, self.all_figures, self.move_list))
                                    visual.markSquare(self.selected_piece.position)

                    else:
                        #an empty tile is selected
                        if(self.is_valid_move(self.last_selected_piece, player_color)) and self.last_selected_piece.color == self.color_to_move:
                            self.makeMove(self.last_selected_piece, (self.board_pos_selected_x, self.board_pos_selected_y),player_color, False, self.all_figures, Gamemode)
                            visual.draw_complete_display(self.all_figures)

                        else:
                            self.deselect()
                            visual.draw_complete_display(self.all_figures)
                                    
                if event.type == py.QUIT:
                    py.quit ()
                    return

            py.display.flip ()

        return self.nextRound



   # In game.py, within the Game class
    def run_Singel_player(self, player_color, bot : Bot):
        GameMode= "1Player"
        visual.draw_complete_display(self.all_figures)
        self.update_full_board()
        print(player_color)
        if player_color == 'white':
            player_to_play = 1
        else: 
            player_to_play = 2
        print(player_to_play)


        while self.game_status==True:
            for event in py.event.get ():
                if event.type == py.QUIT:
                        py.quit ()
                        return
                if player_to_play == 1:
                    
                    if event.type == py.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = py.mouse.get_pos ()

                        self.update_clicked_position ((self.mouse_to_board_coords (mouse_x, mouse_y)))
                        self.last_selected_piece = self.selected_piece
                        self.selected_piece = self.get_piece_at_board_coords ()

                        # there are 2 possibles
                        # cliked positiion, can be a piece or none
                        if self.is_piece_selected(self.selected_piece):

                            if (self.selected_piece == self.last_selected_piece):  # deselect
                                self.deselect()
                                visual.draw_complete_display (self.all_figures)

                            else:
                                # an other piece is selected
                                # 1. it is a capturing move, 2. selecting a new piece
                                if(self.is_valid_move(self.last_selected_piece, player_color)) and self.color_to_move == self.last_selected_piece.color:
                                    self.makeMove(self.last_selected_piece, (self.board_pos_selected_x, self.board_pos_selected_y),player_color, True, self.all_figures, GameMode)
                                    self.update_full_board()
                                    visual.draw_complete_display(self.all_figures)
                                    player_to_play = 2

                                else:
                                   if self.selected_piece.color == self.color_to_move:
                                    # new piece was selected
                                    visual.draw_complete_display(self.all_figures)
                                    visual.mark_accessible_fields(self.selected_piece.get_valid_moves(self.getBoard(), player_color, self.all_figures, self.move_list))
                                    visual.markSquare(self.selected_piece.position)

                        else:
                            #an empty tile is selected
                            if(self.is_valid_move(self.last_selected_piece, player_color)) and self.color_to_move == self.last_selected_piece.color:
                                self.makeMove(self.last_selected_piece, (self.board_pos_selected_x, self.board_pos_selected_y),player_color, False, self.all_figures, GameMode)
                                visual.draw_complete_display(self.all_figures)
                                player_to_play = 2
                            else:
                                self.deselect()
                                visual.draw_complete_display(self.all_figures)                  
                else:


                    figur,move, newPieceType= bot.chooseMoves(self.all_figures, self.board, player_color, self.move_list)
                    isCap= self.is_capturingMove (figur, self.get_piece_at_position (move[0], move[1]))
                    self.makeMove(figur, move, player_color,isCap,self.all_figures, newPieceType)

                    self.update_full_board()
                    self.update_piece_map()
                    visual.draw_complete_display(self.all_figures)
                    player_to_play = 1


            py.display.flip ()

        return self.nextRound