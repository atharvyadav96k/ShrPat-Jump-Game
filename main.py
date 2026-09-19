import os
import pygame
from time import time
from renderer import Renderer, HUD, Camera, easing
from gameevents import Obstacle, InputHandler, CollisionSystem
from gameobjects import Player
from levels import loadLevel, getLevelSize

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
EDGE_ZOOM_MARGIN = 80
ZOOM_DURATION = 0.4
ZOOM_EASING = easing.easeOutQuad
PLAYER_SIZE = [42, 70]

canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Board")

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets", "female-character")

player = Player.fromAssets(ASSETS_DIR, [100, 0], PLAYER_SIZE)

grounds = loadLevel()
LEVEL_WIDTH, LEVEL_HEIGHT = getLevelSize()

class Game():
    def __init__(self):
        self.exit = False
        self.renderer = Renderer(canvas)
        self.hud = HUD(canvas, player)
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, LEVEL_WIDTH, LEVEL_HEIGHT)
        self.objects = [player, *grounds]
        self.inputHandler = InputHandler(self.objects)
        self.collisionSystem = CollisionSystem(self.objects)
        self.cameraZoom = 1

        self.delta = 0
        self.prevTime = time()
        self.currTime = time()

    def deltaTime(self):
        self.currTime = time()
        self.delta = self.currTime - self.prevTime
        self.prevTime = self.currTime

    def gameLoop(self):
        while not self.exit:
            self.deltaTime()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

                self.inputHandler.handleEvent(event)

            canvas.fill((0, 0, 0))
            self.renderer.update(self.objects, self.delta)
            self.collisionSystem.resolve()

            self.camera.follow(player)

            if self.camera.shouldZoomOut(player, triggerMargin=EDGE_ZOOM_MARGIN):
                self.camera.setZoom(self.cameraZoom * 0.6, duration=ZOOM_DURATION, easing=ZOOM_EASING)
            else:
                self.camera.setZoom(self.cameraZoom, duration=ZOOM_DURATION, easing=ZOOM_EASING)

            self.camera.update(self.delta)
            self.camera.follow(player)

            self.renderer.draw(self.objects, self.camera.getOffset(), self.camera.zoom)
            self.hud.render()
            pygame.display.update()

        pygame.quit()

game = Game()
game.gameLoop()
