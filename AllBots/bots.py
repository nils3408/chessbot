# bots.py
from .bot import Bot
from typing import Dict, Tuple
from AllFigures.figures import *
from AllGameParts.helpers import *
import random
import os

from stockfish import Stockfish
from AllGameParts.stockfish_functions import *



class EasyBot(Bot):
    def __init__(self, color: str, piece_map: Dict[Tuple[int, int], 'Figur']):
        super().__init__(color, piece_map)


    def chooseMoves(self,all_figures, board, player_color , movelist):
        #make a random move
        #color is the color of the player (not the bot)!!
        own_figures=self.get_own_figures(all_figures)
        random_figur = own_figures[random.randint (0, len(own_figures)-1)]
        moves= random_figur.get_valid_moves(board, player_color, all_figures,  movelist)

        if len(moves)==0:
            return self.chooseMoves(all_figures, board, player_color, movelist)

        else:
            move= moves[random.randint(0, len(moves)-1)]
            return (random_figur, move)


    def get_own_figures(self,figures):
        figures2=[]
        for figur in figures:
            if figur.color == self.color:
                figures2.append(figur)
        return figures2



class MediumBot(Bot):
    def __init__(self, color: str, piece_map: Dict[Tuple[int, int], 'Figur']):
        super().__init__(color, piece_map)
        


class HardBot(Bot):
    def __init__(self, color: str, piece_map: Dict[Tuple[int, int], 'Figur']):
        self.stockfish = Stockfish(path="C:/Program Files/Stockfish/stockfish2/stockfish-windows-x86-64-avx2",
                                  depth=30,
                                  parameters = {"Threads": max(os.cpu_count() - 2,1 ), "Minimum Thinking Time": 50})


        super().__init__(color, piece_map)


    def chooseMoves(self, all_figures, board, player_color, movelist):

        fen = convert_to_fen(board,all_figures, self.color, player_color)
        if not self.stockfish.is_fen_valid(fen):
            raise Exception("Error. FEN is not valid")

        self.stockfish.set_fen_position(fen)
        move=self.stockfish.get_best_move(8000) #max thinking time of computer
        move2=convert_move(move, board, player_color)
        return move2

