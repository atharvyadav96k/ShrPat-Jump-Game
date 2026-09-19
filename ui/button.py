import pygame
from .panel import Panel
from .text import Text


class Button(Panel):
    def __init__(self, x=0, y=0, width=0.2, height=0.08, relative=True, anchor="topleft",
                 text="Button", onClick=None, color=(70, 70, 70), hoverColor=(110, 110, 110),
                 textColor=(255, 255, 255), fontSize=32, borderRadius=6):
        super().__init__(x, y, width, height, relative, anchor, color=color, borderRadius=borderRadius)
        self.baseColor = color
        self.hoverColor = hoverColor
        self.onClick = onClick
        self.hovered = False
        self.label = self.addChild(Text(text, x=0.5, y=0.5, anchor="center", color=textColor, fontSize=fontSize))

    def drawSelf(self, canvas):
        self.color = self.hoverColor if self.hovered else self.baseColor
        super().drawSelf(canvas)

    def handleSelfEvent(self, event):
        rect = pygame.Rect(self.getRect())

        if event.type == pygame.MOUSEMOTION:
            self.hovered = rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect.collidepoint(event.pos) and self.onClick:
                self.onClick()
