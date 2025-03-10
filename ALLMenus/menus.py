# menus.py
import pygame as py
import sys
from .menu import Menu
from board_rendering import BoardRenderer


class Main_menu (Menu):
    def __init__(self):
        super ().__init__ ()
        self.squareSize = 80
        self.board_size = 8 * self.squareSize
        self.screen = py.display.set_mode ((self.board_size, self.board_size))
        py.display.set_caption ("Chess Menu")
        self.piece_size = int (self.squareSize * 0.8)
        self.bias = self.squareSize / 10

        self.board_renderer = BoardRenderer (self.screen)

        self.font = py.font.Font (None, 74)
        self.small_font = py.font.Font (None, 36)

        self.menu_items = {
            'Start Game': (self.board_size / 2, 150),
            'Choose Color': (self.board_size / 2, 250),
            'Difficulty': (self.board_size / 2, 350),
            'PlayerMode': (self.board_size/2, 450),
            'Exit': (self.board_size / 2, 550)
        }

    def run(self):
        selected_option = None

        while True:

            self.board_renderer.update ()
            for event in py.event.get ():
                if event.type == py.QUIT:
                    py.quit ()
                    sys.exit ()

                if event.type == py.MOUSEBUTTONDOWN:
                    mouse_pos = py.mouse.get_pos ()
                    for option, pos in self.menu_items.items ():
                        rect = py.Rect (pos[0] - 100, pos[1] - 30, 200, 60)
                        if rect.collidepoint (mouse_pos):
                            if option == 'Start Game':
                                return 'start_game'
                            elif option == 'Choose Color':
                                return 'choose_color'
                            elif option == 'Difficulty':
                                return 'difficulty'
                            elif option =='PlayerMode':
                                return 'PlayerMode'
                            elif option == 'Exit':
                                py.quit ()
                                sys.exit ()

            for option, pos in self.menu_items.items ():
                rect = py.Rect (pos[0] - 100, pos[1] - 30, 200, 60)
                py.draw.rect (self.screen, self.GRAY, rect)
                self.draw_text (self.screen, option, self.font, self.BLACK, rect)

            py.display.flip ()


class Color_menu (Menu):
    def __init__(self):
        super ().__init__ ()
        self.screen_size=(640,640)
        self.screen = py.display.set_mode ((self.screen_size))
        #py.display.set_caption ("Choose Color")

        self.font = py.font.Font (None, 48)
        self.colors = ['White', 'Black']
        self.selected_color = None

        self.image_path1 = "AllMenus/Color_menu_pictures/white1.png"
        self.image_path2 = "AllMenus/Color_menu_pictures/black1.png"


    def run(self):

        while True:
            y = py.mouse.get_pos()[1]
            bias = 60 if y <self.screen_size[1]/2 else -60

            picture1= py.transform.scale (py.image.load (self.image_path1).convert_alpha (), (640, 320 + bias))
            picture2= py.transform.scale (py.image.load (self.image_path2).convert_alpha (), (640, 320 - bias))

            self.screen.blit (picture1, (0, 0))
            self.screen.blit (picture2, (0, 320 + bias))

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()

                if event.type == py.MOUSEBUTTONDOWN:
                    x, y = py.mouse.get_pos()
                    self.selected_color = "white" if y < self.screen_size[1] / 2 else "black"
                    return self.selected_color

            py.display.flip()


