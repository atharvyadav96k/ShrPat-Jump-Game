import pygame


class Renderer:
    def __init__(self, canvas):
        self.canvas = canvas

    def update(self, objects, delta):
        for object in objects:
            object.update(delta)

    def draw(self, objects, offset=(0, 0), zoom=1.0, background=None):
        screenWidth, screenHeight = self.canvas.get_size()

        if zoom == 1.0:
            target = self.canvas
        else:
            viewWidth = int(screenWidth / zoom)
            viewHeight = int(screenHeight / zoom)
            target = pygame.Surface((viewWidth, viewHeight))
            target.fill((0, 0, 0))

        if background:
            background.draw(target, offset)

        for object in sorted(objects, key=lambda o: o.zIndex):
            object.drawObject(target, offset)

        if target is not self.canvas:
            scaled = pygame.transform.scale(target, (screenWidth, screenHeight))
            self.canvas.blit(scaled, (0, 0))
