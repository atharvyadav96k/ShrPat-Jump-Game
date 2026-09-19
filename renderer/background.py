import pygame


class Background:
    def __init__(self, image, parallaxFactor=0.3, screenHeight=720, minZoom=1.0):
        self.parallaxFactor = parallaxFactor
        height = int(screenHeight / minZoom)
        width = int(image.get_width() * (height / image.get_height()))
        self.image = pygame.transform.scale(image, (width, height))

    def draw(self, target, offset):
        camX, camY = offset
        targetWidth, targetHeight = target.get_size()
        imageWidth, imageHeight = self.image.get_size()

        camCenterX = camX + targetWidth / 2
        originX = targetWidth / 2 - camCenterX * self.parallaxFactor

        startX = originX % imageWidth
        if startX > 0:
            startX -= imageWidth

        parallaxY = camY * self.parallaxFactor
        y = -min(max(parallaxY, 0), max(0, imageHeight - targetHeight))

        x = startX
        while x < targetWidth:
            target.blit(self.image, (x, y))
            x += imageWidth
