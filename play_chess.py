"""Play chess in terminal."""
import pygame
from pygame.locals import *
from chessgame import ChessGame
from time import sleep

SCREENRECT = Rect(0, 0, 640, 640)

def load_image(filename):
    """Load an image into sdl surface."""
    try:
        surface = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit("Could not load image \"%s\" %s" % (filename, pygame.get_error()))
    return surface.convert_alpha()

class ChessApp:

    sprites = {}
    
    def __init__(self, winstyle=0):
        pygame.init()
        best_depth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
        self.screen = pygame.display.set_mode(SCREENRECT.size, winstyle, best_depth)

        # chess board
        self.sprites['board'] = load_image('img/chessboard.png')

        # white pieces
        self.sprites['K_white'] = load_image('img/king_white.png')
        self.sprites['Q_white'] = load_image('img/queen_white.png')
        self.sprites['B_white'] = load_image('img/bishop_white.png')
        self.sprites['N_white'] = load_image('img/knight_white.png')
        self.sprites['R_white'] = load_image('img/rook_white.png')
        self.sprites['p_white'] = load_image('img/pawn_white.png')

        # black pieces
        self.sprites['K_black'] = load_image('img/king_black.png')
        self.sprites['Q_black'] = load_image('img/queen_black.png')
        self.sprites['B_black'] = load_image('img/bishop_black.png')
        self.sprites['N_black'] = load_image('img/knight_black.png')
        self.sprites['R_black'] = load_image('img/rook_black.png')
        self.sprites['p_black'] = load_image('img/pawn_black.png')

        self.black_highlight = (232, 158, 15)
        self.white_highlight = (255, 208, 21) 

    def draw_board(self, highlight_fields=None):
        # get current setup
        board = self.game.get_board()

        # show checkerboard
        self.screen.fill((255, 64, 64))
        self.screen.blit(self.sprites['board'], Rect(0,0,640,640))

        # fill in highlighted fields
        if highlight_fields is not None:
            for field_pos in highlight_fields:
                row, col = field_pos
                field = board.get(row, col)
                if field.color == 'white':
                    self.screen.fill(self.white_highlight, 
                                     Rect(col * 80, 560 - row * 80, 80, 80))
                else:
                    self.screen.fill(self.black_highlight, 
                                     Rect(col * 80, 560 - row * 80, 80, 80))

        for row in range(board.col_size):
            for col in range(board.row_size):
                field = board.get(row, col)
                if field.occupied:
                    piece = field.get()
                    self.screen.blit(self.sprites[piece.short_name + '_' + piece.color],
                                Rect(col * 80, 560 - row * 80, 80, 80))

        pygame.display.flip()

    def run(self, winstyle=0):
        """Initialize game."""
        self.game = ChessGame()
        self.draw_board()
        # show on screen
        self.wait_for_input()

    def wait_for_input(self):
        """Get user input."""
        board = self.game.get_board()
        highlighted_fields = []
        current_mode = 0
        while True:
            ev = pygame.event.get()
            # proceed events
            for event in ev:
                # handle MOUSEBUTTONUP
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked_row, clicked_col = self.position_to_field(pos)
                    field = board.get(clicked_row, clicked_col)
                    if current_mode == 0:
                        if field.occupied:
                            piece = field.get()
                            if piece.color == self.game.current_player.color:
                                from_row = clicked_row
                                from_col = clicked_col
                                highlighted_fields.append((clicked_row, clicked_col))
                                self.draw_board(highlighted_fields)
                                current_mode = 1
                    elif current_mode == 1:
                        self.game.move((from_row, from_col),
                                       (clicked_row, clicked_col))
                        highlighted_fields = []
                        current_mode = 0
                        self.draw_board(highlighted_fields)
    
    @staticmethod
    def position_to_field(pos):
        """Determine field based on position."""
        row = int((640 - pos[1]) / 80)
        col = int(pos[0] / 80)
        return (row, col)

if __name__ == '__main__':
    app = ChessApp()
    app.run()
    sleep(10)
