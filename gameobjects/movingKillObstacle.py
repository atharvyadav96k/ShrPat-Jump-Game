import os
import pygame
from objects import Image
from animation import Animator
from .killObstacle import KillObstacle

SAW_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "gameobjects", "saw")
SAW_FRAME_DURATION = 0.08

_sawFramesCache = None


def _loadSawFrames():
    global _sawFramesCache

    if _sawFramesCache is None:
        entries = [f for f in os.listdir(SAW_DIR) if os.path.splitext(f)[0].isdigit()]
        files = sorted(entries, key=lambda f: int(os.path.splitext(f)[0]))
        _sawFramesCache = [pygame.image.load(os.path.join(SAW_DIR, f)).convert_alpha() for f in files]

    return _sawFramesCache


class HorizontalMovingKillObstacle(KillObstacle):
    def __init__(self, gameObject, rangeStart, rangeEnd, speed=100):
        super().__init__(gameObject)
        self.zIndex = 5
        self.rangeStart = rangeStart
        self.rangeEnd = rangeEnd
        self.vx = speed
        self.animator = Animator(gameObject)

    @classmethod
    def fromAssets(cls, position, size, travelDistance, speed=100):
        frames = _loadSawFrames()
        gameObject = Image(f"hkill_{position[0]}_{position[1]}", position, size, frames[0])
        obstacle = cls(gameObject, rangeStart=position[0], rangeEnd=position[0] + travelDistance, speed=speed)
        obstacle.animator.add("spin", frames, frameDuration=SAW_FRAME_DURATION, loop=True)
        obstacle.animator.setState("spin")
        return obstacle

    def update(self, delta):
        x, y, w, h = self.getBounds()

        if x <= self.rangeStart:
            self.vx = abs(self.vx)
        elif x + w >= self.rangeEnd:
            self.vx = -abs(self.vx)

        super().update(delta)


class VerticalMovingKillObstacle(KillObstacle):
    def __init__(self, gameObject, rangeStart, rangeEnd, speed=100):
        super().__init__(gameObject)
        self.zIndex = 5
        self.rangeStart = rangeStart
        self.rangeEnd = rangeEnd
        self.vy = speed
        self.animator = Animator(gameObject)

    @classmethod
    def fromAssets(cls, position, size, travelDistance, speed=100):
        frames = _loadSawFrames()
        gameObject = Image(f"vkill_{position[0]}_{position[1]}", position, size, frames[0])
        obstacle = cls(gameObject, rangeStart=position[1], rangeEnd=position[1] + travelDistance, speed=speed)
        obstacle.animator.add("spin", frames, frameDuration=SAW_FRAME_DURATION, loop=True)
        obstacle.animator.setState("spin")
        return obstacle

    def update(self, delta):
        x, y, w, h = self.getBounds()

        if y <= self.rangeStart:
            self.vy = abs(self.vy)
        elif y + h >= self.rangeEnd:
            self.vy = -abs(self.vy)

        super().update(delta)
