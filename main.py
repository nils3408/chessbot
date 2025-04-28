from AllGameParts.game import Game
from ALLMenus.menus import *
from AllBots.bots import *

from AllBots.bot import *
from board_rendering import BoardRenderer
from AllBots.get_wanted_opening import Opening

from stockfish import Stockfish



def main():
    player_color = 'white'
    difficulty = 'medium'
    option = 'none'
    playerMode = "1 PlayerMode"

    while True:# Start Menu, color select and difficutly select
        while option != 'start_game':
            option = Main_menu ().run ()
            if option == 'choose_color':
                player_color = Color_menu ().run ()
                print (f"Chosen color: {player_color}")

            if option == 'difficulty':
                difficulty = Difficulty_menu ().run ()
                print (f"Chosen difficulty: {difficulty}")

            if option == 'PlayerMode':
                playerMode= PlayerMode_menu().run()

        player_color = player_color.lower ()
        difficulty = difficulty.lower ()
    
    
        game = Game (player_color)
        game.update_piece_map ()
        piece_map = game.get_piece_map ()

        # Instantiate the bot based on selected difficulty
        if player_color == "white":
            if difficulty == 'easy':
                bot = EasyBot ("black", piece_map)
            elif difficulty == 'medium':
                bot = MediumBot ("black", piece_map)
            elif difficulty == 'hard':
                bot = HardBot ("black", piece_map)
            else:
                raise ValueError ("Unknown difficulty level")
        if player_color == "black":
            if difficulty == 'easy':
                bot = EasyBot ("white", piece_map)
            elif difficulty == 'medium':
                bot = MediumBot ("white", piece_map)
            elif difficulty == 'hard':
                bot = HardBot ("white", piece_map)
            else:
                raise ValueError ("Unknown difficulty level")

        # Update the piece map for the game
        game.update_piece_map ()
        # debug:


        make_a_game= True
        while make_a_game==True:# Run the game
            game.__init__(player_color)
            if playerMode == '1 PlayerMode':
                mode= game.run_Singel_player(player_color, bot)
            else:
                mode= game.run_2_player(player_color)

            #one Game is over, decide where to go (rematch/ main menu)
            print(mode)
            if mode == "main menu":
                make_a_game=False
                option = 'none'
                break




#-----------------------------------------------------------------------------------------

if __name__ == "__main__":
    main ()



#its over anikan