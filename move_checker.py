"""Returns list of possible moves."""

from chesspiece import ChessPiece

class MoveChecker(object):
    """Check possible moves."""

    def __init__(self, chess_board):
        """Initialize object."""
        self._chess_board = chess_board

    @staticmethod
    def on_board(row, col):
        return (0 <= row < 8) and (0 <= col < 8)

    def _get_pawn_moves(self, row, col):
        """Get moves of pawn."""
        moves = []
        if piece.color == 'white':
            direction = 1
        else:
            direction = -1
        # check forward move
        if not self._chess_board[row + direction][col].is_occpuied:
            moves.append((row + direction, col))
        # check capture moves
        # TODO: this code is probably reused for many pieces!
        for col_move in [-1, 1]:
            if self._chess_board[row + direction][col + col_move].is_occupied:
                if self._chess_board[row + direction][col + col_move].piece.color != piece.color:
                    self.moves.append((row + direction, col + col_move))
        # TODO: implement en-passent
        return moves

    def _get_night_moves(


    def get_moves(self, position):
        """Check possible moves."""
        row, col = position
        piece = chess_board[row][col]
        if type(piece) == ChessPiece.Pawn:
            self._get_pawn_moves(piece, row, col)
