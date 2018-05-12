"""Chess pieces."""

from abc import ABC
from util import on_board

class ChessPiece(ABC):
    """Keep state of chesspiece."""

    def __init__(self, color, initial_position):
        """Initalize chess piece."""
        if color not in ['white', 'black']:
            raise ValueError("Unrecognized color!")
        self._color = color
        self.active = True
        self.name = None
        self.short_name = None
        self.initial_position = initial_position
        self.files = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.may_jump = None
        self.n_moves = 0

    def __str__(self):
        """Display self."""
        print(self._color + '_' + self.name)

    @property
    def color(self):
        """Return color of piece."""
        return self._color


class Pawn(ChessPiece):
    """A pawn."""

    def __init__(self, color, initial_position):
        """Create pawn."""
        ChessPiece.__init__(self, color, initial_position)
        initial_col = initial_position[1]
        self.name = self.files[initial_col] + '_Pawn'
        self.short_name = 'p'
        self.may_jump = False
        self.enpassent = None
        self.attacked_position = None
        if color == 'white':
            self.direction = 1
        else:
            self.direction = -1

    def valid_moves(self, position):
        """Return list of valid moves."""
        row, col = position
        moves = []
        if on_board((row + self.direction, col)):
            moves.append((row + self.direction, col))
        if self.enpassent:
           moves.append(self.enpassent)
        return moves

    def valid_capture_moves(self, position):
        """Return list of valid capture moves."""
        row, col = position
        capture_moves = []
        if on_board((row + self.direction, col - 1)):
            capture_moves.append((row + self.direction, col - 1))
        if on_board((row + self.direction, col + 1)):
            capture_moves.append((row + self.direction, col + 1))
        if self.enpassent:
            capture_moves.append(self.enpassent)
        return capture_moves

    def specialty_moves(self, position):
        """Return list of valid capture_moves."""
        row, col = position
        if row == self.initial_position[0]:
            return [(row + self.direction * 2, col)]
        return []

    def set_enpassent(self, position, attacked_position):
        """Set enpassent move to pawn."""
        self.enpassent = position
        self.attacked_position = attacked_position

    def reset_enpassent(self):
        """Reset enpassent move."""
        self.enpassent = None
        self.attacked_position = None


class Rook(ChessPiece):
    """A rook."""

    def __init__(self, color, initial_position):
        """Create rook."""
        ChessPiece.__init__(self, color, initial_position)
        initial_col = initial_position[1]
        self.name = self.files[initial_col] + '_Rook'
        self.short_name = 'R'
        self.may_jump = False

    def valid_moves(self, position):
        """Return list of valid moves."""
        row, col = position
        # add current column
        moves = [(i, col) for i in range(8) if i != row]
        # add current row
        moves.extend([(row, i) for i in range(8) if i != col])
        return moves

    def valid_capture_moves(self, position):
        """Return list of valid capture moves."""
        return self.valid_moves(position)

    def specialty_moves(self, position):
        """Return list of valid capture_moves."""
        return []


class Bishop(ChessPiece):
    """A bishop."""

    def __init__(self, color, initial_position):
        """Create bishop."""
        ChessPiece.__init__(self, color, initial_position)
        initial_col = initial_position[1]
        self.name = self.files[initial_col] + '_Bishop'
        self.short_name = 'B'
        self.may_jump = False

    def valid_moves(self, position):
        """Return list of valid moves."""
        row, col = position
        # add first diagonal
        moves = [(row + i, col + i)
                 for i in range(-min(row, col), min(8 - row, 8 - col))
                 if i != 0]
        # add second diagonal
        moves.extend(
            [(row + i, col - i)
             for i in range(-min(row, 7 - col), min(8 - row, col + 1))
             if i != 0])
        return moves

    def valid_capture_moves(self, position):
        """Return a list of valid capture moves."""
        return self.valid_moves(position)

    def specialty_moves(self, position):
        """Return list of valid capture_moves."""
        return []


class Knight(ChessPiece):
    """A knight."""

    def __init__(self, color, initial_position):
        """Create knight."""
        ChessPiece.__init__(self, color, initial_position)
        initial_col = initial_position[1]
        self.name = self.files[initial_col] + '_Knight'
        self.short_name = 'N'
        self.may_jump = True

    def valid_moves(self, position):
        """Return list of valid moves."""
        row, col = position
        moves = [(row + i, col + j)
                 for i in [-1, 1] for j in [-2, 2]
                 if on_board((row + i, col + j))]
        moves.extend([(row + i, col + j)
                      for i in [-2, 2] for j in [-1, 1]
                      if on_board((row + i, col + j))])
        return moves

    def valid_capture_moves(self, position):
        """Return list of valid capture moves."""
        return self.valid_moves(position)

    def specialty_moves(self, position):
        """Return list of valid capture_moves."""
        return []


class King(ChessPiece):
    """The king."""

    def __init__(self, color, initial_position):
        """Create knight."""
        ChessPiece.__init__(self, color, initial_position)
        row, col = initial_position
        self.name = 'King'
        self.short_name = 'K'
        self.may_jump = False
        if color == 'white':
            self.castle_fields = [(0, 2), (0, 6)]
        else:
            self.castle_fields = [(7, 2), (7, 6)]

    def valid_moves(self, position):
        """Return list of valid moves."""
        row, col = position
        moves = [(row + i, col + j)
                 for i in range(-min(1, row), min(2, 8 - row))
                 for j in range(-min(1, col), min(2, 8 - col))
                 if (i != 0 or j != 0)]
        return moves

    def valid_capture_moves(self, position):
        """Return list of valid capture moves."""
        return self.valid_moves(position)

    def specialty_moves(self, position):
        """Return list of valid capture_moves."""
        if self.n_moves > 0:
            return []
        else:
            return self.castle_fields


class Queen(ChessPiece):
    """The queen."""

    def __init__(self, color, initial_position):
        """Create queen."""
        ChessPiece.__init__(self, color, initial_position)
        row, col = initial_position
        self.name = 'Queen'
        self.short_name = 'Q'
        self.may_jump = False

    def valid_moves(self, position):
        """Return list of valid moves."""
        row, col = position
        # add first diagonal
        moves = [(row + i, col + i)
                 for i in range(-min(row, col), min(8 - row, 8 - col))
                 if i != 0]
        # add second diagonal
        moves.extend(
            [(row + i, col - i)
             for i in range(-min(row, 7 - col), min(8 - row, col + 1))
             if i != 0])
        # add current column
        moves.extend([(i, col) for i in range(8) if i != row])
        # add current row
        moves.extend([(row, i) for i in range(8) if i != col])
        return moves

    def valid_capture_moves(self, position):
        """Return a list of valid capture moves."""
        return self.valid_moves(position)

    def specialty_moves(self, position):
        """Return list of valid capture_moves."""
        return []
