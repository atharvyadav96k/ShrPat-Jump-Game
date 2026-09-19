import pygame
from .element import UIElement


class Panel(UIElement):
    def __init__(self, x=0, y=0, width=1.0, height=1.0, relative=True, anchor="topleft",
                 color=(30, 30, 30), borderRadius=0):
        super().__init__(x, y, width, height, relative, anchor)
        self.color = color
        self.borderRadius = borderRadius

    def drawSelf(self, canvas):
        rect = pygame.Rect(self.getRect())
        pygame.draw.rect(canvas, self.color, rect, border_radius=self.borderRadius)
