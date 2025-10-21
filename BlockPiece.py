from BlockShape import BLOCKS_SHAPES, BLOCKS_COLOR

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