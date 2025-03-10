from typing import Dict, Tuple
import pygame as py
from typing import Optional, List, Tuple
import math

class Next_Move():
    def __init__(self, bot_color, bitboard_white: Dict[str, int], bitboard_black: Dict[str, int], depth):
        py.init()
        self.color = bot_color  # Bot's color (black or white)
        self.color_enemy = 'white' if bot_color == 'black' else 'black'
        self.total_positional_advatge = 0 
        self.bitboard_black_rules = self.initialize_bitboard_rules("black")
        self.bitboard_white_rules = self.initialize_bitboard_rules("white")
        self.bitboard_black = bitboard_black 
        self.bitboard_white = bitboard_white 
        self.depth = depth
        self.captured_pieces_stack = []  # For undoing captures
        self.best_Move = None
        self.lastEval = 0
        self.maxEval = 0
        self.movelist = []
        self.bitBoard_bot_player = bitboard_black if self.color == 'white' else bitboard_white
        self.bitBoard_bot = bitboard_white if self.color == 'white' else bitboard_black
        
    def initialize_bitboard_rules(self, color: str) -> Dict[str, Dict[int, int]]:
        if self.color == 'black':
            return {
                "K": {
                    -6: 18446744073709551360,
                    -5: 18446744073709486335,
                    -4: 18446744073692839935,
                    -3: 18446744069431361535,
                    -2: 18446742978492891135,
                    -1: 18446463698244468735,
                    0: 18374967954648334335,
                    1: 14123288431433875455,
                    2: 13690942867206307839,
                    3: 9151314442816847871,
                },
                "N": {
                    -1: 10272180914755584,
                    0: 18446605379516753919,
                    1: 18446744072698593279,
                    2: 18446744073707192319,
                    3: 18446743687162494975,
                    4: 18436610974547967999,
                },
                "P": {
                    0: 18374966301085925375,
                    1: 18446463698244468735,
                    2: 18446743785946808319,
                    3: 18446743919090728959,
                    4: 18446743970630336511,
                    6: 18446744073709551360,
                },
                "BW": {
                    -1: 18446744073709486079,
                    0: 23690438443597824,
                    1: 18441068033775501311,
                    2: 18428729675200069631,
                },
                "BB": {
                    -1: 18446744073701163007,
                    0: 11914669052657664,
                    1: 18435392535007330303,
                    2: 18446181123756130303,
                },
                "R": {
                    0: 18446743970227683327,
                    1: 18446677947181170687,
                    2: 18411205374297080319,
                    3: 35604928818708480,
                },
                "Q": {
                    0: 35604928818708480,
                    1: 18411205374297080319,
                    2: 18446677947181170687,
                    3: 18446743970227683327,
                },
                "B": {
                    0: 0
                }
            }
        else:
            return {
                "K": {
                    -6: 18446744073709551360,
                    -5: 18446744073709486335,
                    -4: 18446744073692839935,
                    -3: 18446744069431361535,
                    -2: 18446742978492891135,
                    -1: 18446463698244468735,
                    0: 18374967954648334335,
                    1: 14123288431433875455,
                    2: 13690942867206307839,
                    3: 9151314442816847871,
                },
                "N": {
                    -1: 6894481194108928,
                    0: 18439962001909350399,
                    1: 18446671248244080639,
                    2: 18446704491290951679,
                    3: 18446744072199602175,
                    4: 18446744073707192319
                },
                "P": {
                    0: 18446744071545225471,
                    1: 18446744073692839935,
                    2: 18446462601920511999,
                    3: 18446744073105571839,
                    4: 18446744073306898431,
                    6: 72057594037927935
                },
                "BW": {
                    -1: 18446742974197923839,
                    0: 1135283426304,
                    1: 18446744037937769471,
                    2: 18446744073709535231
                },
                "BB": {
                    -1: 18446603336221196287,
                    0: 140806917990912,
                    1: 18446744004279916543,
                    2: 18446744073709551103
                },
                "R": {
                    0: 18446744073709551615,
                    1: 18446744073707183043,
                    2: 18411205374297080319,
                    3: 35604928818740736
                },
                "Q": {
                    0: 35604928818740736,
                    1: 18411205374297080319,
                    2: 18446677947785150463,
                    3: 18446744073306898431
                },
                "B": {
                    0: 0
                }   
            }
    
    def calculate_positional_advantage1(self, color):
        # Calculate positional advantage based on the bot's color
        if color == "black": 
            bitboard_rules = self.bitboard_black_rules
            bitboard = self.bitboard_black
        else: 
            bitboard_rules = self.bitboard_white_rules
            bitboard = self.bitboard_white
        
        # Iterate through bitboard rules and update positional advantage
        for piece, offsets in bitboard_rules.items():
            for offset, rule in offsets.items():
                bitboard_value = bitboard[piece]
                result = rule | bitboard_value
                if result != rule:
                    self.total_positional_advatge += offset
        return self.total_positional_advatge
    
    def calculate_positional_advantage(self, copied_bitBoard_bot, color):
        if color == "black": 
            bitboard_rules = self.bitboard_black_rules
            bitboard = copied_bitBoard_bot
        else: 
            bitboard_rules = self.bitboard_white_rules
            bitboard = copied_bitBoard_bot
            
        # Iterate through bitboard rules and update positional advantage
        for piece, offsets in bitboard_rules.items():
            for offset, rule in offsets.items():
                bitboard_value = bitboard[piece]
                result = rule | bitboard_value
                if result != rule:
                    self.total_positional_advatge += offset
        return self.total_positional_advatge
    
    def is_square_occupied(self, square: int) -> bool:
        # Check if the square is occupied by any piece
        for bitboard in {**self.bitboard_white, **self.bitboard_black}.values():
            if bitboard & (1 << square):
                return True
        return False

    def get_piece_at_square(self, square: int, color: str) -> Optional[str]:
        # Get the piece located at the square for the given color
        bitboard_map = self.bitboard_white if color == 'white' else self.bitboard_black
        for piece, bitboard in bitboard_map.items():
            if bitboard & (1 << square):
                return piece
        return None

    def is_valid_move(self, from_square: int, to_square: int, color: str) -> bool:
        """Validates whether the move from from_square to to_square is valid."""
        # Check if the from and to squares are within bounds
        if not (0 <= from_square < 64 and 0 <= to_square < 64):
            return False
        
        # Ensure a piece exists at the from_square
        piece = self.get_piece_at_square(from_square, color)
        if piece is None:
            return False

        # Ensure we're not capturing our own piece
        if self.get_piece_color(to_square) is not color:
            return False

        # Now, check if the move is valid for the specific piece
        possible_moves = self.get_possible_moves(piece, from_square, color)
        return to_square in possible_moves

    def get_possible_moves(self, piece: str, square: int, color: str) -> List[int]:
        """Generates all possible moves for a given piece from the given square."""
        #possible Fehler:
            #spring über eigene Figuren
            # nimmt eigene Figuren, nicht keine gegnerischen Figuren
            # pawns schlagen gerade aber irgendwie nicht


        moves = []
        rank = square // 8
        file = square % 8
        enemy_color = 'black' if color == 'white' else 'white'

        if piece == 'P':  # Pawn movement
            direction = 1 if color == 'white' else -1
            start_rank = 1 if color == 'white' else 6

            # One square forward
            forward_rank = rank + direction
            if 0 <= forward_rank < 8:
                forward_square = forward_rank * 8 + file
                if not self.is_square_occupied(forward_square):
                    moves.append(forward_square)
                    # Two squares forward from starting position
                    if rank == start_rank:
                        forward_two_rank = rank + 2 * direction
                        if 0 <= forward_two_rank < 8:
                            forward_two_square = forward_two_rank * 8 + file
                            if not self.is_square_occupied(forward_two_square):
                                moves.append(forward_two_square)
            # Captures
            for df in [-1, 1]:
                capture_file = file + df
                if 0 <= capture_file < 8:
                    capture_square = forward_rank * 8 + capture_file
                    if self.get_piece_at_square(capture_square, enemy_color):
                        moves.append(capture_square)

        elif piece == 'N':  # Knight movement
            knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                            (1, -2), (1, 2), (2, -1), (2, 1)]
            for dr, df in knight_moves:
                r, f = rank + dr, file + df
                if 0 <= r < 8 and 0 <= f < 8:
                    target_square = r * 8 + f
                    if self.get_piece_at_square (target_square, color) is None:
                        moves.append (target_square)

        elif piece in ['B', 'BW', 'BB']:  # Bishop movement
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            moves.extend(self._generate_sliding_moves(square, directions, color))
        
        elif piece == 'R':  # Rook movement
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            moves.extend(self._generate_sliding_moves(square, directions, color))
        
        elif piece == 'Q':  # Queen movement
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1),
                          (-1, 0), (1, 0), (0, -1), (0, 1)]
            moves.extend(self._generate_sliding_moves(square, directions, color))
        
        elif piece == 'K':  # King movement
            king_moves = [(-1, -1), (-1, 0), (-1, 1),
                          (0, -1),          (0, 1),
                          (1, -1),  (1, 0),  (1, 1)]
            for dr, df in king_moves:
                r, f = rank + dr, file + df
                if 0 <= r < 8 and 0 <= f < 8:
                    target_square = r * 8 + f
                    if self.get_piece_at_square(target_square, color) is None or \
                       self.get_piece_at_square(target_square, enemy_color):
                        moves.append(target_square)
        return moves


    def _generate_sliding_moves(self, square: int, directions: List[Tuple[int, int]], color: str) -> List[int]:
        """Generates sliding moves for Rook, Bishop, and Queen."""
        moves = []
        rank = square // 8
        file = square % 8

        for dr, df in directions:
            r, f = rank + dr, file + df
            while 0 <= r < 8 and 0 <= f < 8:
                target_square = r * 8 + f
                piece_color = self.get_piece_color(target_square)
                
                if self.is_square_occupied(target_square) is False:
                    # Empty square, continue sliding
                    moves.append(target_square)
                else:
                    # Square occupied by a piece, check color
                    if piece_color == color:
                        # Can capture enemy piece
                        moves.append(target_square)
                    # Stop sliding in this direction (whether it's own or enemy piece)
                    break
                
                # Move further in the same direction
                r += dr
                f += df

        return moves
    
    def get_all_legal_moves(self, color: str) -> List[Tuple[int, int]]:
        legal_moves = []
        bitboard_map = self.bitboard_white if color == 'white' else self.bitboard_black

        for piece, bitboard in bitboard_map.items():
            for square in range(64):
                if bitboard & (1 << square):
                    possible_moves = self.get_possible_moves(piece, square, color)
                    for to_square in possible_moves:
                        if self.is_valid_move(square, to_square, color):
                            legal_moves.append((square, to_square))
        return legal_moves
    
    def get_piece_color(self, square: int) -> Optional[str]:
        """Returns 'white', 'black', or None if the square is empty."""
        if self.is_square_occupied(square):
            for bitboard in self.bitboard_white.values():
                if bitboard & (1 << square):
                    return 'white'
            return 'black'
        return None

    def evaluate_board1(self, color) -> int:
        # Evaluate the board state
        score = 0
        if color == 'white':
            for piece, bitboard in self.bitboard_white.items():
                score += self.get_piece_value(piece) * self.count_bits(bitboard)
            for piece, bitboard in self.bitboard_black.items():
                score -= self.get_piece_value(piece) * self.count_bits(bitboard)
            score = score + self.calculate_positional_advantage1('white')
            score = score - self.calculate_positional_advantage1('black')

            return score
        else: 
            for piece, bitboard in self.bitboard_black.items():
                score += self.get_piece_value(piece) * self.count_bits(bitboard)
            for piece, bitboard in self.bitboard_white.items():
                score -= self.get_piece_value(piece) * self.count_bits(bitboard)
            score = score + self.calculate_positional_advantage1('black')
            score = score - self.calculate_positional_advantage1('white')

            return score
        
    def evaluate_board(self, copied_bitBoard_bot: Dict[str, int], copied_bitBoard_player: Dict[str, int]):
        score = 0
        for piece, bitBoard in copied_bitBoard_bot.items():
            score += self.get_piece_value(piece) * self.count_bits(bitBoard)
            
        for piece, bitBoards in copied_bitBoard_player.items():
            
            score -= self.get_piece_value(piece) * self.count_bits(bitBoards)
        score = score + self.calculate_positional_advantage(copied_bitBoard_bot, self.color)
        score = score - self.calculate_positional_advantage(copied_bitBoard_player, self.color_enemy)

    def get_piece_value(self, piece: str) -> int:
        values = {
            'P': 1,
            'N': 3,
            'B': 0,
            'BW': 3,
            'BB': 3,
            'R': 5,
            'Q': 9,
            'K': 1000  # Assign a high value to the king
        }
        return values.get(piece, 0)

    def count_bits(self, bitboard: int) -> int:
        # Counts the number of set bits (occupied squares) in the bitboard
        return bin(bitboard).count('1')

    def make_move(self, move: Tuple[int, int], color: str) -> None:
        from_square, to_square = move
        piece = self.get_piece_at_square(from_square, color)
        if piece is None:
            raise ValueError(f"No piece at from_square {from_square} for color {color}")

        # Remove the piece from the starting square
        bitboard_map = self.bitboard_white if color == 'white' else self.bitboard_black
        bitboard_map[piece] &= ~(1 << from_square)
        # Place the piece on the destination square
        bitboard_map[piece] |= (1 << to_square)

        # Handle captures
        opponent_color = 'black' if color == 'white' else 'white'
        opponent_bitboard_map = self.bitboard_black if color == 'white' else self.bitboard_white
        captured_piece = None
        for opp_piece, opp_bitboard in opponent_bitboard_map.items():
            if opp_bitboard & (1 << to_square):
                # Remove the captured piece
                opponent_bitboard_map[opp_piece] &= ~(1 << to_square)
                captured_piece = (opp_piece, to_square)
                break
        self.captured_pieces_stack.append(captured_piece)

    def undo_move(self, move: Tuple[int, int], color: str) -> None:
        from_square, to_square = move
        piece = self.get_piece_at_square(to_square, color)
        if piece is None:
            raise ValueError(f"No piece at to_square {to_square} for color {color}")

        # Remove the piece from the destination square
        bitboard_map = self.bitboard_white if color == 'white' else self.bitboard_black
        bitboard_map[piece] &= ~(1 << to_square)
        # Place the piece back on the starting square
        bitboard_map[piece] |= (1 << from_square)

        # Restore captured piece if any
        captured_piece = self.captured_pieces_stack.pop()
        if captured_piece:
            opp_piece, opp_square = captured_piece
            opponent_bitboard_map = self.bitboard_black if color == 'white' else self.bitboard_white
            opponent_bitboard_map[opp_piece] |= (1 << opp_square)

    def make_bitBoard_copy(self, move, color):
        
        if color == 'white':
            self.make_move(move, 'white')
            copied_bitBoard = self.bitboard_white
            self.undo_move(move, 'white')
            return copied_bitBoard
        else: 
            self.make_move(move, 'black')
            copied_bitBoard = self.bitboard_black
            self.undo_move(move, 'black')
            return copied_bitBoard
        
    def bot_best(self, depth: int, botPlayer, lastEval) -> int:
        
        if depth < 1:
            return lastEval, None
        
        if botPlayer:
            maxEval = -math.inf
            best_Move = None
            for move in self.get_all_legal_moves(self.color):
                print(f"Evaluating move for bot: {move}")  # Debugging
                self.bitBoard_bot = self.make_bitBoard_copy(move, self.color)
                lastEval = self.evaluate_board(self.bitBoard_bot, self.bitBoard_bot_player)
                
                eval, _ = self.bot_best(depth -1, False, lastEval)
                
                if eval > maxEval:
                    maxEval = eval
                    best_Move = move
                    
            print(f"Best move for bot at depth {depth}: {best_Move}")  # Debugging
            return maxEval, best_Move
        else:
            minEval = math.inf
            best_Move = None
            for move in self.get_all_legal_moves(self.color_enemy):
                print(f"Evaluating move for opponent: {move}")  # Debugging

                self.bitBoard_bot_player = self.make_bitBoard_copy(move, self.color_enemy)
                lastEval = self.evaluate_board(self.bitBoard_bot, self.bitBoard_bot_player)
                eval, _ = self.bot_best(depth -1, True, lastEval)
                if eval < minEval:
                    minEval = eval
                    
            print(f"Best move for opponent at depth {depth}: {best_Move}")  # Debugging
            return minEval, best_Move
        

    def find_best_move(self) -> Tuple[int, int]:
        botPlayer = True
        print("best_move_logic")
        print(self.color)
        best_move = self.bot_best(3, botPlayer, self.evaluate_board1(self.color))
        print("bestLogicEnd")
        return best_move