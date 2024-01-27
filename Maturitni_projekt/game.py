from setting import *
import random
from timerr import Timer

class Game:
    def __init__(self):

        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING,PADDING))
        self.sprites = pygame.sprite.Group()

        
        # create individual pieces
        self.shape = random.choice(list(PIECES.keys()))
        self.piece = Piece(self.shape, self.sprites)
        print(self.shape)
        
        
        # timer
        self.timers = {
            "vertical_move": Timer(UPDATE_START_SPEED, True, self.move_down),
            "horizontal_move": Timer(MOVE_WAIT_TIME)
        }

        self.timers["vertical_move"].activate()

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        self.piece.move_down()
    
    def draw_grid(self):
        for col in range(1, COLS):
            x = col * CELL_SIZE
            y = GAME_HEIGHT
            pygame.draw.line(self.surface, LINE_COLOR, (x, 0), (x, y), 1)

        for row in range(1, ROWS):
            x = GAME_WIDTH
            y = row * CELL_SIZE
            pygame.draw.line(self.surface, LINE_COLOR, (0, y), (x, y), 1)
    
    def player_input(self):
        keys = pygame.key.get_pressed()

        if self.timers["horizontal_move"].is_active == False:

            if keys[pygame.K_RIGHT]:
                self.piece.move_horizontaly("right")
                self.timers["horizontal_move"].activate()
                print("--->")

            if keys[pygame.K_LEFT]:
                self.piece.move_horizontaly("left")
                self.timers["horizontal_move"].activate()
                print("<---")
            
    def run(self):

        # update the timer
        self.timer_update()

        self.player_input()
        
        self.sprites.update()

        self.surface.fill(BG_COLOR)
        self.sprites.draw(self.surface)

        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))
        pygame.draw.rect(self.display_surface, (LINE_COLOR), self.rect, 3, -1)

class Piece:
    def __init__(self, shape, group):
        self.block_pos = PIECES[shape]["shape"]
        self.block_color = PIECES[shape]["color"]

        # create a block for each positon in block pos
        self.blocks = [Block(group, position, self.block_color) for position in self.block_pos]

    def move_down(self):
        for block in self.blocks:
            block.position.y += 1
    
    def move_horizontaly(self, side):
        for block in self.blocks:
            if side == "right":
                block.position.x += 1
            if side == "left":
                block.position.x -= 1

class Block(pygame.sprite.Sprite):
    def __init__(self, groups, position, color):
        super().__init__(groups)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        # position
        self.position = pygame.Vector2(position) + BLOCK_OFFSET
        x = self.position.x * CELL_SIZE 
        y = self.position.y * CELL_SIZE 
        self.rect = self.image.get_rect(topleft = (x, y))
    
    def update(self):
        # print(self.position)
        self.rect.topleft = self.position * CELL_SIZE
