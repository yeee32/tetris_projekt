from setting import *
import sys
import random  
import os

# components
from game import Game
from score import Score
from preview import Preview

class Main():
    def __init__(self):

        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("TETRIS GAME")
        
        # next shapes in preview tab
        self.next_shapes = [random.choice(list(PIECES.keys())) for shape in range(3)]
        print(self.next_shapes)

        # buttons imgs
        self.start_button_img = pygame.image.load(os.path.join("Maturitni_projekt","graphics" ,"start_button_img.png")).convert_alpha

        # components 
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()
        
        # music
        self.music = pygame.mixer.music.load(os.path.join("Maturitni_projekt", "sfx", "shitty_music.wav"))
        

    def update_score(self, lines, curr_score, level):
        self.score.lines = lines
        self.score.curr_score = curr_score
        self.score.level = level     

    # generates three random pieces and append them to a list
    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(random.choice(list(PIECES.keys())))
        return next_shape
    
    def main_menu(self):
        while RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        main.run()
            self.display_surface.fill(BLUE)
            pygame.display.update()
            self.clock.tick()

    def game_over_menu(self):
        print("Game over menu")
        while RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print("main menu") 
                        main.run() 
                         
            self.display_surface.fill(RED)
            pygame.display.update()
            self.clock.tick()

    def run(self):
        pygame.mixer.music.play(-1)
        while RUNNING: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.display_surface.fill(GRAY)
        
            # components
            self.game.run()
            self.score.run() 
            self.preview.run(self.next_shapes)
            
             
            pygame.display.update()

            self.clock.tick()         

   

if __name__ == "__main__":
    main = Main()  
    main.main_menu()
