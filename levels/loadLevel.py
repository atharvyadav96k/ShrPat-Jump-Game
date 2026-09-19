import os
import pygame
from objects import Rectangle, TiledImage
from gameobjects import Ground, WoodBox
from .map import map as levelMap

TILE_SIZE = 50
GROUND_TOP_INSET = 10
GROUND_Z_INDEX = 4
GRASS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "ground", "grass")


def _loadGrassTiles():
    files = sorted(os.listdir(GRASS_DIR), key=lambda f: int(os.path.splitext(f)[0]))
    return [pygame.image.load(os.path.join(GRASS_DIR, f)).convert_alpha() for f in files]


def getLevelSize():
    rows = len(levelMap)
    cols = len(levelMap[0])
    return cols * TILE_SIZE, rows * TILE_SIZE


def _mergeRuns(cells):
    runs = []
    col = 0

    while col < len(cells):
        cell = cells[col]
        if cell not in ('_', '$', '#'):
            col += 1
            continue

        start = col
        while col < len(cells) and cells[col] == cell:
            col += 1

        runs.append((cell, start, col - start))

    return runs


def loadLevel(color=(255, 255, 255)):
    grassTiles = _loadGrassTiles()
    grounds = []

    for row, cells in enumerate(levelMap):
        for cell, startCol, length in _mergeRuns(cells):
            x = startCol * TILE_SIZE
            y = row * TILE_SIZE
            width = length * TILE_SIZE

            if cell == '_':
                gameObject = TiledImage(f"ground_{row}_{startCol}", [x, y], [width, TILE_SIZE], grassTiles, TILE_SIZE)
                ground = Ground(gameObject, zIndex=GROUND_Z_INDEX)
                ground.setHitbox(offset=(0, GROUND_TOP_INSET), size=(width, TILE_SIZE - GROUND_TOP_INSET))
                grounds.append(ground)
            elif cell == '$':
                grounds.append(WoodBox.fromRect([x, y], [width, TILE_SIZE]))
            elif cell == '#':
                grounds.append(Ground(Rectangle(f"border_{row}_{startCol}", [x, y], [width, TILE_SIZE], color)))

    return grounds