class Difficulty_menu:
    def __init__(self):
        py.init ()
        self.screen_size = (640, 640)
        self.screen = py.display.set_mode (self.screen_size)
        py.display.set_caption ("Choose Difficulty")

        self.font = py.font.Font (None, 48)
        self.difficulties = ['Easy', 'Medium', 'Hard']
        self.selected_difficulty = None

        self.picture1 = py.image.load ("AllMenus/Difficulty_menu_pictures/soder.png").convert_alpha ()
        self.picture2 = py.image.load ("AllMenus/Difficulty_menu_pictures/zuckerberg.png").convert_alpha ()
        self.picture3 = py.image.load ("AllMenus/Difficulty_menu_pictures/mittens.png").convert_alpha ()

        self.WHITE = (255, 255, 255)



    def run(self):
        while True:
            self.screen.fill ((244, 110, 28))

            for event in py.event.get ():
                if event.type == py.QUIT:
                    py.quit ()
                    sys.exit ()

                if event.type == py.MOUSEBUTTONDOWN:
                    x,y = py.mouse.get_pos()
                    for i,txt in enumerate(self.difficulties, 1): # i starts at 1
                        if x<= (self.screen_size[0]/3)*(i):
                            return txt


            #paint pictures and frame
            x, y = py.mouse.get_pos ()
            size1, size2, size3 = self.get_picture_sizes_x ((x, y))
            size1y, size2y, size3y = self.get_picture_sizes_y((x,y))

            scaled_picture1 = py.transform.scale (self.picture1, (int (size1), size1y))
            scaled_picture2 = py.transform.scale (self.picture2, (int (size2), size2y))
            scaled_picture3 = py.transform.scale (self.picture3, (int (size3), size3y))

            height1,height2, height3= self.getHeightOffset(size1y, size2y, size3y)
            self.screen.blit (scaled_picture1, (0,                         self.screen_size[1]-size1y-height1))
            self.screen.blit (scaled_picture2, (int (size1),               self.screen_size[1]-size2y-height2))
            self.screen.blit (scaled_picture3, (int (size1) + int (size2), self.screen_size[1]-size3y-height3))

            self.draw_border (x, size1, size2, size3)
            py.display.flip ()


    def getHeightOffset(self, s1, s2, s3):
        #add offset to center picutres on y scale more
        normal_offset=50
        h1= normal_offset if s1+normal_offset <= self.screen_size[1] else 0
        h2= normal_offset if s2+normal_offset <= self.screen_size[1] else 0
        h3= normal_offset if s3+normal_offset <= self.screen_size[1] else 0
        return (h1,h2,h3)


    def get_picture_sizes_x(self, mouse_position):
        # 3 pictures should be painted on the screen
        # based where the mouse is, the chosen picture's size becomes 1/2 of screen_size.
        # the 2 other pictures get size = screen_size/4 each
        x, y = mouse_position
        if x<= self.screen_size[0]/3:
            size1= self.screen_size[0]/2
            size2, size3= self.screen_size[0]/4, self.screen_size[0]/4

        elif x<= (self.screen_size[0]/3)*2:
            size2= self.screen_size[0]/2
            size1, size3= self.screen_size[0]/4, self.screen_size[0]/4

        else:
            size3= self.screen_size[0]/2
            size1, size2= self.screen_size[0]/4, self.screen_size[0]/4

        return (size1, size2, size3)


    def get_picture_sizes_y(self, mouse_position):
       #get y_sizes the pictures should have

        x,y=mouse_position
        scal_parameter= 2
        if x <= self.screen_size[0]/3:
            y1=self.screen_size[1]
            y2, y3= self.screen_size[1]/scal_parameter, self.screen_size[1]/scal_parameter

        elif x<= self.screen_size[0]*2/3:
            y2=self.screen_size[1]
            y1, y3= self.screen_size[1]/scal_parameter, self.screen_size[1]/scal_parameter

        else:
            y3=self.screen_size[1]
            y1,y2= self.screen_size[1]/scal_parameter, self.screen_size[1]/(scal_parameter)

        return (y1,y2,y3)




    def draw_border(self, mouse_x, size1, size2, size3):
        color= (200,200,200)

        if mouse_x <= self.screen_size[0] / 3:
            # Draw a border around picture1
            py.draw.rect (self.screen, color, (0, 0, int (size1), self.screen_size[1]), 5)
        elif mouse_x <= (self.screen_size[0] / 3) * 2:
            # Draw a border around picture2
            py.draw.rect (self.screen, color, (int (size1), 0, int (size2), self.screen_size[1]), 5)
        else:
            # Draw a border around picture3
            py.draw.rect (self.screen, color, (int (size1) + int (size2), 0, int (size3), self.screen_size[1]), 5)





class PlayerMode_menu(Menu):
    def __init__(self):
        super ().__init__ ()
        self.screen_size = (640, 640)
        self.screen = py.display.set_mode ((self.screen_size))
        py.display.set_caption ("Choose PlayerMode")

        self.font = py.font.Font (None, 48)
        self.selectedPlayerMode = None
        self.possibleModes = ['1 PlayerMode', '2 PlayerMode']

        self.end_of_picture1 = 313 #hardcoded

    def run(self):
        while True:
            for event in py.event.get ():
                if event.type == py.QUIT:
                    py.quit ()
                    sys.exit ()

                #get cklicked side
                if event.type == py.MOUSEBUTTONDOWN:
                    x,y = py.mouse.get_pos ()
                    if x<= self.end_of_picture1:
                        return '2 PlayerMode'
                    else:
                        return '1 PlayerMode'

            # blit background image
            image_path = "AllMenus/Player_menu_pictures/PlayerMode.png"
            image = py.transform.scale (py.image.load (image_path).convert_alpha (), (640,640))
            self.screen.blit (image, (0, 0))

            #draw white frame
            x1,y1= py.mouse.get_pos()
            color= (200,200,200)
            xPos = 0 if x1<=self.end_of_picture1 else self.end_of_picture1
            bias = 0 if x1<=self.end_of_picture1 else 13   #need bias cause right picture is bigger then left one
            py.draw.rect (self.screen,color, (xPos, 0, self.end_of_picture1+bias, 640), 5)

            py.display.flip()
