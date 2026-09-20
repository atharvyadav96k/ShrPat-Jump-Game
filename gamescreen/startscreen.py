import os
import pygame
from ui import Root, Image, Text, Button
from paths import ASSETS_DIR

BG_IMAGE_PATH = os.path.join(ASSETS_DIR, "bg.png")
PLAY_BUTTON_FRAMES_DIR = os.path.join(ASSETS_DIR, "ui", "buttons", "press")


def _loadFrameSequence(dirPath):
    entries = [f for f in os.listdir(dirPath) if os.path.splitext(f)[0].isdigit()]
    files = sorted(entries, key=lambda f: int(os.path.splitext(f)[0]))
    return [pygame.image.load(os.path.join(dirPath, f)).convert_alpha() for f in files]


class StartScreen:
    def __init__(self, canvas, onStart=None):
        self.canvas = canvas
        self.root = Root(canvas)

        backgroundImage = pygame.image.load(BG_IMAGE_PATH).convert()
        board = self.root.addChild(Image(backgroundImage, x=0.5, y=0.5, width=1.0, height=1.0, anchor="center"))
        board.addChild(Text("My Board", x=0.5, y=0.2, anchor="top", fontSize=48, color=(255, 255, 255)))

        playButtonFrames = _loadFrameSequence(PLAY_BUTTON_FRAMES_DIR)
        board.addChild(Button(
            x=0.5, y=0.7, width=0.5, height=0.25, anchor="center",
            text="", onClick=onStart,
            image=playButtonFrames[0],
            hoverFrames=playButtonFrames,
        ))

    def handleEvent(self, event):
        self.root.handleEvent(event)

    def update(self, delta):
        self.root.update(delta)

    def draw(self, canvas):
        self.root.draw(canvas)
