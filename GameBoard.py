from typing import List, Optional, Tuple
from Settings import COLS, ROWS

Color = Tuple[int, int, int]
Board = List[List[Optional[Color]]]

def new_board() -> Board:
    return [[None for _ in range(COLS)] for _ in range(ROWS)]

def inside(x: int, y: int) -> bool:
    return 0 <= x < COLS and 0 <= y < ROWS

def can_place(board: Board, piece, rot=None, x=None, y=None) -> bool:
    for (cx, cy) in piece.cells(rot, x, y):
        if not inside(cx, cy):
            return False
        if cy >= 0 and board[cy][cx] is not None:
            return False
    return True

def lock_piece(board: Board, piece) -> None:
    for (x, y) in piece.cells():
        if 0 <= y < ROWS and 0 <= x < COLS:
            board[y][x] = piece.color

def clear_lines(board: Board) -> int:
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