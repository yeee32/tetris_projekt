from setting import *
import random
from timerr import Timer
import sys
import os


class Game:
    def __init__(self, get_next_shape, update_score):

        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING,PADDING))
        self.sprites = pygame.sprite.Group()

        self.drop_speed_multiplier = 1
        self.drop_speed = 1

        # sound effects
        self.clear_row_sound = pygame.mixer.Sound(os.path.join("Maturitni_projekt", "sfx","clear_row_sound.wav"))
        self.block_place_sound = pygame.mixer.Sound(os.path.join("Maturitni_projekt", "sfx","block_place_sound.wav"))
        
        self.get_next_shape = get_next_shape
        self.update_score = update_score

        self.field_data = [[0 for x in range(COLS)] for y in range(ROWS)]
        # create random starting piece
        self.shape = random.choice(list(PIECES.keys()))
        self.piece = Piece(self.shape, self.sprites, self.spawn_new_piece, self.field_data)
        print(self.shape)

        # timer
        self.timers = {
            "vertical_move": Timer(MOVE_DOWN_SPEED_WAIT, True, self.move_down),
            "horizontal_move": Timer(PLAYER_MOVE_WAIT_TIME),
            "rotate": Timer(ROTATE_WAIT_TIME),
        }

        self.timers["vertical_move"].activate()

        self.curr_level = 1
        self.curr_score = 0
        self.curr_lines_cleared = 0 

    def score_calc(self,  lines_cleared):
        self.curr_lines_cleared += lines_cleared
        self.curr_score += SCORE_DATA[lines_cleared] * self.curr_level

        # for every 10 lines cleared the level will increase by 1
        if self.curr_lines_cleared / 10 > self.curr_level :
            self.curr_level += 1
            self.drop_speed += 0.5
        self.update_score(self.curr_lines_cleared, self.curr_score, self.curr_level)

    def spawn_new_piece(self):
        
        self.block_place_sound.play()
        self.game_over() # game over check... is kinda broken           
        self.check_clear_rows()

        self.shape = self.get_next_shape()
        
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

            self.clear_row_sound.play()
        # update score
            self.score_calc(len(cleared_rows))
        
    def player_input(self):
        keys = pygame.key.get_pressed()

        # move 
        if self.timers["horizontal_move"].is_active == False:

            if keys[pygame.K_RIGHT]:
                self.piece.move_horizontaly(1)
                self.timers["horizontal_move"].activate()
                # print("--->")

            elif keys[pygame.K_LEFT]:
                self.piece.move_horizontaly(-1)
                self.timers["horizontal_move"].activate()
                # print("<---")

            elif keys[pygame.K_SPACE]: # funguje ??
                self.piece.drop()
                self.timers["horizontal_move"].activate()
                self.timers["rotate"].activate()
                    
        # rotate
        if self.timers["rotate"].is_active == False:

            if keys[pygame.K_UP]:
                self.piece.rotate()
                
                self.timers["rotate"].activate()

        if keys[pygame.K_DOWN] and not keys[pygame.K_SPACE]:
            self.drop_speed_multiplier = 7 * self.drop_speed # increase the drop speed when down arrow is pressed
        else:
            self.drop_speed_multiplier = self.drop_speed # reset to normal drop speed

    def run(self):

        # update the timer
        self.timers["vertical_move"].duration = MOVE_DOWN_SPEED_WAIT // self.drop_speed_multiplier
        self.timer_update()

        self.player_input()
        
        self.sprites.update()

        self.surface.fill(BG_COLOR)
        self.sprites.draw(self.surface)

        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))

        self.grid_outline = pygame.draw.rect(self.display_surface, (LINE_COLOR), self.rect, 3, -1)

    def game_over(self):
        for block in self.piece.blocks:
            if block.position.y < 0:
                print("GAME OVER")
                pygame.time.wait(500)
                return True
                # pygame.quit
                # sys.exit()

        return False
