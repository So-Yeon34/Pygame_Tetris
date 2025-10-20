import sys
import random
import pygame

# Default Setting
COLS, ROWS = 10, 20 # Tetris board size
CELL = 32   # Pixel unit
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL
FPS = 60 # Frames per seconde, how many times the screen updates every second

# Back ground Setting
BG_COLOR = (18, 18, 18) # Red, Green, Blue
GRID_COLOR = (55, 55, 55)

# Block Setting
BLOCKS_COLOR = {
    'I': (0, 186, 255),
    'O': (255, 214, 0),
    'T': (163, 73, 164),
    'S': (0, 200, 70),
    'Z': (230, 0, 38),
    'J': (0, 90, 200),
    'L': (255, 140, 0),
}

BLOCKS_SHAPES = {
    # It should be considered how look like in the case of ratating
    'I': [
        [(0,0), (1,0), (2,0), (3,0)],
        [(2,-1), (2,0), (2,1), (2,2)],
    ],

    'O': [
        [(0,0), (1,0), (0,1), (1,1)],
    ],

    'T': [
        [(1,0), (0,1), (1,1), (2,1)],
        [(1,0), (1,1), (2,1), (1,2)],
        [(0,1), (1,1), (2,1), (1,2)],
        [(1,0), (0,1), (1,1), (1,2)],
    ],

    'S': [
        [(1,0), (2,0), (0,1), (1,1)],
        [(1,0), (1,1), (2,1), (2,2)],
    ],

    'Z': [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
    ],

    'J': [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],

    'L': [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
}

class Piece:
    def __init__(self, kind: str):
        self.kind = kind
        self.rot = 0
        self.x = 3
        self.y = 0
        self.color = BLOCKS_COLOR[kind]

    def cells(self, rot=None, x=None, y=None):
        if rot is None:
            rot = self.rot
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        shape = BLOCKS_SHAPES[self.kind][rot % len(BLOCKS_SHAPES[self.kind])]
        return [(x + cx, y + cy) for (cx, cy) in shape]

def draw_grid(surface):
    for x in range(COLS + 1):
        px = x * CELL
        pygame.draw.line(surface, GRID_COLOR, (px,0), (px, HEIGHT), 1)

    for y in range(ROWS + 1):
        py = y * CELL
        pygame.draw.line(surface, GRID_COLOR, (0, py),(WIDTH, py), 1)

def draw_board(surface, board):
    for y in range(ROWS):
        for x in range(COLS):
            color = board[y][x]
            if color is not None:
                pygame.draw.rect(
                    surface,
                    color,
                    pygame.Rect(x * CELL + 1, y * CELL + 1, CELL -2, CELL -2),
                )

def draw_piece(surface, piece):
    for (x,y) in piece.cells():
        if y>=0:
            pygame.draw.rect(
                surface,
                piece.color,
                pygame.Rect(x * CELL + 1, y * CELL + 1, CELL -2, CELL - 2),
            )

def inside(x, y):
    return 0 <= x < COLS and 0 <= y < ROWS

def put_place(board, piece, rot=None, x=None, y=None):
    for (cx, cy) in piece.cells(rot, x, y):
        if not inside(cx, cy):
            return False

        if cy >= 0 and board[cy][cx] is not None:
            return False
    return True

def lock_piece(board, piece):
    for (x, y) in piece.cells():
        if 0 <= y < ROWS:
            board[y][x] = piece.color

def spawn_new_piece():
    kind = random.choice(list(BLOCKS_SHAPES.keys()))
    return Piece(kind)

def excute_game():
    pygame.init()
    pygame.display.set_caption("TETRIS STEP1")
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()

    board = [[None for _ in range(COLS)] for _ in range(ROWS)]

    current = spawn_new_piece()
    fall_delay = 500  # milliseconds between automatic drops
    last_fall = pygame.time.get_ticks()

    running = True
    while running:
        '''
        Init
        '''
        # When the user clicks the window's close (X) button,
        # pygame generates a QUIT event and puts it into the event queue.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        '''
        Update
        '''
        now = pygame.time.get_ticks()
        if now - last_fall >= fall_delay:
            last_fall = now

        if put_place(board, current, current.rot, current.x, current.y + 1):
            current.y += 1
        else:
            lock_piece(board, current)
            current = spawn_new_piece()
            if not put_place(board, current, current.rot, current.x, current.y):
                board = [[None for _ in range(COLS)] for _ in range(ROWS)]
                current = spawn_new_piece()
        '''
        Drawing
        '''
        screen.fill(BG_COLOR)
        draw_board(screen, board)
        draw_piece(screen, current)
        draw_grid(screen)

        pygame.display.flip() # Screen Update

        '''
        Limit the game loop to run at most 'FPS' times per second 
        Prevents the game from running too fast
        '''
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__=="__main__":
    excute_game()

