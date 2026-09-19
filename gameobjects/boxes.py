import os
import pygame
from objects import Image
from animation import Animator
from gameevents.controllableObject import ControllableObject


class Boxes(ControllableObject):
    def __init__(self, gameObject):
        super().__init__(gameObject, collidable=False, rigid=True, zIndex=3)
        self.animator = Animator(gameObject)

    @classmethod
    def fromAssets(cls, assetsDir, position, size, **kwargs):
        frames = cls._loadFrameSequence(assetsDir)
        box = cls(Image(f"box_{position[0]}_{position[1]}", position, size, frames[0]), **kwargs)
        box.animator.add("idle", frames, frameDuration=0.1, loop=True)
        box.animator.setState("idle")
        return box

    @staticmethod
    def _loadFrameSequence(dirPath):
        files = sorted(os.listdir(dirPath), key=lambda f: int(os.path.splitext(f)[0]))
        return [pygame.image.load(os.path.join(dirPath, f)).convert_alpha() for f in files]

    def update(self, delta):
        self.animator.update(delta)
        super().update(delta)
