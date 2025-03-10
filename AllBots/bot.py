import pygame as py
from AllFigures.figures import Figur
from typing import Dict, Tuple
from AllBots.get_wanted_opening import Opening
from AllBots.bot_calculate_next_move import *
class Bot:
    def chooseMoves(self, a,b,c,d):
        pass

    def __init__(self, color: str, piece_map: Dict[Tuple[int, int], Figur]):
        py.init()
        self.color = color
#-------------------------------------------# BITMAP LOGIC #-------------------------------------------#
        self.piece_map = piece_map

        # Initialize bitboards
        self.bitboard_pawn_white = 0
        self.bitboard_rook_white = 0
        self.bitboard_knight_white = 0
        self.bitboard_king_white = 0
        self.bitboard_queen_white = 0
        self.bitboard_bishop_white = 0
        self.bitboard_bishop_black_black = 0
        self.bitboard_bishop_black_white = 0


        self.bitboard_pawn_black = 0
        self.bitboard_rook_black = 0
        self.bitboard_knight_black = 0
        self.bitboard_king_black = 0
        self.bitboard_queen_black = 0
        self.bitboard_bishop_black = 0
        self.bitboard_bishop_white_white = 0
        self.bitboard_bishop_white_black = 0

        self.bitboard_map_white = {
            'P': self.bitboard_pawn_white,
            'R': self.bitboard_rook_white,
            'N': self.bitboard_knight_white,
            'K': self.bitboard_king_white,
            'Q': self.bitboard_queen_white,
            'B': self.bitboard_bishop_white,
            'BW': self.bitboard_bishop_white_white,
            'BB': self.bitboard_bishop_white_black
        }

        self.bitboard_map_black = {
            'P': self.bitboard_pawn_black,
            'R': self.bitboard_rook_black,
            'N': self.bitboard_knight_black,
            'K': self.bitboard_king_black,
            'Q': self.bitboard_queen_black,
            'B': self.bitboard_bishop_black,
            'BW': self.bitboard_bishop_black_white,
            'BB': self.bitboard_bishop_black_black
        }
        
        self.initialize_bitboards()
        self.finalise_baord()

        
    def finalise_baord(self):
        self.bitboard_map_black['BW'] = self.bitboard_map_black['B'] & 12297829382473034410
        self.bitboard_map_black['BB'] = self.bitboard_map_black['B'] & 6148914691236517205

        self.bitboard_map_white['BW'] = self.bitboard_map_white['B'] & 6148914691236517205
        self.bitboard_map_white['BB'] = self.bitboard_map_white['B'] & 12297829382473034410

    def position_to_index(self, position: Tuple[int, int]) -> int:
        x, y = position
        return y * 8 + x

    def set_bit(self, bitboard: int, index: int) -> int:
        return bitboard | (1 << index)

    def initialize_bitboards(self):
        if self.color == "black":
            for position, piece in self.piece_map.items():
                index = self.position_to_index(position)
            
                if 30 <= piece.id <= 47:
                    key: str = piece.type                       
                    # Set bit and update
                    # print(key)
                    
                    self.bitboard_map_black[key] = self.set_bit(self.bitboard_map_black[key], index) 
                    # print(self.bitboard_map_black[key])
                    
                if 10 <= piece.id <= 27:
                    key: str = piece.type
                    # Set bit and update
                    self.bitboard_map_white[key] = self.set_bit(self.bitboard_map_white[key], index)
        else:
            for position, piece in self.piece_map.items():
                index = self.position_to_index(position)
                if 30 <= piece.id <= 47:
                    key: str = piece.type                        
                    # Set bit and update
                    # print(key)
                    
                    self.bitboard_map_black[key] = self.set_bit(self.bitboard_map_black[key], index) 
                    # print(self.bitboard_map_black[key])
                    
                if 10 <= piece.id <= 27:
                    key: str = piece.type
                    # Set bit and update
                    self.bitboard_map_white[key] = self.set_bit(self.bitboard_map_white[key], index)

            
    def get_bitboards_white(self) -> Dict[str, int]:
        return self.bitboard_map_white

    def get_bitboards_black(self) -> Dict[str, int]:
        return self.bitboard_map_black
    
    def get_next_move(self):
        nextMove = Next_Move(self.color, self.bitboard_map_white, self.bitboard_map_black, 3)
        maxEval, best_move = nextMove.find_best_move()
        return best_move
    
    def update_piece_map(self, piece_map: Dict[Tuple[int, int], Figur]):
        self.piece_map = piece_map
        # Reset bitboards before reinitializing
        self.reset_bitboards()
        self.initialize_bitboards()
        self.finalise_baord()
        
    def reset_bitboards(self):
        # Reset all bitboards to zero
        for key in self.bitboard_map_white:
            self.bitboard_map_white[key] = 0
        for key in self.bitboard_map_black:
            self.bitboard_map_black[key] = 0
    
#-------------------------------------------# OPENINGS LOGIC #-------------------------------------------#

    def get_opening(self, wanted_opening):
        Opening("white", self.wanted_opening, piece_map = self.piece_map)
        
    def play_opening(self):
        pieces = Opening.get_opening_pieces()
        moves = Opening.get_opening_moves()
        if self.player_color == "white": 
            pieces_sliced = pieces[::2]
            moves_sliced = moves[::2]
            for piece, move in zip(pieces_sliced, moves_sliced):
                print("play " + piece + move)