from setting import *
import random
from timerr import Timer

class Game:
    def __init__(self):

        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING,PADDING))
        self.sprites = pygame.sprite.Group()

        
        self.field_data = [[0 for x in range(COLS)] for y in range(ROWS)]

        # create random starting piece
        self.shape = random.choice(list(PIECES.keys()))
        self.piece = Piece(self.shape, self.sprites, self.spawn_new_piece, self.field_data)
        print(self.shape)

        # timer
        self.timers = {
            "vertical_move": Timer(MOVE_DOWN_SPEED_WAIT, True, self.move_down),
            "horizontal_move": Timer(PLAYER_MOVE_WAIT_TIME),
            "rotate": Timer(ROTATE_WAIT_TIME)
        }

        self.timers["vertical_move"].activate()

    def spawn_new_piece(self):

        self.check_clear_rows()

        self.shape = random.choice(list(PIECES.keys()))
        self.piece = Piece(self.shape, self.sprites, self.spawn_new_piece, self.field_data)
        print(self.shape)


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
    
    def check_clear_rows(self):
        cleared_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                cleared_rows.append(i)
        if cleared_rows:
            for clear_row_index in cleared_rows:
                # delete the block
                for block in self.field_data[clear_row_index]:
                    block.kill()
            # move the blocks down
                for row in self.field_data:
                    for block in row:
                        if block and block.position.y < clear_row_index:
                            block.position.y += 1
        
            self.field_data = [[0 for x in range(COLS)] for y in range(ROWS)]
            for block in self.sprites:
                self.field_data[int(block.position.y)][int(block.position.x)] = block


    def player_input(self):
        keys = pygame.key.get_pressed()

        # move left and right
        if self.timers["horizontal_move"].is_active == False:

            if keys[pygame.K_RIGHT]:
                self.piece.move_horizontaly(1)
                self.timers["horizontal_move"].activate()
                print("--->")

            if keys[pygame.K_LEFT]:
                self.piece.move_horizontaly(-1)
                self.timers["horizontal_move"].activate()
                print("<---")
        
        # rotate
        if self.timers["rotate"].is_active == False:

            if keys[pygame.K_UP]:
                self.piece.rotate()
                self.timers["rotate"].activate()

    def run(self):

        # update the timer
        self.timer_update()

        self.player_input()
        
        self.sprites.update()

        self.surface.fill(BG_COLOR)
        self.sprites.draw(self.surface)

        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))

        self.grid_outline = pygame.draw.rect(self.display_surface, (LINE_COLOR), self.rect, 3, -1)

class Piece:
    def __init__(self, shape, group, spawn_new_piece, field_data):
        self.shape = shape
        self.block_pos = PIECES[shape]["shape"]
        self.block_color = PIECES[shape]["color"]
        self.field_data = field_data
        self.spawn_new_piece = spawn_new_piece
        # create a block for each positon in block pos
        self.blocks = [Block(group, position, self.block_color) for position in self.block_pos]

    # collisions
    def horizontal_collision_on_next_move(self, blocks, amount):
        collision_list = [block.horizontal_collision(int(block.position.x + amount), self.field_data) for block in blocks]
        return any(collision_list)

    def down_collision_on_next_move(self, blocks):
        collision_list = [block.down_collision(int(block.position.y + 1), self.field_data) for block in blocks]
        return any(collision_list)

    def move_down(self):
        for block in self.blocks:
            print(block.position)
        print("********")
        if not self.down_collision_on_next_move(self.blocks):
            for block in self.blocks:
                block.position.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.position.y)][int(block.position.x)] = block
            self.spawn_new_piece()
        
    def move_horizontaly(self, amount):
        if not self.horizontal_collision_on_next_move(self.blocks, amount):
            for block in self.blocks:
                block.position.x += amount
    
    def rotate(self):
        if self.shape != "O":
            # pivot point
            pivot_point = self.blocks[0].position
            
            new_block_pos = [block.rotate(pivot_point) for block in self.blocks]
            
            for pos in new_block_pos:
                if pos.x >= COLS or pos.x < 0 or pos.y > ROWS-1:
                    return
                
                if self.field_data[int(pos.y)][int(pos.x)]:
                    return
                
            for i, block in enumerate(self.blocks):
                block.position = new_block_pos[i]
                
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

    def rotate(self, pivot_point):
        rotate_position = pivot_point + (self.position - pivot_point).rotate(90)
        return rotate_position

    def horizontal_collision(self, x_pos, field_data):
        if not 0 <= x_pos < COLS:
            print("wall collision")
            return True
        
        if field_data[int(self.position.y)][x_pos]:
            print("block collision 1")
            return True

    def down_collision(self, y_pos, field_data):
        if y_pos >= ROWS:
            print("down collision")
            return True
        
        if y_pos >= 0 and field_data[y_pos][int(self.position.x)]:
            print("block collision 2")
            return True

    def update(self):
        # print(self.position)
        self.rect.topleft = self.position * CELL_SIZE
