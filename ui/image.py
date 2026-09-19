import pygame
from .element import UIElement


class Image(UIElement):
    def __init__(self, surface, x=0, y=0, width=1.0, height=1.0, relative=True, anchor="topleft"):
        super().__init__(x, y, width, height, relative, anchor)
        self.surface = surface

    def drawSelf(self, canvas):
        x, y, w, h = self.getRect()
        scaled = pygame.transform.scale(self.surface, (int(w), int(h)))
        canvas.blit(scaled, (x, y))
