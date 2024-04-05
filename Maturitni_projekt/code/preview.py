from setting import *
import os

class Preview:
    def __init__(self):
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT - PADDING))
        self.rect = self.surface.get_rect(topright = (WINDOW_WIDTH - PADDING, PADDING))
        self.display_surface = pygame.display.get_surface()

        # pieces
        self.shape_graphics = {shape: pygame.image.load(os.path.join("..", "graphics", f"{shape}.png")).convert_alpha() for shape in PIECES.keys()}

        self.piece_preview_height = self.surface.get_height() / 3

    def draw_preview_shape(self, pieces):
        for i, piece in enumerate(pieces):
            piece_surf = self.shape_graphics[piece]

            x_pos = self.surface.get_width() / 2
            y_pos = self.piece_preview_height / 2 + i * self.piece_preview_height
            rect = piece_surf.get_rect(center=(x_pos,y_pos))
            self.surface.blit(piece_surf, rect)

    def run(self, next_shapes):
        self.surface.fill(BG_COLOR)
        self.draw_preview_shape(next_shapes)
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 3, -1)
        self.next_shapes = next_shapes
        