import pygame


class Renderer:
    def __init__(self, canvas):
        self.canvas = canvas

    def update(self, objects, delta):
        for object in objects:
            object.update(delta)

    def draw(self, objects, offset=(0, 0), zoom=1.0):
        screenWidth, screenHeight = self.canvas.get_size()

        if zoom == 1.0:
            for object in sorted(objects, key=lambda o: o.zIndex):
                object.drawObject(self.canvas, offset)
            return

        viewWidth = int(screenWidth / zoom)
        viewHeight = int(screenHeight / zoom)
        worldView = pygame.Surface((viewWidth, viewHeight))
        worldView.fill((0, 0, 0))

        for object in sorted(objects, key=lambda o: o.zIndex):
            object.drawObject(worldView, offset)

        scaled = pygame.transform.scale(worldView, (screenWidth, screenHeight))
        self.canvas.blit(scaled, (0, 0))
