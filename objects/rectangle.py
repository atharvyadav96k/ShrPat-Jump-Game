import pygame
import math
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

    def moveObject(self, directionAngle, directionSpeed, delta):
        angle = math.radians(directionAngle)

        dx = math.cos(angle) * directionSpeed * delta
        dy = math.sin(angle) * directionSpeed * delta

        self.rectCords[0] += dx
        self.rectCords[1] += dy

    def drawObject(self, canvas):
        pygame.draw.rect(
            canvas,
            self.color,
            pygame.Rect(*self.rectCords)
        )

    def objectCollision(self):
        pass