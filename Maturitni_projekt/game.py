from setting import *

class Game:
    def __init__(self):

        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
    

    def draw_grid(self):
        for col in range(1, COLS):
            x = col * CELL_SIZE
            y = GAME_HEIGHT
            pygame.draw.line(self.surface, LINE_COLOR, (x, 0), (x, y), 1)
        for row in range(1, ROWS):
            x = GAME_WIDTH
            y = row * CELL_SIZE
            pygame.draw.line(self.surface, LINE_COLOR, (0, y), (x, y), 1)

    def run(self):
        self.surface.fill(RED)
        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))

    
        