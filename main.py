import sys
import pygame

# Default Setting
COLS, ROWS = 10, 20 # Tetris board size
CELL = 32   # Pixel unit
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL
FPS = 60 # Frames per seconde, how many times the screen updates every second

BG_COLOR = (18, 18, 18) # Red, Green, Blue
GRID_COLOR = (55, 55, 55)

def draw_grid(surface):
    for x in range(COLS + 1):
        px = x * CELL
        pygame.draw.line(surface, GRID_COLOR, (px,0), (px, HEIGHT), 1)

    for y in range(ROWS + 1):
        py = y * CELL
        pygame.draw.line(surface, GRID_COLOR, (0, py),(WIDTH, py), 1)

def excute_game():
    pygame.init()
    pygame.display.set_caption("TETRIS STEP1")
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()

    running = True
    while running:
        '''
        Input
        '''
        # When the user clicks the window's close (X) button,
        # pygame generates a QUIT event and puts it into the event queue.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        '''
        Update
        '''

        '''
        Drawing
        '''
        screen.fill(BG_COLOR)
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

