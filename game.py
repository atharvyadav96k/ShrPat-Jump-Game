import os
import pygame
from time import time
from renderer import Renderer, HUD, Camera, Background, easing
from gameevents import InputHandler, CollisionSystem
from gameobjects import Player
from levels import loadLevel, getLevelSize
from gamescreen import GameOverScreen

EDGE_ZOOM_MARGIN = 80
ZOOM_DURATION = 0.4
ZOOM_EASING = easing.easeOutQuad
PLAYER_SIZE = [42, 70]
PLAYER_START = [100, 0]
CAMERA_ZOOM = 1.2
EDGE_ZOOM_OUT_FACTOR = 0.6
MIN_ZOOM = CAMERA_ZOOM * EDGE_ZOOM_OUT_FACTOR

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets", "female-character")
BG_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "assets", "bg.png")
BACKGROUND_PARALLAX = 0.8


class Game:
    def __init__(self, canvas):
        self.canvas = canvas
        screenWidth, screenHeight = canvas.get_size()

        self.exit = False
        self.player = Player.fromAssets(ASSETS_DIR, PLAYER_START, PLAYER_SIZE)
        self.background = Background(
            pygame.image.load(BG_IMAGE_PATH).convert(),
            parallaxFactor=BACKGROUND_PARALLAX,
            screenHeight=screenHeight,
            minZoom=MIN_ZOOM,
        )

        grounds = loadLevel()
        levelWidth, levelHeight = getLevelSize()

        self.renderer = Renderer(canvas)
        self.hud = HUD(canvas, self.player)
        self.camera = Camera(screenWidth, screenHeight, levelWidth, levelHeight)
        self.objects = [self.player, *grounds]
        self.inputHandler = InputHandler(self.objects)
        self.collisionSystem = CollisionSystem(self.objects)
        self.cameraZoom = CAMERA_ZOOM
        self.gameOverScreen = GameOverScreen(canvas, onRestart=self.restart)

        self.delta = 0
        self.prevTime = time()
        self.currTime = time()

    def deltaTime(self):
        self.currTime = time()
        self.delta = self.currTime - self.prevTime
        self.prevTime = self.currTime

    def restart(self):
        self.player = Player.fromAssets(ASSETS_DIR, PLAYER_START, PLAYER_SIZE)
        self.objects = [self.player, *loadLevel()]
        self.inputHandler = InputHandler(self.objects)
        self.collisionSystem = CollisionSystem(self.objects)
        self.hud.player = self.player
        self.gameOverScreen.hide()

    def gameLoop(self):
        while not self.exit:
            self.deltaTime()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

                if self.player is None:
                    self.gameOverScreen.handleEvent(event)
                else:
                    self.inputHandler.handleEvent(event)

            self.canvas.fill((0, 0, 0))
            self.renderer.update(self.objects, self.delta)
            self.collisionSystem.resolve()
            self.objects[:] = [obj for obj in self.objects if not getattr(obj, "destroyed", False)]

            if self.player is not None and self.player.destroyed:
                self.hud.player = None
                self.player = None
                self.gameOverScreen.show()

            if self.player is not None:
                self.camera.follow(self.player)

                if self.camera.shouldZoomOut(self.player, triggerMargin=EDGE_ZOOM_MARGIN):
                    self.camera.setZoom(MIN_ZOOM, duration=ZOOM_DURATION, easing=ZOOM_EASING)
                else:
                    self.camera.setZoom(self.cameraZoom, duration=ZOOM_DURATION, easing=ZOOM_EASING)

                self.camera.update(self.delta)
                self.camera.follow(self.player)

            ui = self.gameOverScreen if self.player is None else None
            self.renderer.draw(self.objects, self.camera.getOffset(), self.camera.zoom, self.background, ui=ui)
            self.hud.render()
            pygame.display.update()

        pygame.quit()
