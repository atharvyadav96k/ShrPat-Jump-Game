import pygame
from .object import Object


class Image(Object):
    def __init__(self, objectName, position, size, image):
        self.objectName = objectName
        self.rectCords = [position[0], position[1], size[0], size[1]]
        self.image = pygame.transform.scale(image, (size[0], size[1]))

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

    def setImage(self, image):
        w, h = self.rectCords[2], self.rectCords[3]
        self.image = pygame.transform.scale(image, (w, h))

    def drawObject(self, canvas, offset=(0, 0)):
        ox, oy = offset
        x, y, _, _ = self.rectCords
        canvas.blit(self.image, (x - ox, y - oy))

    def objectCollision(self):
        pass
