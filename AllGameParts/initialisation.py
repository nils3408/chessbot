from AllFigures.figures import *

def initialize_figures_black():
    return [
        Pawn ("white", 10, (0, 1)), Pawn ("white", 11, (1, 1)), Pawn ("white", 12, (2, 1)), Pawn ("white", 13, (3, 1)),
        Pawn ("white", 14, (4, 1)), Pawn ("white", 15, (5, 1)), Pawn ("white", 16, (6, 1)), Pawn ("white", 17, (7, 1)),

        Rook ("white", 20, (0, 0)), Knight ("white", 21, (1, 0)), Bishop ("white", 22, (2, 0)),
        King ("white", 23, (3, 0)),
        Queen ("white", 24, (4, 0)), Bishop ("white", 25, (5, 0)), Knight ("white", 26, (6, 0)),
        Rook ("white", 27, (7, 0)),

        Pawn ("black", 30, (0, 6)), Pawn ("black", 31, (1, 6)), Pawn ("black", 32, (2, 6)), Pawn ("black", 33, (3, 6)),
        Pawn ("black", 34, (4, 6)), Pawn ("black", 35, (5, 6)), Pawn ("black", 36, (6, 6)), Pawn ("black", 37, (7, 6)),

        Rook ("black", 40, (0, 7)), Knight ("black", 41, (1, 7)), Bishop ("black", 42, (2, 7)),
        King ("black", 43, (3, 7)),
        Queen ("black", 44, (4, 7)), Bishop ("black", 45, (5, 7)), Knight ("black", 46, (6, 7)),
        Rook ("black", 47, (7, 7))
    ]


def initialize_figures_white():
    return [
        Pawn ("black", 10, (0, 1)), Pawn ("black", 11, (1, 1)), Pawn ("black", 12, (2, 1)),
        Pawn ("black", 13, (3, 1)),
        Pawn ("black", 14, (4, 1)), Pawn ("black", 15, (5, 1)), Pawn ("black", 16, (6, 1)),
        Pawn ("black", 17, (7, 1)),

        Rook ("black", 20, (0, 0)), Knight ("black", 21, (1, 0)), Bishop ("black", 22, (2, 0)),
        King ("black", 23, (4, 0)),
        Queen ("black", 24, (3, 0)), Bishop ("black", 25, (5, 0)), Knight ("black", 26, (6, 0)),
        Rook ("black", 27, (7, 0)),

        Pawn ("white", 30, (0, 6)), Pawn ("white", 31, (1, 6)), Pawn ("white", 32, (2, 6)),
        Pawn ("white", 33, (3, 6)),
        Pawn ("white", 34, (4, 6)), Pawn ("white", 35, (5, 6)), Pawn ("white", 36, (6, 6)),
        Pawn ("white", 37, (7, 6)),

        Rook ("white", 40, (0, 7)), Knight ("white", 41, (1, 7)), Bishop ("white", 42, (2, 7)),
        King ("white", 43, (4, 7)),
        Queen ("white", 44, (3, 7)), Bishop ("white", 45, (5, 7)), Knight ("white", 46, (6, 7)),
        Rook ("white", 47, (7, 7))
    ]