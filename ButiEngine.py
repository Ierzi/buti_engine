import chess
from typing import Literal, overload
from PySimple import clear

__author__ = "Ierzi"
__version__ = "v3_evalCheck"

CHECKMATE = "CHECKMATE"
STALEMATE = "STALEMATE"
DRAW = "DRAW"
FIFTY_MOVES_RULE = "FIFTY MOVES RULE"
SEVENTY_FIVE_MOVES_RULE = "SEVENTY FIVE MOVES RULE"
REPETITION = "REPETITION"
INSUFFICIENT_MATERIAL = "INSUFFICIENT MATERIAL"


class Engine:
    def __init__(self):

        # Pieces Tables
        self.pieces_tables = {
            # Pawn Table
            'P': [
                [0,  0,  0,  0,  0,  0,  0,  0],
                [5, 10, 10, -20, -20, 10, 10,  5],
                [5, -5, -10,  0,  0, -10, -5,  5],
                [0,  0,  0, 20, 20,  0,  0,  0],
                [5,  5, 10, 25, 25, 10,  5,  5],
                [10, 10, 20, 30, 30, 20, 10, 10],
                [50, 50, 50, 50, 50, 50, 50, 50],
                [0,  0,  0,  0,  0,  0,  0,  0]
            ],

            # Knight Table
            'N': [
                [-50, -40, -30, -30, -30, -30, -40, -50],
                [-40, -20,  0,  5,  5,  0, -20, -40],
                [-30,  5, 10, 15, 15, 10,  5, -30],
                [-30,  0, 15, 20, 20, 15,  0, -30],
                [-30,  5, 15, 20, 20, 15,  5, -30],
                [-30,  0, 10, 15, 15, 10,  0, -30],
                [-40, -20,  0,  0,  0,  0, -20, -40],
                [-50, -40, -30, -30, -30, -30, -40, -50]
            ],

            # Bishop table
            'B': [
                [-20, -10, -10, -10, -10, -10, -10, -20],
                [-10,  5,  0,  0,  0,  0,  5, -10],
                [-10, 10, 10, 10, 10, 10, 10, -10],
                [-10,  0, 10, 10, 10, 10,  0, -10],
                [-10,  5,  5, 10, 10,  5,  5, -10],
                [-10,  0,  5, 10, 10,  5,  0, -10],
                [-10,  0,  0,  0,  0,  0,  0, -10],
                [-20, -10, -10, -10, -10, -10, -10, -20]
            ],

            # Rook Table
            'R': [
                [0,  0,  0,  0,  0,  0,  0,  0],
                [5, 10, 10, 10, 10, 10, 10,  5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [0,  0,  0,  5,  5,  0,  0,  0]
            ],

            # Queen Table
            'Q': [
                [-20, -10, -10, -5, -5, -10, -10, -20],
                [-10,  0,  0,  0,  0,  0,  0, -10],
                [-10,  0,  5,  5,  5,  5,  0, -10],
                [-5,  0,  5,  5,  5,  5,  0, -5],
                [0,  0,  5,  5,  5,  5,  0, -5],
                [-10,  5,  5,  5,  5,  5,  0, -10],
                [-10,  0,  5,  0,  0,  0,  0, -10],
                [-20, -10, -10, -5, -5, -10, -10, -20]
            ],

            # Black Pawn Table
            'p': [
                [0,  0,  0,  0,  0,  0,  0,  0],
                [50, 50, 50, 50, 50, 50, 50, 50],
                [10, 10, 20, 30, 30, 20, 10, 10],
                [5,  5, 10, 25, 25, 10,  5,  5],
                [0,  0,  0, 20, 20,  0,  0,  0],
                [5, -5, -10,  0,  0, -10, -5,  5],
                [5, 10, 10, -20, -20, 10, 10,  5],
                [0,  0,  0,  0,  0,  0,  0,  0]
            ],

            # Black Knight Table
            'n': [
                [-50, -40, -30, -30, -30, -30, -40, -50],
                [-40, -20,  0,  0,  0,  0, -20, -40],
                [-30,  0, 10, 15, 15, 10,  0, -30],
                [-30,  5, 15, 20, 20, 15,  5, -30],
                [-30,  0, 15, 20, 20, 15,  0, -30],
                [-30,  5, 10, 15, 15, 10,  5, -30],
                [-40, -20,  0,  5,  5,  0, -20, -40],
                [-50, -40, -30, -30, -30, -30, -40, -50]
            ],

            # Black Bishop Table
            'b': [
                [-20, -10, -10, -10, -10, -10, -10, -20],
                [-10,  0,  0,  0,  0,  0,  0, -10],
                [-10,  0,  5, 10, 10,  5,  0, -10],
                [-10,  5,  5, 10, 10,  5,  5, -10],
                [-10,  0, 10, 10, 10, 10,  0, -10],
                [-10, 10, 10, 10, 10, 10, 10, -10],
                [-10, 10,  0,  0,  0,  0, 10, -10],
                [-20, -10, -10, -10, -10, -10, -10, -20]
            ],

            # Black Rook Table
            'r': [
                [0,  0,  0,  5,  5,  0,  0,  0],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [5, 10, 10, 10, 10, 10, 10,  5],
                [0,  0,  0,  0,  0,  0,  0,  0]
            ],

            # Black Queen Table
            'q': [
                [-20, -10, -10, -5, -5, -10, -10, -20],
                [-10,  0,  5,  0,  0,  0,  0, -10],
                [-10,  5,  5,  5,  5,  5,  0, -10],
                [0,  0,  5,  5,  5,  5,  0, -5],
                [-5,  0,  5,  5,  5,  5,  0, -5],
                [-10,  0,  5,  5,  5,  5,  0, -10],
                [-10,  0,  0,  0,  0,  0,  0, -10],
                [-20, -10, -10, -5, -5, -10, -10, -20]
            ]
        }

        # Pieces Values
        self.piece_values = {
            'P': 1,
            'N': 3,
            'B': 3.5,  # Bishops are better than knights
            'R': 5,
            'Q': 9.5,
            'K': 0,  # We assign a value of 0 to the king for simplicity in this basic evaluation
            'p': -1,
            'n': -3,
            'b': -3.5,
            'r': -5,
            'q': -9.5,
            'k': 0
        }

    def evaluate_position(self, board: list, turn: bool):
        # best_evaluation = float("-inf")

        # Search for mate in a depth of 5
        mate_move = self.search_mate(board, 5)
        check, _new_board = self._eval_check(
            board, True if turn == True else False)

        if check != None:
            return check, _new_board

        if mate_move == None:  # No mates found
            evaluation = self.alpha_evaluate_position(board)

            # My calculation of the evaluation (maybe changed later) (v2c)
            return evaluation / self.black_count_pieces(board)
        else:
            return "#"

    def _eval_check(self, board: list, turn: bool, depth: int = 2):
        """Checks for : Mates, Stalemates, Repetitions, Check Repetitions and the 50 moves rule."""

        fen = self.fen_maker(board)
        _board = chess.Board(fen)
        _board.turn = chess.WHITE if turn == True else chess.BLACK

        if depth == 0:  # Last Check
            for move in _board.legal_moves:
                _board.push(move)
                if _board.is_checkmate:
                    return CHECKMATE, _board
                elif _board.is_stalemate:
                    return STALEMATE, _board
                elif _board.is_fifty_moves:
                    return FIFTY_MOVES_RULE, _board
                elif _board.is_repetition:
                    return REPETITION, _board
                elif _board.has_insufficient_material(chess.WHITE and chess.BLACK):
                    return INSUFFICIENT_MATERIAL, _board
                else:
                    return None, _board

        for move in _board.legal_moves:
            _board.push(move)
            if _board.is_checkmate:
                return CHECKMATE
            elif _board.is_stalemate:
                return STALEMATE
            elif _board.is_fifty_moves:
                return FIFTY_MOVES_RULE
            elif _board.is_repetition:
                return REPETITION
            elif _board.has_insufficient_material(chess.WHITE and chess.BLACK):
                return INSUFFICIENT_MATERIAL
            else:
                fen = _board.fen()
                __board = self.fen_to_board(fen)
                return self._eval_check(__board, True if turn == False else False, depth - 1)

    def alpha_evaluate_position(self, board: list):
        score = 0
        for row in board:
            for square in row:
                if square != '.':
                    piece = square
                    score += self.piece_values[piece]
                    score += self.get_piece_square_value(
                        piece, row.index(square), board.index(row))

        return score

    def get_piece_square_value(self, piece, file, rank):
        if piece in self.pieces_tables:
            table = self.pieces_tables[piece]
            if piece.islower():
                table = table[::-1]  # Reverse the table for black pieces

            if rank >= 0 and rank < len(table) and file >= 0 and file < len(table[rank]):
                return table[rank][file]

        return 0

    def search_mate(self, board: list, depth: int):
        _board = chess.Board(self.fen_maker(board))
        best_move = None

        for move in _board.legal_moves:
            _board.push(move)
            mate_score = self._mate_search(_board, depth - 1)
            _board.pop()

            if mate_score == 1:
                # Checkmate found, return the move
                return move

        # No checkmate found
        return None

    def _mate_search(self, board: chess.Board, depth: int):
        if depth == 0:
            if board.is_checkmate():
                return 1  # Checkmate found
            else:
                return 0  # Depth reached, but no checkmate

        for move in board.legal_moves:
            board.push(move)
            mate_score = self._mate_search(board, depth - 1)
            board.pop()

            if mate_score == 0:
                # At least one non-checkmate position found
                return 0

    def best_move(self, board: list, turn: Literal["WHITE", "BLACK"]):
        best_move = ""
        best_evaluation = float("-inf")
        new_board = ...
        self.fen = self.fen_maker(board)
        _board = chess.Board(self.fen)
        # Set the turn.
        _board.turn = chess.WHITE if turn == "WHITE" else chess.BLACK
        for move in _board.legal_moves:
            _board.push(move)  # Make the move
            fen = _board.fen()  # Translate the board into an FEN notation
            # Using a function I made to translate fen into my board notation
            board_ = self.fen_to_board(fen)
            evaluation = self.evaluate_position(
                board_, False if turn == True else True)  # Evaluating the position

            if type(evaluation) == int and evaluation > best_evaluation or evaluation == "#" and best_evaluation != "#":
                best_evaluation = evaluation
                best_move = move
                new_board = board_

            _board.pop()  # Undo last move

        return best_move, new_board

    @overload
    def count_legal_moves(self, board: list, turn) -> int:
        fen = self.fen_maker(board)
        _board = chess.Board(fen)

        if turn == chess.WHITE:
            _board.turn = chess.WHITE
        else:
            _board.turn = chess.BLACK

        legal_moves_count = 0
        for _ in _board.legal_moves():
            legal_moves_count += 1

        return legal_moves_count

    @overload
    def count_legal_moves(self, fen: str, turn) -> int:
        board = chess.Board(fen)

        if turn == chess.WHITE:
            board.turn = chess.WHITE
        else:
            board.turn = chess.BLACK

        legal_moves_count = 0
        for _ in board.legal_moves():
            legal_moves_count += 1

        return legal_moves_count

    def count_pieces(self, board: list):
        pieces_count = 0
        for _, rank in enumerate(board):
            for _, square in enumerate(rank):
                if square != ".":
                    pieces_count += 1

        return pieces_count

    def black_count_pieces(self, board: list):
        b_pieces_count = 0
        for _, rank in enumerate(board):
            for _, square in enumerate(rank):
                if square != "." and square.islower():
                    b_pieces_count += 1

        return b_pieces_count

    def white_count_pieces(self, board: list):
        w_pieces_count = 0
        for _, rank in enumerate(board):
            for _, square in enumerate(rank):
                if square != "." and square.isupper():
                    w_pieces_count += 1

        return w_pieces_count

    def fen_maker(self, board: list):

        fen_voids = 0
        is_not_first_time = False
        self.fen = ""

        for rank in range(8):

            if is_not_first_time:
                self.fen += "/"
            else:
                is_not_first_time = True

            for file in range(8):

                _piece = board[rank][file]

                if _piece == ".":
                    fen_voids += 1
                    if fen_voids == 8:
                        fen_voids = 0
                        self.fen += f"8"
                    elif file == 7:  # End of the line
                        self.fen += f"{fen_voids}"
                        fen_voids = 0

                elif _piece == "P":
                    if fen_voids != 0:
                        self.fen += f"{fen_voids}"
                        fen_voids = 0
                    self.fen += "P"
                elif _piece == "p":
                    if fen_voids != 0:
                        self.fen += f"{fen_voids}"
                        fen_voids = 0
                    self.fen += "p"
                elif _piece == "N":
                    if fen_voids != 0:
                        self.fen += f"{fen_voids}"
                        fen_voids = 0
                    self.fen += "N"
                elif _piece == "n":
                    if fen_voids != 0:
                        self.fen += f"{fen_voids}"
                        fen_voids = 0
                    self.fen += "n"
                elif _piece == "B":
                    if fen_voids != 0:
                        self.fen += f"{fen_voids}"
                        fen_voids = 0
                    self.fen += "B"
                elif _piece == "b":
                    if fen_voids != 0:
                        self.fen += f"{fen_voids}"
                        fen_voids = 0
                    self.fen += "b"
                elif _piece == "R":
                    if fen_voids != 0:
                        self.fen += f"{fen_voids}"
                        fen_voids = 0
                    self.fen += "R"
                elif _piece == "r":
                    if fen_voids != 0:
                        self.fen += f"{fen_voids}"
                        fen_voids = 0
                    self.fen += "r"
                elif _piece == "Q":
                    if fen_voids != 0:
                        self.fen += f"{fen_voids}"
                        fen_voids = 0
                    self.fen += "Q"
                elif _piece == "q":
                    if fen_voids != 0:
                        self.fen += f"{fen_voids}"
                        fen_voids = 0
                    self.fen += "q"
                elif _piece == "K":
                    if fen_voids != 0:
                        self.fen += f"{fen_voids}"
                        fen_voids = 0
                    self.fen += "K"
                elif _piece == "k":
                    if fen_voids != 0:
                        self.fen += f"{fen_voids}"
                        fen_voids = 0
                    self.fen += "k"

        return self.fen

    def create_empty_board(self):
        board = []
        for _ in range(8):
            row = [None] * 8
            board.append(row)

        return board

    def fen_to_board(self, fen: str):

        # Assuming you have a create_empty_board() function
        board = self.create_empty_board()

        # Split the FEN string into separate components
        fen_parts = fen.split()
        fen_position = fen_parts[0]  # Position component of FEN

        # Convert FEN position string to nested list representation
        rank_strings = fen_position.split('/')

        for rank, rank_string in enumerate(rank_strings):
            file_index = 0

            for char in rank_string:
                if char.isdigit():
                    file_index += int(char)
                else:
                    piece = char
                    board[7 - rank][file_index] = piece
                    file_index += 1

        # Replace None with "."
        for rank in range(8):
            for file in range(8):
                if board[rank][file] is None:
                    board[rank][file] = "."

        return board


ButiEngine = Engine()

starting_board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                  ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                  ['.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.'],
                  ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                  ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
                  ]

