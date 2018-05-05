"""Chess utility functions"""


def on_board(row, col):
    """Check if position is on board."""
    return (0 <= row < 8) and (0 <= col < 8)

def filter_moves(moves):
    """Remove moves that go from board."""
    out_moves = []
    for move in moves:
        if on_board(move):
            out_moves.append(move)
    return out_moves
