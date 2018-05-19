"""Play chess in terminal."""
import sys
import pygame
import json
from pygame.locals import *
from pygame import mixer
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
    sounds = {}
    
    def __init__(self, theme="Theme1", winstyle=0):
        mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        best_depth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
        self.screen = pygame.display.set_mode(SCREENRECT.size, winstyle, best_depth)
        
        with open("img/themes.json", 'r') as fh:
            theme_data = json.load(fh)

        theme_data = theme_data[theme]

        # chess board
        self.sprites['board'] = load_image('img/' + theme_data['filename'])

        # white pieces
        self.sprites['K_white'] = load_image('img/king_white.png')
        self.sprites['Q_white'] = load_image('img/queen_white.png')
        self.sprites['B_white'] = load_image('img/bishop_white.png')
        self.sprites['N_white'] = load_image('img/knight_white.png')
        self.sprites['R_white'] = load_image('img/rook_white.png')
        self.sprites['p_white'] = load_image('img/pawn_white.png')
        self.sprites['DK_white'] = load_image('img/king_white_dead.png')

        # black pieces
        self.sprites['K_black'] = load_image('img/king_black.png')
        self.sprites['Q_black'] = load_image('img/queen_black.png')
        self.sprites['B_black'] = load_image('img/bishop_black.png')
        self.sprites['N_black'] = load_image('img/knight_black.png')
        self.sprites['R_black'] = load_image('img/rook_black.png')
        self.sprites['p_black'] = load_image('img/pawn_black.png')
        self.sprites['DK_black'] = load_image('img/king_black_dead.png')

        self.sprites['Check'] = load_image('img/check.png')
        self.sprites['Promotion'] = load_image('img/promotion.png')

        self.white_highlight = theme_data['highlight_color_light']
        self.black_highlight = theme_data['highlight_color_dark']

        self.overlay = pygame.Surface((SCREENRECT.size), pygame.SRCALPHA)

        self.check = 0
        self.turn_board = False
        self.promotion_pieces = {0: 'Queen', 1: 'Rook', 2: 'Bishop', 3: 'Knight'}
        self.selected_promotion_piece = 0
        self.sounds['move'] = mixer.Sound('snd/move.wav')

    def get_rect(self, position):
        row, col = position
        if self.turn_board and self.game.current_player.color == 'black':
            pos_rect = Rect(560 - col *80, row * 80, 80, 80)
        else:
            pos_rect = Rect(col * 80, 560 - row * 80, 80, 80)
        return pos_rect

    def draw_board(self, highlight_fields=None):
        # get current setup
        board = self.game.get_board()

        # show checkerboard
        self.screen.fill((255, 64, 64))
        self.screen.blit(self.sprites['board'], Rect(0, 0, 640, 640))
        self.overlay.fill((0, 0, 0, 0))

        promotion = board.promotion
        if promotion:
            promotion_pos = promotion[1]
            pos_rect = self.get_rect(promotion_pos)
            self.overlay.blit(self.sprites['Promotion'], pos_rect)

        if self.check:
            # get current king position
            king_position = board.king_positions[self.game.current_player.color]
        else:
            king_position = None

        # fill in highlighted fields
        if highlight_fields is not None:
            for field_pos in highlight_fields:
                row, col = field_pos
                field = board.get((row, col))
                pos_rect = self.get_rect((row, col))
                if field.color == 'white':
                    self.overlay.fill(self.white_highlight, 
                            pos_rect)
                else:
                    self.overlay.fill(self.black_highlight, 
                            pos_rect)
        self.screen.blit(self.overlay, (0, 0))

        for row in range(board.col_size):
            for col in range(board.row_size):
                field = board.get((row, col))
                if field.occupied:
                    piece = field.get()
                    if self.turn_board and self.game.current_player.color == 'black':
                        pos_rect = Rect(560 - col *80, row * 80, 80, 80)
                    else:
                        pos_rect = Rect(col * 80, 560 - row * 80, 80, 80)
                    if (row, col) == king_position:
                        if self.check == 2:
                            self.screen.blit(self.sprites['Check'],
                                pos_rect)
                        elif self.check == 3:
                            self.screen.blit(self.sprites['DK_' + piece.color],
                                pos_rect)
                            continue
                    self.screen.blit(self.sprites[piece.short_name + '_' + piece.color],
                            pos_rect)

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
        state = 0
        while True:
            ev = pygame.event.get()
            # proceed events
            for event in ev:
                # handle MOUSEBUTTONUP
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if current_mode == 2:
                        if event.button == 4:
                            self.selected_promotion_piece = (self.selected_promotion_piece + 1) % 4
                            self.game.choose_promotion(self.promotion_pieces[self.selected_promotion_piece])
                        elif event.button == 5:
                            self.selected_promotion_piece = (self.selected_promotion_piece - 1) % 4
                            self.game.choose_promotion(self.promotion_pieces[self.selected_promotion_piece])
                        elif event.button == 1:
                            self.check = self.game.choose_promotion(self.promotion_pieces[self.selected_promotion_piece], final=True)
                            current_mode = 0
                            self.draw_board()
                        self.draw_board()
                    elif event.button == 1:
                        inverted = self.turn_board and self.game.current_player.color == 'black'

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    clicked_row, clicked_col = self.position_to_field(pos, inverted)
                    field = board.get((clicked_row, clicked_col))
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
                        # deselect piece?
                        if not (clicked_row == from_row and clicked_col == from_col):
                            state = self.game.move((from_row, from_col),
                                    (clicked_row, clicked_col))
                            if state == 0:
                                continue
                            else:
                                self.sounds['move'].play()
                            if state == 1:
                                self.check = 0
                            elif state == 4:
                                # choose promotion
                                current_mode = 2
                                self.selected_promotion_piece = 0
                                self.game.choose_promotion(self.promotion_pieces[self.selected_promotion_piece])
                                highlighted_fields = []
                                self.draw_board(highlighted_fields)
                                continue
                            else:
                                self.check = state
                        highlighted_fields = []
                        current_mode = 0
                        self.draw_board(highlighted_fields)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    @staticmethod
    def position_to_field(pos, inverted):
        """Determine field based on position."""
        if inverted:
            row = int(pos[1] / 80)
            col = int((640 - pos[0]) / 80)
        else:
            row = int((640 - pos[1]) / 80)
            col = int(pos[0] / 80)
        return (row, col)

if __name__ == '__main__':
    app = ChessApp("Theme4")
    app.run()
    sleep(10)
