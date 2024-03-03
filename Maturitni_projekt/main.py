from setting import *
import sys
import random  

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
        # components 
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()
    
    def update_score(self, lines, curr_score, level):
        self.score.lines = lines
        self.score.curr_score = curr_score
        self.score.level = level     

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(random.choice(list(PIECES.keys())))
        return next_shape
    
    def run(self):
        while RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_surface.fill(GRAY)

            # components
            self.game.run()
            self.score.run()
            self.preview.run()

            pygame.display.update()

            self.clock.tick()

if __name__ == "__main__":
    main = Main()
    main.run()
