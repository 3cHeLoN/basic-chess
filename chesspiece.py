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
        self._row = initial_position[0]
        self._col = initial_position[1]
        self.name = None
        self.short_name = None
        self.initial_position = initial_position
        self.files = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.may_jump = None

    def set_position(self, row, col):
        """Change position on the board."""
        self._row = row
        self._col = col

    def __str__(self):
        """Display self."""
        print(self._color + '_' + self.name)

    @property
    def row(self):
        """Return row position of piece."""
        return self._row

    @property
    def col(self):
        """Return col position of piece."""
        return self._col
    @property
    def color(self):
        """Return color of piece."""
        return self._color


class Pawn(ChessPiece):
    """A pawn."""

    def __init__(self, color, initial_position):
        """Create pawn."""
        ChessPiece.__init__(self, color, initial_position)
        self.name = self.files[self._col] + '_Pawn'
        self.short_name = 'p'
        self.may_jump = False
        if color == 'white':
            self.direction = 1
        else:
            self.direction = -1

    def valid_moves(self):
        """Return list of valid moves."""
        capture_moves = []
        moves = []
        if on_board(self._row + self.direction, self._col):
            moves.append((self._row + self.direction, self._col))
        if on_board(self._row + self.direction, self._col - 1):
            capture_moves.append((self._row + self.direction, self._col - 1))
        if on_board(self._row + self.direction, self._col + 1):
            capture_moves.append((self._row + self.direction, self._col + 1))
        return moves, capture_moves


class Rook(ChessPiece):
    """A rook."""

    def __init__(self, color, initial_position):
        """Create rook."""
        ChessPiece.__init__(self, color, initial_position)
        self.name = self.files[self._col] + '_Rook'
        self.short_name = 'R'
        self.may_jump = False

    def valid_moves(self):
        """Return list of valid moves."""
        # add current column
        moves = [(i, self._col) for i in range(8) if i != self._row]
        # add current row
        moves.extend([(self._row, i) for i in range(8) if i != self._col])
        capture_moves = moves.copy()
        return moves, capture_moves


class Bishop(ChessPiece):
    """A bishop."""

    def __init__(self, color, initial_position):
        """Create bishop."""
        ChessPiece.__init__(self, color, initial_position)
        self.name = self.files[self._col] + '_Bishop'
        self.short_name = 'B'
        self.may_jump = False

    def valid_moves(self):
        """Return list of valid moves."""
        # add first diagonal
        moves = [(self._row + i, self._col + i)
                 for i in range(-min(self._row, self._col), min(8 - self._row, 8 - self._col))
                 if i != 0]
        # add second diagonal
        moves.extend(
                [(self._row + i, self._col - i)
                 for i in range(-min(self._row, 8 - self._col), min(8 - self._row, self._col))
                 if i != 0])
        capture_moves = moves.copy()
        return moves, capture_moves


class Knight(ChessPiece):
    """A knight."""

    def __init__(self, color, initial_position):
        """Create knight."""
        ChessPiece.__init__(self, color, initial_position)
        row, col = initial_position
        self.name = self.files[col] + '_Knight'
        self.short_name = 'N'
        self.may_jump = True

    def valid_moves(self):
        """Return list of valid moves."""
        moves = [(self._row + i, self._col + j)
                 for i in [-1, 1] for j in [-2, 2]
                 if on_board(self._row + i, self._col + j)]
        moves.extend([(self._row + i, self._col + j)
                      for i in [-2, 2] for j in [-1, 1]
                      if on_board(self._row + i, self._col + j)])
        capture_moves = moves.copy()
        return moves, capture_moves


class King(ChessPiece):
    """The king."""

    def __init__(self, color, initial_position):
        """Create knight."""
        ChessPiece.__init__(self, color, initial_position)
        row, col = initial_position
        self.name = 'King'
        self.short_name = 'K'
        self.may_jump = False

    def valid_moves(self):
        """Return list of valid moves."""
        moves = [(self._row + i, self._col + j)
                 for i in range(-min(1, self._row), min(2, 8 - self._row))
                 for j in range(-min(1, self._col), min(2, 8 - self.col), 2)]
        capture_moves = moves.copy()
        return moves, capture_moves


class Queen(ChessPiece):
    """The queen."""

    def __init__(self, color, initial_position):
        """Create queen."""
        ChessPiece.__init__(self, color, initial_position)
        row, col = initial_position
        self.name = 'Queen'
        self.short_name = 'Q'
        self.may_jump = False

    def valid_moves(self):
        """Return list of valid moves."""
        # add first diagonal
        moves = [(self._row + i, self._col + i)
                 for i in range(-min(self._row, self._col), min(8 - self._row, 8 - self._col))
                 if i != 0]
        # add second diagonal
        moves.extend(
                [(self._row + i, self._col - i)
                 for i in range(-min(self._row, 8 - self._col), min(8 - self._row, self._col))
                 if i != 0])
        # add current column
        moves.extend([(i, self._col) for i in range(8) if i != self._row])
        # add current row
        moves.extend([(self._row, i) for i in range(8) if i != self._col])
        capture_moves = moves.copy()
        return moves, capture_moves
