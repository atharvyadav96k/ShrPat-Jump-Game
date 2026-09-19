from objects import Rectangle
from gameobjects import Ground, Boxes
from .map import map as levelMap

TILE_SIZE = 50


def getLevelSize():
    rows = len(levelMap)
    cols = len(levelMap[0])
    return cols * TILE_SIZE, rows * TILE_SIZE


def _mergeRuns(cells):
    runs = []
    col = 0

    while col < len(cells):
        cell = cells[col]
        if cell not in ('_', '*'):
            col += 1
            continue

        start = col
        while col < len(cells) and cells[col] == cell:
            col += 1

        runs.append((cell, start, col - start))

    return runs


def loadLevel(color=(255, 255, 255)):
    grounds = []

    for row, cells in enumerate(levelMap):
        for cell, startCol, length in _mergeRuns(cells):
            x = startCol * TILE_SIZE
            y = row * TILE_SIZE
            width = length * TILE_SIZE

            if cell == '_':
                grounds.append(Ground(Rectangle(f"ground_{row}_{startCol}", [x, y], [width, TILE_SIZE], color)))
            elif cell == '*':
                grounds.append(Boxes(Rectangle(f"box_{row}_{startCol}", [x, y], [width, TILE_SIZE], (0, 0, 255))))

    return grounds
