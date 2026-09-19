import pygame


class InputHandler:
    def __init__(self, controllables):
        self.controllables = controllables

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            for controllable in self.controllables:
                controllable.handleKeyDown(event.key)
        elif event.type == pygame.KEYUP:
            for controllable in self.controllables:
                controllable.handleKeyUp(event.key)
