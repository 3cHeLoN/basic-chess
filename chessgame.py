"""A game of chess."""

from chessplayer import ChessPlayer
from chessboard import ChessBoard


class ChessGame(object):
    """A game of chess."""

    def __init__(self):
        """Instantiate object."""
        self.chessboard = ChessBoard()
        self.player_white = ChessPlayer('white')
        self.player_black = ChessPlayer('black')
        self.setup_board()

    def setup_board(self):
        """Initialize the board."""
        for player in [self.player_white, self.player_black]:
            for piece in player.active_pieces:
                self.chessboard.position(piece, piece.initial_position)

    def __str__(self):
        print(self.chessboard)
