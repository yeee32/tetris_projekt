import pygame 

# Game size 
COLS = 10
ROWS = 20
CELL_SIZE = 35
GAME_WIDTH = COLS * CELL_SIZE # 350
GAME_HEIGHT =  ROWS * CELL_SIZE # 700

FPS = 120

RUNNING = True

# buttons
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 75

# side bar size 
SIDEBAR_WIDTH = 200 
PREVIEW_HEIGHT = 0.7
SCORE_HEIGHT = 1 - PREVIEW_HEIGHT

# window
PADDING = 20
WINDOW_WIDTH = (GAME_WIDTH + SIDEBAR_WIDTH + PADDING * 3) # 610
WINDOW_HEIGHT = GAME_HEIGHT + PADDING * 2  # 740

# game behaviour 
MOVE_DOWN_SPEED_WAIT = 500
PLAYER_MOVE_WAIT_TIME = 100
ROTATE_WAIT_TIME = 225
BLOCK_OFFSET = pygame.Vector2(COLS // 2, -1)

PREVIEW_BLOCK_OFFSET = pygame.Vector2(COLS * 1.5, 30)

# Colors 
WHITE = (255, 255, 255)

# pieces colors
YELLOW = (241, 230, 13)
RED = (229, 27, 32)
BLUE = (14, 113, 237)
LIGHT_GREEN = (12, 237, 119)
PURPLE = (113, 27, 117)
CYAN = (12, 228, 232)
ORANGE = (232, 120, 14)
BROWN = (237, 171, 17)
GREEN = (21, 230, 28)
DARK_GREEN = (9, 107, 28)
DARK_RED = (153, 14, 32)
PINK = (247, 30, 222)

LINE_COLOR = (20, 20,50)
BG_COLOR = (0,0,0)

# shapes
PIECES = {
	"T": {"shape": [(0,0), (-1,0), (1,0), (0,-1)], "color": RED},
	"O": {"shape": [(0,0), (0,-1), (1,0), (1,-1)], "color": CYAN},
	"J": {"shape": [(0,0), (0,-1), (0,1), (-1,1)], "color": GREEN},
	"L": {"shape": [(0,0), (0,-1), (0,1), (1,1)], "color": PINK},
	"I": {"shape": [(0,0), (0,-1), (0,1), (0,2)], "color": YELLOW},
	"S": {"shape": [(0,0), (-1,0), (0,-1), (1,-1)], "color": BLUE},
	"Z": {"shape": [(0,0), (1,0), (0,-1), (-1,-1)], "color": PURPLE},
    "C": {"shape": [(0,0), (-1,0), (-1,-1), (1,0), (1,-1)], "color": LIGHT_GREEN},
    "q": {"shape": [(0,0), (-1,0), (1,0), (0,-1),(1,-1)], "color": DARK_RED},
    "P": {"shape": [(0,0), (-1,0), (1,0), (0,-1),(-1,-1)], "color": ORANGE},
    "DOT": {"shape": [(0,0)], "color": DARK_GREEN},
    "PLUS": {"shape": [(0,0), (-1,0), (1,0), (0,1), (0,-1)], "color": BROWN}
}

SCORE_DATA = {1: 40, 2: 100, 3: 300, 4: 1200}