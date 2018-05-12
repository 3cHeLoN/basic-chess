"""Chess utility functions"""


def on_board(position):
    """Check if position is on board."""
    return (0 <= position[0] < 8) and (0 <= position[1] < 8)

def filter_moves(moves):
    """Remove moves that go from board."""
    out_moves = []
    for move in moves:
        if on_board(move):
            out_moves.append(move)
    return out_moves
