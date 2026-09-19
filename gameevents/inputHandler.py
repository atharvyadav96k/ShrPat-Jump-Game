import pygame


class InputHandler:
    def __init__(self, objectEventList, keyBindingRegistry):
        self.objectEventList = objectEventList
        self.keyBindingRegistry = keyBindingRegistry
        self.activeKeys = {}

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            self._handleKeyDown(event.key)
        elif event.type == pygame.KEYUP:
            self._handleKeyUp(event.key)

    def _handleKeyDown(self, key):
        for objectName in self.keyBindingRegistry.objectNames():
            bindings = self.keyBindingRegistry.getBindings(objectName)
            if key not in bindings:
                continue

            moveEvent = self.objectEventList.getEvent(objectName)
            if moveEvent is None:
                continue

            angle, speed = bindings[key]
            moveEvent.move(angle, speed)
            self.activeKeys[objectName] = key

    def _handleKeyUp(self, key):
        for objectName in self.keyBindingRegistry.objectNames():
            if self.activeKeys.get(objectName) != key:
                continue

            moveEvent = self.objectEventList.getEvent(objectName)
            if moveEvent is None:
                continue

            moveEvent.move(0, 0)
            del self.activeKeys[objectName]
