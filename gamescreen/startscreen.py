import os
import pygame
from ui import Root, Image, Text, Button

BG_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "bg.png")


class StartScreen:
    def __init__(self, canvas, onStart=None):
        self.canvas = canvas
        self.root = Root(canvas)

        backgroundImage = pygame.image.load(BG_IMAGE_PATH).convert()
        board = self.root.addChild(Image(backgroundImage, x=0.5, y=0.5, width=1.0, height=1.0, anchor="center"))
        board.addChild(Text("My Board", x=0.5, y=0.2, anchor="top", fontSize=48, color=(255, 255, 255)))
        board.addChild(Button(
            x=0.5, y=0.7, width=0.5, height=0.25, anchor="center",
            text="Play", onClick=onStart,
        ))

    def handleEvent(self, event):
        self.root.handleEvent(event)

    def draw(self, canvas):
        self.root.draw(canvas)
