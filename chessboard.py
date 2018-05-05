"""A chess board."""

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

    def __init__(self):
        """Create instance."""
        self.board = [[None for j in range(8)] for i in range(8)]
        color = 'black'
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

    def move(self, from_pos, to_pos):
        """Move a piece."""
        pass

    def position(self, piece, position):
        """Place a piece."""
        row, col = position
        self.board[row][col].set(piece)

    def show(self):
        """Show self."""
        # start from last row
        end_char = u'\u001b[0m'
        white = u'\u001b[48;5;251m'#u'\u001b[37;1m'
        black = u'\u001b[48;5;237m'#u'\u001b[37;1m'
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


