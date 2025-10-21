import random
import pygame
from Settings import WIDTH, HEIGHT, FPS, BG_COLOR, GRID_COLOR, FONT_WHITE
from Settings import COLS, ROWS, CELL
from Settings import FALL_DELAY
from BlockPiece import Piece
from GameBoard import new_board, can_place, lock_piece, clear_lines

def draw_grid(surface):
    for x in range(COLS + 1):
        px = x * CELL
        pygame.draw.line(surface, GRID_COLOR, (px,0), (px, HEIGHT), 1)

    for y in range(ROWS + 1):
        py = y * CELL
        pygame.draw.line(surface, GRID_COLOR, (0,py), (WIDTH, py), 1)


def draw_board(surface, board):
    for y in range(ROWS):
        for x in range(COLS):
            color = board[y][x]
            if color is not None:
                pygame.draw.rect(
                    surface,
                    color,
                    pygame.Rect(x * CELL +1, y * CELL +1, CELL -2, CELL -2)
                )

def draw_piece(surface, piece):
    for (x,y) in piece.cells():
        if y >= 0:
            pygame.draw.rect(
                surface,
                piece.color,
                pygame.Rect(x * CELL +1, y * CELL +1, CELL -2, CELL -2)
            )

def draw_hud(surface, score, font):
    text = font.render(f"SCORE: {score}", True, FONT_WHITE)
    surface.blit(text, (8,6))


def spawn_new_piece()->Piece:
    from BlockShape import BLOCKS_SHAPES
    kind = random.choice(list(BLOCKS_SHAPES.keys()))
    return Piece(kind)

def try_move(board, piece, dx=0, dy=0):
    nx = piece.x + dx
    ny = piece.y + dy

    if can_place(board, piece, piece.rot, nx, ny):
        piece.x = nx
        piece.y = ny
        return True
    return False

def try_rotate(board, piece, dr=1):
    from BlockShape import BLOCKS_SHAPES
    new_rot = (piece.rot + dr) % len(BLOCKS_SHAPES[piece.kind])
    for ox in (0, -1, 1, -2, 2):
        if can_place(board, piece, new_rot, piece.x+ox, piece.y):
            piece.rot = new_rot
            piece.x += ox
            return True
    return False

def gravity_step(board, piece):
    if try_move(board, piece, dy=1):
        return False
    lock_piece(board, piece)
    return True

def excute_game():
    pygame.init()
    pygame.display.set_caption("TETRIS GAME")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font =  pygame.font.Font(None, 24)

    board = new_board()
    current = spawn_new_piece()
    fall_delay = FALL_DELAY
    last_fall = pygame.time.get_ticks()
    score = 0

    running = True
    while running:
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
                elif event.key == pygame.K_SPACE:
                    while try_move(board, current, dy=1):
                        pass
                    lock_piece(board, current)
                    cleared = clear_lines(board)
                    if cleared:
                        score += cleared * 100
                    current = spawn_new_piece()

        now = pygame.time.get_ticks()
        if now - last_fall >= fall_delay:
            last_fall = now
            if gravity_step(board, current):
                cleared = clear_lines(board)
                if cleared:
                    score += cleared * 100
                current = spawn_new_piece()

        screen.fill(BG_COLOR)
        draw_board(screen, board)
        draw_piece(screen, current)
        draw_grid(screen)
        draw_hud(screen, score, font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()