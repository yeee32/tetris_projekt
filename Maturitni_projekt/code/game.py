from setting import *
import random
from timerr import Timer
import os

class Game:
    def __init__(self, get_next_shape, update_score, game_over_check):
        pygame.mixer.init()
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING,PADDING))
        self.sprites = pygame.sprite.Group()
        self.game_over_check = game_over_check

        self.drop_speed_multiplier = 1
        self.drop_speed = 1

        # sound effects
        self.clear_row_sound = pygame.mixer.Sound(os.path.join("..", "sfx","clear_row_sound.wav"))
        self.game_over_sound = pygame.mixer.Sound(os.path.join("..", "sfx","game_over_sound.wav"))

        # funcs
        self.get_next_shape = get_next_shape
        self.update_score = update_score
        self.field_data = [[0 for x in range(COLS)] for y in range(ROWS)]
        # create random starting piece
        self.shape = random.choice(list(PIECES.keys()))
        self.piece = Piece(self.shape, self.sprites, self.spawn_new_piece, self.field_data)

        # timer
        self.timers = {
            "vertical_move": Timer(MOVE_DOWN_SPEED_WAIT, True, self.move_down),
            "horizontal_move": Timer(PLAYER_MOVE_WAIT_TIME),
            "rotate": Timer(ROTATE_WAIT_TIME),
        }

        self.timers["vertical_move"].activate()

        # preview info
        self.curr_level = 1
        self.curr_score = 0
        self.curr_lines_cleared = 0 

    # function that calculates the score based on the amount of lines cleared
    def update_preview(self,  lines_cleared):
        self.curr_lines_cleared += lines_cleared # number of lines cleared 
        self.curr_score += SCORE_DATA[lines_cleared] * self.curr_level # checks how much should the score change

        # for every 10 lines cleared the level will increase by 1 and drop speed by 0.25
        if self.curr_lines_cleared / 10 > self.curr_level :
            self.curr_level += 1
            self.drop_speed += 0.25
        self.update_score(self.curr_lines_cleared, self.curr_score, self.curr_level) # puts on display

    # function that creates the piece and puts it in the game window
    def spawn_new_piece(self):
        
        self.game_over() # checks if the game has ended, if not, spawns another piece
        self.check_clear_rows()

        self.shape = self.get_next_shape()
            
        self.piece = Piece(self.shape, self.sprites, self.spawn_new_piece, self.field_data)
        
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
            self.update_preview(len(cleared_rows))
        
    def player_input(self):
        keys = pygame.key.get_pressed()

        # move 
        if self.timers["horizontal_move"].is_active == False:

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.piece.move_horizontaly(1)
                self.timers["horizontal_move"].activate()

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.piece.move_horizontaly(-1)
                self.timers["horizontal_move"].activate()

            if keys[pygame.K_SPACE] and not self.spacebar_pressed: # funguje ??
                self.piece.drop()
                self.spacebar_pressed = True
            elif not keys[pygame.K_SPACE]:
                self.spacebar_pressed = False
        # rotate
        if self.timers["rotate"].is_active == False:

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.piece.rotate_piece()
                
                self.timers["rotate"].activate()

        if keys[pygame.K_DOWN] or keys[pygame.K_s] and not keys[pygame.K_SPACE]:
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

    def reset_game(self):
        # reset field data
        self.field_data = [[0 for x in range(COLS)] for y in range(ROWS)]
        
        # clear all blocks
        self.sprites.empty()

        # reset the score values
        self.curr_level = 1
        self.curr_score = 0
        self.curr_lines_cleared = 0 
        
        # reset drop speed
        self.drop_speed_multiplier = 1
        self.drop_speed = 1
        
        # reset next shape
        self.shape = random.choice(list(PIECES.keys()))
        self.piece = Piece(self.shape, self.sprites, self.spawn_new_piece, self.field_data)
        

        # generate new random shapes for next pieces preview
        self.next_pieces = [random.choice(list(PIECES.keys())) for shape in range(3)]
        self.get_next_shape()

        self.update_score(0, 0, 1)

    def game_over(self):
        self.final_score = 0
        for block in self.piece.blocks:
            if block.position.y <= -1:
                self.game_over_sound.play()
                self.final_score = self.curr_score
                self.reset_game()
                pygame.time.wait(250)
                
                self.game_over_check()
                return self.final_score

class Piece:
    def __init__(self, shape, group, spawn_new_piece, field_data):
        self.shape = shape
        self.block_pos = PIECES[shape]["shape"]
        self.block_color = PIECES[shape]["color"]
        self.field_data = field_data
        self.spawn_new_piece = spawn_new_piece
        # create a block for each positon in block pos
        self.blocks = [Block(group, position, self.block_color, BLOCK_OFFSET) for position in self.block_pos]
    
        # sound effects
        self.block_place_sound = pygame.mixer.Sound(os.path.join("..", "sfx","block_place_sound.wav"))    
        self.rotate_sound = pygame.mixer.Sound(os.path.join("..", "sfx","rotate_sound.wav"))
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

        self.spawn_new_piece()
        self.block_place_sound.play()
    def move_down(self):
        if not self.down_collision_on_next_move(self.blocks, 1):
            for block in self.blocks:
                block.position.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.position.y)][int(block.position.x)] = block
            self.spawn_new_piece()
            self.block_place_sound.play()

    def move_horizontaly(self, amount):
        if not self.horizontal_collision_on_next_move(self.blocks, amount):
            for block in self.blocks:
                block.position.x += amount
    
    def rotate_piece(self):
        if self.shape not in ["O", "DOT", "PLUS"]:
            pivot_point = self.blocks[0].position
            
            new_block_pos = [pivot_point + (block.position - pivot_point).rotate(90) for block in self.blocks]

            for position in new_block_pos:
                    # horizontal collision check
                if position.x >= COLS:
                    return

                elif position.x < 0:
                    return
                
                elif position.y > ROWS:
                    return

                    # vertical collision check
                if self.field_data[int(position.y)][int(position.x)]:
                    return
                
            for i, block in enumerate(self.blocks):
                    block.position = new_block_pos[i]
            
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
            return True
        
        if field_data[int(self.position.y)][x_pos]:
            return True

    def down_collision(self, y_pos, field_data):
        if y_pos >= ROWS:
            return True
        
        if y_pos >= 0 and field_data[y_pos][int(self.position.x)]:
            return True

    def update(self):
        self.rect.topleft = self.position * CELL_SIZE
