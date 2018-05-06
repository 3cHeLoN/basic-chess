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
        self.current_player = self.player_white
        self.moves = 0

    def setup_board(self):
        """Initialize the board."""
        for player in [self.player_white, self.player_black]:
            for piece in player.active_pieces:
                self.chessboard.position(piece, piece.initial_position)

    def print_board(self):
        self.chessboard.show()

    def get_board(self):
        return self.chessboard

    def move(self, from_pos, to_pos):
        self.chessboard.move(self.current_player.color, from_pos, to_pos)
        # switch current player
        if self.current_player.color == 'white':
            self.current_player = self.player_black
        else:
            self.current_player = self.player_white
        self.moves += 1
