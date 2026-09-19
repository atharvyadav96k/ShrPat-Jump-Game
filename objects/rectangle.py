import pygame
from .object import Object


class Rectangle(Object):
    def __init__(self, rectCords, rectSize):
        self.color = (255, 255, 255)

        self.rectCords = [
            rectCords[0],
            rectCords[1],
            rectSize[0],
            rectSize[1]
        ]

    def drawObject(self, canvas):
        pygame.draw.rect(
            canvas,
            self.color,
            pygame.Rect(*self.rectCords)
        )

    def objectCollision(self):
        pass