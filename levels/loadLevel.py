from objects import Rectangle
from gameobjects import Ground
from .map import map as levelMap


def loadLevel(screenWidth, screenHeight, color=(255, 255, 255)):
    rows = len(levelMap)
    cols = len(levelMap[0])
    tileWidth = 50
    tileHeight = 50

    grounds = []

    for row, cells in enumerate(levelMap):
        for col, cell in enumerate(cells):
            if cell != '_':
                continue

            x = col * tileWidth
            y = row * tileHeight
            grounds.append(Ground(Rectangle(f"ground_{row}_{col}", [x, y], [tileWidth, tileHeight], color)))

    return grounds