board = starting_board  # Default value of the board

turn = True


def evaluate(board):
    print("Evaluating the position...")

    evaluation = ButiEngine.evaluate_position(board, turn)

    print(f"Buti Engine v3 says that the evaluation is {evaluation}")


def finding_best_move(board):
    print("Finding the best move...")

    best_move, new_board = ButiEngine.best_move(board, 'WHITE')

    print(
        f"Buti Engine v3 says that the best move, in this posittion is {best_move}")
    # Returns a fen of the new board and prints the chess.Board board
    print(chess.Board(ButiEngine.fen_maker(new_board)))
    # I did not use my board representation beacause it's wrongly formatted.


if __name__ == "__main__":
    while True:
        command = input("Enter a command: ")
        match command:
            case "evaluate" | "eval" | "evaluation":
                evaluate(board)
            case "best_move" | "bm":
                finding_best_move(board)
            case "all" | "play":
                evaluate(board)
                finding_best_move(board)
            case "fen":
                fen = input("Enter a fen: ")
                match fen:
                    case _:
                        board = ButiEngine.fen_to_board(fen)
                        print(chess.Board(ButiEngine.fen_maker(board)))
            case "board":
                board_command = input("Enter a board / command: ")
                match board_command:
                    case "see":
                        print(chess.Board(ButiEngine.fen_maker(board)))
            case "quit":
                clear()
                quit()
            case "cls" | "clear":
                clear()
            case "count":
                turn = input("Which turn? (W/B) ")
                turn = chess.WHITE if turn == "W" else chess.BLACK
                ButiEngine.count_legal_moves(board, turn)
            case "turn":
                turn = input("Which turn? (W/B) ")
                turn = True if turn == "W" else False
