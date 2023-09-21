"""A game of chess."""

from time import time
from chessplayer import ChessPlayer
from chessboard import ChessBoard
import chesspiece


class ChessGame(object):
class ChessGame:
    """A game of chess."""

    def __init__(self):
        """Instantiate object."""
        self.chessboard = ChessBoard()
        self.player_white = ChessPlayer('white')
        self.player_black = ChessPlayer('black')
        self.setup_board()
        self.current_player = self.player_white
        self.moves = 0
        self.move_number = 1

    def setup_board(self):
        """Initialize the board."""
        for player in [self.player_white, self.player_black]:
            for piece in player.active_pieces:
                self.chessboard.set(piece, piece.initial_position)

    def print_board(self):
        self.chessboard.show()

    def get_board(self):
        return self.chessboard

    def choose_promotion(self, piece_name, final=False):
        # promotion state
        if not self.chessboard.promotion:
            return False
        else:
            state = 4
            promoted_piece, promoted_pos = self.chessboard.promotion
            if piece_name == 'Queen':
                new_piece = chesspiece.Queen(promoted_piece.color, promoted_pos)
            elif piece_name == 'Rook':
                new_piece = chesspiece.Rook(promoted_piece.color, promoted_pos)
            elif piece_name == 'Bishop':
                new_piece = chesspiece.Bishop(promoted_piece.color, promoted_pos)
            elif piece_name == 'Knight':
                new_piece = chesspiece.Knight(promoted_piece.color, promoted_pos)
            self.chessboard.set(new_piece, promoted_pos)
            if final:
                self.chessboard.promotion = None
                # check for check or checkmate!
                check, checkmate = self.chessboard.check_or_mate(self.current_player.color)
                # return state
                if checkmate:
                    state = 3
                elif check:
                    state = 2
                else:
                    state = 1
                # remove piece from player pieces
                if self.current_player.color == 'black':
                    promoted_player = self.player_white
                else:
                    promoted_player = self.player_black
                promoted_player.inactivate_piece(promoted_piece)
                promoted_player.add(new_piece)
            return state

    def move(self, from_pos, to_pos):
        notation, captured_piece = self.chessboard.move(self.current_player.color, from_pos, to_pos)

        # an illegal move was performed
        if notation is None:
            return False

        # add captured piece to captured_pieces list
        if captured_piece is not None:
            self.current_player.captured_pieces.append(captured_piece)
        # switch current player
        if self.current_player.color == 'white':
            print(str(self.move_number) + '. ' + notation, end=' ')
            self.current_player = self.player_black
        else:
            print(notation)
            self.move_number += 1
            self.current_player = self.player_white

        # remove captured piece from active pieces (from other player)
        if captured_piece is not None:
            self.current_player.inactivate_piece(captured_piece)

        # check for check or checkmate!
        check, checkmate = self.chessboard.check_or_mate(self.current_player.color)
        if checkmate:
            print("Checkmate!")
        elif check:
            print("Check!")

        # return state
        if checkmate:
            state = 3
        elif check:
            state = 2
        # check for promoted piece
        elif self.chessboard.promotion:
            state = 4
        else:
            state = 1

        self.moves += 1
        return state
