import os
import pygame
from objects import Rectangle, Image
from animation import Animator
from gameevents.controllableObject import ControllableObject


DESTROY_DELAY = 0.3
WOOD_COLOR = (139, 69, 19)
WOODBOX_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "ground", "woodbox")

_woodboxFramesCache = None


def _loadWoodboxFrames():
    global _woodboxFramesCache

    if _woodboxFramesCache is None:
        entries = [f for f in os.listdir(WOODBOX_DIR) if os.path.splitext(f)[0].isdigit()]
        files = sorted(entries, key=lambda f: int(os.path.splitext(f)[0]))
        _woodboxFramesCache = [pygame.image.load(os.path.join(WOODBOX_DIR, f)).convert_alpha() for f in files]

    return _woodboxFramesCache


class WoodBox(ControllableObject):
    def __init__(self, gameObject):
        super().__init__(gameObject, collidable=True, rigid=True, zIndex=3)
        self.touched = False
        self.destroyTimer = 0
        self.destroyed = False
        self.animator = None

    @classmethod
    def fromRect(cls, position, size, color=WOOD_COLOR):
        return cls(Rectangle(f"woodbox_{position[0]}_{position[1]}", position, size, color))

    @classmethod
    def fromAssets(cls, position, size):
        frames = _loadWoodboxFrames()
        gameObject = Image(f"woodbox_{position[0]}_{position[1]}", position, size, frames[0])
        box = cls(gameObject)

        breakFrames = frames[1:]
        box.animator = Animator(gameObject)
        box.animator.add("idle", frames[:1], loop=True)
        box.animator.add("break", breakFrames, frameDuration=DESTROY_DELAY / len(breakFrames), loop=False)
        box.animator.setState("idle")
        return box

    def onCollision(self, other):
        super().onCollision(other)

        if not self.touched:
            self.touched = True
            self.destroyTimer = 0
            if self.animator:
                self.animator.setState("break", restart=True)

    def update(self, delta):
        super().update(delta)

        if self.animator:
            self.animator.update(delta)

        if self.touched and not self.destroyed:
            self.destroyTimer += delta
            if self.destroyTimer >= DESTROY_DELAY:
                self.destroyed = True
