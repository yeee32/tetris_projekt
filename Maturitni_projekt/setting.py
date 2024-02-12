import pygame 

RUNNING = True

# Game size 
COLS = 10
ROWS = 20
CELL_SIZE = 35
GAME_WIDTH = COLS * CELL_SIZE
GAME_HEIGHT =  ROWS * CELL_SIZE

# side bar size 
SIDEBAR_WIDTH = 200
PREVIEW_HEIGHT = 0.7
SCORE_HEIGHT = 1 - PREVIEW_HEIGHT

# window
PADDING = 20
WINDOW_WIDTH = (GAME_WIDTH + SIDEBAR_WIDTH + PADDING * 3)
WINDOW_HEIGHT = GAME_HEIGHT + PADDING * 2

# game behaviour 
MOVE_DOWN_SPEED_WAIT = 500
PLAYER_MOVE_WAIT_TIME = 100
ROTATE_WAIT_TIME = 200
BLOCK_OFFSET = pygame.Vector2(COLS // 2, -1)

# Colors 
YELLOW = "#f1e60d"
RED = "#e51b20"
BLUE = "#0D78FF"
GREEN = "#0DFF80"
PURPLE = "#7b217f"
CYAN = "#0CA7E8"
ORANGE = "#f07e13"
GRAY = "#1C1C1C"
LIGHT_GREEN = "#0CE8B3"
LINE_COLOR = (20, 20,50)
BG_COLOR = (0,0,0)

# shapes
PIECES = {
	"T": {"shape": [(0,0), (-1,0), (1,0), (0,-1)], "color": PURPLE},
	"O": {"shape": [(0,0), (0,-1), (1,0), (1,-1)], "color": YELLOW},
	"J": {"shape": [(0,0), (0,-1), (0,1), (-1,1)], "color": BLUE},
	"L": {"shape": [(0,0), (0,-1), (0,1), (1,1)], "color": ORANGE},
	"I": {"shape": [(0,0), (0,-1), (0,1), (0,2)], "color": CYAN},
	"S": {"shape": [(0,0), (-1,0), (0,-1), (1,-1)], "color": GREEN},
	"Z": {"shape": [(0,0), (1,0), (0,-1), (-1,-1)], "color": RED},
    "C": {"shape": [(0,0), (-1,0), (-1,-1), (1,0), (1,-1)], "color": LIGHT_GREEN}
}

SCORE_DATA = {1: 40, 2: 100, 3: 300, 4: 1200}
