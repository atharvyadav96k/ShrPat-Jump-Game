import pygame
from .panel import Panel
from .text import Text


class Button(Panel):
    def __init__(self, x=0, y=0, width=0.2, height=0.08, relative=True, anchor="topleft",
                 text="Button", onClick=None, color=(70, 70, 70), hoverColor=(110, 110, 110),
                 textColor=(255, 255, 255), fontSize=32, borderRadius=6,
                 image=None, hoverImage=None,
                 hoverFrames=None, hoverFrameDuration=0.08):
        super().__init__(x, y, width, height, relative, anchor, color=color, borderRadius=borderRadius)
        self.baseColor = color
        self.hoverColor = hoverColor
        self.onClick = onClick
        self.hovered = False

        self.image = image
        self.hoverImage = hoverImage

        self.hoverFrames = hoverFrames
        self.hoverFrameDuration = hoverFrameDuration
        self.hoverIndex = 0.0

        self.label = self.addChild(Text(text, x=0.5, y=0.5, anchor="center", color=textColor, fontSize=fontSize)) if text else None

    def update(self, delta):
        super().update(delta)

        if self.hoverFrames:
            target = len(self.hoverFrames) - 1 if self.hovered else 0
            step = delta / self.hoverFrameDuration if self.hoverFrameDuration > 0 else len(self.hoverFrames)

            if self.hoverIndex < target:
                self.hoverIndex = min(target, self.hoverIndex + step)
            elif self.hoverIndex > target:
                self.hoverIndex = max(target, self.hoverIndex - step)

    @staticmethod
    def _blitContain(canvas, image, rect):
        imageW, imageH = image.get_size()
        scaleFactor = min(rect.width / imageW, rect.height / imageH)
        scaledSize = (max(1, round(imageW * scaleFactor)), max(1, round(imageH * scaleFactor)))
        scaled = pygame.transform.smoothscale(image, scaledSize)
        blitRect = scaled.get_rect(center=rect.center)
        canvas.blit(scaled, blitRect)

    def drawSelf(self, canvas):
        rect = pygame.Rect(self.getRect())

        if self.hoverFrames:
            frame = self.hoverFrames[round(self.hoverIndex)]
            self._blitContain(canvas, frame, rect)
        elif self.image is not None:
            image = self.hoverImage if (self.hovered and self.hoverImage is not None) else self.image
            self._blitContain(canvas, image, rect)
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
