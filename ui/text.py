import pygame
from .element import UIElement

_PYGAME_ANCHOR = {
    "topleft": "topleft",
    "top": "midtop",
    "topright": "topright",
    "left": "midleft",
    "center": "center",
    "right": "midright",
    "bottomleft": "bottomleft",
    "bottom": "midbottom",
    "bottomright": "bottomright",
}


class Text(UIElement):
    def __init__(self, text, x=0, y=0, relative=True, anchor="center",
                 color=(255, 255, 255), fontSize=28, font=None):
        super().__init__(x, y, width=0, height=0, relative=relative, anchor=anchor)
        self.text = text
        self.color = color
        self.font = font or pygame.font.SysFont(None, fontSize)

    def setText(self, text):
        self.text = text

    def drawSelf(self, canvas):
        x, y, _, _ = self.getRect()
        surface = self.font.render(self.text, True, self.color)
        pygameAnchor = _PYGAME_ANCHOR.get(self.anchor, "topleft")
        rect = surface.get_rect(**{pygameAnchor: (x, y)})
        canvas.blit(surface, rect)
