from setting import *
import os

class Score:
    def __init__(self):

        # info about what to display on the score tab
        self.curr_score = 0
        self.level = 1
        self.lines = 0

        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT - PADDING))
        # create a rectangle, so we can place it bottom left
        self.rect = self.surface.get_rect(bottomright = (WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))
        self.display_surface = pygame.display.get_surface()

        # font
        self.font = pygame.font.Font(os.path.join("..","graphics","pixeboy.ttf"), 35)

        self.increment_height = self.surface.get_height() / 3
    
    def display_text(self, positon, text):
        text_surface = self.font.render(f"{text[0]}: {text[1]}", True, WHITE)
        text_rect = text_surface.get_rect(center = positon)
        self.surface.blit(text_surface, text_rect)

    def run(self):
        self.surface.fill(BG_COLOR)
        
        for i, text in enumerate([("score", self.curr_score), ("level".lower(), self.level), ("lines".lower(), self.lines)]):
            x = self.surface.get_width()/2
            y = (self.increment_height / 2) + i * self.increment_height

            self.display_text((x,y), text)
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 3, -1)