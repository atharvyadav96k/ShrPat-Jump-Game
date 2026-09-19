import pygame
from .object import Object


class TiledAnimatedImage(Object):
    def __init__(self, objectName, position, size, image, tileSize):
        self.objectName = objectName
        self.rectCords = [position[0], position[1], size[0], size[1]]
        self.tileSize = tileSize
        self.tile = pygame.transform.scale(image, (tileSize, tileSize))

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
        self.tile = pygame.transform.scale(image, (self.tileSize, self.tileSize))

    def drawObject(self, canvas, offset=(0, 0)):
        ox, oy = offset
        x, y, w, _ = self.rectCords
        tileCount = max(1, round(w / self.tileSize))

        for i in range(tileCount):
            canvas.blit(self.tile, (x + i * self.tileSize - ox, y - oy))

    def objectCollision(self):
        pass
