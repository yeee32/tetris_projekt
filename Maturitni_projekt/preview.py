from setting import *


class Preview:
    def __init__(self):
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT - PADDING))
        self.rect = self.surface.get_rect(topright = (WINDOW_WIDTH - PADDING, PADDING))
        self.display_surface = pygame.display.get_surface()

    def run(self, next_shapes):
        self.surface.fill(BG_COLOR)
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 3, -1)
        self.next_shapes = next_shapes
        
