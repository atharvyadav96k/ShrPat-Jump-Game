import os
import pygame
from objects import TiledImage
from gameobjects import Ground, WoodBox, KillObstacle, HorizontalMovingKillObstacle, VerticalMovingKillObstacle, ScoreCoin, JumpCoin, FallingPlatform
from .map import map as DEFAULT_MAP

TILE_SIZE = 50
GROUND_TOP_INSET = 10
GROUND_Z_INDEX = 4
GRASS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "ground", "grass")
MOVING_KILL_TRAVEL_TILES = 4
MOVING_KILL_SPEED = 100


def _loadGrassTiles():
    entries = [f for f in os.listdir(GRASS_DIR) if os.path.splitext(f)[0].isdigit()]
    files = sorted(entries, key=lambda f: int(os.path.splitext(f)[0]))
    return [pygame.image.load(os.path.join(GRASS_DIR, f)).convert_alpha() for f in files]


def getLevelSize(levelMap=None):
    levelMap = levelMap if levelMap is not None else DEFAULT_MAP
    rows = len(levelMap)
    cols = len(levelMap[0])
    return cols * TILE_SIZE, rows * TILE_SIZE


def _mergeRuns(cells):
    runs = []
    col = 0

    while col < len(cells):
        cell = cells[col]
        if cell not in ('_', '$', '!', 'H', 'V', 'Y', 'B'):
            col += 1
            continue

        start = col
        while col < len(cells) and cells[col] == cell:
            col += 1

        runs.append((cell, start, col - start))

    return runs


def loadLevel(levelMap=None):
    levelMap = levelMap if levelMap is not None else DEFAULT_MAP
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
            elif cell == '!':
                grounds.append(KillObstacle.fromAssets([x, y], [width, TILE_SIZE]))
            elif cell == 'H':
                grounds.append(HorizontalMovingKillObstacle.fromAssets(
                    [x, y], [width, TILE_SIZE], travelDistance=TILE_SIZE * MOVING_KILL_TRAVEL_TILES, speed=MOVING_KILL_SPEED
                ))
            elif cell == 'V':
                grounds.append(VerticalMovingKillObstacle.fromAssets(
                    [x, y], [width, TILE_SIZE], travelDistance=TILE_SIZE * MOVING_KILL_TRAVEL_TILES, speed=MOVING_KILL_SPEED
                ))
            elif cell == 'Y':
                grounds.append(ScoreCoin.fromAssets([x, y], [width, TILE_SIZE]))
            elif cell == 'B':
                grounds.append(JumpCoin.fromAssets([x, y], [width, TILE_SIZE]))

        for col, cell in enumerate(cells):
            if cell == 'F':
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                platform = FallingPlatform.fromAssets([x, y], [TILE_SIZE, TILE_SIZE], grassTiles[0])
                platform.setHitbox(offset=(0, GROUND_TOP_INSET), size=(TILE_SIZE, TILE_SIZE - GROUND_TOP_INSET))
                grounds.append(platform)

    return grounds
