import pygame


class InputHandler:
    def __init__(self, controllables):
        self.controllables = controllables

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            for controllable in self.controllables:
                controllable.handleKeyDown(event.key)
