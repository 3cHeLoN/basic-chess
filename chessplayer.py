"""Chess player."""

from chesspiece import *


class ChessPlayer:
    """A chess player."""

    def __init__(self, color):
        """Setp chess player."""
        if color not in ['white', 'black']:
            raise ValueError("Unrecognized color!")
        self.color = color
        self.active_pieces = None
        self.captured_pieces = []
        self.setup_pieces()

    def setup_pieces(self):
        """Initialize pieces."""
        self.active_pieces = []
        cols = range(8)
        if self.color == 'white':
            front_row = 1
            back_row = 0
        if self.color == 'black':
            front_row = 6
            back_row = 7

        # add pawns
        for i in cols:
            self.active_pieces.append(Pawn(self.color, (front_row, i)))
        # add rooks
        self.active_pieces.append(Rook(self.color, (back_row, cols[0])))
        self.active_pieces.append(Rook(self.color, (back_row, cols[-1])))
        # add knights
        self.active_pieces.append(Knight(self.color, (back_row, cols[1])))
        self.active_pieces.append(Knight(self.color, (back_row, cols[-2])))
        # add bishops
        self.active_pieces.append(Bishop(self.color, (back_row, cols[2])))
        self.active_pieces.append(Bishop(self.color, (back_row, cols[-3])))
        # add king
        self.active_pieces.append(King(self.color, (back_row, cols[4])))
        # add queen
        self.active_pieces.append(Queen(self.color, (back_row, cols[3])))

    def inactivate_piece(self, chess_piece):
        """Remove a captured piece."""
        self.active_pieces.remove(chess_piece)

    def add(self, piece):
        """Add a piece."""
        self.active_pieces.append(piece)
