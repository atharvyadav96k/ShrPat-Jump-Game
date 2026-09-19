import os
import pygame
from objects import Rectangle, Image
from animation import Animator
from gameevents.controllableObject import ControllableObject

KILL_COLOR = (200, 0, 0)
LAVA_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "ground", "lava")
LAVA_FRAME_DURATION = 0.15

_lavaFramesCache = None


def _loadLavaFrames():
    global _lavaFramesCache

    if _lavaFramesCache is None:
        entries = [f for f in os.listdir(LAVA_DIR) if os.path.splitext(f)[0].isdigit()]
        files = sorted(entries, key=lambda f: int(os.path.splitext(f)[0]))
        _lavaFramesCache = [pygame.image.load(os.path.join(LAVA_DIR, f)).convert_alpha() for f in files]

    return _lavaFramesCache


class KillObstacle(ControllableObject):
    def __init__(self, gameObject):
        super().__init__(gameObject, collidable=True, rigid=True, zIndex=3)
        self.animator = None

    @classmethod
    def fromRect(cls, position, size, color=KILL_COLOR):
        return cls(Rectangle(f"kill_{position[0]}_{position[1]}", position, size, color))

    @classmethod
    def fromAssets(cls, position, size, frameDuration=LAVA_FRAME_DURATION):
        frames = _loadLavaFrames()
        gameObject = Image(f"kill_{position[0]}_{position[1]}", position, size, frames[0])
        obstacle = cls(gameObject)
        obstacle.animator = Animator(gameObject)
        obstacle.animator.add("idle", frames, frameDuration=frameDuration, loop=True)
        obstacle.animator.setState("idle")
        return obstacle

    def onCollision(self, other):
        super().onCollision(other)

        if hasattr(other, "takeDamage"):
            other.takeDamage(other.maxHealth)

    def update(self, delta):
        if self.animator:
            self.animator.update(delta)

        super().update(delta)
