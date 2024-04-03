from setting import *
import sys
import random  
import os

# components
from game import Game
from score import Score
from preview import Preview

class Main:
    def __init__(self):

        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # next shapes in preview tab
        self.next_pieces = [random.choice(list(PIECES.keys())) for shape in range(3)]
        print(self.next_pieces)

        # components 
        self.game = Game(self.get_next_shape, self.update_score, self.game_over_menu)
        self.score = Score()
        self.preview = Preview()
        
        # music
        self.music = pygame.mixer.music.load(os.path.join("Maturitni_projekt", "sfx", "shitty_music.wav"))

        # background 
        self.background_image = pygame.image.load(os.path.join("Maturitni_projekt", "graphics", "background.png"))
        self.game_over_image = pygame.image.load(os.path.join("Maturitni_projekt", "graphics", "game_over.png"))
        self.game_background_image = pygame.image.load(os.path.join("Maturitni_projekt", "graphics", "game_bg.png"))
        
        # buttons
        self.start_button_img = pygame.image.load(os.path.join("Maturitni_projekt", "graphics", "start_buton.png"))
        self.quit_button_img = pygame.image.load(os.path.join("Maturitni_projekt", "graphics", "quit_button.png"))
        self.continue_button_img = pygame.image.load(os.path.join("Maturitni_projekt", "graphics", "continue.png" ))
        self.menu_button_img = pygame.image.load(os.path.join("Maturitni_projekt", "graphics", "menu_button.png" ))

    def update_score(self, lines, curr_score, level):
        self.score.lines = lines
        self.score.curr_score = curr_score
        self.score.level = level     


    # generates three random pieces and append them to a list
    def get_next_shape(self):
        next_shape = self.next_pieces.pop(0)
        self.next_pieces.append(random.choice(list(PIECES.keys())))
        return next_shape
    
    def main_menu(self):
        click = False
        self.running = True
        
        pygame.display.set_caption("MAIN MENU")
        while self.running:
            self.display_surface.fill((BG_COLOR))
            
            self.display_surface.blit(self.background_image, (0,0))
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

            self.start_button = pygame.Rect((WINDOW_WIDTH - BUTTON_WIDTH)/2, 225, BUTTON_WIDTH, BUTTON_HEIGHT)
            self.quit_button = pygame.Rect((WINDOW_WIDTH - BUTTON_WIDTH)/2, 350, BUTTON_WIDTH, BUTTON_HEIGHT)

            if self.start_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True:
                    pygame.mixer.music.play(-1)
                    main.run()
            if self.quit_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True:
                    pygame.quit()
                    sys.exit()

            pygame.draw.rect(self.display_surface, RED, self.start_button)
            pygame.draw.rect(self.display_surface, GREEN, self.quit_button)
            self.display_surface.blit(self.start_button_img, ((WINDOW_WIDTH - BUTTON_WIDTH)/2, 225))
            self.display_surface.blit(self.quit_button_img, ((WINDOW_WIDTH - BUTTON_WIDTH)/2, 350))
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        pygame.quit()
                        sys.exit()
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            
                pygame.display.update()
                self.clock.tick(FPS)


    def pause_menu(self):
        click = False
        pygame.mixer.music.pause()
        self.display_surface.fill(BG_COLOR)
        self.running = True
        pygame.display.set_caption("PAUSE")

        while self.running: 
            self.display_surface.fill(BG_COLOR)
            self.display_surface.blit(self.game_background_image, (0,0))
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

            self.continue_button = pygame.Rect((WINDOW_WIDTH - BUTTON_WIDTH)/2, 225, BUTTON_WIDTH, BUTTON_HEIGHT)
            self.main_menu_button = pygame.Rect((WINDOW_WIDTH - BUTTON_WIDTH)/2, 350, BUTTON_WIDTH, BUTTON_HEIGHT)
            self.quit_button = pygame.Rect((WINDOW_WIDTH - BUTTON_WIDTH)/2, 475, BUTTON_WIDTH, BUTTON_HEIGHT)
            
            if self.continue_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True:
                    pygame.mixer.music.unpause()
                    main.run()

            if self.main_menu_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True:
                    self.game.reset_game()
                    self.running = False
                    self.main_menu()
                    
                    
            if self.quit_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True:
                    self.running = False
                    pygame.quit()
                    sys.exit()

            pygame.draw.rect(self.display_surface, RED, self.continue_button)
            pygame.draw.rect(self.display_surface, BLUE, self.main_menu_button)
            pygame.draw.rect(self.display_surface, GREEN, self.quit_button)

            self.display_surface.blit(self.continue_button_img, ((WINDOW_WIDTH - BUTTON_WIDTH)/2, 225))
            self.display_surface.blit(self.menu_button_img, ((WINDOW_WIDTH - BUTTON_WIDTH)/2, 350))
            self.display_surface.blit(self.quit_button_img, ((WINDOW_WIDTH - BUTTON_WIDTH)/2, 475))
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.unpause()
                        self.run()
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                pygame.display.update()
                self.clock.tick(FPS)
        pygame.display.quit()
    
    def game_over_menu(self):
        click = False
        pygame.mixer.music.stop()
        self.display_surface.fill(BG_COLOR)
        self.running = True
        self.show_game_over_menu = True
        
        pygame.display.set_caption("GAME OVER")
        while self.running:
            
            self.display_surface.blit(self.game_background_image, (0,0))
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

            self.main_menu_button = pygame.Rect((WINDOW_WIDTH - BUTTON_WIDTH)/2, 225, BUTTON_WIDTH, BUTTON_HEIGHT)
            self.quit_button = pygame.Rect((WINDOW_WIDTH - BUTTON_WIDTH)/2, 350, BUTTON_WIDTH, BUTTON_HEIGHT)

            if self.main_menu_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True:
                    self.game_over_menu = False
                    main.main_menu()
            if self.quit_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True:
                    pygame.quit()
                    sys.exit()

            pygame.draw.rect(self.display_surface, RED, self.start_button)
            pygame.draw.rect(self.display_surface, GREEN, self.quit_button)
            self.display_surface.blit(self.menu_button_img, ((WINDOW_WIDTH - BUTTON_WIDTH)/2, 225))
            self.display_surface.blit(self.quit_button_img, ((WINDOW_WIDTH - BUTTON_WIDTH)/2, 350))
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        pygame.quit()
                        sys.exit()
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            
            pygame.display.update()
            self.clock.tick(FPS)

    def run(self):
        
        self.running = True
        pygame.display.set_caption("TETRIS")
        pygame.mixer.music.set_volume(10)
        
        while self.running: 
            self.display_surface.fill(BG_COLOR)
            self.display_surface.blit(self.game_background_image, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu()
            
            # components
            self.game.run()
            self.score.run() 
            self.preview.run(self.next_pieces)

            pygame.display.update()
            self.clock.tick(FPS)  
        
            
if __name__ == "__main__":
    main = Main()  
    main.main_menu()
