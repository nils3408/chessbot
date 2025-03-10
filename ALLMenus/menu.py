import pygame as py
import sys
#from game import Game

class Menu:
    
    def __init__(self):
        py.init()
        # Define colors as instance variables
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (91, 69, 102)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)

        # Define screen size and initialize screen
        self.screen = py.display.set_mode((640, 640))
        py.display.set_caption("Menu")

    def draw_text(self, surface, text, font, color, rect):
        """Draw text on the surface at the specified rectangle."""
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = rect.center
        surface.blit(textobj, textrect)
        
    def run(self):
        """This method should be overridden by subclasses."""
        raise NotImplementedError("Subclasses should implement this!")
