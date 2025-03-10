import pygame as py
from AllFigures.figures import *
import random


class BoardRenderer:

    def __init__(self, screen, squareSize=80, color1='#DFBF93', color2='#C5844E'):
        self.screen = screen
        self.squareSize = squareSize
        self.color1 = color1
        self.color2 = color2
        self.pieces = self.initialize_pieces ()  # Initialize pieces here
        self.piece_speed = 1  # Speed at which pieces move
        self.piece_size = int (self.squareSize * 0.8)
        self.bias = (self.squareSize - self.piece_size) // 2
        self.clock = py.time.Clock ()  # Initialize clock for frame rate control

    def initialize_pieces(self):
        # Initialize pieces with random positions
        pieces = []
        piece_types = [Pawn, Rook, Knight, Bishop, Queen, King]
        colors = ['white', 'black']

        for _ in range (10):  # Adjust number of pieces
            piece_type = random.choice (piece_types)
            color = random.choice (colors)
            position = (random.randint (0, 7), random.randint (0, 7))
            pieces.append (piece_type (color, random.randint (0, 100), position))

        return pieces

    def draw_board(self):
        for y in range (8):
            for x in range (8):
                color = self.color1 if (x + y) % 2 == 0 else self.color2
                py.draw.rect (self.screen, color,
                              py.Rect (x * self.squareSize, y * self.squareSize, self.squareSize, self.squareSize))

    def draw_pieces(self):
        for piece in self.pieces:
            picture = self.load_piece_image (piece)
            x, y = piece.position
            self.screen.blit (picture, (x * self.squareSize + self.bias, y * self.squareSize + self.bias))

    def load_piece_image(self, piece):
        piece_type = type (piece).__name__.lower ()
        color = 'w' if piece.color == 'white' else 'b'
        image_path = f"AllFigures/figures_pictures/{color}{piece_type}.png"
        image = py.image.load (image_path).convert_alpha ()
        return py.transform.scale (image, (self.piece_size, self.piece_size))

    def move_pieces(self):
        for piece in self.pieces:
            new_x = piece.position[0] + random.randint (-self.piece_speed, self.piece_speed)
            new_y = piece.position[1] + random.randint (-self.piece_speed, self.piece_speed)
            piece.position = (max (0, min (new_x, 7)), max (0, min (new_y, 7)))

    def update(self):
        self.move_pieces ()
        self.draw_board ()
        self.draw_pieces ()
        self.clock.tick (5)




