from setting import *

class Score:
    def __init__(self):
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT - PADDING))
        # create a rectangle, so we can place it bottom left
        self.rect = self.surface.get_rect(bottomright = (WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))
        self.display_surface = pygame.display.get_surface()
    
    def run(self):
        self.display_surface.blit(self.surface, self.rect)