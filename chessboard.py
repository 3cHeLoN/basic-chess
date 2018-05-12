"""A chess board."""

import numpy as np


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
        self.enpassent_pieces = []
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

    def get(self, position):
        return self.board[position[0]][position[1]]

    def set(self, piece, position):
        """Place a piece."""
        self.board[position[0]][position[1]].set(piece)
        # did the king move?
        if piece is None:
            self.get(position).occupied = False
        elif piece.short_name == 'K':
            self.king_positions[piece.color] = position

    def legal_move(self, color, from_pos, to_pos, test_check=False):
        """Check if move is legal."""
        # first check if piece at target is not the same color
        from_field = self.get(from_pos)
        to_field = self.get(to_pos)
        piece = from_field.get()
        if to_field.occupied:
            to_piece = to_field.get()
            if to_piece.color == color:
                return False
            else:
                valid_moves = piece.valid_capture_moves(from_pos)
        else:
            # is this a normal move?
            valid_moves = piece.valid_moves(from_pos)

        # check if this move corresponds to piece abilities
        if to_pos not in valid_moves:
            # check if this is a specialty move?
            valid_moves = piece.specialty_moves(from_pos)
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
            for i in range(1, n_steps):
                if self.get((from_pos[0] + row_dir * i,
                            from_pos[1] + col_dir * i)).occupied:
                    return False

        # test if king will be in check
        if test_check:
            # attempt the move
            to_piece = to_field.get()
            self.set(piece, to_pos)
            from_field.empty()
            positions_under_attack = self.under_attack_by(self.opponent_color(color))
            if self.king_positions[piece.color] in positions_under_attack:
                # undo move
                self.set(piece, from_pos)
                self.set(to_piece, to_pos)
                return False
            else:
                # undo move
                self.set(piece, from_pos)
                self.set(to_piece, to_pos)

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
        rook = self.get((rook_row, rook_col)).get()
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
                piece = self.get((row, col)).get()
                if piece is not None and piece.color == color:
                    positions.extend(self.legal_capture_moves((row, col), test_check))
        return positions

    def reachable_positions(self, color, test_check=False):
        """Return list of reachable positions."""
        positions = []

        for row in range(8):
            for col in range(8):
                piece = self.get((row, col)).get()
                if piece is not None and piece.color == color:
                    positions.extend(self.legal_moves((row, col), test_check))
        return positions

    def legal_capture_moves(self, from_pos, test_check=False):
        """Determine legal capture moves for a certain position."""
        valid_moves = []
        piece = self.get(from_pos).get()
        if piece is None:
            return []
        capture_moves = piece.valid_capture_moves(from_pos)
        for to_pos in capture_moves:
            if self.legal_move(piece.color, from_pos, to_pos, test_check):
                valid_moves.append(to_pos)
        return valid_moves

    # TODO: This and above functions could be combined
    def legal_moves(self, from_pos, test_check=False):
        """Determine legal moves for a certain position."""
        valid_moves = []
        piece = self.get(from_pos).get()
        if piece is None:
            return []
        moves = piece.valid_moves(from_pos)
        for to_pos in moves:
            if self.legal_move(piece.color, from_pos, to_pos, test_check):
                valid_moves.append(to_pos)
        return valid_moves

    @staticmethod
    def opponent_color(color):
        """Return opponent color."""
        if color == 'white':
            opponent_color = 'black'
        else:
            opponent_color = 'white'
        return opponent_color

    def check_or_mate(self, color):
        """Test if current player in checkmate."""
        opponent_color = self.opponent_color(color)
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
                attackers = self.get_attackers(king_position, opponent_color)
                if len(attackers) > 1:
                    checkmate = True
                else:
                    # check if we can attack the attacker
                    attacker_position = attackers[0]
                    attacking_positions = self.under_attack_by(color, test_check=True)
                    if not attacker_position in attacking_positions:
                        attacking_piece = self.get(attacker_position).get()
                        if attacking_piece.may_jump:
                            checkmate = True
                        else:
                            reachable_positions = self.reachable_positions(color, test_check=True)
                            # see if any fields are under attack
                            n_steps = max(abs(king_position[0] - attacker_position[0]), abs(king_position[1] - attacker_position[1]))
                            row_dir = np.sign(king_position[0] - attacker_position[0])
                            col_dir = np.sign(king_position[1] - attacker_position[1])
                            checkmate = True
                            for i in range(1, n_steps):
                                if (attacker_position[0] + row_dir * i,
                                    attacker_position[1] + col_dir * i) in reachable_positions:
                                    checkmate = False
        return (check, checkmate)

    def get_attackers(self, position, opponent_color, test_check=False):
        """Find the attacker of a certain position."""
        # TODO: make simpler
        attackers = []
        for row in range(8):
            for col in range(8):
                piece = self.get((row, col)).get()
                if piece is not None and piece.color == opponent_color:
                    if position in self.legal_capture_moves((row, col)):
                        attackers.append((row, col))
        return attackers

    def move(self, color, from_pos, to_pos):
        """Move a piece.
        
        Returns notation of the move (if legal) and the captured piece.
        If no piece was captured then the returned piece is None.
        """
        opponent_color = self.opponent_color(color)
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
            from_field = self.get(from_pos)
            to_field = self.get(to_pos)
            # get piece
            piece = from_field.get()
            # first reset enpassent
            if self.enpassent_pieces is not []:
                # was a piece captured enpassent?
                if piece.short_name == 'p' and piece.enpassent == to_pos:
                    # remove piece from board
                    attacked_field = self.get(piece.attacked_position)
                    captured_piece = attacked_field.get()
                    attacked_field.empty()
                for enpassent_piece in self.enpassent_pieces:
                    enpassent_piece.reset_enpassent()
                self.enpassent_pieces = []
            # check again for enpassent
            step = to_pos[0] - from_pos[0]
            if piece.short_name == 'p' and abs(step) == 2:
                # Are the neigbouring fields enemy pawns?
                neighbors = [self.get((to_pos[0], to_pos[1] - i)).get() for i in [-1, 1]]
                direction = np.sign(step)

                for neighbor in neighbors:
                    if neighbor is not None and neighbor.short_name == 'p' \
                        and neighbor.color == opponent_color:
                        # add position to capture moves
                        neighbor.set_enpassent((to_pos[0] - direction, to_pos[1]), to_pos)
                        self.enpassent_pieces.append(neighbor)

            # empty field
            from_field.empty()
            captured_piece = to_field.get()
            # put piece to field
            self.set(piece, to_pos)
            # increment number of moves
            piece.n_moves += 1

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
        from_piece = self.get(from_pos).get()
        to_piece = self.get(to_pos).get()
        
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


