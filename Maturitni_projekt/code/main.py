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

        # components 
        self.game = Game(self.get_next_shape, self.update_score, self.game_over_menu)
        self.score = Score()
        self.preview = Preview()
        
        # music
        self.music = os.path.join("..", "sfx", "game_music.wav")
        self.main_menu_music = os.path.join("..", "sfx", "main_menu_music.wav")
        self.game_over_music = os.path.join("..", "sfx", "game_over_music.wav")
        self.mute_music = False

        # backgrounds
        self.background_image = pygame.image.load(os.path.join("..", "graphics", "backgrounds", "background.png"))
        self.game_over_image = pygame.image.load(os.path.join("..", "graphics", "backgrounds", "game_over.png"))
        self.game_background_image = pygame.image.load(os.path.join("..", "graphics", "backgrounds", "game_bg.png"))
        self.pause_menu_image = pygame.image.load(os.path.join("..", "graphics", "backgrounds", "pause_menu.png"))
        
        # buttons
        self.start_button_img = pygame.image.load(os.path.join("..", "graphics", "buttons",  "start_buton.png"))
        self.quit_button_img = pygame.image.load(os.path.join("..", "graphics", "buttons",  "quit_button.png"))
        self.continue_button_img = pygame.image.load(os.path.join("..", "graphics", "buttons", "continue.png" ))
        self.menu_button_img = pygame.image.load(os.path.join("..", "graphics", "buttons",  "menu_button.png" ))
        self.option_button_img = pygame.image.load(os.path.join("..", "graphics", "buttons",  "options_button_img.png" ))

        # sound on/off icons
        self.sound_on_img = pygame.image.load(os.path.join("..", "graphics", "buttons",  "sound_on.png"))
        self.sound_off_img = pygame.image.load(os.path.join("..", "graphics", "buttons",  "sound_mute.png"))

        # fonts
        self.pixel_font = os.path.join("..", "graphics", "fonts", "PublicPixel.ttf")

    def update_score(self, lines, curr_score, level):
        self.score.lines = lines
        self.score.curr_score = curr_score
        self.score.level = level     

    # generates three random pieces and append them to a list
    def get_next_shape(self):
        next_shape = self.next_pieces.pop(0)
        self.next_pieces.append(random.choice(list(PIECES.keys())))
        return next_shape
    
    def option_menu(self):
        click = False
        self.font = pygame.font.Font(self.pixel_font, 25)
        
        self.text1 = self.font.render("A D, ← → MOVE", True, WHITE)
        self.text_rect1 = self.text1.get_rect(center = (WINDOW_WIDTH/2, 175))

        self.text2 = self.font.render("W, ↑ ROTATE", True, WHITE)
        self.text_rect2 = self.text1.get_rect(center = (WINDOW_WIDTH/2, 225))

        self.text3 = self.font.render("S, ↓ SPEED UP", True, WHITE)
        self.text_rect3 = self.text1.get_rect(center = (WINDOW_WIDTH/2, 275))

        self.text4 = self.font.render("SPACE HARD DROP", True, WHITE)
        self.text_rect4 = self.text1.get_rect(center = (WINDOW_WIDTH/2, 325))

        pygame.display.set_caption("OPTIONS")
        while RUNNING:
            self.display_surface.fill(BG_COLOR)
            self.display_surface.blit(self.game_background_image, (0,0))

            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

            self.display_surface.blit(self.text1, self.text_rect1)
            self.display_surface.blit(self.text2, self.text_rect2)
            self.display_surface.blit(self.text3, self.text_rect3)
            self.display_surface.blit(self.text4, self.text_rect4)
            
            self.back_button = self.menu_button_img.get_rect(center = ((WINDOW_WIDTH)/2, 512.5))

            if self.mute_music == True:
                self.sound_button = self.sound_on_img.get_rect(center = ((WINDOW_WIDTH)/2, 425))
            else:
                self.sound_button = self.sound_off_img.get_rect(center = ((WINDOW_WIDTH)/2, 425))

            if self.option_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True:
                    main.main_menu()
            if self.sound_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True and self.mute_music == False:
                    self.mute_music = True
                    print("music off")
                elif click == True and self.mute_music == True:
                    self.mute_music = False
                    print("music on")

            self.display_surface.blit(self.menu_button_img, self.back_button)
            if self.mute_music == True:
                self.display_surface.blit(self.sound_off_img, self.sound_button)
            else:
                self.display_surface.blit(self.sound_on_img, self.sound_button)

            
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main.main_menu()
                    if event.key == pygame.K_m and self.mute_music == False:
                        self.mute_music = True
                    elif event.key == pygame.K_m and self.mute_music == True:
                        self.mute_music = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()
            self.clock.tick(FPS)


    def main_menu(self):
        click = False
        if not self.mute_music:
            pygame.mixer.music.load(self.main_menu_music)
            pygame.mixer.music.play(-1)
        pygame.display.set_caption("MAIN MENU")
        while RUNNING:
            self.display_surface.fill((BG_COLOR))
            
            self.display_surface.blit(self.background_image, (0,0))
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

            self.start_button = self.start_button_img.get_rect(center = ((WINDOW_WIDTH)/2, 265))
            self.quit_button = self.quit_button_img.get_rect(center = ((WINDOW_WIDTH)/2, 390))
            self.option_button = self.option_button_img.get_rect(center= ((WINDOW_WIDTH)/2, 515))

            if self.start_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True:
                    if not self.mute_music:
                        pygame.mixer.music.load(self.music)
                        pygame.mixer.music.play(-1)
                    main.run()
            if self.quit_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True:
                    pygame.quit()
                    sys.exit()
            if self.option_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True:
                    pygame.mixer.music.stop()
                    main.option_menu()

            self.display_surface.blit(self.start_button_img, self.start_button)
            self.display_surface.blit(self.quit_button_img, self.quit_button)
            self.display_surface.blit(self.option_button_img, self.option_button)
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN: # enter
                        if not self.mute_music:
                            pygame.mixer.music.load(self.music)
                            pygame.mixer.music.play(-1)
                        main.run()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            
            pygame.display.update()
            self.clock.tick(FPS)

    def pause_menu(self):
        click = False
        pygame.mixer.music.pause()
        self.display_surface.fill(BG_COLOR)
        pygame.display.set_caption("PAUSE")

        while RUNNING: 
            self.display_surface.fill(BG_COLOR)
            self.display_surface.blit(self.pause_menu_image, (0,0))
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

            self.continue_button = self.continue_button_img.get_rect(center = ((WINDOW_WIDTH)/2, 265))
            self.main_menu_button = self.menu_button_img.get_rect(center = ((WINDOW_WIDTH)/2, 390))
            self.quit_button = self.quit_button_img.get_rect(center = ((WINDOW_WIDTH)/2, 515))
            
            if self.continue_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True:
                    pygame.mixer.music.unpause()
                    main.run()

            if self.main_menu_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True:
                    self.game.reset_game()
                    
                    main.main_menu()
                    
            if self.quit_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True:
                    
                    pygame.quit()
                    sys.exit()

            self.display_surface.blit(self.continue_button_img, self.continue_button)
            self.display_surface.blit(self.menu_button_img, self.main_menu_button)
            self.display_surface.blit(self.quit_button_img, self.quit_button)
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.unpause()
                        main.run()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()
            self.clock.tick(FPS)
    
    def game_over_menu(self):
        click = False
        if not self.mute_music:
            pygame.mixer.music.load(self.game_over_music)
            pygame.mixer.music.play(-1)
        self.display_surface.fill(BG_COLOR)
        self.show_game_over_menu = True

        self.font = pygame.font.Font(self.pixel_font, 35)
        self.text = self.font.render(f"SCORE:{self.game.final_score}", True, WHITE)
        self.text_rect = self.text.get_rect(center = (WINDOW_WIDTH/2, 185))

        pygame.display.set_caption("GAME OVER")
        while RUNNING:
            
            self.display_surface.blit(self.game_over_image, (0,0))
            self.display_surface.blit(self.text, self.text_rect)
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

            self.main_menu_button = self.menu_button_img.get_rect(center = ((WINDOW_WIDTH)/2, 265))
            self.quit_button = self.quit_button_img.get_rect(center = ((WINDOW_WIDTH)/2, 390))

            if self.main_menu_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True:
                    self.game_over_menu = False
                    main.main_menu()
            if self.quit_button.collidepoint((self.mouse_x, self.mouse_y)):
                if click == True:
                    pygame.quit()
                    sys.exit()
            self.display_surface.blit(self.menu_button_img, self.main_menu_button)
            self.display_surface.blit(self.quit_button_img, self.quit_button)
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN:
                        self.game_over_menu = False
                        main.main_menu()
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            
            pygame.display.update()
            self.clock.tick(FPS)

    def run(self):
        pygame.display.set_caption("TETRIS")
        
        while RUNNING: 
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
