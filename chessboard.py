"""A chess board."""

import numpy as np
from time import time


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

    def __init__(self, row_size=8, col_size=8):
        """Create instance."""
        self.row_size = row_size
        self.col_size = col_size
        self.board = [[None for j in range(row_size)] for i in range(col_size)]
        color = 'white'
        self.flag_castle = False
        self.col_names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.king_positions = {'white': None, 'black': None}
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

    def get(self, row, col):
        return self.board[row][col]

    def legal_move(self, color, from_pos, to_pos, test_check=False):
        """Check if move is legal."""
        # first check if piece at target is not the same color
        from_field = self.get(from_pos[0], from_pos[1])
        to_field = self.get(to_pos[0], to_pos[1])
        piece = from_field.get()
        if to_field.occupied:
            to_piece = to_field.get()
            if to_piece.color == color:
                return False
            else:
                valid_moves = piece.valid_capture_moves(from_pos[0], from_pos[1])
        else:
            # is this a normal move?
            valid_moves = piece.valid_moves(from_pos[0], from_pos[1])

        # check if this move corresponds to piece abilities
        if to_pos not in valid_moves:
            # check if this is a specialty move?
            valid_moves = piece.specialty_moves(from_pos[0], from_pos[1])
            # still not a valid (specialty) move?
            if to_pos not in valid_moves:
                return False
            elif piece.short_name == 'K':
                # separately handle castling
                if not self.may_castle(piece.color, from_pos, to_pos):
                    return False
                else:
                    # raise castle flag
                    self.flag_castle = True

        # check if piece does not need to jump
        if not piece.may_jump:
            n_steps = max(abs(to_pos[0] - from_pos[0]), abs(to_pos[1] - from_pos[1]))
            row_dir = np.sign(to_pos[0] - from_pos[0])
            col_dir = np.sign(to_pos[1] - from_pos[1])
            if n_steps > 1:
                for i in range(1, n_steps):
                    if self.get(from_pos[0] + row_dir * i,
                                 from_pos[1] + col_dir * i).occupied:
                        return False

        # test if king will be in check
        if test_check:
            if piece.color == 'white':
                opponent_color = 'black'
            else:
                opponent_color = 'white'
            # attempt the move
            to_piece = to_field.get()
            self.position(piece, to_pos)
            from_field.empty()
            positions_under_attack = self.under_attack_by(opponent_color)
            if self.king_positions[piece.color] in positions_under_attack:
                # undo move
                self.position(piece, from_pos)
                self.position(to_piece, to_pos)
                return False
            else:
                # undo move
                self.position(piece, from_pos)
                self.position(to_piece, to_pos)

        return True

    def may_castle(self, color, from_pos, to_pos):
        """Determines if king with COLOR can castle."""
        # simply check if the squares are not under attack
        if color == 'white':
            opponent_color = 'black'
            rook_row = 0
        else:
            opponent_color = 'white'
            rook_row = 7

        # obtain rook closest to to_pos
        rook_col = np.floor(to_pos[1] / 4).astype('int') * 7
        rook = self.get(rook_row, rook_col).get()
        # check if rook has not moved
        if rook is None or rook.n_moves > 0:
            return False

        positions_under_attack = self.under_attack_by(opponent_color)
        
        n_steps = abs(to_pos[1] - from_pos[1])
        col_dir = np.sign(to_pos[1] - from_pos[1])
        for i in range(1, n_steps + 1):
            if (from_pos[0], from_pos[1] + col_dir * i) in positions_under_attack:
                return False
        return True

    def under_attack_by(self, color, test_check=False):
        """Return list of positions under attack."""
        positions = []

        for row in range(8):
            for col in range(8):
                piece = self.get(row, col).get()
                if piece is not None and piece.color == color:
                    positions.extend(self.legal_capture_moves((row, col), test_check))
        return positions

    def legal_capture_moves(self, from_pos, test_check=False):
        """Determine legal capture moves for a certain position."""
        valid_moves = []
        from_row, from_col = from_pos
        piece = self.get(from_row, from_col).get()
        if piece is None:
            return []
        capture_moves = piece.valid_capture_moves(from_row, from_col)
        for to_pos in capture_moves:
            if self.legal_move(piece.color, from_pos, to_pos, test_check):
                valid_moves.append(to_pos)
        return valid_moves

    def check_or_mate(self, color):
        """Test if current player in checkmate."""
        if color == 'white':
            opponent_color = 'black'
        else:
            opponent_color = 'white'
        positions_under_attack = self.under_attack_by(opponent_color)

        check = False
        checkmate = False

        king_position = self.king_positions[color]

        # is king in check?
        if king_position in positions_under_attack:
            check = True
            # can the king move?
            legal_king_moves = self.legal_capture_moves(king_position, test_check=True)
            if len(legal_king_moves) ==  0:
                # find the attacker(s)
                attackers = self.get_attackers(king_position)
                if len(attackers) > 1:
                    checmate = True
                else:
                    # check if we can attack the attacker
                    attacking_positions = self.under_attack_by(color, test_check=True)
                    if not attackers[0] in attacking_positions:
                        checkmate = True
        return (check, checkmate)

    def get_attackers(self, position, test_check=False):
        """Find the attacker of a certain position."""
        piece = self.get(position[0], position[1]).get()
        if piece.color == 'white':
            opponent_color = 'black'
        else:
            opponent_color = 'white'
        # TODO: make simpler
        attackers = []
        for row in range(8):
            for col in range(8):
                piece = self.get(row, col).get()
                if piece is not None and piece.color == opponent_color:
                    if position in self.legal_capture_moves((row, col)):
                        attackers.append((row, col))
        return attackers

    def move(self, color, from_pos, to_pos):
        """Move a piece.
        
        Returns notation of the move (if legal) and the captured piece.
        If no piece was captured then the returned piece is None.
        """
        t_0 = time()
        if self.legal_move(color, from_pos, to_pos, test_check=True):
            notation = self.get_notation(from_pos, to_pos)
            # check if castle move
            if self.flag_castle:
                # also move corresponding rook
                rook_col = np.floor(to_pos[1] / 4).astype('int') * 7
                rook_field = self.get(from_pos[0], rook_col)
                rook = rook_field.get()

                # determine queen side or king side
                if rook_col == 0:
                        castling_side = 'Queen side'
                        notation = 'O-O-O'
                else:
                        castling_side = 'King side'
                        notation = 'O-O'

                rook_field.empty()
                rook_col = to_pos[1] + np.sign(from_pos[1] - to_pos[1])
                rook_field = self.get(from_pos[0], rook_col)
                rook_field.set(rook)
                # recall castle flag
                self.flag_castle = False

            # get field
            from_field = self.get(from_pos[0], from_pos[1])
            to_field = self.get(to_pos[0], to_pos[1])
            # get piece
            piece = from_field.get()
            # empty field
            from_field.empty()
            captured_piece = to_field.get()
            # put piece to field
            self.position(piece, to_pos)
            # increment number of moves
            piece.n_moves += 1

            print("Move took", time() - t_0, "seconds")
            return notation, captured_piece
        else:
            # make sure castle flag is recalled
            self.flag_castle = False
            return None, None

    def fieldname(self, position):
        """Give fieldname of position."""
        row, col = position
        return self.col_names[col] + str(row + 1) 

    def get_notation(self, from_pos, to_pos):
        """Get notation of move."""
        from_piece = self.get(from_pos[0], from_pos[1]).get()
        to_piece = self.get(to_pos[0], to_pos[1]).get()
        
        if from_piece.short_name == 'p':
            notation_str = ''
        else:
            notation_str = from_piece.short_name 

        if to_piece is not None:
            if from_piece.short_name == 'p':
                notation_str += self.col_names[from_pos[1]]
            notation_str += 'x'
        notation_str += self.fieldname(to_pos)
        return notation_str

    def position(self, piece, position):
        """Place a piece."""
        row, col = position
        self.board[row][col].set(piece)
        # did the king move?
        if piece is None:
            self.get(row, col).occupied = False
        elif piece.short_name == 'K':
            self.king_positions[piece.color] = position

    def show(self):
        """Show self."""
        # start from last row
        end_char = u'\u001b[0m'
        white = u'\u001b[48;5;251m'
        black = u'\u001b[48;5;237m'
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
        print('\n')