class Piece:
    def __init__(self, shape, group, spawn_new_piece, field_data, current = True):
        self.shape = shape
        self.block_pos = PIECES[shape]["shape"]
        self.block_color = PIECES[shape]["color"]
        self.field_data = field_data
        self.spawn_new_piece = spawn_new_piece
        # create a block for each positon in block pos
        self.blocks = [Block(group, position, self.block_color, BLOCK_OFFSET) for position in self.block_pos]
    
        self.rotate_sound = pygame.mixer.Sound(os.path.join("Maturitni_projekt", "sfx","rotate_sound.wav"))
        self.rotate_sound.set_volume(0.25)

    # collisions
    def horizontal_collision_on_next_move(self, blocks, amount):
        collision_list = [block.horizontal_collision(int(block.position.x + amount), self.field_data) for block in blocks]
        return any(collision_list)

    def down_collision_on_next_move(self, blocks, amount):
        collision_list = [block.down_collision(int(block.position.y + amount), self.field_data) for block in blocks]
        return any(collision_list)

    def drop(self):
        distance_to_bottom = 0
        # counts until it hits sth
        while not self.down_collision_on_next_move(self.blocks, distance_to_bottom + 1):
            distance_to_bottom += 1

        # move the piece to its final position at the bottom
        for block in self.blocks:
            block.position.y += distance_to_bottom

        # place the piece on the field
        for block in self.blocks:
            self.field_data[int(block.position.y)][int(block.position.x)] = block

    def move_down(self):
        if not self.down_collision_on_next_move(self.blocks, 1):
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
        if self.shape not in ["O", "DOT", "PLUS"]:
            self.num = 1
            if self.shape == "I":
                self.num = 2
            print(self.num)
            pivot_point = self.blocks[0].position

            new_block_pos = [pivot_point + (block.position - pivot_point).rotate(90) for block in self.blocks]

            for position in new_block_pos:

                if position.y >= ROWS:
                    return
                
            for i, block in enumerate(self.blocks):
                block.position = new_block_pos[i]

            for position in new_block_pos:
                    # horizontal collision check
                if position.x >= COLS and not self.horizontal_collision_on_next_move(self.blocks, -self.num):
                    if self.shape != "I":
                        self.move_horizontaly(-1)
                    else:
                        self.move_horizontaly(-2)
                    return
                
                elif position.x < 0 and not self.horizontal_collision_on_next_move(self.blocks, self.num):
                    if self.shape != "I":
                        self.move_horizontaly(1)
                    else:
                        self.move_horizontaly(2)
                    return
  
                if self.field_data[int(position.y)][int(position.x)] and not self.horizontal_collision_on_next_move(self.blocks, 1):
                    if position.x >= COLS // 2:
                        if self.shape != "I":
                            self.move_horizontaly(-1)
                        else:
                            self.move_horizontaly(-2)
                        # return
                    else:
                        if self.shape != "I":
                            self.move_horizontaly(1)
                        else:
                            self.move_horizontaly(2)
                    return
            
                
            
            
            self.rotate_sound.play()
                
class Block(pygame.sprite.Sprite):
    def __init__(self, groups, position, color, block_offset):
        super().__init__(groups)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        # position
        self.position = pygame.Vector2(position) + block_offset
        x = self.position.x * CELL_SIZE 
        y = self.position.y * CELL_SIZE 
        self.rect = self.image.get_rect(topleft = (x, y))

    def horizontal_collision(self, x_pos, field_data):
        if not 0 <= x_pos < COLS:
            # print("wall collision")
            return True
        
        if field_data[int(self.position.y)][x_pos]:
            # print("block collision 1")
            return True

    def down_collision(self, y_pos, field_data):
        if y_pos >= ROWS:
            # print("down collision")
            return True
        
        if y_pos >= 0 and field_data[y_pos][int(self.position.x)]:
            # print("block collision 2")
            return True

    def update(self):
        # print(self.position)
        self.rect.topleft = self.position * CELL_SIZE
