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
FONT_WHITE = (230, 230, 230)

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

# Timing Parameter
FALL_DELAY = 10000 # milliseconds between automatic drops

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

def draw_hud(surface, score, font):
    text = font.render(f"SCORE: {score}", True, FONT_WHITE)
    surface.blit(text, (8,6))

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

def clear_lines(board):
    cleared = 0
    y = ROWS - 1
    while y >= 0:
        if all(board[y][x] is not None for x in range(COLS)):
            del board[y]
            board.insert(0, [None for _ in range(COLS)])
            cleared += 1
        else:
            y -= 1
    return cleared

def spawn_new_piece():
    kind = random.choice(list(BLOCKS_SHAPES.keys()))
    return Piece(kind)

def try_move(board, piece, dx=0, dy=0):
    nx, ny = piece.x + dx, piece.y + dy
    if put_place(board, piece, piece.rot, nx, ny):
        piece.x, piece.y = nx, ny
        return True
    return False

def try_rotate(board, piece, dr = 1):
    new_rot = (piece.rot + dr) % len(BLOCKS_SHAPES[piece.kind])
    for ox in (0, -1, 1, -2, 2):
        if put_place(board, piece, new_rot, piece.x + ox, piece.y):
            piece.rot = new_rot
            piece.x += ox
            return True
    return False

def excute_game():
    pygame.init()
    pygame.display.set_caption("TETRIS")
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    board = [[None for _ in range(COLS)] for _ in range(ROWS)]

    current = spawn_new_piece()
    fall_delay = FALL_DELAY
    last_fall = pygame.time.get_ticks()
    score = 0

    running = True
    while running:
    # --- Input ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    try_move(board, current, dx=-1)
                elif event.key == pygame.K_RIGHT:
                    try_move(board, current, dx=1)
                elif event.key == pygame.K_DOWN:
                    if try_move(board, current, dy=1):
                        last_fall = pygame.time.get_ticks()
                elif event.key == pygame.K_UP:
                    try_rotate(board, current, dr=1)
                elif event.key == pygame.K_SPACE:  # hard drop
                    while try_move(board, current, dy=1):
                        pass
                    lock_piece(board, current)
                    cleared = clear_lines(board)
                    if cleared:
                        score += cleared * 100
                    current = spawn_new_piece()
                    # 스폰 불가면 리셋 (간단한 게임오버 처리)
                    if not put_place(board, current, current.rot, current.x, current.y):
                        board = [[None for _ in range(COLS)] for _ in range(ROWS)]
                        score = 0
                        current = spawn_new_piece()

            # --- Gravity ---
            now = pygame.time.get_ticks()
            if now - last_fall >= fall_delay:
                last_fall = now
                locked = gravity_step(board, current)
                if locked:
                    cleared = clear_lines(board)
                    if cleared:
                        score += cleared * 100
                    current = spawn_new_piece()
                    if not put_place(board, current, current.rot, current.x, current.y):
                        board = [[None for _ in range(COLS)] for _ in range(ROWS)]
                        score = 0
                        current = spawn_new_piece()
        '''
        Update
        '''
        now = pygame.time.get_ticks()
        if now - last_fall >= fall_delay:
            last_fall = now
            if not try_move(board, current, dy=1):
                lock_piece(board, current)
                cleared = clear_lines(board)
                if cleared > 0:
                    score += cleared * 100
                current = spawn_new_piece()
                if not put_place(board, current, current.rot, current.x, current.y +1):
                    board = [[None for _ in rage(COLS)] for _ in range(ROWS)]
                    score = 0
                    current = spawn_new_piece()

        '''
        Drawing
        '''
        screen.fill(BG_COLOR)
        draw_board(screen, board)
        draw_piece(screen, current)
        draw_grid(screen)
        draw_hud(screen, score, font)

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

