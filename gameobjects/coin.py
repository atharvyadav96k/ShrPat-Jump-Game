import os
import re
import pygame
from objects import Image
from animation import Animator
from gameevents.controllableObject import ControllableObject

COINS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "gameobjects", "coins")
YELLOW_COIN_DIR = os.path.join(COINS_DIR, "yellow")
BLUE_COIN_DIR = os.path.join(COINS_DIR, "blue")
COIN_FRAME_DURATION = 0.08

_frameCache = {}


def _loadNumberedFrames(dirPath):
    if dirPath not in _frameCache:
        def frameNumber(filename):
            match = re.search(r"(\d+)(?=\.\w+$)", filename)
            return int(match.group(1)) if match else 0

        files = sorted(
            (f for f in os.listdir(dirPath) if re.search(r"\d+(?=\.\w+$)", f)),
            key=frameNumber,
        )
        _frameCache[dirPath] = [pygame.image.load(os.path.join(dirPath, f)).convert_alpha() for f in files]

    return _frameCache[dirPath]


class Coin(ControllableObject):
    def __init__(self, gameObject):
        super().__init__(gameObject, collidable=True, rigid=True, zIndex=3)
        self.passthrough = True
        self.animator = Animator(gameObject)
        self.destroyed = False

    def _spawnFrames(self, frames):
        self.animator.add("spin", frames, frameDuration=COIN_FRAME_DURATION, loop=True)
        self.animator.setState("spin")

    def applyEffect(self, player):
        raise NotImplementedError

    def onCollision(self, other):
        super().onCollision(other)

        if self.destroyed or not hasattr(other, "takeDamage"):
            return

        self.applyEffect(other)
        self.destroyed = True

    def update(self, delta):
        self.animator.update(delta)
        super().update(delta)


class ScoreCoin(Coin):
    def __init__(self, gameObject, value=10):
        super().__init__(gameObject)
        self.value = value

    @classmethod
    def fromAssets(cls, position, size, value=10):
        frames = _loadNumberedFrames(YELLOW_COIN_DIR)
        gameObject = Image(f"scorecoin_{position[0]}_{position[1]}", position, size, frames[0])
        coin = cls(gameObject, value=value)
        coin._spawnFrames(frames)
        return coin

    def applyEffect(self, player):
        player.addScore(self.value)


class JumpCoin(Coin):
    def __init__(self, gameObject, amount=1):
        super().__init__(gameObject)
        self.amount = amount

    @classmethod
    def fromAssets(cls, position, size, amount=1):
        frames = _loadNumberedFrames(BLUE_COIN_DIR)
        gameObject = Image(f"jumpcoin_{position[0]}_{position[1]}", position, size, frames[0])
        coin = cls(gameObject, amount=amount)
        coin._spawnFrames(frames)
        return coin

    def applyEffect(self, player):
        player.grantExtraJump(self.amount)
