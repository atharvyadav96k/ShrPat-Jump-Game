from objects import Rectangle
from gameobjects import Ground, Boxes
from .map import map as levelMap

TILE_SIZE = 50


def getLevelSize():
    rows = len(levelMap)
    cols = len(levelMap[0])
    return cols * TILE_SIZE, rows * TILE_SIZE


def loadLevel(color=(255, 255, 255)):
    grounds = []

    for row, cells in enumerate(levelMap):
        for col, cell in enumerate(cells):
            if cell == '_':
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                grounds.append(Ground(Rectangle(f"ground_{row}_{col}", [x, y], [TILE_SIZE, TILE_SIZE], color)))

            elif cell == '*':
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                grounds.append(Boxes(Rectangle(f"ground_{row}_{col}", [x, y], [TILE_SIZE, TILE_SIZE], (0, 0, 255))))

    return grounds
