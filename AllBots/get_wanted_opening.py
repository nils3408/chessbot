import csv 
import pygame as py
from AllFigures.figures import *
import re
from typing import Dict, Optional

#-------------------------------------------# OPENINGS LOGIC #-------------------------------------------#
#           chess_openings.csv is sturcutred like: Key/ ECO code name, Opening name, move order          #
#                                        STRING, STRING, STRING                                          #
#    this class will translate the moves into number values the bots can use and serves as a database    #
#                                                                                                        #
#        it gets the wanted opening as input in form of ECO code and searches the csv File for it        #
#                                                                                                        #
#-------------------------------------------# OPENINGS LOGIC #-------------------------------------------#

class Opening():
    def __init__(self, player_color: str, key, piece_map):
        py.init()
        self.filename = 'chess_openings.csv' 
        self.key = key
        self.player_color = player_color
        self.opening_name: str
        self.opening_moves: str
        self.moves_list
        self.piece_map: Dict[tuple, Figur] = piece_map
        self.valid_moves
        self.piece: Figur
        self.x: int
        self.y: int
        self.opening_pieces: list
        self.opening_move: list
        
    def get_opening_pieces(self):
        return self.opening_pieces
    
    def get_opening_moves(self):
        return self.opening_move
    
    # searches for the key/ ECO code and return the raw string with the moves. Also sets the opening_name to the corresponding Opening
    def find_wanted_opening(self):
        with open(self.filename, newline ='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                key = row[1]
                if key == self.key:
                    self.opening_name = row[1]
                    raw_opening_moves = row[2]
                    return raw_opening_moves
        return "key not found"
    
    def find_played_opening(self):
        print("lol")
        
    # translates the string into usable numbers 
    def process_opening_moves(self, raw_opening_moves):
        # ("1.MOVE move 2.Move")
        # gets rid of "1." and such 
        cleaned_moves = re.sub(r'\d+\.', '', raw_opening_moves)
        # splits at spaces and puts it into a list
        self.moves_list = cleaned_moves.split() # (a3, N.., Q..)
        self.translate_piece()
        
        
    def translate_piece(self):
        self.x, self.y = self.translate_moves()
        for move in self.moves_list:
            if move[0].isupper():
                for position, piece in self.piece_map.items():
                    if move[0] == "N" & piece.type == "N":
                        self.valid_moves = piece.get_valid_moves()
                    if move[0] == "R" & piece.type == "R":
                        self.valid_moves = piece.get_valid_moves()
                    if move[0] == "Q" & piece.type == "Q":
                        self.valid_moves = piece.get_valid_moves()
                    if move[0] == "K" & piece.type == "K":
                        self.valid_moves = piece.get_valid_moves()
                    if move[0] == "B" & piece.type == "B":
                        self.valid_moves = piece.get_valid_moves()

                    for valid_move in self.valid_moves:
                        if valid_move == [self.x, self.y]:
                            self.opening_pieces.append(piece)
                            self.opening_move.append(self.x, self.y)
            else: # Pawn
                for position, piece in self.piece_map.items():
                    if piece.id == self.x: 
                        self.opening_pieces.append(piece)
                        self.opening_move.append(self.x, self.y)
                    
    def translate_moves(self):
        self.x: int
        self.y: int
        for move in self.moves_list:
            if move[0].isupper():
                self.x = self.letterToX(move, 1)
                self.y = move[2]
                return self.x, self.y
            else: # Pawn
                self.x = self.letterToX(move, 0)
                self.y = move[1]
                return self.x, self.y
            
    def letterToX(move, strPos):
         match move[strPos]:
                    case "a":
                        return 1
                    case "b":
                        return 2
                    case "c":
                        return 3
                    case "d":
                        return 4
                    case "e":
                        return 5
                    case "f":
                        return 6
                    case "g":
                        return 7
                    case "h":
                        return 8 
                    case "":
                        return 0      
