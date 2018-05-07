"""A chess board."""

import numpy as np


class Field(object):
    """Keep state of filed on the board."""

    def __init__(self, color):
        """Initialize."""
        if color not in ['white', 'black']:
            raise ValueError("Wrong color!")
        self.color = color
        self.occupied = False
        self.contents = None
    
    def set(self, piece):
        """Set piece on field."""
        self.contents = piece
        self.occupied = True
    
    def get(self):
        """Get contents."""
        return self.contents

    def empty(self):
        """Remove contents."""
        self.contents = None
        self.occupied = False


class ChessBoard(object):
    """Keep state of chessboard."""

    def __init__(self, row_size=8, col_size=8):
        """Create instance."""
        self.row_size = row_size
        self.col_size = col_size
        self.board = [[None for j in range(row_size)] for i in range(col_size)]
        color = 'white'
        for row in range(0, 8):
            if color == 'white':
                color = 'black'
            else:
                color = 'white'
            for col in range(0,8):
                self.board[row][col] = Field(color)
                if color == 'black':
                    color = 'white'
                else:
                    color = 'black'

    def get(self, row, col):
        return self.board[row][col]

    def legal_move(self, color, from_pos, to_pos):
        """Check if move is legal."""
        # first check if piece at target is not the same color
        from_field = self.get(from_pos[0], from_pos[1])
        to_field = self.get(to_pos[0], to_pos[1])
        from_piece = from_field.get()
        if to_field.occupied:
            to_piece = to_field.get()
            if to_piece.color == color:
                return False
            else:
                valid_moves = from_piece.valid_capture_moves(from_pos[0], from_pos[1])
        else:
            # is this a normal move?
            valid_moves = from_piece.valid_moves(from_pos[0], from_pos[1])

        # check if this move corresponds to piece abilities
        if to_pos not in valid_moves:
            # check if this is a specialty move?
            valid_moves = from_piece.specialty_moves(from_pos[0], from_pos[1])
            # still not a valid (specialty) move?
            if to_pos not in valid_moves:
                return False

        # check if piece does not need to jump
        if not from_piece.may_jump:
            n_steps = max(abs(to_pos[0] - from_pos[0]), abs(to_pos[1] - from_pos[1]))
            row_dir = np.sign(to_pos[0] - from_pos[0])
            col_dir = np.sign(to_pos[1] - from_pos[1])
            if n_steps > 1:
                for i in range(1, n_steps):
                    if self.get(from_pos[0] + row_dir * i,
                                 from_pos[1] + col_dir * i).occupied:
                        return False

        return True

    def move(self, color, from_pos, to_pos):
        """Move a piece."""
        if self.legal_move(color, from_pos, to_pos):
            # get field
            from_field = self.get(from_pos[0], from_pos[1])
            to_field = self.get(to_pos[0], to_pos[1])
            # get piece
            piece = from_field.get()
            # empty field
            from_field.empty()
            # put piece to field
            to_field.set(piece)
            return True
        else:
            return False

    def position(self, piece, position):
        """Place a piece."""
        row, col = position
        self.board[row][col].set(piece)

    def show(self):
        """Show self."""
        # start from last row
        end_char = u'\u001b[0m'
        white = u'\u001b[48;5;251m'
        black = u'\u001b[48;5;237m'
        underl = u'\u001b[4m'
        row_color = black
        color = black
        for row in range(7, -1, -1):
            print('\n', end='')
            if row_color == black:
                color = white
                row_color = white
            else:
                color = black
                row_color = black
            for col in range(8):
                if color == white:
                    color = black
                else:
                    color = white
                field = self.board[row][col]
                if not field.occupied:
                    print(color + '   ' + end_char, end='')
                    continue
                piece = field.get()
                if piece is None:
                    continue
                if piece.color == 'white':
                    print(color + ' ' + piece.short_name + ' ' + end_char, end='')
                else:
                    print(color + ' ' + underl + piece.short_name + end_char +  color + ' ' + end_char, end='')
        print('\n')


