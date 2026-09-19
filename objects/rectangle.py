import pygame
from .object import Object


class Rectangle(Object):
    def __init__(self, objectName,rectCords, rectSize, color):
        self.color = color
        self.objectName = objectName
        self.rectCords = [
            rectCords[0],
            rectCords[1],
            rectSize[0],
            rectSize[1]
        ]

    def getObjName(self):
        return self.objectName

    def getBounds(self):
        return tuple(self.rectCords)

    def setPosition(self, x, y):
        self.rectCords[0] = x
        self.rectCords[1] = y

    def translate(self, dx, dy):
        self.rectCords[0] += dx
        self.rectCords[1] += dy

    def drawObject(self, canvas, offset=(0, 0)):
        ox, oy = offset
        x, y, w, h = self.rectCords
        pygame.draw.rect(
            canvas,
            self.color,
            pygame.Rect(x - ox, y - oy, w, h)
        )

    def objectCollision(self):
        pass