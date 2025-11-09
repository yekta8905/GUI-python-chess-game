import copy                        # chess game project
import tkinter as tk               # yekta bayat 40116463 

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def match(self, list_pos):
        pass

class Piece:
    def __init__(self, color, board, position=None):
        self.color = color
        self.board = board
        self.has_moved = False
        self.position = position

    def possible_moves(self):
        pass

    def move(self, end_pos):
        for pos in self.possible_moves():
            if pos.row == end_pos.row and pos.col == end_pos.col:
                return True
        return False

    def __str__(self):
        pass

class King(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "king"

    def possible_moves(self):
        moves = []
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1),
                   (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (
                    self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
        # Castling
        if not self.board.board[self.position.row][self.position.col].has_moved:
            # Check kingside castling
            if self.board.board[self.position.row][7] and not self.board.board[self.position.row][7].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in
                       range(self.position.col + 1, 7)):
                    moves.append(Position(self.position.row, self.position.col + 2))
            # Check queenside castling
            if self.board.board[self.position.row][0] and not self.board.board[self.position.row][0].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in range(1, self.position.col)):
                    moves.append(Position(self.position.row, self.position.col - 2))
        return moves

    def __str__(self):
        pass


class Bishop(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "bishop"

    def possible_moves(self):
        moves = []
        offsets = [(1, 1), (2, 2), (3, 3), (4, 4),(5, 5), (6, 6), (7, 7), (-1, -1), (-2, -2), (-3, -3), (-4, -4),
                   (-5, -5), (-6, -6), (-7, -7), (-1, 1), (-2, 2), (-3, 3), (-4, 4),
                   (-5, 5), (-6, 6), (-7, 7), (1, -1), (2, -2), (3, -3), (4, -4),
                   (5, -5), (6, -6), (7, -7)]
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (
                    self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                if dr > 0:
                    i = -1
                else:
                    i = 1
                if dc > 0:
                    j = -1
                else:
                    j = 1
                flag = True
                while dr + i != 0 and flag:
                    dr += i
                    dc += j
                    test_pos = Position(self.position.row + dr, self.position.col + dc)
                    if not self.board.is_square_empty(test_pos):
                        flag = False
                if flag:
                    moves.append(new_pos)
        return moves

    def __str__(self):
        pass


class Pawn(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "pawn"
        self.double_step = False

    def possible_moves(self):
        moves = []
        direction = 1 if self.color == "White" else -1
        coefficient = [1, 2]
        # Moves for regular pawn advance
        for x in coefficient:
            new_pos = Position(self.position.row +
                               (direction*x), self.position.col)
            if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos)):
                moves.append(new_pos)
                if not self.has_moved:
                    continue
                else:
                    break
        # Moves for capturing diagonally
        for x in [1, -1]:
            new_pos = Position(self.position.row +
                               direction, self.position.col+x)
            if self.board.is_inside_board(new_pos) and self.board.is_enemy_piece(new_pos, self.color):
                moves.append(new_pos)

        # en passant
        near_piece1 = None
        near_piece2 = None
        if self.position.row == 4 and self.color == "White":

            if -1 < self.position.col + 1 < 8:
                near_piece1 = self.board.board[self.position.row][self.position.col + 1]
            if -1 < self.position.col - 1 < 8:
                near_piece2 = self.board.board[self.position.row][self.position.col - 1]

            if near_piece1 and near_piece1.color != self.color and near_piece1.piece_type == 'pawn' and near_piece1.double_step:
                moves.append(Position(self.position.row + 1, self.position.col + 1))
            if near_piece2 and near_piece2.color != self.color and near_piece2.piece_type == 'pawn' and near_piece2.double_step:
                moves.append(Position(self.position.row + 1, self.position.col - 1))

        if self.position.row == 3 and self.color == "Black":

            if -1 < self.position.col + 1 < 8:
                near_piece1 = self.board.board[self.position.row][self.position.col + 1]
            if -1 < self.position.col - 1 < 8:
                near_piece2 = self.board.board[self.position.row][self.position.col - 1]

            if near_piece1 and near_piece1.color != self.color and near_piece1.piece_type == 'pawn' and near_piece1.double_step:
                moves.append(Position(self.position.row - 1, self.position.col + 1))
            if near_piece2 and near_piece2.color != self.color and near_piece2.piece_type == 'pawn' and near_piece2.double_step:
                moves.append(Position(self.position.row - 1, self.position.col - 1))
        return moves

    def __str__(self):
        pass


class Rook(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "rook"

    def possible_moves(self):

        moves = []
        offsets = [(1, 0), (2, 0), (3, 0), (4, 0),
                   (5, 0), (6, 0), (7, 0), (-1, 0), (-2, 0), (-3, 0), (-4, 0),
                   (-5, 0), (-6, 0), (-7, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                   (0, 5), (0, 6), (0, 7), (0, -1), (0, -2), (0, -3), (0, -4),
                   (0, -5), (0, -6), (0, -7)]
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (
                    self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                if dr > 0:
                    i = -1
                elif dr < 0:
                    i = 1
                else:
                    i = 0
                if dc > 0:
                    j = -1
                elif dc < 0:
                    j = 1
                else:
                    j = 0
                flag = True
                while (dr + i != 0 or dc + j != 0) and flag:
                    dr += i
                    dc += j
                    test_pos = Position(self.position.row + dr, self.position.col + dc)
                    if not self.board.is_square_empty(test_pos):
                        flag = False
                if flag:
                    moves.append(new_pos)

        return moves

    def __str__(self):
        pass


class Knight(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "knight"

    def possible_moves(self):
        moves = []
        offsets = [(1, -2), (2, 1), (1, 2), (-2, -1),
                   (-1, -2), (2, -1), (-1, 2), (-2, 1)]
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
        return moves
    
    def __str__(self):
        pass

class Queen(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "queen"

    def possible_moves(self):
        moves = []
        offsets = [(1, 0), (2, 0), (3, 0), (4, 0),
                   (5, 0), (6, 0), (7, 0), (-1, 0), (-2, 0), (-3, 0), (-4, 0),
                   (-5, 0), (-6, 0), (-7, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                   (0, 5), (0, 6), (0, 7), (0, -1), (0, -2), (0, -3), (0, -4),
                   (0, -5), (0, -6), (0, -7), (1, 1), (2, 2), (3, 3), (4, 4),
                   (5, 5), (6, 6), (7, 7), (-1, -1), (-2, -2), (-3, -3), (-4, -4),
                   (-5, -5), (-6, -6), (-7, -7), (-1, 1), (-2, 2), (-3, 3), (-4, 4),
                   (-5, 5), (-6, 6), (-7, 7), (1, -1), (2, -2), (3, -3), (4, -4),
                   (5, -5), (6, -6), (7, -7)]
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (
                    self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                if dr > 0:
                    i = -1
                elif dr < 0:
                    i = 1
                else:
                    i = 0
                if dc > 0:
                    j = -1
                elif dc < 0:
                    j = 1
                else:
                    j = 0
                flag = True
                while (dr + i != 0 or dc + j != 0) and flag:
                    dr += i
                    dc += j
                    test_pos = Position(self.position.row + dr, self.position.col + dc)
                    if not self.board.is_square_empty(test_pos):
                        flag = False
                if flag:
                    moves.append(new_pos)
        return moves

    def __str__(self):
        pass

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]  # initialize the board

    def place_piece(self, piece, position):
        self.board[position.row][position.col] = piece 
        piece.position = position

    def remove_piece(self, piece):
        self.board[piece.position.row][piece.position.col] = None

    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos.row][start_pos.col]
        if piece:
            if piece.move(end_pos):
                self.remove_piece(piece)
                self.place_piece(piece, end_pos)
                piece.has_moved = True
                return True
        else:
            print("there is no pieace there.")
            return False

    def is_square_empty(self, position):
        return self.board[position.row][position.col] is None

    def is_enemy_piece(self, position, color):
        piece = self.board[position.row][position.col]
        if piece:
            return piece.color != color
        return False

    def is_inside_board(self, position):
        return (-1 < position.row < 8) and (-1 < position.col < 8)

class ChessSet:
    def __init__(self):
        self.board = Board()
        self.setup_board()

    def setup_board(self):
        # Place white pieces
        for i in range(8):
            self.board.place_piece(Pawn("White", self.board), Position(1, i))
        self.board.place_piece(Rook("White", self.board), Position(0, 0))
        self.board.place_piece(Knight("White", self.board), Position(0, 1))
        self.board.place_piece(Bishop("White", self.board), Position(0, 2))
        self.board.place_piece(King("White", self.board), Position(0, 4))
        self.board.place_piece(Queen("White", self.board), Position(0, 3))
        self.board.place_piece(Rook("White", self.board), Position(0, 7))
        self.board.place_piece(Knight("White", self.board), Position(0, 6))
        self.board.place_piece(Bishop("White", self.board), Position(0, 5))        

        # Place black pieces
        for i in range(8):
            self.board.place_piece(Pawn("Black", self.board), Position(6, i))
        self.board.place_piece(Rook("Black", self.board), Position(7, 0))
        self.board.place_piece(Knight("Black", self.board), Position(7, 1))
        self.board.place_piece(Bishop("Black", self.board), Position(7, 2))
        self.board.place_piece(King("Black", self.board), Position(7, 4))
        self.board.place_piece(Queen("Black", self.board), Position(7, 3))
        self.board.place_piece(Rook("Black", self.board), Position(7, 7))
        self.board.place_piece(Knight("Black", self.board), Position(7, 6))
        self.board.place_piece(Bishop("Black", self.board), Position(7, 5))
        
class Chess:
    def __init__(self):
        self.chess_set = ChessSet()
        self.buttonBoard = [[None for _ in range(8)] for _ in range(8)]
        self.root = tk.Tk()
        self.root.title('Chess Game Yekta bayat 40116463')
        self.start_pos = None
        self.turn = 'White'
        self.castling = False
        self.pawn_double_step = None
        self.blackKingImage = tk.PhotoImage(file="blackKing.png")
        self.blackBishopImage = tk.PhotoImage(file='blackBishop.png')
        self.blackKnightImage = tk.PhotoImage(file='blackKnight.png')
        self.blackQueenImage = tk.PhotoImage(file='blackQueen.png')
        self.blackRookImage = tk.PhotoImage(file='blackRook.png')
        self.blackPawnImage = tk.PhotoImage(file='blackPawn.png')
        self.whiteKingImage = tk.PhotoImage(file="whiteKing.png")
        self.whiteBishopImage = tk.PhotoImage(file="whiteBishop.png")
        self.whiteQueenImage = tk.PhotoImage(file="whiteQueen.png")
        self.whiteRookImage = tk.PhotoImage(file="whiteRook.png")
        self.whitePawnImage = tk.PhotoImage(file="whitePawn.png")
        self.whiteKnightImage = tk.PhotoImage(file='whiteKnight.png')

    def is_check(self, current_player):
        king = None
        enemy = "Black" if current_player == "White" else "White"
        for i in range(8):
            for j in range(8):
                piece = self.chess_set.board.board[i][j]
                if piece:
                    if piece.color == current_player and piece.piece_type == 'king':
                        king = piece
        for i in range(8):
            for j in range(8):
                piece = self.chess_set.board.board[i][j]
                if piece and king:
                    if piece.color == enemy:
                        if piece.move(Position(king.position.row, king.position.col)):
                            return True
        return False

    def is_checkmate(self, current_player):
        if self.is_check(current_player):
            start_board = copy.deepcopy(self.chess_set.board.board)
            for i in range(8):
                for j in range(8):
                    piece = self.chess_set.board.board[i][j]
                    if piece and piece.color == current_player:
                        for move in piece.possible_moves():
                            piece = self.chess_set.board.board[i][j]
                            self.chess_set.board.move_piece(piece.position, move)
                            if not self.is_check(current_player):
                                self.chess_set.board.board = copy.deepcopy(start_board)
                                return False
                            self.chess_set.board.board = copy.deepcopy(start_board)

            return True
        return False

    def is_pat(self, current_player):
        start_board = copy.deepcopy(self.chess_set.board.board)
        for i in range(8):
            for j in range(8):
                piece = self.chess_set.board.board[i][j]
                if piece and piece.color == current_player:
                    for move in piece.possible_moves():
                        piece = self.chess_set.board.board[i][j]
                        self.chess_set.board.move_piece(piece.position, move)
                        if not self.is_check(current_player):
                            self.chess_set.board.board = copy.deepcopy(start_board)
                            return False
                        self.chess_set.board.board = copy.deepcopy(start_board)
        return True
    
    def print_board(self):
        color = 'white'
        for i, row in enumerate(self.chess_set.board.board):
            color = '#ffce9e' if color == '#d18b47' else '#d18b47'
            for j, cell in enumerate(row):
                if cell:
                    if cell.color == 'White':
                        if cell.piece_type == 'king':
                            b = tk.Button(self.root, image=self.whiteKingImage, width=89, height=89, bg=color, bd=0)
                        elif cell.piece_type == 'queen':
                            b = tk.Button(self.root, image=self.whiteQueenImage,
                                          bg=color, fg='grey', width=89, height=89, bd=0)
                        elif cell.piece_type == 'bishop':
                            b = tk.Button(self.root, image=self.whiteBishopImage,
                                          bg=color, fg='grey', width=89, height=89, bd=0)
                        elif cell.piece_type == 'knight':
                            b = tk.Button(self.root, image=self.whiteKnightImage,
                                          bg=color, fg='grey', width=89, height=89, bd=0)
                        elif cell.piece_type == 'rook':
                            b = tk.Button(self.root, image=self.whiteRookImage,
                                          bg=color, fg='grey', width=89, height=89, bd=0)
                        elif cell.piece_type == 'pawn':
                            b = tk.Button(self.root, image=self.whitePawnImage,
                                          bg=color, fg='grey', width=89, height=89, bd=0)
                    else:
                        if cell.piece_type == 'king':
                            b = tk.Button(self.root, image=self.blackKingImage, width=89, height=89, bg=color, bd=0)
                        elif cell.piece_type == 'queen':
                            b = tk.Button(self.root, image=self.blackQueenImage,
                                          bg=color, fg='grey', width=89, height=89, bd=0)
                        elif cell.piece_type == 'bishop':
                            b = tk.Button(self.root, image=self.blackBishopImage,
                                          bg=color, fg='grey', width=89, height=89, bd=0)
                        elif cell.piece_type == 'knight':
                            b = tk.Button(self.root, image=self.blackKnightImage,
                                          bg=color, fg='grey', width=89, height=89, bd=0)
                        elif cell.piece_type == 'rook':
                            b = tk.Button(self.root, image=self.blackRookImage,
                                          bg=color, fg='grey', width=89, height=89, bd=0)
                        elif cell.piece_type == 'pawn':
                            b = tk.Button(self.root, image=self.blackPawnImage,
                                          bg=color, fg='grey', width=89, height=89, bd=0)
                else:
                    pixel = tk.PhotoImage(width=1, height=1)
                    b = tk.Button(self.root, text='', image=pixel, width=89, height=89, bg=color, bd=0)
                color = '#ffce9e' if color == '#d18b47' else '#d18b47'
                b.grid(row=i, column=j)
                b.bind("<Button-1>", self.left_click(i, j))
                self.buttonBoard[i][j] = b

    def change_board(self, start_pos, end_pos):
        start_button = self.buttonBoard[start_pos.row][start_pos.col]
        end_button = self.buttonBoard[end_pos.row][end_pos.col]
        start_button.config(image=tk.PhotoImage(width=1, height=1))
        piece_type = self.chess_set.board.board[end_pos.row][end_pos.col].piece_type
        piece_color = self.chess_set.board.board[end_pos.row][end_pos.col].color
        if piece_type == 'king':
            if piece_color == 'White':
                end_button.config(image=self.whiteKingImage)
            else:
                end_button.config(image=self.blackKingImage)
        elif piece_type == 'queen':
            if piece_color == 'White':
                end_button.config(image=self.whiteQueenImage)
            else:
                end_button.config(image=self.blackQueenImage)
        elif piece_type == 'bishop':
            if piece_color == 'White':
                end_button.config(image=self.whiteBishopImage)
            else:
                end_button.config(image=self.blackBishopImage)
        elif piece_type == 'knight':
            if piece_color == 'White':
                end_button.config(image=self.whiteKnightImage)
            else:
                end_button.config(image=self.blackKnightImage)
        elif piece_type == 'rook':
            if piece_color == 'White':
                end_button.config(image=self.whiteRookImage)
            else:
                end_button.config(image=self.blackRookImage)
        elif piece_type == 'pawn':
            if piece_color == 'White':
                end_button.config(image=self.whitePawnImage)
            else:
                end_button.config(image=self.blackPawnImage)

    def pawn_promotion(self):
        for i in range(8):
            for j in range(8):
                piece = self.chess_set.board.board[i][j]
                if piece and piece.piece_type == 'pawn' and (piece.position.row == 0 or piece.position.row == 7):
                    position = piece.position
                    color = piece.color
                    self.chess_set.board.remove_piece(piece)
                    window = tk.Tk()

                    def knight():
                        self.chess_set.board.place_piece(Knight(color, self.chess_set.board, position), position)
                        window.destroy()
                        if color == "White":
                            self.buttonBoard[position.row][position.col].config(image=self.whiteKnightImage)
                        else:
                            self.buttonBoard[position.row][position.col].config(image=self.blackKnightImage)

                    def bishop():
                        self.chess_set.board.place_piece(Bishop(color, self.chess_set.board, position), position)
                        window.destroy()
                        if color == "White":
                            self.buttonBoard[position.row][position.col].config(image=self.whiteBishopImage)
                        else:
                            self.buttonBoard[position.row][position.col].config(image=self.blackBishopImage)

                    def queen():
                        self.chess_set.board.place_piece(Queen(color, self.chess_set.board, position), position)
                        window.destroy()
                        if color == "White":
                            self.buttonBoard[position.row][position.col].config(image=self.whiteQueenImage)
                        else:
                            self.buttonBoard[position.row][position.col].config(image=self.blackQueenImage)

                    def rook():
                        self.chess_set.board.place_piece(Rook(color, self.chess_set.board, position), position)
                        window.destroy()
                        if color == "White":
                            self.buttonBoard[position.row][position.col].config(image=self.whiteRookImage)
                        else:
                            self.buttonBoard[position.row][position.col].config(image=self.blackRookImage)

                    b1 = tk.Button(window, text='knight', width=6, height=3, command=knight)
                    b2 = tk.Button(window, text='bishop', width=6, height=3, command=bishop)
                    b3 = tk.Button(window, text='queen', width=6, height=3, command=queen)
                    b4 = tk.Button(window, text='rook', width=6, height=3, command=rook)
                    b1.grid(row=0, column=0)
                    b2.grid(row=0, column=1)
                    b3.grid(row=1, column=0)
                    b4.grid(row=1, column=1)

    def left_click(self, row, col):
        def inner(event):
            if self.start_pos:
                piece = self.chess_set.board.board[self.start_pos.row][self.start_pos.col]
                if piece.color == self.turn:
                    pass
                else:
                    piece = None
                if piece:
                    if piece.move(Position(row, col)):
                        en_passant_pawn = self.chess_set.board.board[row][col]
                        start_board = copy.deepcopy(self.chess_set.board.board)
                        x = self.chess_set.board.move_piece(self.start_pos, Position(row, col))
                        # castling
                        if piece.piece_type == 'king' and (col == 6 or col == 2) and (col - self.start_pos.col)**2 != 1:
                            if col == 6:
                                rook = self.chess_set.board.board[row][col + 1]
                                self.chess_set.board.remove_piece(rook)
                                self.chess_set.board.place_piece(rook, Position(row, 5))
                                self.castling = col
                            else:
                                rook = self.chess_set.board.board[row][col - 2]
                                self.chess_set.board.remove_piece(rook)
                                self.chess_set.board.place_piece(rook, Position(row, 3))
                                self.castling = col

                            rook.has_moved = True
                        if piece.piece_type == "pawn" and (not en_passant_pawn) and (self.start_pos.row == 3 and row == 2 and (
                                col == self.start_pos.col - 1 or col == self.start_pos.col + 1)) and x:
                            self.chess_set.board.remove_piece(self.chess_set.board.board[3][col])
                            self.buttonBoard[3][col].config(image=tk.PhotoImage(width=1, height=1))
                        elif piece.piece_type == "pawn" and (not en_passant_pawn) and (self.start_pos.row == 4 and row == 5 and (
                                col == self.start_pos.col - 1 or col == self.start_pos.col + 1)) and x:
                            self.chess_set.board.remove_piece(self.chess_set.board.board[4][col])
                            self.buttonBoard[4][col].config(image=tk.PhotoImage(width=1, height=1))

                        if not self.is_check(self.turn):
                            self.turn = "Black" if self.turn == "White" else "White"
                            self.change_board(self.start_pos, Position(row, col))
                            self.pawn_promotion()
                            if self.castling:
                                self.change_board(Position(row, 7 if col == 6 else 0),
                                                  Position(row, 5 if self.castling == 6 else 3))

                            if self.pawn_double_step:
                                pawn = self.chess_set.board.board[self.pawn_double_step.row][self.pawn_double_step.col]
                                if pawn:
                                    pawn.double_step = None
                                self.pawn_double_step = None
                            if piece.piece_type == 'pawn' and (self.start_pos.row - row) ** 2 != 1:
                                piece.double_step = True
                                self.pawn_double_step = Position(row, col)

                        else:
                            self.chess_set.board.board = start_board
                            print('your king in check')
                        self.castling = False
                    else:
                        print("this move is not possible please try again")

                else:
                    print(f"It is {self.turn}'s turn")

                self.start_pos = None

            else:

                if not self.chess_set.board.is_square_empty(Position(row, col)):
                    self.start_pos = Position(row, col)

            if self.is_checkmate(self.turn):
                self.root.destroy()
                enemy = 'White' if self.turn == "Black" else "Black"
                print(f'{enemy} is win')

            if not self.is_check(self.turn) and self.is_pat(self.turn):
                self.root.destroy()
                print('**   draw!  **')
        return inner

    def start_game(self):
        print(" ****  Welcome to Chess game!  **** \n  @@ Yekta bayat 40116463  @@  \n")
        self.print_board()
        self.root.mainloop()

if __name__ == "__main__":
    chess_game = Chess()
    chess_game.start_game()
