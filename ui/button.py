import pygame
from .panel import Panel
from .text import Text


class Button(Panel):
    def __init__(self, x=0, y=0, width=0.2, height=0.08, relative=True, anchor="topleft",
                 text="Button", onClick=None, color=(70, 70, 70), hoverColor=(110, 110, 110),
                 textColor=(255, 255, 255), fontSize=32, borderRadius=6,
                 image=None, hoverImage=None, hoverScale=1.08, animationSpeed=12):
        super().__init__(x, y, width, height, relative, anchor, color=color, borderRadius=borderRadius)
        self.baseColor = color
        self.hoverColor = hoverColor
        self.onClick = onClick
        self.hovered = False

        self.image = image
        self.hoverImage = hoverImage
        self.hoverScale = hoverScale
        self.animationSpeed = animationSpeed
        self.scale = 1.0

        self.label = self.addChild(Text(text, x=0.5, y=0.5, anchor="center", color=textColor, fontSize=fontSize)) if text else None

    def update(self, delta):
        super().update(delta)

        target = self.hoverScale if self.hovered else 1.0
        self.scale += (target - self.scale) * min(1.0, self.animationSpeed * delta)

    def _scaledRect(self):
        x, y, w, h = self.getRect()
        centerX, centerY = x + w / 2, y + h / 2
        scaledW, scaledH = w * self.scale, h * self.scale
        return (centerX - scaledW / 2, centerY - scaledH / 2, scaledW, scaledH)

    def drawSelf(self, canvas):
        rect = pygame.Rect(self._scaledRect())

        if self.image is not None:
            image = self.hoverImage if (self.hovered and self.hoverImage is not None) else self.image
            scaled = pygame.transform.scale(image, (rect.width, rect.height))
            canvas.blit(scaled, rect.topleft)
        else:
            color = self.hoverColor if self.hovered else self.baseColor
            pygame.draw.rect(canvas, color, rect, border_radius=self.borderRadius)

    def handleSelfEvent(self, event):
        rect = pygame.Rect(self.getRect())

        if event.type == pygame.MOUSEMOTION:
            self.hovered = rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect.collidepoint(event.pos) and self.onClick:
                self.onClick()
