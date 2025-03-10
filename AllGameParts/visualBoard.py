# -----------------------------------------------------------------------------------------------------------
# game is splittet into two parts
# what happens intern will be find in game.py
# everythink the User sees in the GUI is defined here

import pygame as py
from typing import Tuple
import time

squareSize = 80
piece_size = int (squareSize * 0.8)
bias = (squareSize - piece_size) // 2
screen = py.display.set_mode ((8 * squareSize, 8 * squareSize))

color1 = '#DFBF93'
color2 = '#C5844E'

alpha = 128  # Adjust transparency


small_window_size_x, small_window_size_y = (4 * squareSize-30, 2 * squareSize-20)
small_window_position= (100,150)


def draw_complete_display(all_figures):
    draw_board ()
    draw_all_pieces (all_figures)
    py.display.flip ()


def draw_board():
    #draw the squares of the Board
    for y in range (8):
        for x in range (8):
            color = color1 if (x + y) % 2 == 0 else color2
            py.draw.rect (screen, color,py.Rect (x * squareSize, y * squareSize, squareSize,squareSize))


def draw_single_piece(piece):
        picture = load_piece_image (piece)
        x, y = piece.position
        screen.blit (picture, (x * squareSize + bias, y * squareSize + bias))


def draw_all_pieces(all_figures):
        for piece in all_figures:
            draw_single_piece (piece)


def load_piece_image(piece):
        piece_type = type (piece).__name__.lower ()
        color = 'w' if piece.color == 'white' else 'b'
        image_path = f"AllFigures/figures_pictures/{color}{piece_type}.png"
        image = py.image.load (image_path).convert_alpha ()
        return py.transform.scale (image, (piece_size, piece_size))


def mark_accessible_fields(moves: Tuple[int, int]):
    #mark the squares a piece can move on
    for x1, y1 in moves:
        py.draw.circle (screen, (0, 255, 0), ((x1) * squareSize + squareSize / 2,(y1) * squareSize + squareSize / 2), 10, 0)
        py.display.flip ()


def markSquare(position:Tuple[int,int]):
    #mark the square the selected piece is standing on
    x,y= position
    py.draw.rect (screen, (0,255,0), (x*squareSize, y*squareSize, squareSize,squareSize),1)
    py.display.flip()



def draw_background_while_pawn_transition():
    #when pawn reaches end of the board, the player has to choose which kind of new piece he wants
    # this function is responsible for the visiual part of this scene
    # Create a surface with the same size as the screen
    overlay = py.Surface(screen.get_size())
    overlay.fill((255,255,255))
    overlay.set_alpha(alpha)  # Set the transparency level

    screen.blit(overlay, (0, 0))
    py.display.flip()



def draw_figures_while_pawn_transition(figures):
    small_window = py.Surface ((small_window_size_x, small_window_size_y))
    small_window.fill ((255, 255, 255))  # Weiß
    all_buttons=[]
    bias=74

    p1 = 2
    p2 = 0.6
    for e in figures:
        picture = load_piece_image (e)
        x, y = get_relative_maus_coords_for_screen2 ()

        color = (128,128,128) if (p1 * 50-bias <= x <= p1 * 50-bias + picture.get_size ()[0] and
                                    p2 * 100 <= y <= p2 * 100 + picture.get_size ()[1]) else (255,255,255)

        r=py.draw.rect (small_window, color, (p1 * 50-bias, p2 * 100, picture.get_width (), picture.get_height ()))
        all_buttons.append((r, e))
        small_window.blit (picture, (p1 * 50-bias, p2 * 100))
        p1 += 1.3

    #text
    font = py.font.SysFont('timesnewroman', 26)
    text_surface= font.render ("Choose new Piece", True, (0, 0, 0))
    small_window.blit(text_surface, (44, 10))

    screen.blit (small_window, small_window_position)
    py.display.flip()

    return all_buttons



def get_relative_maus_coords_for_screen2():
    # get mouse_coords inside of small_window
    x, y = py.mouse.get_pos ()
    # Koordinaten relativ zum kleinen Fenster berechnen
    return (x - small_window_position[0], y - small_window_position[1])




def endGameSurface1(all_figures, message):
    #when game is over: static parts of the  Surface (parts that do not change while beeing in this mode)

    update_square_size(55)
    screen.fill((244, 110, 28))
    draw_complete_display(all_figures)

    #plot message
    string1, string2 = split_string(message)
    font1= py.font.SysFont ('timesnewroman', 37)
    font2= py.font.SysFont('timesnewroman', 30)

    text1= font1.render(str(string1), True, ((0,0,0)))
    screen.blit(text1, (470, 170))
    text2= font2.render(str(string2), True, (0,0,0))
    screen.blit(text2,(470, 200))

    py.display.flip()


def endGameSurface2():
    font2 = py.font.SysFont('timesnewroman', 30)

    rect1 = py.Rect(40, 500, 160, 60)
    rect2 = py.Rect(280, 500, 160, 60)

    x,y= py.mouse.get_pos()
    for event in py.event.get():
       x,y= py.mouse.get_pos()   #need to upate them, do not aks me why

    for rect in [rect1, rect2]:
        if rect.collidepoint((x, y)):
            py.draw.rect(screen, (200, 200, 200), rect.inflate(5, 5), border_radius=40)
        else:
            py.draw.rect(screen, (244, 110, 28),   rect.inflate(5,5), border_radius=40)


    py.draw.rect(screen, (91, 69, 102), rect1, border_radius=40)
    text3 = font2.render("New Game", True, (0, 0, 0))
    screen.blit(text3, (50, 510))

    py.draw.rect(screen, (91, 69, 102), rect2, border_radius=40)
    text4 = font2.render("Main Menu", True, (0, 0, 0))
    screen.blit(text4, (290, 510))

    py.display.flip()
    resetValues()
    return [(rect1, "new Game"),(rect2, "main menu")]




def resetValues():
    global squareSize, piece_size, bias, small_window_size_x, small_window_size_y
    squareSize = 80
    piece_size = int (squareSize * 0.8)
    bias = (squareSize - piece_size) // 2




def update_square_size(new_size):
    global squareSize, piece_size, bias, small_window_size_x, small_window_size_y

    squareSize = new_size
    piece_size = int (squareSize * 0.8)
    bias = (squareSize - piece_size) // 2


def split_string(input_string):
    # Split den String an den Leerzeichen
    words = input_string.split(' ', 1)
    string1 = words[0]
    string2 = words[1] if len(words) > 1 else ''
    return string1, string2


