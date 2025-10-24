from GameProcess import excute_game
import sys
import os

def resource_path(relative_path: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, relative_path)


if __name__=="__main__":
    excute_game()

